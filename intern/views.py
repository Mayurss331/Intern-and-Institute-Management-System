from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages

from myapp.models import Announcement
from .forms import InternSignupForm, InternLoginForm
from .models import Intern, Meeting, PracticeSession, Resource
from .models import Notification
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.utils import timezone
    







def notifications(request):
    user = request.session.get('email')  # Get username from session
    if not user:
        return redirect('intern_login')
    user=Intern.objects.get(email=user)
    user_notifications = Notification.objects.filter(user=user).order_by('-created_at')
    return render(request, 'interns/notifications.html', {'user':user,'notifications': user_notifications,'notification':getNotificationCount(user)})

def profile_view(request):
    user = request.session.get('email')  # Get username from session
    if not user:
        return redirect('intern_login')
    user=Intern.objects.get(email=user)
    
    if request.method == "POST":
        user.first_name = request.POST.get("first_name")
        user.last_name = request.POST.get("last_name")
        user.phone_number = request.POST.get("phone_number")
        user.college_name = request.POST.get("college_name")
        user.degree = request.POST.get("degree")
        user.passing_year = request.POST.get("passing_year")

        if 'profile_picture' in request.FILES:
            user.profile_picture = request.FILES['profile_picture']
        Notification.objects.create(user=user, message="Your profile was updated successfully!")
        user.save()
        return redirect("profile")  # Refresh page after update

    return render(request, "interns/profile.html", {"user": user,'notification':getNotificationCount(user)})

def intern_dashboard(request):
    """
    Intern Dashboard/Home Page
    """
    username = request.session.get('email')  # Get username from session
    if not username:
        return redirect('intern_login')
    user=Intern.objects.get(email=username)
    upcoming_meetings = Meeting.objects.filter(date__gte=timezone.now()).order_by('date')[:5]
    announcements = Announcement.objects.all()  # Fetch all announcements



    
    return render(request, 'interns/dashboard.html', {"user": user,'announcements': announcements,'notification':getNotificationCount(user),'upcoming_meetings': upcoming_meetings})
    return render(request, 'interns/dashboard.html')



def change_password(request):
    user = request.session.get('email')  # Get username from session
    if not user:
        return redirect('intern_login')
    user=Intern.objects.get(email=user)
    if request.method == "POST":
        old_password = request.POST.get("old_password")
        new_password1 = request.POST.get("new_password1")
        new_password2 = request.POST.get("new_password2")

        if not user.check_password(old_password):
            messages.error(request, "Old password is incorrect.")
            return redirect("profile")

        if new_password1 != new_password2:
            messages.error(request, "New passwords do not match.")
            return redirect("profile")

        user.set_password(new_password1)
        user.save()
        messages.success(request, "Password changed successfully!")
        return redirect("profile")

    return redirect("profile")

# def intern_signup(request):
#     """
#     Intern Signup View
#     """
#     if request.method == "POST":
#         form = InternSignupForm(request.POST, request.FILES)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.save()
#             login(request, user)
#             return redirect('intern_dashboard')  
#     else:
#         form = InternSignupForm()
    
#     return render(request, 'interns/signup.html', {'form': form})

def intern_login(request):
    """
    Intern Login View
    """
    if request.method == "POST":
        form = InternLoginForm(request, data=request.POST)

        username = request.POST.get('username')  # Now using username
        password = request.POST.get('password')
        print(username)
        print(password)


        # Authenticate using username instead of email
        user = Intern.objects.get( email=username)
        print(user)
        if user.check_password(password):
            request.session['username'] = username  # Store username in session
            request.session['email'] = user.email  # Store username in session
            print(user)
            return redirect('intern_dashboard') 
        else:
            messages.error(request, "Invalid username or password")  # Show error message

    else:
        form = InternLoginForm()

    return render(request, 'interns/login.html', {'form': form})

def intern_logout(request):
    request.session.flush()  # Clears all session data
    logout(request)
    return redirect('intern_login')  # Redirect to login page

def getNotificationCount(user):
    return Notification.objects.filter(user=user, is_read=False).count()



def mark_notification_read(request, notification_id):
    """
    Marks a specific notification as read when clicked.
    """
    user = request.session.get('email')  # Get username from session
    if not user:
        return redirect('intern_login')
    user=Intern.objects.get(email=user)
    notification =Notification.objects.get(id=notification_id, user=user)
    print(notification)
    notification.is_read = True
    notification.save()
    return JsonResponse({"success": True})


from .models import DailyWorkUpdate
from .forms import DailyWorkUpdateForm

def daily_work_update(request):
    """ Display the list of daily work updates for the logged-in intern. """
    user = request.session.get('email')  # Get username from session
    if not user:
        return redirect('intern_login')
    user=Intern.objects.get(email=user)
    work_updates = DailyWorkUpdate.objects.filter(intern=user).order_by('-date')
    return render(request, 'interns/daily_work_update.html', {'user':user,'work_updates': work_updates,'notification':getNotificationCount(user)})



from .models import DailyWorkUpdate, WorkSubmission
from .forms import DailyWorkUpdateForm
from django.utils.timezone import now


def submit_work_update(request):
    user_email = request.session.get('email')  # Get email from session
    if not user_email:
        return redirect('intern_login')

    user = Intern.objects.get(email=user_email)  # Get Intern object

    # Check if today's work update exists
    today = now().date()
    today_update = DailyWorkUpdate.objects.filter(intern=user, date=today).first()
    work_submissions = WorkSubmission.objects.filter(work_update=today_update) if today_update else None

    if request.method == 'POST':
        if today_update:  # If update exists, edit it
            work_form = DailyWorkUpdateForm(request.POST, instance=today_update)
        else:
            work_form = DailyWorkUpdateForm(request.POST)

        if work_form.is_valid():
            work_update = work_form.save(commit=False)
            work_update.intern = user  # Assign logged-in intern
            work_update.save()

            # Handle new file uploads
            uploaded_files = request.FILES.getlist('files')
            for file in uploaded_files:
                WorkSubmission.objects.create(work_update=work_update, file=file)

            return redirect('intern_dashboard')  # Redirect after submission

    else:
        work_form = DailyWorkUpdateForm(instance=today_update)

    return render(request, 'interns/submit_work_update.html', {'user':user,
        'today_update': today_update,
        'work_form': work_form,
        'work_submissions': work_submissions,
        'already_submitted': bool(today_update),
        'notification':getNotificationCount(user)
    })


def delete_submission(request, submission_id):
    submission = get_object_or_404(WorkSubmission, id=submission_id)
    submission.delete()
    return JsonResponse({'success': True})


def intern_practice(request):
    user_email = request.session.get('email')  # Get email from session
    if not user_email:
        return redirect('intern_login')

    user = Intern.objects.get(email=user_email)  # Get Intern object
    resources = Resource.objects.all().order_by('-uploaded_at')  # Latest first
    upcoming_sessions = PracticeSession.objects.filter(date__gte=datetime.now()).order_by('date')  # Future sessions
    

    return render(request, 'interns/intern_practice.html', {
        'resources': resources,
        'practice_sessions': upcoming_sessions,
        'user':user,
        'notification':getNotificationCount(user)
    })