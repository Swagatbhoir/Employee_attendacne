from django.core.exceptions import ValidationError
from django.db import models

from employees.models import Employee
from machines.models import Machine


class Attendance(models.Model):
    PRESENT = 'Present'
    ABSENT = 'Absent'

    STATUS_CHOICES = [
        (PRESENT, 'Present'),
        (ABSENT, 'Absent'),
    ]

    # Statuses that require a machine to be assigned
    MACHINE_REQUIRED_STATUSES = (PRESENT,)

    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name='attendance_records'
    )
    date = models.DateField()
    attendance_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PRESENT)
    machine = models.ForeignKey(
        Machine, on_delete=models.SET_NULL, null=True, blank=True, related_name='attendance_records'
    )
    remarks = models.CharField(max_length=255, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', 'employee__employee_id']
        unique_together = ('employee', 'date')
        verbose_name = 'Attendance Record'
        verbose_name_plural = 'Attendance Records'

    def __str__(self):
        return f'{self.employee.employee_id} - {self.date} - {self.attendance_status}'

    def clean(self):
        # Enforce business rule: Present requires a machine.
        if self.attendance_status in self.MACHINE_REQUIRED_STATUSES and not self.machine:
            raise ValidationError({
                'machine': 'Machine assignment is required when attendance status is '
                           f'"{self.attendance_status}".'
            })
        # Absent should not carry a machine assignment.
        if self.attendance_status not in self.MACHINE_REQUIRED_STATUSES and self.machine:
            self.machine = None

    @property
    def machine_required(self):
        return self.attendance_status in self.MACHINE_REQUIRED_STATUSES
