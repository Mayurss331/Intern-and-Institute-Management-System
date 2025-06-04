# mail.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from .letters import *

telegram_link = 'https://t.me/ElementisSoftTech/'
linkedin_link = 'https://www.linkedin.com/company/elementis-softtech/'
insta_link = 'https://www.instagram.com/elementis_softtech/'
fb_link = 'https://www.facebook.com/share/1ALiiCWEUP/'
# logo = "https://iifqeflrhglzyamxesei.supabase.co/storage/v1/object/sign/elementis%20data/brand_logo.png?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1cmwiOiJlbGVtZW50aXMgZGF0YS9icmFuZF9sb2dvLnBuZyIsImlhdCI6MTczNzU2NjA4NiwiZXhwIjoxODk1MjQ2MDg2fQ.k798tLJpjpCdjAqEoXyAgVo6lwCp4_RF0wYGo0jpnj8&t=2025-01-22T17%3A14%3A45.448Z"
logo = 'https://www.elementissofttech.com/images/Elementis-01.png'


company_credentials = {
        "gmail": {
            "email": "teams.elementis@gmail.com",
            "password": "dhkn jsnh yeyl qlbr",
            "smtp": "smtp.gmail.com",
        },
        "titan": {
            "email": "info.elementis@onlyformachinelearning.in",
            "password": "@gendu_generation_2024",
            "smtp": "smtp.titan.email",
        },
    }


# Email credentials
root_mail = 'titan'

config = company_credentials[root_mail]
company_mail = config["email"]  # Company email address
company_password = config["password"]  # Company email password
smtp = config["smtp"]  # SMTP server for the company email
port = 587  # Port for the SMTP server (Gmail uses 587)
    

# Function to start an SMTP session and send an email
def start_session(message):
    """
    Starts an SMTP session to send an email securely.

    Args:
        message (MIMEMultipart): The email message to be sent, including sender, receiver, subject, and body.

    Returns:
        Bool
    """
    session = smtplib.SMTP(smtp, port)

    session.starttls()  # Upgrade to secure connection

    # Login to Gmail account
    session.login(company_mail, company_password)  # Avoid storing passwords in plaintext
    

    # Send the email
    session.sendmail(message["From"], message["To"], message.as_string())
    session.quit()  # Cleanly close the SMTP session

    return

def faild_email(full_name, email, role):
    """
    Saves the details of an email that failed to send to a CSV file, including the current date and time.
    """
    file_name = "failed_emails.csv"
    current_date = datetime.now().strftime("%d-%m-%Y")
    current_time = datetime.now().strftime("%I:%M %p")
    
    # Load existing data if file exists, else create a new DataFrame
    if os.path.isfile(file_name):
        df2 = pd.read_csv(file_name)
    else:
        df2 = pd.DataFrame(columns=["First Name", "Last Name", "Email", "Role", "Date", "Time"])
    
    first_name, last_name = full_name.split()
    # Append new entry
    new_entry = pd.DataFrame([[first_name, last_name, email, role, current_date, current_time]], 
                             columns=["First Name", "Last Name", "Email", "Role", "Date", "Time"])
    df2 = pd.concat([df2, new_entry], ignore_index=True)
    # Save back to CSV
    df2.to_csv(file_name, index=False)

# Function to convert a date from 'YYYY-MM-DD' format to 'DD-MM-YYYY' format
def get_date(date):
    """
    Converts a date from 'YYYY-MM-DD' format to 'DD-MM-YYYY' format.

    Args:
        date (str): The date in 'YYYY-MM-DD' format (e.g., "2025-01-26").

    Returns:
        str: The date in 'DD-MM-YYYY' format (e.g., "26-01-2025").
    """
    try:
        # Convert the string date to a datetime object
        date_obj = datetime.strptime(date, '%Y-%m-%d')

        # Return the date formatted as 'DD-MM-YYYY'
        return date_obj.strftime('%d-%m-%Y')

    except ValueError:
        # Handle incorrect date format
        print("Invalid date format. Please provide the date in 'YYYY-MM-DD' format.")
        return None
    
# Convert time into 12 hour clock
def get_time(time_str):
    # Parse the input 24-hour format time
    time_obj = datetime.strptime(time_str, "%H:%M")
    # Convert to 12-hour format with AM/PM
    return time_obj.strftime("%I:%M %p").lstrip("0")  # Removes leading zero


# Function for returning CSS content for HTML content
def get_css():
    """
    Returns the CSS content that can be applied to an HTML document.

    Returns:
        str: The CSS content as a string.
    """
    css_text = f'''
            body {{
                font-family: Arial, sans-serif;
                background-color: #f9f9f9;
                margin: 0;
                padding: 0;
            }}
            .email-container {{
                max-width: 600px;
                margin: 20px auto;
                background: #ffffff;
                padding: 20px;
                border: 4px solid #18def3;
                border-radius: 10px;
            }}
            .header-logo {{
                text-align: center;
                margin-bottom: 20px;
            }}
            .instructions {{
                font-size: 14px;
                text-align: left;
                margin-bottom: 20px;
                line-height: 1.6;
            }}
            .content {{
                font-size: 14px;
                text-align: left;
                margin-bottom: 20px;
                line-height: 1.6;
            }}
            .action-button {{
                display: inline-block;
                background-color: #004aad;
                color: white;
                font-weight: bold;
                text-decoration: none;
                padding: 12px 20px;
                font-size: 16px;
                border-radius: 5px;
                text-align: center;
                margin: 20px auto;
                cursor: pointer;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
                transition: background-color 0.3s ease, transform 0.2s ease;
            }}
            .action-button:hover {{
                background-color: #003580;
                color: white;
                transform: scale(1.05);
            }}
            .reminder {{
                font-size: 16px;
                font-weight: bold;
                margin-bottom: 20px;
            }}
            ul {{
                margin: 0 0 20px 20px;
            }}
            li {{
                margin-bottom: 10px;
            }}
                            .social-links {{
                text-align: center;
                margin-top: 20px;
            }}
            .social-links a {{
                color: #004aad;
                font-weight: bold;
                text-decoration: none;
                margin: 0 10px;
            }}
            .social-links a:hover {{
                text-decoration: underline;
            }}
            .important-instructions {{
                color: red;
                font-weight: bold;
                margin-bottom: 20px;
            }}
            .fallback-link {{
                font-size: 14px;
                margin-top: 20px;
                text-align: center;
                word-wrap: break-word;
            }}
            .footer {{
                font-size: 12px;
                color: #888;
                text-align: center;
                margin-top: 20px;
            }}
        '''
    return css_text

def pre_placement_talk(to,role='',sub='',link='',date='',time='',name="Candidate"):
    """
    Sends an email invitation for the Pre-Placement Talk with a company profile attachment.

    Args:
        to (str): Recipient's email address.
        role (str): Role applied for.
        sub (str): Subject of the email.
        meeting_link (str): Link to join the meeting.
        date (str): Meeting date in 'YYYY-MM-DD' format.
        time (str): Meeting start time.
        name (str): Candidate's name (default is "Candidate").
        logo (str): URL of the company logo.
        linkedin_link (str): LinkedIn URL.
        telegram_link (str): Telegram group URL.

    Returns:
        str: Confirmation message if the email is sent or an error message.
    """
    try:
        # Create a multi-part message to include both plain text and HTML content        
        message = MIMEMultipart("alternative")
        message["From"] = company_mail
        
        
        # Email subject and sender information
        message["Subject"] = "Invitation: Pre-Placement Talk || Elementis SoftTech"
        message["To"] = to


        date = get_date(date) #get date in dd-mm-yyyy format 
        time = get_time(time) # get time into 12 hour clock
        meeting_link = link
        

        # HTML email content
        html_content = f"""
        <html>
        <head>
            <style>
                {get_css()}
            </style>
        </head>
        <body>
            <div class="email-container">
                <div class="header-logo">
                    <img src="{logo}" width="250">
                </div>
                <h2 style="text-align: center;">Elementis SoftTech || Pre-Placement Talk</h2>
                <p class="instructions">
                    Hello {name},<br><br>
                    We are excited to invite you to our Pre-Placement Talk for the <b>{role}</b> role at <b>Elementis SoftTech</b>. 
                    This session will give you insights into our company, work culture, and hiring process.
                    <br><br>
                    <b>Meeting Details:</b><br>
                    📅 Date: <b>{date}</b><br>
                    ⏰ Time: <b>{time}</b><br>
                    🔗 Meeting Link: <a href="{meeting_link}" target="_blank">{meeting_link}</a><br><br>
                    
                    <b>Why attend?</b>
                    <ul>
                        <li>Understand our company values & projects.</li>
                        <li>Learn about the selection process.</li>
                        <li>Get answers to your questions directly from our team.</li>
                    </ul>
                </p>
                <div style="text-align: center;height:60px;justify-content: center;">
                    <a href="{meeting_link}" class="action-button" style="color:white;">Join Meeting</a>
                </div>
                
                <p class="instructions" style="text-align: center;">
                    Follow us to stay updated on career opportunities and hiring events.
                </p>
                <div class="social-links">
                    <a href="{linkedin_link}" target="_blank">LinkedIn</a> | 
                    <a href="{telegram_link}" target="_blank">Telegram</a> |
                    <a href="{insta_link}" target="_blank">Instagram</a> |
                    <a href="{fb_link}" target="_blank">Facebook</a>
                </div><br>
                <p class="content">
                    If you have any questions, feel free to reach out at: <b>support@elementissofttech.com</b>
                </p>
                <div class="footer">
                    Best regards,<br>
                    <b>Team Elementis SoftTech</b>
                </div>
            </div>
        </body>
        </html>
        """

        # Attach HTML content
        content = MIMEText(html_content, "html")
        message.attach(content)

        # Send the email (Assuming `start_session(message)` is defined)
        start_session(message)

        print(f"Pre-Placement Talk Email Sent to {name}")

        return f"Email successfully sent to {name}  ({to})"

    except Exception as e:
        faild_email(name, to, role)
        print(f"Error sending email: {e}")  # Provide more detailed error information

        return f"Error sending email: {e} <br>"
    

    

