from django import forms
from django.forms import formset_factory

from machines.models import Machine
from .models import Attendance


class DateSelectForm(forms.Form):
    date = forms.DateField(
        widget=forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'type': 'date'}),
        input_formats=['%Y-%m-%d'],
    )


class AttendanceEntryForm(forms.Form):
    """
    A single row in the daily attendance table.
    `employee_id` and `employee_label` are hidden/display-only fields used
    to identify which employee this row belongs to.
    """
    employee_id = forms.IntegerField(widget=forms.HiddenInput())
    attendance_status = forms.ChoiceField(
        choices=[('', '-- Select Status --')] + Attendance.STATUS_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select attendance-status-select',
        }),
    )
    machine = forms.ModelChoiceField(
        queryset=Machine.objects.all(),
        required=False,
        empty_label='-- Select Machine --',
        widget=forms.Select(attrs={
            'class': 'form-select machine-select',
        }),
    )
    remarks = forms.CharField(
        required=False,
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Remarks (optional)',
        }),
    )

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get('attendance_status')
        machine = cleaned_data.get('machine')

        if not status:
            raise forms.ValidationError('Please select an attendance status.')

        if status in Attendance.MACHINE_REQUIRED_STATUSES and not machine:
            raise forms.ValidationError(
                f'Machine selection is required when status is "{status}".'
            )

        if status not in Attendance.MACHINE_REQUIRED_STATUSES and machine:
            cleaned_data['machine'] = None

        return cleaned_data


AttendanceFormSet = formset_factory(AttendanceEntryForm, extra=0)
