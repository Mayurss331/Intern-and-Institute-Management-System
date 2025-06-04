from django import forms
from .models import UserPerformance
from .models import Transaction
from .models import CandidatePerformance
from django import forms
from myapp.models import Application
from intern.models import Intern

class CandidatePerformanceForm(forms.ModelForm):
    class Meta:
        model = CandidatePerformance
        fields = [
            'candidate', 'date', 'assigned_task', 'task_completed', 'project_name',
            'attendance_status', 'check_in_time', 'check_out_time', 'total_hours_worked',
            'quality_of_work', 'efficiency', 'collaboration', 'learning_progress',
            'overall_performance', 'feedback', 'improvement_suggestions', 'work_submission'
        ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'check_in_time': forms.TimeInput(attrs={'type': 'time'}),
            'check_out_time': forms.TimeInput(attrs={'type': 'time'}),
        }


class UserPerformanceForm(forms.ModelForm):
    class Meta:
        model = UserPerformance
        fields = [
            'aptitude_score', 'gd1_attendance', 'gd1_marks', 
            'gd2_attendance', 'gd2_marks', 'fees_paid', 'technical_marks'
        ]
        widgets = {
            'aptitude_score': forms.NumberInput(attrs={'class': 'form-control'}),
            'gd1_attendance': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'gd1_marks': forms.NumberInput(attrs={'class': 'form-control'}),
            'gd2_attendance': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'gd2_marks': forms.NumberInput(attrs={'class': 'form-control'}),
            'fees_paid': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'technical_marks': forms.NumberInput(attrs={'class': 'form-control'}),
        }
  

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['transaction_type', 'amount', 'description', 'category', 'payment_mode', 'status', 'document']
        widgets = {
            'transaction_type': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'category': forms.TextInput(attrs={'class': 'form-control'}),
            'payment_mode': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'document': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
# forms.py


class CreateInternFromApplicationForm(forms.Form):
    application = forms.ModelChoiceField(queryset=Application.objects.all(), label="Select Candidate")
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

    def save(self):
        app = self.cleaned_data['application']
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        intern = Intern.objects.create_user(
            username=username,
            password=password,
            email=app.email,
            first_name=app.first_name,
            last_name=app.last_name,
            phone_number=app.phone_number,
            college_name=app.college_name,
            degree=app.undergraduate_degree,
            passing_year=app.undergraduate_passing_year,
        )
        return intern