# Function to send an aptitude assessment email
def send_aptitude_assessment_mail(to,role='',sub='',link='',date='',time='',name="Candidate"):
    """
    Sends an email for the aptitude assessment with an attachment, HTML content, and styling.

    Args:
        to (str): Recipient's email address.
        role (str): Role applied for.
        sub (str): Subject of the email.
        link (str): Link to the assessment.
        date (str): Assessment start date in 'YYYY-MM-DD' format.
        time (str): Time when the assessment opens.
        name (str): Name of the candidate (default is "Candidate").

    Returns:
        str: Confirmation message if the email is sent or an error message.
    """
    try:
        # Create a multi-part message to include both plain text and HTML content        
        message = MIMEMultipart("alternative")
        message["From"] = company_mail
        
        # Email subject and sender information
        message["Subject"] = 'Invitation: Aptitude Assessment || Elementis Softech' # Default subject line
        message["To"] = to
        date = get_date(date) #get date in dd-mm-yyyy format  
        time = get_time(time) # get time into 12 hour clock  
        assessment_link = link
        

        # PDF Attachment
        with open(r"CompanyProfile.pdf", 'rb') as f:
            pdf_attachment = MIMEApplication(f.read(), _subtype='pdf')
            pdf_attachment.add_header('Content-Disposition', 'attachment', filename='CompanyProfile.pdf')
            message.attach(pdf_attachment)

        # HTML content styled for design
        html_content = f"""<html>
        <head>
            <style>

            {get_css()}

            </style>
        </head>
        <body>
            <div class="email-container">
                <div class="header-logo">
                    <img src={logo} width="250">
                </div>
                <h2 style="text-align: center;">Elementis SoftTech || Aptitude Assessment</h2>
                <p class="instructions">
                    Hii {name},<br><br>
                    Thank you for your interest in joining our team. Please read the following instructions carefully before starting your assessment:<br>
                    - Test Content: 20 questions of Aptitude.<br>
                    - Time: 30 minutes to complete the 20 questions.<br>
                    - The link will be <b>Open From {date} {time}</b>.
                    <br><br>
                    A couple of things to keep in mind while taking the assessment:<br>
                    1. Ensure you have a stable internet connection.<br>
                    2. Use a desktop or laptop to take the test.<br>
                    3. Find a quiet place where you won't be interrupted.<br>
                </p>
                <div style="text-align: center;height:60px;justify-content: center;">
                    <a href="{assessment_link}" class="action-button" style="color:white;">Start Assessment</a>
                </div>
                <p class="fallback-link">If the button above doesn't work, use the following link:<a href="{assessment_link}">{assessment_link}</a> </p> 
                <br>
                <p class="instructions" style="text-align: center;">
                    Follow us to stay updated on this drive, as well as upcoming opportunities and hiring events.
                </p>
                <div class="social-links">
                    <a href="{linkedin_link}" target="_blank">LinkedIn</a> | 
                    <a href="{telegram_link}" target="_blank">Telegram</a> |
                    <a href="{insta_link}" target="_blank">Instagram</a> |
                    <a href="{fb_link}" target="_blank">Facebook</a>
                </div><br>
                <p class="content">
                    If you have any query write an email to : support@elementissofttech.com 
                </p>
                <div class="footer">
                    Best regards,<br>
                    Team Elementis SoftTech
                </div>
            </div>
        </body>
        </html>
        """

        # Attach the HTML content
        content = MIMEText(html_content, "html")
        message.attach(content)

        # Send the email using the previously defined start_session function
        start_session(message)

        print("Email Sent to -",name)

        return f"Email sent to: {name}<br>"

    except Exception as e:
        print(f"Error sending email: {e}")  # Provide more detailed error information

        return f"Error sending email: {e} <br>"



# Function to send an aptitude assessment reminder email
def send_aptitude_assessment_reminder_mail(to,role='',sub='',link='',date='',time='',name="Candidate"):
    """
    Sends a reminder email for the aptitude assessment.

    Args:
        to (str): Recipient's email address.
        role (str): Role applied for.
        sub (str): Subject of the email.
        link (str): Link to the assessment.
        date (str): Assessment start date in 'YYYY-MM-DD' format.
        time (str): Time when the assessment opens.
        name (str): Name of the candidate (default is "Candidate").

    Returns:
        str: Confirmation message if the email is sent or an error message.
    """
    try:
        # Create a multi-part message to include both plain text and HTML content        
        message = MIMEMultipart("alternative")
        message["From"] = company_mail
        
        # Email subject and sender information
        message["Subject"] = 'Reminder: Aptitude Assessment || Elementis SoftTech' # Default subject line
        message["To"] = to 
        date = get_date(date) #get date in dd-mm-yyyy format  
        time = get_time(time) # get time into 12 hour clock
        assessment_link = link

        # HTML content styled for design
        html_content = f"""
        <html>
        <head>
            <style>
            
            {get_css()}

            </style>
        </head>
        <body>
            <div class="email-container">
                <div class="header-logo">
                    <img src={logo} width="250">
                </div>
                <h2 style="text-align: center;">Elementis SoftTech Aptitude Assessment</h2>
                <p class="instructions">
                    Hi {name},<br><br>
                    This is a friendly reminder to complete the Elementis SoftTech Aptitude Assessment as part of the application process. Below are the details for your reference:<br><br>
                    <b>Test Content:</b> 20 questions (Aptitude).<br>
                    <b>Time Limit:</b> 30 minutes.<br>
                    <b>Availability:</b> The assessment link is open on <Br> 
                    <b>Date:{date}</b>.<br>
                    <b>Time:{time}</b>.<br><br>
                    To successfully complete the test, please keep the following in mind:<br>
                    1. Ensure you have a stable internet connection.<br>
                    2. Use a desktop or laptop for the best experience.<br>
                    3. Find a quiet place where you won't be interrupted.<br><br>
                </p>
                <div style="text-align: center;height:60px;justify-content: center;">
                    <a href="{assessment_link}" class="action-button" style="color:white;">Start Assessment</a>
                </div>
                <p class="fallback-link">If the button above doesn't work, use the following link: </p> <br> 
                <a href="{assessment_link}">{assessment_link}</a>
                <p class="instructions" style="text-align: center;">
                    Follow us to stay updated on this drive, as well as upcoming opportunities and hiring events.
                </p>
                <div class="social-links">
                    <a href="{linkedin_link}" target="_blank">LinkedIn</a> | 
                    <a href="{telegram_link}" target="_blank">Telegram</a> |
                    <a href="{insta_link}" target="_blank">Instagram</a> |
                    <a href="{fb_link}" target="_blank">Facebook</a>
                </div><br>
                <p class="content">
                    If you have any query write an email to : support@elementissofttech.com 
                </p>
                <div class="footer">
                    Best regards,<br>
                    Team Elementis SoftTech
                </div>
            </div>
        </body>
        </html>
        """

        # Attach the HTML content to the email
        content = MIMEText(html_content, "html")
        message.attach(content)

        # Send the email using the start_session function
        start_session(message)

        print("Email Sent to -",name)

        return f"Email sent to: {name}<br>"

    except Exception as e:
        faild_email(name, to, role)
        print(f"Error sending email: {e}")  # Provide more detailed error information

        return f"Error sending email: {e} <br>"

