from django.db import models
from django.urls import reverse


class Employee(models.Model):
    employee_id = models.CharField(
        max_length=20, unique=True, editable=False, blank=True
    )
    full_name = models.CharField(max_length=150)
    mobile_number = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['employee_id']

    def __str__(self):
        return f'{self.employee_id} - {self.full_name}'

    def get_absolute_url(self):
        return reverse('employees:detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        if not self.employee_id:
            self.employee_id = self.generate_employee_id()
        super().save(*args, **kwargs)

    @staticmethod
    def generate_employee_id():
        """Generate the next sequential Employee ID, e.g. EMP001, EMP002 ..."""
        last_employee = Employee.objects.order_by('-id').first()
        next_number = (last_employee.id + 1) if last_employee else 1
        new_id = f'EMP{next_number:03d}'
        # Guard against any collisions (e.g. records were deleted)
        while Employee.objects.filter(employee_id=new_id).exists():
            next_number += 1
            new_id = f'EMP{next_number:03d}'
        return new_id


