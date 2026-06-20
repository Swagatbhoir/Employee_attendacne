from django.db import models
from django.urls import reverse


class Machine(models.Model):
    machine_id = models.CharField(
        max_length=20, unique=True, editable=False, blank=True
    )
    machine_name = models.CharField(max_length=150)
    machine_number = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['machine_id']

    def __str__(self):
        return f'{self.machine_name} ({self.machine_number})'

    def get_absolute_url(self):
        return reverse('machines:list')

    def save(self, *args, **kwargs):
        if not self.machine_id:
            self.machine_id = self.generate_machine_id()
        super().save(*args, **kwargs)

    @staticmethod
    def generate_machine_id():
        """Generate the next sequential Machine ID, e.g. MCH001, MCH002 ..."""
        last_machine = Machine.objects.order_by('-id').first()
        next_number = (last_machine.id + 1) if last_machine else 1
        new_id = f'MCH{next_number:03d}'
        while Machine.objects.filter(machine_id=new_id).exists():
            next_number += 1
            new_id = f'MCH{next_number:03d}'
        return new_id


