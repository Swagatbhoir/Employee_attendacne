from django.db import migrations


def remove_old_statuses(apps, schema_editor):
    Attendance = apps.get_model('attendance', 'Attendance')
    # This migration assumes that Leave and Half Day have been removed from model
    # If there are any old records, they will be handled by the model constraints
    pass


def reverse_remove_old_statuses(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(remove_old_statuses, reverse_remove_old_statuses),
    ]
