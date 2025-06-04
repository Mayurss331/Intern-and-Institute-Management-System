import csv
import re
import pandas as pd
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from .utils import process_excel
from django.contrib import messages
from .models import Announcement, Application
from datetime import datetime
from django.http import JsonResponse
from .models import UserPerformance
import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.db.models import Count, Avg, Q
from django.db.models.functions import Substr
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Transaction
from django.views.decorators.csrf import csrf_exempt

from .forms import CreateInternFromApplicationForm, TransactionForm
from django.db import models
from django.shortcuts import render, get_object_or_404, redirect
from .models import CandidatePerformance
from .forms import CandidatePerformanceForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.utils.timezone import now
from intern.models import *
from django.utils.dateparse import parse_datetime



def custom_404(request, exception=None):
    return render(request, '404.html', status=404)



def add_meeting(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            title = data.get("title")
            description = data.get("description", "")
            date = data.get("date")
            location = data.get("location", "")

            if not title or not date:
                return JsonResponse({"error": "Title and date are required!"}, status=400)

            Meeting.objects.create(title=title, description=description, date=date, location=location)
            return JsonResponse({"success": "Meeting added successfully!"})
        
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    
    return JsonResponse({"error": "Invalid request method!"}, status=405)

def send_notification(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            intern_id = data.get("intern_id")
            message = data.get("message")

            if not intern_id or not message:
                return JsonResponse({"error": "Missing fields"}, status=400)

            intern = Intern.objects.get(id=intern_id)
            Notification.objects.create(user=intern, message=message, created_at=now())

            return JsonResponse({"success": "Notification sent successfully!"})

        except Intern.DoesNotExist:
            return JsonResponse({"error": "Intern not found"}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=405)


def interns_performance(request):
    today_submissions = DailyWorkUpdate.objects.filter(date=now().date())
    interns = Intern.objects.all()



    return render(request, "internship/performance_list.html", {"today_submissions": today_submissions, "interns": interns})
                  


@login_required
def transaction_list(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-timestamp')

    # Calculate the total available balance
    total_income = sum(t.amount for t in transactions if t.transaction_type == "Income")
    total_expense = sum(t.amount for t in transactions if t.transaction_type == "Expense"and t.status=="Completed")
    available_balance = total_income - total_expense

    return render(request, 'transaction_list.html', {
        'transactions': transactions,
        'available_balance': available_balance,
    })

@login_required
def add_transaction(request):
    """ Add a new income or expense transaction """
    if request.method == "POST":
        form = TransactionForm(request.POST, request.FILES)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user  # Assign logged-in user
            transaction.save()
            return redirect('transaction_list')  # Redirect to list view
    else:
        form = TransactionForm()

    return render(request, 'transaction_form.html', {'form': form})


@login_required
def edit_transaction(request, transaction_id):
    """ Edit an existing transaction """
    transaction = get_object_or_404(Transaction, id=transaction_id, user=request.user)

    if request.method == "POST":
        form = TransactionForm(request.POST, request.FILES, instance=transaction)
        if form.is_valid():
            form.save()
            return redirect('transaction_list')

    else:
        form = TransactionForm(instance=transaction)

    return render(request, 'transaction_form.html', {'form': form, 'edit': True})


@login_required
def delete_transaction(request, transaction_id):
    """ Delete a transaction securely """
    transaction = get_object_or_404(Transaction, id=transaction_id, user=request.user)

    if request.method == "POST":
        transaction.delete()
        return redirect('transaction_list')

    return render(request, 'confirm_delete.html', {'transaction': transaction})


@login_required
def download_document(request, transaction_id):
    """ Download the uploaded document of a transaction """
    transaction = get_object_or_404(Transaction, id=transaction_id, user=request.user)

    if transaction.document:
        file_path = transaction.document.path
        with open(file_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type="application/octet-stream")
            response['Content-Disposition'] = f'attachment; filename={transaction.document.name}'
            return response
    else:
        return HttpResponse("No document found.", status=404)


# Created by Dhaneshwar

from django.http import HttpResponse, StreamingHttpResponse
from .emails import *  # Import email-related functions
#pandas imported as pd from latex.py-->email.py-->views.py For handling CSV files


# Map email types to their corresponding functions
email_functions = {
    'pre_placement_talk': pre_placement_talk,
    'send_aptitude_assessment_mail': send_aptitude_assessment_mail,
    'send_aptitude_assessment_reminder_mail': send_aptitude_assessment_reminder_mail,
    'send_aptitude_assessment_feedback_mail': send_aptitude_assessment_feedback_mail,
    'send_GD1_mail': send_GD1_mail,
    'send_GD1_reminder_mail': send_GD1_reminder_mail,
    'send_GD2_mail': send_GD2_mail,
    'send_GD2_reminder_mail': send_GD2_reminder_mail,
    'send_technical_assessment_register_mail': send_technical_assessment_register_mail,
    'send_technical_assessment_register_reminder_mail': send_technical_assessment_register_reminder_mail,
    'send_technical_assessment_confirmation_mail': send_technical_assessment_confirmation_mail,
    'send_technical_assessment_mail': send_technical_assessment_mail,
    'send_process_feedback_mail': send_process_feedback_mail,
    'send_non_selection_mail': send_non_selection_mail,
    'send_selection_mail': send_selection_mail,
    'send_internship_offer_letter_mail': send_internship_offer_letter_mail,
}

def send_email_to_candidate(data, batch_id, email_type,subject, link, date, time):
    """
    Sends emails to candidates based on the provided email type and candidate data.

    Args:
        data (DataFrame): Candidate data from the uploaded file.
        email_type (str): Type of email to send (e.g., 'send_selection_mail').
        role (str): Role related to the email content.
        subject (str): Subject of the email.
        link (str): Link included in the email body.
        date (str): Date related to the email content.
        time (str): Time related to the email content.

    Returns:
        str: Summary of email sending status.
    """
    add_col = []
    if email_type == 'send_technical_assessment_confirmation_mail':
        add_col = ['trs_id']
    # Define the required columns for candidate data
    required_columns = ['Batch Id', 'Role', 'First Name', 'Last Name', 'Email']+add_col

    # Validate the presence of required columns in the data
    missing_columns = [col for col in required_columns if col not in data.columns]
    if missing_columns:
        return f"Missing columns in CSV: {missing_columns}"

    # Initialize variables for internship offer emails
    last_batch, Id = 0, 0
    if email_type == 'send_internship_offer_letter_mail':
        filename = "Candidates.csv"
        try:
            # Read the file to fetch the last batch
            df = pd.read_csv(filename)
            if 'Batch' in df.columns:
                last_batch = df['Batch'].iloc[-1] if not df.empty else 0
            else:
                return f"Error: 'Batch' column not found in the '{filename}' file."
        except FileNotFoundError:
            return f"Error: The file '{filename}' does not exist."

    # Extract required columns and remove rows with missing values
    extracted_data = data[required_columns].dropna()
    records = extracted_data.to_dict('records')  # Convert data to a list of dictionaries


    # Validate the email type
    if email_type not in email_functions:
        return f"Invalid email type: {email_type}"
    
    roles = {'WEB-DEVELOPER':'Associate Web Developer Intern','DATA-ANALYST':'Associate Data Analyst Intern','ANDROID':'Associate Android Developer Intern'}

    # Send emails to each candidate
    i = 1
    for record in records:
        name = f"{record['First Name']} {record['Last Name']}"
        email = record['Email']
        role = roles[record['Role']]

        if int(batch_id) != int(record['Batch Id']):
            continue

        try:

            if email_type == 'send_internship_offer_letter_mail':
                Id += 1
                msg = email_functions[email_type](email, role, subject, link, date, last_batch, Id, name)
            elif email_type == 'send_technical_assessment_confirmation_mail':
                t_id = record['trs_id']
                msg = email_functions[email_type](email, role, t_id, link, date, time, name)
            else:
                msg = email_functions[email_type](email, role, subject, link, date, time, name)
            msg = str(i)+' - '+msg+'<br>'
            i+=1
        except Exception as e:
            file_name = "failed_emails.csv"
            # Load existing data if file exists, else create a new DataFrame
            if os.path.isfile(file_name):
                df2 = pd.read_csv(file_name)
            else:
                df2 = pd.DataFrame(columns=["First Name", "Last Name", "Email", "Role"])
            
            # Append new entry
            new_entry = pd.DataFrame([[record['First Name'], record['Last Name'], email, role]], columns=["First Name", "Last Name", "Email", "Role"])
            df2 = pd.concat([df2, new_entry], ignore_index=True)
            # Save back to CSV
            df2.to_csv(file_name, index=False)
            msg = f"Failed to send email to {name}: {e}"
        finally:
            yield msg

    return f"Last email sent to: {name}"

@login_required
def send_mail(request):
    """
    Handles the main page for uploading files and sending emails.
    """
    if request.method == "POST":
        # Retrieve form data
        uploaded_file = request.FILES.get('fileUpload', None)  # Get uploaded file
        batch_id = request.POST.get('batch_id')  # Get Batch ID
        email_type = request.POST.get("email_type")  # Selected email type
        subject = request.POST.get("subject")  # Email subject
        link = request.POST.get("link")  # Link in the email
        time = request.POST.get("time")  # Email-specific time
        date = request.POST.get("date")  # Email-specific date


        # Process the uploaded file
        data = pd.read_csv(uploaded_file)
        return StreamingHttpResponse(
            send_email_to_candidate(data, batch_id, email_type, subject, link, date, time),
            content_type='text/html'
        )

    # Render the index page for GET requests
    return render(request, 'send_mail.html')

# views.py


@login_required
def single(request):
    """
    Renders the send single mail page.
    """
    if request.method == "POST":
        # Retrieve form data
        role = request.POST.get('role')  # Get role
        email_type = request.POST.get("email_type")  # Selected email type
        name = request.POST.get("name")  # Candidate name   
        email = request.POST.get("email")  # Email Address
        link = request.POST.get("link")  # Link in the email
        date = request.POST.get("date")  # Email-specific date
        time = request.POST.get("time")  # Email-specific time
        subject = request.POST.get("subject")  # Email subject

        last_batch, Id = 0, 0

        if email_type == 'send_internship_offer_letter_mail':
            Id += 1
            msg = email_functions[email_type](email, role, subject, link, date, last_batch, Id, name)
        else:
            msg = email_functions[email_type](email, role, subject, link, date, time, name)

        return HttpResponse(msg)


    return render(request, 'single-email.html')

@login_required
def helper(request):
    """
    Renders the help page.
    """
    return render(request, 'help.html')











def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("home")  # Redirect to home after login
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "login.html")

def logout_view(request):
    logout(request)
    return redirect("login")  # Redirect to login page after logout


@login_required
def home(request):
    # Application statistics
    total_applications = Application.objects.count()
    male_count = Application.objects.filter(gender='Male').count()
    female_count = Application.objects.filter(gender='Female').count()
    other_count = Application.objects.filter(gender='Other').count()

    # Performance statistics
    total_performances = UserPerformance.objects.count()
    avg_aptitude_score = UserPerformance.objects.aggregate(Avg('aptitude_score'))['aptitude_score__avg'] or 0
    avg_technical_score = UserPerformance.objects.aggregate(Avg('technical_marks'))['technical_marks__avg'] or 0

    batch_performance = (
        UserPerformance.objects
        .annotate(batch_prefix=Substr('batch_id', 1, 2))  # Extract first 2 characters (B1, B2)
        .values('batch_prefix')
        .annotate(avg_technical=Avg('technical_marks'))
        .order_by('batch_prefix')
    )

    batch_labels = [batch['batch_prefix'] for batch in batch_performance]
    batch_scores = [batch['avg_technical'] if batch['avg_technical'] else 0  for batch in batch_performance]

    # Fees Paid among GD1 attendees
    gd1_attendees = UserPerformance.objects.filter(gd1_attendance=True).count()
    fees_paid_gd1 = UserPerformance.objects.filter(gd1_attendance=True, fees_paid=True).count()
    fees_unpaid_gd1 = gd1_attendees - fees_paid_gd1
    conversion_rate = (fees_paid_gd1 / fees_unpaid_gd1) * 100 if fees_unpaid_gd1 > 0 else 0
    overall_ratio = (fees_paid_gd1 / total_applications) * 100 if total_applications > 0 else 0

    print(fees_paid_gd1,gd1_attendees)

    context = {
        'total_applications': total_applications,
        'male_count': male_count,
        'female_count': female_count,
        'other_count': other_count,
        'total_performances': total_performances,
        'avg_aptitude_score': round(avg_aptitude_score, 2),
        'avg_technical_score': round(avg_technical_score, 2),
        'batch_labels': batch_labels,
        'batch_scores': batch_scores,
        'gd1_attendees': gd1_attendees,
        'fees_paid_gd1': fees_paid_gd1,
        'fees_unpaid_gd1': fees_unpaid_gd1,
        'conversion_rate': round(conversion_rate, 2),
        'overall_ratio': round(overall_ratio, 2),
    }
    return render(request, 'home.html', context)


# def update_timestamp(request):
#     try:
#         # Define the new timestamp
#         new_timestamp = datetime(2025, 3, 4, 12, 0)  # 1 Feb 2025, 12:00 PM
        
#         # Update all records where id < 107
#         updated_count = Application.objects.filter(id__gt=339).update(timestamp=new_timestamp)
        
#         return JsonResponse({"message": f"Updated {updated_count} records successfully!"})
#     except Exception as e:
#         return JsonResponse({"error": str(e)}, status=500)
    

@login_required 
def upload_excel(request):
    if request.method == "POST" and request.FILES['excel_file']:
        excel_file = request.FILES['excel_file']
        fs = FileSystemStorage()
        file_path = fs.save(excel_file.name, excel_file)
        process_excel(fs.path(file_path))
        messages.success(request, "Excel file uploaded successfully!")
    return render(request, 'upload.html')



@login_required
def search_applications(request):
    query = request.GET.get("q", "").strip()  # Get search input from URL parameter
    results = []

    if query:
        results = Application.objects.filter(
            email__icontains=query
        ) | Application.objects.filter(
            first_name__icontains=query
        ) | Application.objects.filter(
            last_name__icontains=query
        )

    return render(request, "search.html", {"results": results, "query": query})




@login_required
def sorted_applications(request):
    current_year = datetime.now().year
    years = list(range(2024, current_year + 1))  # Generate years from 2024 to the current year
    months = [
        {"month": i, "name": datetime(2000, i, 1).strftime("%B")}
        for i in range(1, 13)  # Generate all months
    ]

    year_filter = request.GET.get("year")
    month_filter = request.GET.get("month")

    applications = Application.objects.all()
    
    if year_filter and month_filter:
        applications = applications.filter(timestamp__year=year_filter, timestamp__month=month_filter)
    else :
        applications={}
    context = {
        "applications": applications,
        "years": years,
        "months": months,
    }
    return render(request, "sorted_applications.html", context)



@login_required
def user_list(request):
    users = Application.objects.all()
    return render(request, 'user_list.html', {'users': users})



@login_required
def user_performance_list(request):
    users = UserPerformance.objects.select_related('user')

    if request.method == "GET":
        batch_id = request.GET.get("batch_id", "").strip()  # Get and clean input

        if batch_id:
            users = users.filter(batch_id__icontains=batch_id)  # Proper filtering
        else:
            users = users.filter(batch_id=None)  # Return an empty queryset when batch_id is empty

        return render(request, "update_performance.html", {"users": users})

    return render(request, "update_performance.html", {"users": users.all()})

@login_required
def update_performance(request, user_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)  # If using JSON data
        except json.JSONDecodeError:
            data = request.POST  # If using form data

        print("Received Data:", data)  # Debugging
        
        field = data.get("field")
        value = data.get("value")

        if not field:
            return JsonResponse({"error": "Missing field name"}, status=400)
        
        # Find the user performance record
        try:
            performance = UserPerformance.objects.get(user__id=user_id)
        except UserPerformance.DoesNotExist:
            return JsonResponse({"error": "User performance not found"}, status=404)

        # Convert boolean values properly
        if field in ["gd1_attendance", "gd2_attendance", "fees_paid"]:
            value = value.lower() in ["true", "1"]

        # Update the field dynamically
        setattr(performance, field, value)
        performance.save()

        return JsonResponse({"message": "Performance updated successfully!"})

    return JsonResponse({"error": "Invalid request"}, status=400)



# def filter_performance(request):
#     if request.method == "GET":
#         batch_id = request.POST.get("batch_id")
#         users = UserPerformance.objects.filter(batch_id=batch_id) if batch_id else UserPerformance.objects.all()
#         return render(request, "performa.html", {"users": users})
#     return JsonResponse({"error": "Invalid request"}, status=400)


def upload_performance(request):
    if request.method == "POST" and request.FILES.get("file"):
        excel_file = request.FILES["file"]

        try:
            df = pd.read_excel(excel_file)  # Read Excel file

            # Define required columns and default values
            default_values = {
                "Batch ID": None,
                "Aptitude Score": 0,
                "GD-1 Attend": False,
                "GD-1 Marks": 0,
                "GD-2 Attend": False,
                "GD-2 Marks": 0,
                "Fees Paid": False,
                "Technical Marks": 0,
            }

            # Check available columns in the uploaded file
            available_columns = set(df.columns)

            # Fill missing columns with default values
            for col, default in default_values.items():
                if col not in available_columns:
                    df[col] = default  # Assign default value to missing columns

            updated_count = 0
            for _, row in df.iterrows():
                email = row["Email"]

                try:
                    user = Application.objects.get(email=email)  # Find user by email
                    performance, created = UserPerformance.objects.get_or_create(user=user)

                    # Update performance fields with data or default values
                    performance.batch_id = row["Batch ID"]
                    performance.aptitude_score = row["Aptitude Score"]
                    performance.gd1_attendance = bool(row["GD-1 Attend"])
                    performance.gd1_marks = row["GD-1 Marks"]
                    performance.gd2_attendance = bool(row["GD-2 Attend"])
                    performance.gd2_marks = row["GD-2 Marks"]
                    performance.fees_paid = bool(row["Fees Paid"])
                    performance.technical_marks = row["Technical Marks"]
                    performance.save()

                    updated_count += 1

                except Application.DoesNotExist:
                    continue  # Skip users not found

            return JsonResponse({"message": f"Successfully updated {updated_count} records."})

        except Exception as e:
            return JsonResponse({"error": f"Error processing file: {str(e)}"}, status=500)

    return render(request, 'upload_performance.html')

@login_required
def update_single_performance(request):
    user_id = request.GET.get("id")  # Get user ID from URL

    if not user_id:
        messages.error(request, "User ID is required.")
        return redirect("user_performance_list")  # Redirect to list page if no ID provided

    user_perf, created = UserPerformance.objects.get_or_create(user_id=user_id)
    if user_perf==None:
        user_perf=created
    if request.method == "POST":
        user_perf.batch_id = request.POST.get("batch_id")
        user_perf.aptitude_score = request.POST.get("aptitude_score") if request.POST.get("aptitude_score")!="" else None
        user_perf.gd1_attendance = request.POST.get("gd1_attendance") == "on"
        user_perf.gd1_marks = request.POST.get("gd1_marks") if request.POST.get("gd1_marks")!="" else None
        user_perf.gd2_attendance = request.POST.get("gd2_attendance") == "on"
        user_perf.gd2_marks = request.POST.get("gd2_marks") if request.POST.get("gd2_marks")!="" else None
        user_perf.fees_paid = request.POST.get("fees_paid") == "on"
        user_perf.technical_marks = request.POST.get("technical_marks") if request.POST.get("technical_marks")!="" else None

        user_perf.save()
        messages.success(request, "User performance updated successfully!")
        return redirect(f"/update-single-performance?id={user_id}")  # Stay on the same page

    return render(request, "performance_table.html", {"user_perf": user_perf})


@login_required
def download_csv(request):
    year = request.GET.get("year")
    month = request.GET.get("month")

    if not year or not month:
        return HttpResponse("Invalid request. Year and Month required.", status=400)

    try:
        applications = Application.objects.filter(timestamp__year=year, timestamp__month=month)
    except Exception as e:
        return HttpResponse(f"Error fetching data: {str(e)}", status=500)

    if not applications.exists():
        return HttpResponse("No applications found for the selected month.", status=404)

    # Create response with CSV
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = f'attachment; filename="applications_{year}_{month}.csv"'

    writer = csv.writer(response)

    # **Write CSV Headers** (Include all fields from the model)
    writer.writerow([
        "Timestamp", "First Name", "Last Name", "Email", "Role", "Phone", "Resume", "Source",
        "Gender", "Date of Birth", "Domicile State", "Current Location", "Citizenship",
        "Postgraduate Degree", "Postgraduate Stream", "Postgraduate Passing Year",
        "Undergraduate Degree", "Undergraduate Stream", "Undergraduate Passing Year",
        "College Name", "Score Above 60%", "Standing Arrears", "Coding Languages",
        "Currently Working", "Company Name", "CTC/Stipend", "Designation",
        "Open to Relocate", "Passport Photo"
    ])

    # **Write Application Data**
    for app in applications:
        writer.writerow([
            app.timestamp, app.first_name, app.last_name, app.email, app.role, app.phone_number,
            app.resume.url if app.resume else "N/A",  # Get URL of resume file
            app.source, app.gender, app.date_of_birth, app.domicile_state,
            app.current_location, app.citizenship, app.postgraduate_degree or "N/A",
            app.postgraduate_stream or "N/A", app.postgraduate_passing_year or "N/A",
            app.undergraduate_degree, app.undergraduate_stream, app.undergraduate_passing_year,
            app.college_name, "YES" if app.score_above_60 else "NO",
            "YES" if app.standing_arrears else "NO", app.coding_languages,
            "YES" if app.currently_working else "NO", app.company_name or "N/A",
            app.ctc_or_stipend or "N/A", app.designation or "N/A",
            "YES" if app.open_to_relocate else "NO",
            app.passport_photo.url if app.passport_photo else "N/A"
        ])

    return response




def get_application_data(request):
    emails = request.GET.getlist("emails[]")  # Get list of emails from request
    applications = Application.objects.filter(email__in=emails).values(
        "role","first_name", "last_name", "email",
        "phone_number" # Add more fields if necessary
    )
    return JsonResponse(list(applications), safe=False)




def get_details(request, user_id):
    try:
        print(user_id)
        application = Application.objects.get(id=user_id)  # Fetch by email

        return JsonResponse({
            "success": True,
            "role": application.role,
            "first_name": application.first_name,
            "last_name": application.last_name,
            "email": application.email,
            "phone": application.phone_number,
            "gender": application.gender,
            "date_of_birth": application.date_of_birth.strftime("%Y-%m-%d"),
            "domicile_state": application.domicile_state,
            "current_location": application.current_location,
            "citizenship": application.citizenship,
            "postgraduate_degree": application.postgraduate_degree or "",
            "postgraduate_stream": application.postgraduate_stream or "",
            "postgraduate_passing_year": application.postgraduate_passing_year or "",
            "undergraduate_degree": application.undergraduate_degree,
            "undergraduate_stream": application.undergraduate_stream,
            "undergraduate_passing_year": application.undergraduate_passing_year,
            "college_name": application.college_name,
            "coding_languages": application.coding_languages,
            "currently_working": application.currently_working,
            "company_name": application.company_name or "",
            "designation": application.designation or "",
            "open_to_relocate": application.open_to_relocate,
            "resume_url": application.resume if application.resume else "#",
            "passport_photo_url": application.passport_photo if application.passport_photo else None,
        })
    except Application.DoesNotExist:
        return JsonResponse({"success": False, "message": "Application not found"})
    



from django.core.mail import EmailMessage

import os

def search_candidates(request):
    query = request.GET.get('q', '')
    results = Application.objects.filter(Q(email__icontains=query) | Q(first_name__icontains=query)) if query else []
    return render(request, 'internship/internship_list.html', {'results': results, 'query': query})

def send_offer_letter(request, candidate_id):
    # Fetch candidate details
    candidate = get_object_or_404(Application, id=candidate_id)

    # Map role names correctly
    role_mapping = {
        'WEB-DEVELOPER': 'Associate Web Developer Intern',
        'DATA-ANALYST': 'Data Analyst Intern',
        'ANDROID': 'Associate Android Developer Intern'
    }
    role = role_mapping.get(candidate.role, 'Associate Web Developer Intern')

    # Get the last batch number from Candidates.csv
    csv_file_path = os.path.join(settings.BASE_DIR, 'static', 'Candidates.csv')

    if os.path.exists(csv_file_path):
        df = pd.read_csv(csv_file_path)
        if not df.empty:
            last_batch = df['Batch'].max()
        else:
            last_batch = 0
    else:
        last_batch = 0  # Default to 0 if the file doesn't exist

    # Generate the offer letter PDF
    pdf_filename = create_internship_offer_letter(
        full_name=f"{candidate.first_name} {candidate.last_name}",
        email=candidate.email,
        last_batch=last_batch,
        Id=candidate.id,
        role=role,
        date=datetime.today().strftime('%Y-%m-%d')  # Current date in "YYYY-MM-DD" format
    )

    # Update candidate's offer status
    candidate.offer_status = "Sent"
    candidate.save()

    # Correct file path for PDF
    file_path = os.path.join(settings.BASE_DIR, "static","Offer", f"{pdf_filename}")

    # Debug: Check if the file exists
    print(f"Checking for PDF file at: {file_path}")

    if os.path.exists(file_path):
        with open(file_path, 'rb') as pdf:
            response = HttpResponse(pdf.read(), content_type="application/pdf")
            response['Content-Disposition'] = f'inline; filename="{pdf_filename}.pdf"'
            return response
    else:
        return HttpResponse(f"Error: File not found{file_path}", status=404)




import openai
from django.shortcuts import render
from django.http import JsonResponse

openai.api_key = ""  # Replace with your actual API key



# Extract field names dynamically
application_fields = {field.name for field in Application._meta.fields}

# Extend the fields list with __icontains for text-based fields
text_fields = {f"{field.name}__icontains" for field in Application._meta.fields if isinstance(field, models.CharField) or isinstance(field, models.TextField)}
application_fields.update(text_fields)
text_fields = {f"{field.name}__startswith" for field in Application._meta.fields if isinstance(field, models.CharField) or isinstance(field, models.TextField)}

# Merge both sets
application_fields.update(text_fields)
user_performance_fields = {field.name for field in UserPerformance._meta.fields}

# Extend the fields list with __icontains for text-based fields
text_fields = {f"{field.name}__icontains" for field in UserPerformance._meta.fields if isinstance(field, models.CharField) or isinstance(field, models.TextField)}

# Merge both sets
user_performance_fields.update(text_fields)
text_fields = {f"{field.name}__startswith" for field in UserPerformance._meta.fields if isinstance(field, models.CharField) or isinstance(field, models.TextField)}

# Merge both sets
user_performance_fields.update(text_fields)


@csrf_exempt
def get_ai_data(request):
    if request.method == "POST":
        user_query = request.POST.get("query", "")
        results = []  # Initialize to avoid referencing before assignment


        # Send query to OpenAI
        try:

            response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
            {
                "role": "system",
                "content": (
                    "You are an AI that converts user queries into Django ORM filter conditions.\n"
                    "Example Query: 'Find candidate with ID 5'\n"
                    "Example Output: \"id=5\"\n"
                    "ONLY return the filter condition inside double quotes without any explanation.\n"
                    "if asking for role the roles are ANDROID OR WEB-DEVELOPER OR DATA-ANALYST\n"
                    "Here are my models:\n\n"

                    "### Transaction Model ###\n"
                    "class Transaction(models.Model):\n"
                    "    TRANSACTION_TYPES = [\n"
                    "        ('Income', 'Income'),\n"
                    "        ('Expense', 'Expense')\n"
                    "    ]\n"
                    "    PAYMENT_MODES = [\n"
                    "        ('Cash', 'Cash'),\n"
                    "        ('Bank Transfer', 'Bank Transfer'),\n"
                    "        ('Credit Card', 'Credit Card'),\n"
                    "        ('UPI', 'UPI'),\n"
                    "        ('Other', 'Other')\n"
                    "    ]\n"
                    "    STATUS_CHOICES = [\n"
                    "        ('Pending', 'Pending'),\n"
                    "        ('Completed', 'Completed'),\n"
                    "        ('Failed', 'Failed')\n"
                    "    ]\n"
                    "    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)\n"
                    "    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')\n"
                    "    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)\n"
                    "    amount = models.DecimalField(max_digits=12, decimal_places=2)\n"
                    "    description = models.TextField()\n"
                    "    category = models.CharField(max_length=100)\n"
                    "    payment_mode = models.CharField(max_length=20, choices=PAYMENT_MODES, default='Cash')\n"
                    "    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Completed')\n"
                    "    timestamp = models.DateTimeField(auto_now_add=True)\n"
                    "    document = models.FileField(upload_to='transaction_documents/', blank=True, null=True)\n"
                    "\n"

                    "### Application Model ###\n"
                    "class Application(models.Model):\n"
                    "    GENDER_CHOICES = [('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')]\n"
                    "    OFFER_STATUS_CHOICES = [('Pending', 'Pending'), ('Sent', 'Sent'), ('Rejected', 'Rejected')]\n"
                    "    role = models.CharField(max_length=255)\n"
                    "    timestamp = models.DateTimeField(auto_now_add=True)\n"
                    "    first_name = models.CharField(max_length=255)\n"
                    "    last_name = models.CharField(max_length=255)\n"
                    "    email = models.EmailField(unique=True)\n"
                    "    phone_number = models.CharField(max_length=20)\n"
                    "    resume = models.URLField(default="")\n"
                    "    source = models.CharField(max_length=255)\n"
                    "    date_of_birth = models.DateField()\n"
                    "    current_location = models.CharField(max_length=255)\n"
                    "    citizenship = models.CharField(max_length=255)\n"
                    "    postgraduate_degree = models.CharField(max_length=255, blank=True, null=True)\n"
                    "    postgraduate_stream = models.CharField(max_length=255, blank=True, null=True)\n"
                    "    postgraduate_passing_year = models.IntegerField(blank=True, null=True)\n"
                    "    undergraduate_passing_year = models.IntegerField()\n"
                    "    college_name = models.CharField(max_length=255)\n"
                    "    score_above_60 = models.BooleanField(default=False)\n"
                    "    standing_arrears = models.BooleanField(default=False)\n"
                    "    coding_languages = models.TextField()\n"
                    "    currently_working = models.BooleanField(default=False)\n"
                    "    company_name = models.CharField(max_length=255, blank=True, null=True)\n"
                    "    ctc_or_stipend = models.FloatField(blank=True, null=True)\n"
                    "    designation = models.CharField(max_length=255, blank=True, null=True)\n"
                    "    open_to_relocate = models.BooleanField(default=False)\n"
                    "    passport_photo = models.URLField(default="")\n"
                    "    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)\n"
                    "    domicile_state = models.CharField(max_length=255)\n"
                    "    undergraduate_degree = models.CharField(max_length=255)\n"
                    "    undergraduate_stream = models.CharField(max_length=255)\n"
                    "    offer_status = models.CharField(max_length=10, choices=OFFER_STATUS_CHOICES, default='Pending')\n"
                    "\n"

                    "### User Performance Model ###\n"
                    "class UserPerformance(models.Model):\n"
                    "    batch_id=models.CharField(max_length=255, blank=True, null=True)\n"
                    "    user = models.ForeignKey(Application, on_delete=models.CASCADE)\n"
                    "    aptitude_score = models.FloatField(default=0, blank=True)\n"
                    "   gd1_attendance = models.BooleanField(default=False)  # Attendance for GD1\n"
                    "    gd1_marks = models.FloatField(default=0, blank=True)\n"
                    "   gd2_attendance = models.BooleanField(default=False)  # Attendance for GD2\n"
                    "    gd2_marks = models.FloatField(default=0, blank=True)\n"
                    "    fees_paid = models.BooleanField(default=False)\n"
                    "    technical_marks = models.FloatField(default=0, blank=True)\n"
                    "   created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when record is created\n"
                    "\n"
                    "Convert user queries into Django ORM filters for these models."
                )
            },
            {
                "role": "user",
                "content": f"Convert this query into a structured filter for my Django models: {user_query}"
            }
        ]
    )


            ai_response = response.choices[0].message.content.strip()
            print("AI Generated Filter:", ai_response)

            # Remove surrounding quotes if present
            ai_response = ai_response.strip('"')

            # Ensure the response is valid
            if not ai_response or "=" not in ai_response:
                return JsonResponse({"error": "Invalid filter condition from AI"}, status=400)

            # Convert AI-generated string into a dictionary
            try:
                filter_dict = {}
                for cond in ai_response.split(","):
                    key, value = map(str.strip, cond.split("=", 1))
                    # Convert booleans and numbers correctly
                    if value.lower() in ["true", "false"]:
                        value = value.lower() == "true"
                    elif value.isdigit():
                        value = int(value)
                    elif re.match(r"^\d+\.\d+$", value):  # Check for float
                        value = float(value)
                    else:
                        value = value.strip("'")  # Remove extra quotes around strings
                    filter_dict[key] = value

            except Exception:
                return JsonResponse({"error": "Error parsing filter condition"}, status=400)

            # Identify the model based on filter fields
            filter_fields = set(filter_dict.keys())

            if filter_fields & user_performance_fields:
                queryset = UserPerformance.objects.filter(**filter_dict).select_related("user")

                # Extract user fields dynamically
                user_fields = [f"user__{field.name}" for field in Application._meta.fields if field.name not in ["id"]]

                # Extract UserPerformance fields
                performance_fields = [field.name for field in UserPerformance._meta.fields]

                # Combine both
                all_fields = user_fields + performance_fields

                results = list(queryset.values(*all_fields))
                print("UserPerformance Data:", len(results))

            elif any(field in filter_dict for field in ["first_name", "last_name", "user__first_name", "user__last_name"]):
                # Convert AI response keys to match Application model fields
                name_filter = {}

                if "user__first_name" in filter_dict:
                    name_filter["first_name__icontains"] = filter_dict["user__first_name"]
                elif "first_name" in filter_dict:
                    name_filter["first_name__icontains"] = filter_dict["first_name"]

                if "user__last_name" in filter_dict:
                    name_filter["last_name__icontains"] = filter_dict["user__last_name"]
                elif "last_name" in filter_dict:
                    name_filter["last_name__icontains"] = filter_dict["last_name"]

                # Fetch users matching the name
                application_qs = Application.objects.filter(**name_filter)

                # Fetch UserPerformance records linked to these users
                queryset = UserPerformance.objects.filter(user__in=application_qs).select_related("user")

                # Extract user fields dynamically
                user_fields = [f"user__{field.name}" for field in Application._meta.fields if field.name not in ["id"]]

                # Extract UserPerformance fields
                performance_fields = [field.name for field in UserPerformance._meta.fields]

                # Combine both
                all_fields = user_fields + performance_fields

                results = list(queryset.values(*all_fields))
                print("UserPerformance Data by Name:", len(results))

            if len(results)==0 and filter_fields & application_fields:
                queryset = Application.objects.filter(**filter_dict)

                # Fetch all fields dynamically for Application
                all_fields = [field.name for field in Application._meta.fields]

                results = list(queryset.values(*all_fields))
                print("Application Data:", len(results))


            return JsonResponse(results, safe=False)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return render(request, 'fetch_ai.html')



