import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('employees', '0001_initial'),
        ('machines', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('attendance_status', models.CharField(choices=[('Present', 'Present'), ('Absent', 'Absent'), ('Leave', 'Leave'), ('Half Day', 'Half Day')], default='Present', max_length=10)),
                ('remarks', models.CharField(blank=True, default='', max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendance_records', to='employees.employee')),
                ('machine', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='attendance_records', to='machines.machine')),
            ],
            options={
                'verbose_name': 'Attendance Record',
                'verbose_name_plural': 'Attendance Records',
                'ordering': ['-date', 'employee__employee_id'],
            },
        ),
        migrations.AlterUniqueTogether(
            name='attendance',
            unique_together={('employee', 'date')},
        ),
    ]