# Function to send an aptitude assessment feedback email
def send_aptitude_assessment_feedback_mail(to,role='',sub='',link='',date='',time='',name="Candidate"):
    """
    Sends a feedback email after the candidate completes the aptitude assessment.

    Args:
        to (str): Recipient's email address.
        role (str): Role applied for.
        sub (str): Subject of the email.
        link (str): Link to the feedback form.
        date (str): Assessment completion date in 'YYYY-MM-DD' format.
        time (str): Time when the assessment was completed.
        name (str): Name of the candidate (default is "Candidate").

    Returns:
        str: Confirmation message if the email is sent or an error message.
    """
    try:
        # Create a multi-part message to include both plain text and HTML content        
        message = MIMEMultipart("alternative")
        message["From"] = company_mail
        
        # Email subject and sender information
        message["Subject"] = 'Share Your Feedback – We Value Your Opinion! || Elementis Softech' # Default subject line
        message["To"] = to
        date = get_date(date) #get date in dd-mm-yyyy format  
        time = get_time(time) # get time into 12 hour clock
        feedback_link = link

        # HTML content styled for design
        html_content = f"""
        <html>
        <head>
            <style>
            
            {get_css()}

            </style>
        </head>
        <body>
            <div class="email-container">
                <div class="header-logo">
                    <img src={logo} width="250">
                </div>
                <h2 style="text-align: center;">Elementis SoftTech || Feedback </h2>
                <p class="instructions">
                    Hi {name},<br><br>
                    Thank you for successfully submitting your assessment. We appreciate your effort and time in completing it.
                    <br>
                    <br>
                    <b>If you encountered any issues during the submission process or have any feedback to share, please let us know by filling out the form linked below. Your input is invaluable in helping us improve our processes.<br><br>
                    <br>
                    <br>
                    <b>If you encountered any issues we will reschedule the Test for you.You need to fill the form.</b>
                </p>
                <div style="text-align: center;height:60px;justify-content: center;">
                    <a href="{feedback_link}" class="action-button" style="color:white;">Raise Issue</a>
                </div>
                <p class="fallback-link">If the button above doesn't work, use the following link: </p> <br> 
                <a href="{feedback_link}">{feedback_link}</a>
                <p class="instructions" style="text-align: center;">
                    Follow us to stay updated on this drive, as well as upcoming opportunities and hiring events.
                </p>
                <div class="social-links">
                    <a href="{linkedin_link}" target="_blank">LinkedIn</a> | 
                    <a href="{telegram_link}" target="_blank">Telegram</a> |
                    <a href="{insta_link}" target="_blank">Instagram</a> |
                    <a href="{fb_link}" target="_blank">Facebook</a>
                </div><br>
                <p class="content">
                    If you have any query write an email to : support@elementissofttech.com 
                </p>
                <div class="footer">
                    Best regards,<br>
                    Team Elementis SoftTech
                </div>
            </div>
        </body>
        </html>
        """


        # Attach the HTML content to the email
        content = MIMEText(html_content, "html")
        message.attach(content)

        # Send the email using the start_session function
        start_session(message)

        print("Email Sent to -", name)

        return f"Email sent to: {name}<br>"

    except Exception as e:
        faild_email(name, to, role)
        print(f"Error sending email: {e}")  # Provide more detailed error information

        return f"Error sending email: {e} <br>"

# Function to send GD-1 mail (Group Discussion Invitation)
def send_GD1_mail(to,role='',sub='',link='',date='',time='',name="Candidate"):
    """
    Sends an email inviting a candidate to participate in the Group Discussion (GD-1) round.

    Args:
        to (str): Recipient's email address.
        role (str): Role applied for.
        sub (str): Subject of the email.
        link (str): Google Meet link for the GD-1 session.
        date (str): Date of the GD-1 round in 'YYYY-MM-DD' format.
        time (str): Time when the GD-1 will start.
        name (str): Name of the candidate (default is "Candidate").

    Returns:
        str: Confirmation message if the email is sent or an error message.
    """
    try:
        # Create a multi-part message to include both plain text and HTML content        
        message = MIMEMultipart("alternative")
        message["From"] = company_mail
        
        # Email subject and sender information
        # message["Subject"] = 'Congratulations! You Are Shortlisted for Group Discussion Round 1 || Elementis SoftTech' # Default subject line
        message["Subject"] = 'Final Opportunity! Rescheduled Group Discussion Round 1 || Elementis SoftTech' # Default subject line
        message["To"] = to
        date = get_date(date) #get date in dd-mm-yyyy format  
        time = get_time(time) # get time into 12 hour clock
        gd1_link = link    

        # PDF Attachment
        with open(r"CompanyProfile.pdf", 'rb') as f:
            pdf_attachment = MIMEApplication(f.read(), _subtype='pdf')
            pdf_attachment.add_header('Content-Disposition', 'attachment', filename='CompanyProfile.pdf')
            message.attach(pdf_attachment)

        # HTML content styled for design
        html_content = f"""
        <html>
        <head>
            <style>
            
            {get_css()}

            </style>
        </head>
        <body>
            <div class="email-container">
                <div class="header-logo">
                    <img src={logo} width="250">
                </div>
                <h2 style="text-align: center;">Elementis SoftTech || GD-1</h2>
                <p class="instructions">
                    Dear {name},<br><br>
                    Congratulations! We are pleased to inform you that you have been shortlisted for the next stage of our joining process for the role <b>{role}</b>.
                    <br><br>
                    We are excited to move forward with your application. The next step will be a Group Discussion(GD-1) , which will assess your Communication skills.<br>
                    <br>
                    Here are the details for the Group Discussion:<br>
                    📅 Date: <b>{date}</b><br>
                    ⏰ Time: <b>{time}</b><br>
                    Venue: Google Meet<br>
                    🔗 Meeting Link: <a href="{gd1_link}" target="_blank">{gd1_link}</a><br><br>
                    Please ensure you:<br>
                    1. Join the session at least 10 minutes before the scheduled time.<br>
                    2. Are well-prepared, as the evaluation will focus on your performance during the discussion.<br><br>
                    If you have any questions or need further assistance, feel free to reach out to us.
                    <br>
                    <b>We look forward to your participation in this round of the selection process.</b>
                </p>
                <div style="text-align: center;height:60px;justify-content: center;">
                    <a href="{gd1_link}" class="action-button" style="color:white;">Join Meet</a>
                </div>
                <p class="fallback-link">If the button above doesn't work, use the following link: <a href="{gd1_link}">{gd1_link}</a></p>
                
                <p class="instructions" style="text-align: center;">
                    Follow us to stay updated on this drive, as well as upcoming opportunities and hiring events.
                </p>
                <div class="social-links">
                    <a href="{linkedin_link}" target="_blank">LinkedIn</a> | 
                    <a href="{telegram_link}" target="_blank">Telegram</a> |
                    <a href="{insta_link}" target="_blank">Instagram</a> |
                    <a href="{fb_link}" target="_blank">Facebook</a>
                </div><br>
                <p class="content">
                    If you have any query write an email to : support@elementissofttech.com 
                </p>
                <div class="footer">
                    Best regards,<br>
                    Team Elementis SoftTech
                </div>
            </div>
        </body>
        </html>
        """


        # Attach the HTML content to the email
        content = MIMEText(html_content, "html")
        message.attach(content)

        # Send the email using the start_session function
        start_session(message)

        print("Email Sent to -", name)

        return f"Email sent to: {name}<br>"
    
    except Exception as e:
        faild_email(name, to, role)
        print(f"Error sending email: {e}")  # Provide more detailed error information

        return f"Error sending email: {e} <br>"