def add_or_update_practice_session(request, session_id=None):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description", "")
        date = request.POST.get("date")
        location = request.POST.get("location", "")
        meeting_link = request.POST.get("meeting_link", "")

        if not title or not date:
            return JsonResponse({"error": "Title and Date are required!"}, status=400)

        parsed_date = parse_datetime(date)  # Convert string to datetime
        if not parsed_date:
            return JsonResponse({"error": "Invalid date format!"}, status=400)

        if session_id:
            session = get_object_or_404(PracticeSession, id=session_id)
            session.title = title
            session.description = description
            session.date = parsed_date
            session.location = location
            session.meeting_link = meeting_link
        else:
            session = PracticeSession.objects.create(
                title=title, description=description, date=parsed_date, location=location, meeting_link=meeting_link
            )

        session.save()
        return JsonResponse({"success": "Session saved successfully!"})

    session = None
    if session_id:
        session = get_object_or_404(PracticeSession, id=session_id)

    return render(request, "practice_session_form.html", {"session": session})


def add_announcement(request):
    if request.method == "POST":
        title = request.POST.get("title")
        message = request.POST.get("message")
        category = request.POST.get("category")
        link = request.POST.get("link")
        is_important = request.POST.get("is_important") == "on"  # Checkbox handling

        if not title or not message:
            return JsonResponse({"error": "Title and message are required!"}, status=400)

        announcement = Announcement.objects.create(
            title=title,
            message=message,
            category=category,
            is_important=is_important,
            link=link if link else None,
        )
        return JsonResponse({"success": "Announcement added successfully!"})

    return render(request, "add_announcement.html")


