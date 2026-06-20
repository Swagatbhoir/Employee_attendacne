from django.db import migrations


def delete_machines(apps, schema_editor):
    Machine = apps.get_model('machines', 'Machine')
    machine_ids_to_delete = ['MCH004', 'MCH005', 'MCH006', 'MCH007', 'MCH008']
    Machine.objects.filter(machine_id__in=machine_ids_to_delete).delete()


def reverse_machines(apps, schema_editor):
    # This is a data migration that deletes machines, so we can't reliably reverse it
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('machines', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(delete_machines, reverse_machines),
    ]