# Function to send a reminder for GD-1 (Group Discussion) round
def send_GD1_reminder_mail(to,role='',sub='',link='',date='',time='',name="Candidate"):
    """
    Sends a reminder email for the Group Discussion (GD-1) round of the selection process.

    Args:
        to (str): Recipient's email address.
        role (str): Role the candidate is applying for.
        sub (str): Subject of the email.
        link (str): Google Meet link for the GD-1 session.
        date (str): Date of the GD-1 round in 'YYYY-MM-DD' format.
        time (str): Time when the GD-1 will start.
        name (str): Name of the candidate (default is "Candidate").

    Returns:
        str: Confirmation message if the email is sent or an error message.
    """
    try:
        # Create a multi-part message to include both plain text and HTML content        
        message = MIMEMultipart("alternative")
        message["From"] = company_mail
        
        # Email subject and sender information

        message["Subject"] = 'Reminder: Group Discussion Round 1 || Elementis SoftTech' # Default subject line
        message["To"] = to
        date = get_date(date) #get date in dd-mm-yyyy format  
        time = get_time(time) # get time into 12 hour clock
        gd1_link = link 


        # HTML content styled for design
        html_content = f"""
        <html>
        <head>
            <style>
            
            {get_css()}

            </style>
        </head>
        <body>
            <div class="email-container">
                <div class="header-logo">
                    <img src="{logo}" width="250" alt="Elementis SoftTech Logo">
                </div>
                <h2 style="text-align: center;">Elementis SoftTech || GD-1</h2>
                <p class="instructions">
                    Dear {name},<br><br>
                    This is a friendly reminder about your upcoming Group Discussion Round (GD-1) as part of the selection process for the role <b>{role}</b>.
                    <br>
                    Here are the details for the Group Discussion:<br>
                    📅 Date: <b>{date}</b><br>
                    ⏰ Time: <b>{time}</b><br>
                    Venue: Google Meet<br>
                    🔗 Meeting Link: <a href="{gd1_link}" target="_blank">{gd1_link}</a><br><br>
                    Please ensure you:<br>
                    1. Join the session at least 10 minutes before the scheduled time.<br>
                    2. Are well-prepared, as the evaluation will focus on your performance during the discussion.<br><br>
                    If you have any questions or need further assistance, feel free to reach out to us.
                    <br>
                    <b>We look forward to your participation in this round of the selection process.</b>
                </p>
                <div style="text-align: center;height:60px;justify-content: center;">
                    <a href="{gd1_link}" class="action-button" style="color:white;">Join Meet</a>
                </div>
                <p class="fallback-link">If the button above doesn't work, use the following link: <a href="{gd1_link}">{gd1_link}</a></p>
                
                <p class="instructions" style="text-align: center;">
                    Follow us to stay updated on this drive, as well as upcoming opportunities and hiring events.
                </p>
                <div class="social-links">
                    <a href="{linkedin_link}" target="_blank">LinkedIn</a> | 
                    <a href="{telegram_link}" target="_blank">Telegram</a> |
                    <a href="{insta_link}" target="_blank">Instagram</a> |
                    <a href="{fb_link}" target="_blank">Facebook</a>
                </div><br>
                <p class="content">
                    If you have any query write an email to : support@elementissofttech.com 
                </p>
                <div class="footer">
                    Best regards,<br>
                    Team Elementis SoftTech
                </div>
            </div>
        </body>
        </html>
        """

        # Attach the HTML content to the email
        content = MIMEText(html_content, "html")
        message.attach(content)

        # Send the email using the start_session function
        start_session(message)

        # Log the success message
        print("Email Sent to -", name)

        return f"Email sent to: {name}<br>"

    except Exception as e:
        faild_email(name, to, role)
        print(f"Error sending email: {e}")  # Provide more detailed error information

        return f"Error sending email: {e} <br>"
    
# Function to send an email for the GD-2 (Group Discussion Round 2) selection
def send_GD2_mail(to,role='',sub='',link='',date='',time='',name="Candidate"):
    """
    Sends a confirmation email to the candidate who has been selected for Group Discussion Round 2 (GD-2).

    Args:
        to (str): Recipient's email address.
        role (str): Role the candidate is applying for.
        sub (str): Subject of the email.
        link (str): Google Meet link for the GD-2 session.
        date (str): Date of the GD-2 round in 'YYYY-MM-DD' format.
        time (str): Time when the GD-2 will start.
        name (str): Name of the candidate (default is "Candidate").

    Returns:
        str: Confirmation message if the email is sent or an error message.
    """
    try:
        # Create a multi-part message to include both plain text and HTML content        
        message = MIMEMultipart("alternative")
        message["From"] = company_mail
        
        # Email subject and sender information
        message["Subject"] = 'Congratulations! You Are Shortlisted for Group Discussion Round 2 || Elementis SoftTech' # Default subject line
        message["To"] = to
        date = get_date(date) #get date in dd-mm-yyyy format  
        time = get_time(time) # get time into 12 hour clock
        gd2_link = link

        # HTML content styled for design
        html_content = f"""
        <html>
        <head>
            <style>
            
            {get_css()}

            </style>
        </head>
        <body>
            <div class="email-container">
                <div class="header-logo">
                    <img src={logo} width="250">
                </div>
                <h2 style="text-align: center;">Elementis SoftTech || GD-2</h2>
                <p class="instructions">
                    Dear {name},<br><br>
                    Congratulations! We are pleased to inform you that you have successfully cleared Group Discussion Round 1 and have been selected to proceed to the next round (GD-2) of the selection process for the role <b>{role}</b>.
                    <br>
                    Your performance in the Group Discussion was impressive, and we are excited to move forward with your application. The next step will be a Group Discussion(GD-2).<br>
                    <br>
                    Here are the details for the Group Discussion:<br>
                    📅 Date: <b>{date}</b><br>
                    ⏰ Time: <b>{time}</b><br>
                    Venue: Google Meet<br>
                    🔗 Meeting Link: <a href="{gd2_link}" target="_blank">{gd2_link}</a><br><br>
                    Please ensure you:<br>
                    1. Join the session at least 10 minutes before the scheduled time.<br>
                    2. Are well-prepared, as the evaluation will focus on your performance during the discussion.<br><br>
                    If you have any questions or need further assistance, feel free to reach out to us.
                    <br>
                    <b>We look forward to your participation in this round of the selection process.</b>
                </p>
                <div style="text-align: center;height:60px;justify-content: center;">
                    <a href="{gd2_link}" class="action-button" style="color:white;">Join Meet</a>
                </div>
                <p class="fallback-link">If the button above doesn't work, use the following link: <a href="{gd2_link}">{gd2_link}</a> </p>
                
                <p class="instructions" style="text-align: center;">
                    Follow us to stay updated on this drive, as well as upcoming opportunities and hiring events.
                </p>
                <div class="social-links">
                    <a href="{linkedin_link}" target="_blank">LinkedIn</a> | 
                    <a href="{telegram_link}" target="_blank">Telegram</a> |
                    <a href="{insta_link}" target="_blank">Instagram</a> |
                    <a href="{fb_link}" target="_blank">Facebook</a>
                </div><br>
                <p class="content">
                    If you have any query write an email to : support@elementissofttech.com 
                </p>
                <div class="footer">
                    Best regards,<br>
                    Team Elementis SoftTech
                </div>
            </div>
        </body>
        </html>
        """

        # Attach the HTML content to the email
        content = MIMEText(html_content, "html")
        message.attach(content)

        # Send the email using the start_session function
        start_session(message)

        # Log the success message
        print("Email Sent to -", name)

        return f"Email sent to: {name}<br>"

    except Exception as e:
        faild_email(name, to, role)
        print(f"Error sending email: {e}")  # Provide more detailed error information

        return f"Error sending email: {e} <br>"

