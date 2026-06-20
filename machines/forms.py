from django import forms
from .models import Machine


class MachineForm(forms.ModelForm):
    class Meta:
        model = Machine
        fields = ['machine_name', 'machine_number']
        widgets = {
            'machine_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Excavator 01',
            }),
            'machine_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. EXC-001',
            }),
        }


class MachineSearchForm(forms.Form):
    q = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by Machine ID, Name or Number...',
        })
    )
