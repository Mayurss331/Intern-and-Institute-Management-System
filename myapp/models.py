from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
import uuid

from datetime import date

class TransactionManager(models.Manager):
    def incomes(self):
        return self.filter(transaction_type="Income")

    def expenses(self):
        return self.filter(transaction_type="Expense")


class Transaction(models.Model):
    # Transaction Type Choices
    TRANSACTION_TYPES = [
        ('Income', 'Income'),
        ('Expense', 'Expense'),
    ]

    # Payment Mode Choices
    PAYMENT_MODES = [
        ('Cash', 'Cash'),
        ('Bank Transfer', 'Bank Transfer'),
        ('Credit Card', 'Credit Card'),
        ('UPI', 'UPI'),
        ('Other', 'Other'),
    ]

    # Status Choices
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Failed', 'Failed'),
    ]

    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="transactions")  
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)  # High precision for transactions
    description = models.TextField()
    category = models.CharField(max_length=100)  # Consider using choices if predefined categories exist
    payment_mode = models.CharField(max_length=20, choices=PAYMENT_MODES, default='Cash')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="Completed")
    timestamp = models.DateTimeField(auto_now_add=True)  # Automatically set when created
    document = models.FileField(upload_to='transaction_documents/', blank=True, null=True)  

    class Meta:
        ordering = ['-timestamp']
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"

    def __str__(self):
        return f"{self.user.username} | {self.transaction_type} | {self.amount} | {self.timestamp.strftime('%Y-%m-%d %H:%M')}"





class Application(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other')
    ]
    OFFER_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Sent', 'Sent'),
        ('Rejected', 'Rejected'),
    ]

    role = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20)
    resume = models.URLField(default="")
    source = models.CharField(max_length=255)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    domicile_state = models.CharField(max_length=255)
    current_location = models.CharField(max_length=255)
    citizenship = models.CharField(max_length=255)
    postgraduate_degree = models.CharField(max_length=255, blank=True, null=True)
    postgraduate_stream = models.CharField(max_length=255, blank=True, null=True)
    postgraduate_passing_year = models.IntegerField(blank=True, null=True)
    undergraduate_degree = models.CharField(max_length=255)
    undergraduate_stream = models.CharField(max_length=255)
    undergraduate_passing_year = models.IntegerField()
    college_name = models.CharField(max_length=255)
    score_above_60 = models.BooleanField(default=False)
    standing_arrears = models.BooleanField(default=False)
    coding_languages = models.TextField()
    currently_working = models.BooleanField(default=False)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    ctc_or_stipend = models.FloatField(blank=True, null=True)
    designation = models.CharField(max_length=255, blank=True, null=True)
    open_to_relocate = models.BooleanField(default=False)
    passport_photo = models.URLField(default="")
    offer_status = models.CharField(max_length=10, choices=OFFER_STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"


class UserPerformance(models.Model):
    batch_id=models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey(Application, on_delete=models.CASCADE)  # Link to User model
    aptitude_score = models.FloatField(default=0, blank=True)  # Aptitude Test Score
    gd1_attendance = models.BooleanField(default=False)  # Attendance for GD1
    gd1_marks = models.FloatField(default=0, blank=True)  # Marks for GD1
    gd2_attendance = models.BooleanField(default=False)  # Attendance for GD2
    gd2_marks = models.FloatField(default=0, blank=True)  # Marks for GD2
    fees_paid = models.BooleanField(default=False)  # Has the user paid the fees?
    technical_marks = models.FloatField(default=0, blank=True)  # Technical Evaluation Score
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when record is created
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp for the last update

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - Performance"
    


class CandidatePerformance(models.Model):
    PERFORMANCE_RATINGS = [(i, str(i)) for i in range(1, 11)]  # Rating scale from 1 to 10
    ATTENDANCE_STATUS = [
        ('Present', 'Present'),
        ('Absent', 'Absent'),
        ('Late', 'Late'),
        ('Excused', 'Excused')
    ]

    candidate = models.ForeignKey(Application, on_delete=models.CASCADE, related_name="performance")
    date = models.DateField(default=date.today)  # Automatically sets the current date

    # Work & Task Details
    task_completed = models.TextField()  # Summary of the tasks completed
    assigned_task = models.TextField()  # The task assigned for that day
    project_name = models.CharField(max_length=255, blank=True, null=True)  # If they are working on a specific project

    # Attendance & Work Timings
    attendance_status = models.CharField(max_length=10, choices=ATTENDANCE_STATUS, default='Present')
    check_in_time = models.TimeField(blank=True, null=True)  # Time they checked in
    check_out_time = models.TimeField(blank=True, null=True)  # Time they checked out
    total_hours_worked = models.FloatField(default=0.0)  # Automatically calculated from check-in & check-out

    # Performance Metrics
    quality_of_work = models.IntegerField(choices=PERFORMANCE_RATINGS, default=5)  # Rating on quality
    efficiency = models.IntegerField(choices=PERFORMANCE_RATINGS, default=5)  # How efficient they were
    collaboration = models.IntegerField(choices=PERFORMANCE_RATINGS, default=5)  # Teamwork skills
    learning_progress = models.IntegerField(choices=PERFORMANCE_RATINGS, default=5)  # Learning & improvement
    overall_performance = models.IntegerField(choices=PERFORMANCE_RATINGS, default=5)  # Final score of the day

    # Supervisor/Manager's Notes
    feedback = models.TextField(blank=True, null=True)  # Feedback from the mentor/supervisor
    improvement_suggestions = models.TextField(blank=True, null=True)  # Areas where the candidate needs to improve

    # Any documents/screenshots of work submitted
    work_submission = models.FileField(upload_to='performance_submissions/', blank=True, null=True)

    # DateTime tracking
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date']
        verbose_name = "Candidate Performance"
        verbose_name_plural = "Candidate Performances"

    def __str__(self):
        return f"{self.candidate.username} - {self.date} - {self.overall_performance}/10"


class Announcement(models.Model):
    CATEGORY_CHOICES = [
        ('general', 'General'),
        ('meeting', 'Meeting'),
        ('deadline', 'Deadline'),
        ('event', 'Event'),
        ('update', 'Update'),
    ]

    title = models.CharField(max_length=255)  # Title of the announcement
    message = models.TextField()  # Announcement content
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='general')  # Type of announcement
    date = models.DateTimeField(auto_now_add=True)  # Automatically sets the current date/time
    is_important = models.BooleanField(default=False)  # Flag for important announcements
    link = models.URLField(blank=True, null=True, help_text="Optional link for more details")  # External link

    def __str__(self):
        return f"{self.title} - {self.date.strftime('%b %d, %Y')}"

    class Meta:
        ordering = ["-date"]  # Show latest announcements first