# Function to send a reminder email for GD-2 (Group Discussion Round 2)
def send_GD2_reminder_mail(to,role='',sub='',link='',date='',time='',name="Candidate"):
    """
    Sends a reminder email to the candidate for their upcoming GD-2 round (Group Discussion Round 2).

    Args:
        to (str): Recipient's email address.
        role (str): Role the candidate is applying for.
        sub (str): Subject of the email.
        link (str): Google Meet link for the GD-2 session.
        date (str): Date of the GD-2 round in 'YYYY-MM-DD' format.
        time (str): Time when the GD-2 will start.
        name (str): Name of the candidate (default is "Candidate").

    Returns:
        str: Confirmation message if the email is sent or an error message.
    """
    try:
        # Create a multi-part message to include both plain text and HTML content        
        message = MIMEMultipart("alternative")
        message["From"] = company_mail
        
        # Email subject and sender information
        message["Subject"] = 'Reminder: Group Discussion Round 2 || Elementis SoftTech' # Default subject line
        # message["Subject"] = 'Rescheduled Group Discussion Round 2 || Elementis SoftTech' # Default subject line
        message["To"] = to
        date = get_date(date) #get date in dd-mm-yyyy format  
        time = get_time(time) # get time into 12 hour clock
        gd2_link = link


        # HTML content styled for design
        html_content = f"""
        <html>
        <head>
            <style>
            
            {get_css()}

            </style>
        </head>
        <body>
            <div class="email-container">
                <div class="header-logo">
                    <img src="{logo}" width="250" alt="Elementis SoftTech Logo">
                </div>
                <h2 style="text-align: center;">Elementis SoftTech || GD-2</h2>
                <p class="instructions">
                    Dear {name},<br><br>
                    This is a friendly reminder about your upcoming Group Discussion Round 2 (GD-2) as part of the selection process for the role <b>{role}</b>.
                    <br>Here are the details for the Group Discussion:<br>
                    📅 Date: <b>{date}</b><br>
                    ⏰ Time: <b>{time}</b><br>
                    Venue: Google Meet<br>
                    🔗 Meeting Link: <a href="{gd2_link}" target="_blank">{gd2_link}</a><br><br>
                    Please ensure you:<br>
                    1. Join the session at least 10 minutes before the scheduled time.<br>
                    2. Are well-prepared, as the evaluation will focus on your performance during the discussion.<br><br>
                    If you have any questions or need further assistance, feel free to reach out to us.
                    <br>
                    <b>We look forward to your participation in this round of the selection process.</b>
                </p>
                <div style="text-align: center;height:60px;justify-content: center;">
                    <a href="{gd2_link}" class="action-button" style="color:white;">Join Meet</a>
                </div>
                <p class="fallback-link">If the button above doesn't work, use the following link: 
                <a href="{gd2_link}">{gd2_link}</a></p>
                <p class="instructions" style="text-align: center;">
                    Follow us to stay updated on this drive, as well as upcoming opportunities and hiring events.
                </p>
                <div class="social-links">
                    <a href="{linkedin_link}" target="_blank">LinkedIn</a> | 
                    <a href="{telegram_link}" target="_blank">Telegram</a> |
                    <a href="{insta_link}" target="_blank">Instagram</a> |
                    <a href="{fb_link}" target="_blank">Facebook</a>
                </div><br>
                <p class="content">
                    If you have any query write an email to : support@elementissofttech.com 
                </p>
                <div class="footer">
                    Best regards,<br>
                    Team Elementis SoftTech
                </div>
            </div>
        </body>
        </html>
        """

        # Attach the HTML content to the email
        content = MIMEText(html_content, "html")
        message.attach(content)

        # Send the email using the start_session function
        start_session(message)

        # Log the success message
        print("Email Sent to -", name)

        return f"Email sent to: {name}<br>"

    except Exception as e:
        faild_email(name, to, role)
        # Provide detailed error handling
        print(f"Error sending email: {e}")

        return f"Error sending email: {e} <br>"

# Function for sending technical assessment registration email
def send_technical_assessment_register_mail(to,role='',sub='',link='',date='',time='',name="Candidate"):
    """
    Sends an email to the candidate with the registration details for the technical assessment round.

    Args:
        to (str): Recipient's email address.
        role (str): Role the candidate is applying for.
        sub (str): Subject of the email.
        link (str): Registration link for the technical round.
        date (str): Date of the technical round in 'YYYY-MM-DD' format.
        time (str): Time of the technical round.
        name (str): Name of the candidate (default is "Candidate").

    Returns:
        str: Confirmation message if the email is sent, or error message.
    """
    try:
        # Create a multi-part message to include both plain text and HTML content        
        message = MIMEMultipart("alternative")
        message["From"] = company_mail
        
        # Email subject and sender information
        message["Subject"] = 'Registration for Technical Round || Elementis SoftTech' # Default subject line
        message["To"] = to
        date = get_date(date) #get date in dd-mm-yyyy format  
        time = get_time(time) # get time into 12 hour clock
        registration_link = link

        # HTML content styled for design
        html_content = f"""
        <html>
        <head>
            <style>
            
            {get_css()}

            </style>
        </head>
        <body>
            <div class="email-container">
                <div class="header-logo">
                    <img src="{logo}" width="250" alt="Elementis SoftTech Logo">
                </div>
                <h2 style="text-align: center;">Congratulations || Registration for Technical Round</h2>
                <p class="content">
                    Dear {name},<br><br>
                    Thank you for participating in Elementis SoftTech’s selection process for the role <b>{role}</b>. We value your enthusiasm and interest.<br><br>
                    To maintain a transparent and fair process, we charge a nominal fee for the technical round. This covers costs for using HackerRank, a premium assessment platform that ensures high standards in evaluating technical skills.<br><br>
                    Passing this fee to candidates helps us manage resources responsibly and avoid unnecessary expenses for no-shows after registration.
                </p>
                <p class="content">
                    Here’s what this step ensures for all candidates:
                    <ul>
                        <li><b>Fair Opportunity:</b> By conducting an advanced technical evaluation, we aim to shortlist candidates who meet the technical standards we require for our projects.</li>
                        <li><b>Transparency:</b> The fee charged is entirely directed towards covering the costs associated with your assessment.</li>
                        <li><b>Career Development:</b> Every participant in this process, regardless of the outcome, will have an opportunity to gain valuable experience.</li>
                    </ul>
                </p>
                <p class="content">
                    After the technical round:<br>
                    <ul>
                        <li><b>Qualified Candidates:</b> Those who qualify will join as stipend interns (₹6000/month). Outstanding performers will also be eligible for a Pre-Placement Offer (PPO) with a starting salary of ₹4–6 LPA.</li>
                        <li><b>Candidates Who Couldn’t Qualify:</b> We believe learning is a journey. To support this, we will offer an unpaid internship where you can gain hands-on experience and earn a certificate of completion. This certificate will serve as a valuable addition to your résumé, reflecting relevant industry exposure.</li>
                    </ul>
                </p>
                <div style="text-align: center;height:60px;justify-content: center;">
                    <a href="{registration_link}" class="action-button" style="color:white;">Register</a>
                </div>
                <p class="fallback-link">If the button above doesn't work, use the following link:</p>
                <p style="word-wrap: break-word; text-align: center;"><a href="{registration_link}">{registration_link}</a></p><br>
                <p class="content">
                    To proceed further, please register for the Technical Round using the link below. After registration, you will receive the date and time slot for your technical round. <br>
                </p>
                <p class="instructions" style="text-align: center;">
                    Follow us to stay updated on this drive, as well as upcoming opportunities and hiring events.
                </p>
                <div class="social-links">
                    <a href="{linkedin_link}" target="_blank">LinkedIn</a> | 
                    <a href="{telegram_link}" target="_blank">Telegram</a> |
                    <a href="{insta_link}" target="_blank">Instagram</a> |
                    <a href="{fb_link}" target="_blank">Facebook</a>
                </div><br>
                <p class="content">
                    If you have any query write an email to : support@elementissofttech.com 
                </p>
                <div class="footer">
                    Best regards,<br>
                    Elementis SoftTech
                </div>
            </div>
        </body>
        </html>
        """


        # Attach the HTML content to the email
        content = MIMEText(html_content, "html")
        message.attach(content)

        # Send the email using the start_session function
        start_session(message)

        # Log the success message
        print("Email Sent to -", name)

        return f"Email sent to: {name}<br>"

    except Exception as e:
        faild_email(name, to, role)
        # Provide detailed error handling
        print(f"Error sending email: {e}")

        return f"Error sending email: {e} <br>"

