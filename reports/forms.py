from django import forms

from attendance.models import Attendance
from employees.models import Employee
from machines.models import Machine


class DateRangeForm(forms.Form):
    start_date = forms.DateField(
        required=False,
        widget=forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'type': 'date'}),
        input_formats=['%Y-%m-%d'],
    )
    end_date = forms.DateField(
        required=False,
        widget=forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'type': 'date'}),
        input_formats=['%Y-%m-%d'],
    )

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get('start_date')
        end = cleaned_data.get('end_date')
        if start and end and start > end:
            raise forms.ValidationError('Start date cannot be after end date.')
        return cleaned_data


class AttendanceReportFilterForm(DateRangeForm):
    employee = forms.ModelChoiceField(
        required=False,
        queryset=Employee.objects.all(),
        empty_label='All Employees',
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    machine = forms.ModelChoiceField(
        required=False,
        queryset=Machine.objects.all(),
        empty_label='All Machines',
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    attendance_status = forms.ChoiceField(
        required=False,
        choices=[('', 'All Status')] + Attendance.STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