def manage_shedule(request):
    announcements = Announcement.objects.all().order_by("-date")
    sessions = PracticeSession.objects.all().order_by("-date")
    meetings = Meeting.objects.all().order_by("-date")

    context = {
        'announcements': announcements,
        'sessions': sessions,
        'meetings': meetings,
    }
    return render(request,"internship/manage_shedule.html",context)

@csrf_exempt
def edit_meeting(request, id):
    if request.method == "POST":
        meeting = get_object_or_404(Meeting, id=id)
        meeting.title = request.POST.get('title')
        meeting.description = request.POST.get('description')
        meeting.date = request.POST.get('date')
        meeting.location = request.POST.get('location')
        meeting.save()
        return JsonResponse({"success": "Meeting updated successfully!"})
    return JsonResponse({"error": "Invalid request."})

@csrf_exempt
def delete_meeting(request, id):
    if request.method == "POST":
        meeting = get_object_or_404(Meeting, id=id)
        meeting.delete()
        return JsonResponse({"success": "Meeting deleted successfully!"})
    return JsonResponse({"error": "Invalid request."})
@csrf_exempt
def delete_announcement(request, id):
    if request.method == "POST":
        announcement = get_object_or_404(Announcement, id=id)
        announcement.delete()
        return JsonResponse({"success": "Announcement deleted successfully!"})
    return JsonResponse({"error": "Invalid request."})

@csrf_exempt
def delete_practice_session(request, session_id):
    if request.method == "POST":
        try:
            session = PracticeSession.objects.get(id=session_id)
            session.delete()
            return JsonResponse({'success': "Practice session deleted successfully!"})
        except PracticeSession.DoesNotExist:
            return JsonResponse({'error': "Practice session not found."}, status=404)
    else:
        return JsonResponse({'error': "Invalid request method."}, status=400)
    

@login_required
def create_intern_from_application(request):
    if request.method == 'POST':
        form = CreateInternFromApplicationForm(request.POST)
        if form.is_valid():
            intern = form.save()
            messages.success(request, f"Intern account created for {intern.username}")
            return redirect('create_intern_from_application')
    else:
        form = CreateInternFromApplicationForm()
    
    return render(request, 'internship/create_intern.html', {'form': form})