# Function to send a reminder email for the technical assessment registration
def send_technical_assessment_register_reminder_mail(to,role='',sub='',link='',date='',time='',name="Candidate"):   
    """
    Sends a reminder email to the candidate to complete the registration for the technical assessment round.

    Args:
        to (str): Recipient's email address.
        role (str): Role the candidate is applying for.
        sub (str): Subject of the email.
        link (str): Registration link for the technical round.
        date (str): Date of the technical round in 'YYYY-MM-DD' format.
        time (str): Time of the technical round.
        name (str): Name of the candidate (default is "Candidate").

    Returns:
        str: Confirmation message if the email is sent, or error message.
    """
    try:
        # Create a multi-part message to include both plain text and HTML content        
        message = MIMEMultipart("alternative")
        message["From"] = company_mail
        
        # Email subject and sender information
        message["Subject"] = 'Reminder: Registration for Technical Round || Elementis SoftTech' # Default subject line
        message["To"] = to
        date = get_date(date) #get date in dd-mm-yyyy format  
        time = get_time(time) # get time into 12 hour clock
        registration_link = link

        # HTML content styled for design
        html_content = f"""
        <html>
        <head>
            <style>
            
            {get_css()}

            </style>
        </head>
        <body>
            <div class="email-container">
                <div class="header-logo">
                    <img src={logo} width="250">
                </div>
                <h2 style="text-align: center;">Elementis SoftTech || Technical Round Registration</h2>
                <p class="instructions">
                    Dear {name},<br><br>
                    <b>If you have already registered, please ignore this reminder.</b> This is a friendly reminder to complete your registration for the upcoming Technical Round for the role <b>{role}</b>. The registration is a crucial step in the selection process, and we don't want you to miss out on this opportunity.
                    <br><br>
                    <b> Note: </b> The registration link will expire soon. Kindly complete the registration process at the earliest to avoid missing out on this opportunity.
                    <br><br>
                    Please click the button below to complete your registration and secure your spot for the Technical Round.
                </p>
                <div style="text-align: center;height:60px;justify-content: center;">
                    <a href="{registration_link}" class="action-button" style="color:white;">Register Now</a>   
                </div>
                <p class="fallback-link">If the button above doesn't work, use the following link: <a href="{registration_link}">{registration_link}</a></p>    
                <p class="instructions" style="text-align: center;">
                    Follow us to stay updated on this drive, as well as upcoming opportunities and hiring events.   
                </p>
                <div class="social-links">      
                    <a href="{linkedin_link}" target="_blank">LinkedIn</a> |
                    <a href="{telegram_link}" target="_blank">Telegram</a> |
                    <a href="{insta_link}" target="_blank">Instagram</a> |
                    <a href="{fb_link}" target="_blank">Facebook</a>  
                </div><br>      
                <p class="content">
                    If you have any query write an email to : support@elementissofttech.com 
                </p>
                <div class="footer">
                    Best regards,<br>
                    Team Elementis SoftTech 
                </div>  
            </div>
        </body> 
        </html>
        """

        # Attach the HTML content to the email
        content = MIMEText(html_content, "html")    
        message.attach(content)

        # Send the email using the start_session function
        start_session(message)

        # Log the success message
        print("Email Sent to -", name)

        return f"Email sent to: {name}<br>"
    
    except Exception as e:
        faild_email(name, to, role)
        # Provide detailed error handling
        print(f"Error sending email: {e}")

# Function to send a confirmation email for the technical assessment round with transaction details

def send_technical_assessment_confirmation_mail(to,role='',t_id='',link='',date='',time='',name="Candidate"):
    """
    Sends an email to the candidate confirming their registration for the technical assessment round.

    Args:
        to (str): Recipient's email address.
        role (str): Role the candidate is applying for.
        sub (str): Subject of the email.
        link (str): Registration link for the technical round.
        date (str): Date of the technical round in 'YYYY-MM-DD' format.
        time (str): Time of the technical round.    
        name (str): Name of the candidate (default is "Candidate").

    Returns:
        str: Confirmation message if the email is sent, or error message.
    """

    try:
        # Create a multi-part message to include both plain text and HTML content        
        message = MIMEMultipart("alternative")
        message["From"] = company_mail
        
        # Email subject and sender information
        message["Subject"] = 'Confirmation: Registration for Technical Round || Elementis SoftTech' # Default subject line
        message["To"] = to
        date = get_date(date) #get date in dd-mm-yyyy format  
        time = get_time(time) # get time into 12 hour clock
        registration_link = link

        # HTML content styled for design
        html_content = f"""
        <html>
        <head>
            <style>
            
            {get_css()}

            </style>
        </head>
        <body>
            <div class="email-container">
                <div class="header-logo">
                    <img src={logo} width="250">
                </div>
                <h2 style="text-align: center;">Elementis SoftTech || Technical Round Registration</h2>
                <p class="content">
                    Dear {name},<br><br>
                    We are pleased to confirm your successful registration for the upcoming Technical Round for the role <b>{role}</b>.<br><br>
                    Here are the details for the Technical Round:<br>
                    📅 Date: <b>{date}</b><br>
                    ⏰ Time: <b>{time}</b><br><br>
                    This invite is valid from: {date} {time} to {date} {(datetime.strptime(time, "%I:%M %p") + timedelta(hours=6)).strftime("%I:%M %p").lstrip("0")}.<br><br>
                    Please ensure you are prepared for the assessment and follow the instructions provided during the test.<br><br>
                    If you have any questions or need further assistance, feel free to reach out to us.<br><br>
                    We wish you the best of luck for the Technical Round and look forward to your participation.<br>
                </p>
                <p class="content">
                    <b>Transaction Details:</b><br>
                    <ul>
                        <li><b>Transaction ID:</b> {t_id}</li>
                        <li><b>Amount Paid:</b> ₹299</li>
                    </ul>
                </p>
                <div style="text-align: center;height:60px;justify-content: center;">
                    <a href="{registration_link}" class="action-button" style="color:white;">Start Assessment</a>
                </div>
                <p class="fallback-link">If the button above doesn't work, use the following link: <a href="{registration_link}">{registration_link}</a></p>    
                <p class="instructions" style="text-align: center;">
                    Follow us to stay updated on this drive, as well as upcoming opportunities and hiring events.
                </p>
                <div class="social-links">
                    <a href="{linkedin_link}" target="_blank">LinkedIn</a> |
                    <a href="{telegram_link}" target="_blank">Telegram</a> |
                    <a href="{insta_link}" target="_blank">Instagram</a> |
                    <a href="{fb_link}" target="_blank">Facebook</a>
                </div><br>
                <p class="content">
                    If you have any query write an email to : support@elementissofttech.com 
                </p>
                <div class="footer">
                    Best regards,<br>
                    Team Elementis SoftTech
                </div>
            </div>
        </body>
        </html>
        """

        # Attach the HTML content to the email
        content = MIMEText(html_content, "html")
        message.attach(content)

        # Send the email using the start_session function
        start_session(message)

        # Log the success message
        print("Email Sent to -", name," with Transaction ID -", t_id)

        return f"Email sent to: {name} with Transaction ID - {t_id}<br>"
    
    except Exception as e:
        faild_email(name, to, role)
        # Provide detailed error handling
        print(f"Error sending email: {e}")




