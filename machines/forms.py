from django import forms
from .models import Machine


class MachineForm(forms.ModelForm):
    class Meta:
        model = Machine
        fields = ['machine_name', 'machine_number', 'machine_type', 'status']
        widgets = {
            'machine_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Excavator 01',
            }),
            'machine_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. EXC-001',
            }),
            'machine_type': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }


class MachineSearchForm(forms.Form):
    q = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by Machine ID, Name or Number...',
        })
    )
    status = forms.ChoiceField(
        required=False,
        choices=[('', 'All Status')] + Machine.STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    machine_type = forms.ChoiceField(
        required=False,
        choices=[('', 'All Types')] + Machine.MACHINE_TYPE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
