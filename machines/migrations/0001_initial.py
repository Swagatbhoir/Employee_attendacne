from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Machine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('machine_id', models.CharField(blank=True, editable=False, max_length=20, unique=True)),
                ('machine_name', models.CharField(max_length=150)),
                ('machine_number', models.CharField(max_length=50, unique=True)),
                ('machine_type', models.CharField(choices=[('Excavator', 'Excavator'), ('JCB', 'JCB'), ('Crane', 'Crane'), ('Loader', 'Loader'), ('Bulldozer', 'Bulldozer'), ('Dumper', 'Dumper'), ('Other', 'Other')], default='Other', max_length=50)),
                ('status', models.CharField(choices=[('Active', 'Active'), ('Inactive', 'Inactive')], default='Active', max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['machine_id'],
            },
        ),
    ]