# Function for sending technical assessment email
def send_technical_assessment_mail(to,role='',sub='',link='',date='',time='',name="Candidate"):
    """
    Sends an email with the technical assessment details to the candidate.

    Args:
        to (str): Recipient's email address.
        role (str): Role the candidate is applying for.
        sub (str): Subject of the email.
        link (str): Link to start the technical assessment.
        date (str): Date when the assessment is available (in 'YYYY-MM-DD' format).
        time (str): Time when the assessment is available.
        name (str): Name of the candidate (default is "Candidate").

    Returns:
        str: Confirmation message if the email is sent, or error message.
    """
    try:
        # Create a multi-part message to include both plain text and HTML content        
        message = MIMEMultipart("alternative")
        message["From"] = company_mail
        
        # Email subject and sender information
        message["Subject"] = 'Invitation to Technical Round || Elementis SoftTech' # Default subject line
        message["To"] = to
        date = get_date(date) #get date in dd-mm-yyyy format  
        time = get_time(time) # get time into 12 hour clock
        assessment_link = link

        # HTML content styled for design
        html_content = f"""
        <html>
        <head>
            <style>
            
            {get_css()}

            </style>
        </head>
        <body>
            <div class="email-container">
                <div class="header-logo">
                    <img src={logo} width="250">
                </div>
                <h2 style="text-align: center;">Elementis SoftTech || Technical Round</h2>
                <p class="instructions">
                    Hi {name},<br><br>
                    Welcome to Elementis SoftTech Campus Drive(Technical Round) for the role <b>{role}</b><br>
                    - This is a 120-minute Assessment.<br>
                    - Make sure to take the assessment on your Desktop/Laptop.<br>
                    - Mute all notifications. Any popup or antivirus notification is treated as off-tab activity. Disable all notifications before starting the test.<br>
                    - Highly Important: Please clear browser cache and cookies before starting the test; otherwise, it can affect the test session.<br>
                    - Ensure that your laptop time zone is set to (UTC+05:30) Chennai, Kolkata, Mumbai, New Delhi, to avoid any timezone-related issues.<br>
                    - Any attempt to copy from the internet, copy from others, or impersonate would lead to outright rejection as all the submissions are monitored by AI.</b>.<br>
                    <br><br>
                    <b>A couple of things to keep in mind while taking the assessment:<br>
                    i) This invite is valid from: {date} {time} to {date} {(datetime.strptime(time, "%I:%M %p") + timedelta(hours=6)).strftime("%I:%M %p").lstrip("0")}.<br>
                    ii) Please take the test on your desktop or laptop.<br>
                    iii) Choose a quiet location where you will not be interrupted.<br>
                    iv) Ensure you have a reliable internet connection before starting the test.<br></b>
                </p>
                <div style="text-align: center;">
                    <a href="{assessment_link}" style="color:white"class="action-button">Start Assessment</a>
                </div>
                <p class="fallback-link">If the button above doesn't work, use the following link: <a href="{assessment_link}">{assessment_link}</a></p> <br> 
                <p class="instructions" style="text-align: center;">
                    Follow us to stay updated on this drive, as well as upcoming opportunities and hiring events.
                </p>
                <div class="social-links">
                    <a href="{linkedin_link}" target="_blank">LinkedIn</a> | 
                    <a href="{telegram_link}" target="_blank">Telegram</a> |
                    <a href="{insta_link}" target="_blank">Instagram</a> |
                    <a href="{fb_link}" target="_blank">Facebook</a>
                </div><br>
                <p class="content">
                    If you have any query write an email to : support@elementissofttech.com 
                </p>
                <div class="footer">
                    Best regards,<br>
                    Team Elementis SoftTech
                </div>
            </div>
        </body>
        </html>
        """

        # Attach the HTML content to the email
        content = MIMEText(html_content, "html")
        message.attach(content)

        # Send the email using the start_session function
        start_session(message)

        # Log the success message
        print("Email Sent to -", name)

        return f"Email sent to: {name}<br>"

    except Exception as e:
        faild_email(name, to, role)
        # Provide detailed error handling
        print(f"Error sending email: {e}")

        return f"Error sending email: {e} <br>"
    

# Function for sending process feedback email
def send_process_feedback_mail(to,role='',sub='',link='',date='',time='',name="Candidate"):
    """
    Sends an email to the candidate asking for feedback on the hiring process.

    Args:
        to (str): Recipient's email address.
        role (str): Role the candidate applied for.
        sub (str): Subject of the email.
        link (str): Link to the feedback form.
        date (str): The date when the email is being sent (in 'YYYY-MM-DD' format).
        time (str): The time when the email is being sent.
        name (str): Name of the candidate (default is "Candidate").

    Returns:
        str: Confirmation message if the email is sent, or error message.
    """
    try:
        # Create a multi-part message to include both plain text and HTML content        
        message = MIMEMultipart("alternative")
        message["From"] = company_mail
        
        # Email subject and sender information
        message["Subject"] = 'Share Your Feedback – We Value Your Opinion! || Elementis Softech' # Default subject line
        message["To"] = to
        date = get_date(date) #get date in dd-mm-yyyy format  
        time = get_time(time) # get time into 12 hour clock
        feedback_link = link

        # HTML content styled for design
        html_content = f"""
        <html>
        <head>
            <style>
            
            {get_css()}

            </style>
        </head>
        <body>
            <div class="email-container">
                <div class="header-logo">
                    <img src="{logo}" width="250" alt="Elementis SoftTech Logo">
                </div>
                <h2 style="text-align: center;">Elementis SoftTech || Feedback</h2>
                <p class="instructions">
                    Dear {name},<br><br>
                    Thank you for your interest in our opportunity and the effort you put into your application for the role <b>{role}</b>.<br><br>
                    After much consideration, we’ve decided not to proceed with your candidacy at this time. This decision was not easy, as we had many strong applicants, and it’s not a reflection of your skills or potential.<br><br>
                    We’ll keep your profile on file for future opportunities and encourage you to stay connected with us.<br><br>
                    We sincerely wish you the best in your career journey and thank you again for considering us.
                </p>
                <p class="instructions">
                    Thank you for participating in the hiring process for the Associate Web Developer role at Elementis SoftTech. We value your input and would like to hear your feedback on the overall hiring experience.
                </p>
                <div style="text-align: center;height:60px;justify-content: center;">
                    <a href="{feedback_link}" class="action-button" style="color:white;">Give Feedback</a>
                </div>
                <p class="instructions" style="text-align: center;">
                    Follow us to stay updated on this drive, as well as upcoming opportunities and hiring events.
                </p>
                <div class="social-links">
                    <a href="{linkedin_link}" target="_blank">LinkedIn</a> | 
                    <a href="{telegram_link}" target="_blank">Telegram</a> |
                    <a href="{insta_link}" target="_blank">Instagram</a> |
                    <a href="{fb_link}" target="_blank">Facebook</a>
                </div><br>
                <p class="content">
                    If you have any query write an email to : support@elementissofttech.com 
                </p>
                <div class="footer">
                    Best regards,<br>
                    Team Elementis SoftTech
                </div>
            </div>
        </body>
        </html>
        """


        # Attach the HTML content to the email
        content = MIMEText(html_content, "html")
        message.attach(content)

        # Send the email using the start_session function
        start_session(message)

        # Log the success message
        print("Email Sent to -", name)

        return f"Email sent to: {name}<br>"

    except Exception as e:
        faild_email(name, to, role)
        # Provide detailed error handling
        print(f"Error sending email: {e}")

        return f"Error sending email: {e} <br>"


# Function for sending non-selection email
def send_non_selection_mail(to, role='', sub='', link='', date='', time='', name="Candidate"):
    """
    Sends an email to a candidate informing them that they have not been selected for the role but offering an unpaid internship.

    Args:
        to (str): Recipient's email address.
        role (str): Role the candidate applied for.
        sub (str): Subject of the email.
        link (str): Link to the meeting (e.g., Google Meet) for discussing the internship.
        date (str): The date of the meeting (in 'YYYY-MM-DD' format).
        time (str): The time of the meeting.
        name (str): Name of the candidate (default is "Candidate").

    Returns:
        str: Confirmation message if the email is sent, or error message.
    """
    try:
        # Create a multi-part message to include both plain text and HTML content        
        message = MIMEMultipart("alternative")
        message["From"] = company_mail
        
        # Email subject and sender information
        message["Subject"] = 'Application Update – Unpaid Internship Opportunity || Elementis Softech' # Default subject line
        message["To"] = to
        date = get_date(date) #get date in dd-mm-yyyy format  
        time = get_time(time) # get time into 12 hour clock
        meeting_link = link

        # HTML content
        html_content = f"""
        <html>
        <head>
            <style>
            
            {get_css()}

            </style>
        </head>
        <body>
            <div class="email-container">
                <div class="header-logo">
                    <img src="{logo}" width="250" alt="Elementis SoftTech Logo">
                </div>
                <h2 style="text-align: center;">Elementis SoftTech || Application Update</h2>
                <p class="instructions">
                    Dear {name},<br><br>
                    Thank you for participating in the selection process for the role <b>{role}</b> at Elementis SoftTech.<br><br>
                    While you didn’t pass the technical round, we are pleased to offer you an opportunity to join our unpaid internship program. This will provide you with hands-on experience, learning opportunities, and a certificate of completion that will strengthen your resume and career prospects.<br><br>
                    We have scheduled an introductory meeting to discuss the internship and answer any questions you might have. Please find the details below:<br>
                    <b>Date:</b> {date}<br>
                    <b>Time:</b> {time}<br>
                </p>
                <div style="text-align: center;height:60px;justify-content: center;">
                    <a href="{meeting_link}" class="action-button" style="color:white;">Join meet</a>
                </div>
                <p class="fallback-link">If the button above doesn't work, use the following link: </p>
                <a href="{meeting_link}">{meeting_link}</a>
                <p class="instructions">
                    <b>Instructions for Joining the Meeting:</b><br>
                    1. Ensure a stable internet connection.<br>
                    2. Use the link above to join the meeting at the scheduled time.<br>
                    3. Keep your microphone muted unless speaking.<br>
                </p>
                <p class="instructions" style="text-align: center;">
                    Follow us to stay updated on this drive, as well as upcoming opportunities and hiring events.
                </p>
                <div class="social-links">
                    <a href="{linkedin_link}" target="_blank">LinkedIn</a> | 
                    <a href="{telegram_link}" target="_blank">Telegram</a> |
                    <a href="{insta_link}" target="_blank">Instagram</a> |
                    <a href="{fb_link}" target="_blank">Facebook</a>
                </div><br>
                <p class="content">
                    If you have any query write an email to : support@elementissofttech.com 
                </p>
                <div class="footer">
                    Best regards,<br>
                    Team Elementis SoftTech
                </div>
            </div>
        </body>
        </html>
        """

        # Attach the HTML content to the email
        content = MIMEText(html_content, "html")
        message.attach(content)

        # Send the email using the start_session function
        start_session(message)

        # Log the success message
        print("Email Sent to -", name)

        return f"Email sent to: {name}<br>"

    except Exception as e:
        faild_email(name, to, role)
        # Provide detailed error handling
        print(f"Error sending email: {e}")

        return f"Error sending email: {e} <br>"


