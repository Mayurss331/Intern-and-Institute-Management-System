from django.db import models
from django.contrib.auth.models import AbstractUser

class Intern(AbstractUser):
    """
    Custom User Model for Interns with additional fields.
    """
    phone_number = models.CharField(max_length=15, unique=True)
    college_name = models.CharField(max_length=255)
    degree = models.CharField(max_length=255)
    passing_year = models.IntegerField()
    profile_picture = models.ImageField(upload_to='intern_profiles/', blank=True, null=True)

    REQUIRED_FIELDS = ['first_name', 'last_name', 'email', 'phone_number']

    # Fixing conflicts by adding unique related_name attributes
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="intern_groups",
        blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="intern_permissions",
        blank=True
    )

    def __str__(self):
        return f"{self.username} - {self.email}"

class Notification(models.Model):
    user = models.ForeignKey(Intern, on_delete=models.CASCADE, related_name="notifications")
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.email} - {self.message[:30]}"
    


class DailyWorkUpdate(models.Model):
    TASK_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]

    intern = models.ForeignKey(Intern, on_delete=models.CASCADE)
    task_title = models.CharField(max_length=255)
    task_description = models.TextField()
    task_status = models.CharField(max_length=20, choices=TASK_STATUS_CHOICES, default='pending')
    report = models.TextField(blank=True, null=True)
    learnings = models.TextField(blank=True, null=True)
    challenges = models.TextField(blank=True, null=True)
    suggestions = models.TextField(blank=True, null=True)
    is_reviewed = models.BooleanField(default=False)
    feedback = models.TextField(blank=True, null=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.intern.username} - {self.task_title} ({self.date})"

class WorkSubmission(models.Model):
    work_update = models.ForeignKey(DailyWorkUpdate, on_delete=models.CASCADE, related_name="submissions")
    file = models.FileField(upload_to='work_submissions/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Submission for {self.work_update.task_title} by {self.work_update.intern.username}"
    


class Meeting(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    date = models.DateTimeField()  # Stores the date & time of the meeting
    location = models.CharField(max_length=255, blank=True, null=True)  # Meeting location or link
    created_at = models.DateTimeField(auto_now_add=True)  # Stores when the meeting was created

    def __str__(self):
        return f"{self.title} - {self.date.strftime('%Y-%m-%d %H:%M')}"
    

class Resource(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='resources/', blank=True, null=True)
    link = models.URLField(blank=True, null=True)  # External resources
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class PracticeSession(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    date = models.DateTimeField()
    location = models.CharField(max_length=255, blank=True, null=True)
    meeting_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} on {self.date.strftime('%Y-%m-%d %H:%M')}"