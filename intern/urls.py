from django.urls import path
from .views import change_password, daily_work_update, delete_submission, intern_dashboard, intern_practice, intern_login, intern_logout, mark_notification_read, notifications, profile_view, submit_work_update

urlpatterns = [
    # path('signup/', intern_signup, name='intern_signup'),
    path('login/', intern_login, name='intern_login'),
    path('logout/', intern_logout, name='intern_logout'),
    path('', intern_dashboard, name='intern_dashboard'),
    path("profile/", profile_view, name="profile"),
    path('notifications/', notifications, name='notifications'),
    
    path('daily-work-updates/', daily_work_update, name='daily_work_update'),
    path('submit-work-update/', submit_work_update, name='submit_work_update'),
    path('delete-submission/<int:submission_id>/', delete_submission, name='delete_submission'),

    path("change-password/", change_password, name="change_password"),

    path('notifications/mark-read/<int:notification_id>/', mark_notification_read, name='mark_notification_read'),
    path('intern/practice/', intern_practice, name='intern_practice'),

]
