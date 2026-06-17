from django import forms
from .models import Employee


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['full_name', 'mobile_number', 'status']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter full name',
            }),
            'mobile_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter 10-digit mobile number',
            }),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean_mobile_number(self):
        mobile = self.cleaned_data.get('mobile_number', '').strip()
        if not mobile.isdigit():
            raise forms.ValidationError('Mobile number must contain digits only.')
        if len(mobile) < 7 or len(mobile) > 15:
            raise forms.ValidationError('Enter a valid mobile number.')
        return mobile


class EmployeeSearchForm(forms.Form):
    q = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by Employee ID or Name...',
        })
    )
    status = forms.ChoiceField(
        required=False,
        choices=[('', 'All Status')] + Employee.STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
