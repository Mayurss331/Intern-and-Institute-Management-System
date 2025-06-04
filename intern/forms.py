from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Intern



class InternSignupForm(UserCreationForm):
    class Meta:
        model = Intern
        fields = ['username', 'email', 'first_name', 'last_name', 'phone_number', 'college_name', 'degree', 'passing_year', 'profile_picture']



class InternLoginForm(AuthenticationForm):
    """
    Intern Login Form - Uses username for authentication
    """
    username = forms.CharField(label="Username", widget=forms.TextInput(attrs={"class": "form-control"}))


from .models import DailyWorkUpdate, WorkSubmission


class DailyWorkUpdateForm(forms.ModelForm):
    class Meta:
        model = DailyWorkUpdate
        fields = ['task_title', 'task_description', 'task_status', 'report', 'learnings', 'challenges', 'suggestions']