# Function for sending selection mail
def send_selection_mail(to, role='', sub='', link='', date='', time='', name="Candidate"):
    try:
        # Create a multi-part message to include both plain text and HTML content        
        message = MIMEMultipart("alternative")
        message["From"] = company_mail
        
        # Email subject and sender information
        # Email subject and recipient
        message["Subject"] = 'Application Update – Internship Opportunity || Elementis Softech' # Default subject line
        message["To"] = to

        # Google meet link
        meeting_link = link

        # Format the date to 'DD-MM-YYYY' format
        date = get_date(date)

        # HTML content for the selection email
        html_content = f"""
        <html>
        <head>
            <style>
            {get_css()}
            </style>
        </head>
        <body>
            <div class="email-container">
                <div class="header-logo">
                    <img src="{logo}" width="250" alt="Elementis SoftTech Logo">
                </div>
                <h2 style="text-align: center;">Elementis SoftTech || Internship Opportunity</h2>
                <p class="instructions">
                    Dear {name},<br><br>
                    Congratulations! We are pleased to inform you that you have been selected for the role of {role} at Elementis SoftTech.<br><br>
                    After careful consideration, we have selected you based on your strong performance and skills shown during the assessment.<br><br>
                    Here are the details for the next steps in the process:<br>
                    <b>Date:</b> {date}<br>
                    <b>Time:</b> {time}<br><br>
                    Please join the meeting at the specified time by clicking the link below:
                </p>
                <div style="text-align: center;height:60px;justify-content: center;">
                    <a href="{meeting_link}" class="action-button" style="color:white;">Join the Meeting</a>
                </div>
                <p class="fallback-link">If the button above doesn't work, use the following link: </p>
                <a href="{meeting_link}">{meeting_link}</a><br>
                <p class="instructions">
                    <b>Instructions:</b><br>
                    1. Please confirm your availability by clicking on the link above.<br>
                    2. Join the meeting at the specified time.<br>
                    3. Make sure you are in a quiet environment and have a stable internet connection.<br>
                    4. Prepare any documents or materials as per the instructions provided in the link.<br>
                    5. If you have any questions, feel free to reach out to us.
                </p>
                <p class="instructions" style="text-align: center;">
                    Follow us to stay updated on this drive, as well as upcoming opportunities and hiring events.
                </p>
                <div class="social-links">
                    <a href="{linkedin_link}" target="_blank">LinkedIn</a> | 
                    <a href="{telegram_link}" target="_blank">Telegram</a> |
                    <a href="{insta_link}" target="_blank">Instagram</a> |
                    <a href="{fb_link}" target="_blank">Facebook</a>
                </div><br>
                <p class="content">
                    If you have any query, please write an email to: support@elementissofttech.com
                </p>
                <div class="footer">
                    Best regards,<br>
                    Team Elementis SoftTech
                </div>
            </div>
        </body>
        </html>
        """

        # Attach the HTML content to the email
        content = MIMEText(html_content, "html")
        message.attach(content)

        # Send the email using the start_session function
        start_session(message)

        # Log the success message
        print("Email Sent to -", name)

        return f"Email sent to: {name}<br>"

    except Exception as e:
        faild_email(name, to, role)
        # Provide detailed error handling
        print(f"Error sending email: {e}")

        return f"Error sending email: {e} <br>"


# Function for sending internship offer letter email
def send_internship_offer_letter_mail(to,role='',sub='',link='',date='',batch='',Id="",name=""):
    """
    Sends an internship offer letter to the selected candidate.

    Args:
        to (str): Recipient's email address.
        role (str): Role for the internship.
        sub (str): Subject of the email.
        link (str): Link to the internship details (if any).
        date (str): Date the internship starts.
        batch (str): Batch or cohort the intern belongs to.
        Id (str): Candidate's ID.
        name (str): Name of the candidate.

    Returns:
        str: Confirmation message if the email is sent, or error message.
    """
    try:
        # Create a multi-part message to include both plain text and HTML content        
        message = MIMEMultipart("alternative")
        message["From"] = company_mail
        
        # Email subject and sender information
        message["Subject"] = 'Congratulations on Your Internship Offer || Elementis Softech' # Default subject line
        message["To"] = to
        file_path = create_internship_offer_letter(name,to,batch,Id,role,date)

        # PDF Attachment
        with open(file_path, 'rb') as f:
            pdf_attachment = MIMEApplication(f.read(), _subtype='pdf')
            pdf_attachment.add_header('Content-Disposition', 'attachment', filename=name+' Offer Letter.pdf')
            message.attach(pdf_attachment)

        # HTML content
        html_content = f"""
        <html>
        <head>
            <style>
            
            {get_css()}

            </style>
        </head>
        <body>
            <div class="email-container">
                <div class="header-logo">
                    <img src="{logo}" width="250" alt="Elementis SoftTech Logo">
                </div>
                <h2 style="text-align: center;">Congratulations on Your Internship Offer!</h2>
                <p class="instructions">
                    Dear {name},<br><br>
                    We are delighted to inform you that you have been selected for an internship position at Elementis SoftTech for the role of <b>{role}</b>.<br><br>
                    This internship provides a fantastic opportunity to gain hands-on experience, expand your skill set, and earn a certificate upon completion. We are excited to have you on board and look forward to working with you.<br><br>
                    
                    Find your official offer letter attached to this email. Please review the details of your internship.<br><br>
                </p>
                <p class="important-instructions">
                    Please mail the signed and scanned soft copy of the offer letter and the documents as mentioned below to
                    <b>hr@elementissofttech.com</b> within 2 working days from the receipt of this mail:
                </p>
                <ul class="instructions">
                    <li>Copy of valid government-issued ID (Aadhar, Passport, etc.)</li>
                    <li>Updated resume</li>
                    <li>Educational certificates (highest qualification)</li>
                </ul>
                <p class="instructions" style="text-align: center;">
                    Follow us to stay updated on this drive, as well as upcoming opportunities and hiring events.
                </p>
                <div class="social-links">
                    <a href="{linkedin_link}" target="_blank">LinkedIn</a> | 
                    <a href="{telegram_link}" target="_blank">Telegram</a> |
                    <a href="{insta_link}" target="_blank">Instagram</a> |
                    <a href="{fb_link}" target="_blank">Facebook</a>
                </div><br>
                <p class="content">
                    If you have any query write an email to : support@elementissofttech.com 
                </p>
                <div class="footer">
                    Best regards,<br>
                    Team Elementis SoftTech
                </div>
            </div>
        </body>
        </html>
        """


        # Attach HTML content
        content = MIMEText(html_content, "html")
        message.attach(content)

        # Send the email using the start_session function
        start_session(message)

        # Log the success message
        print("Email Sent to -", name)

        return f"Email sent to: {name}<br>"

    except Exception as e:
        faild_email(name, to, role)
        # Provide detailed error handling
        print(f"Error sending email: {e}")

        return f"Error sending email: {e} <br>"
    