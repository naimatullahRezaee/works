# Generated by Django 4.0.6 on 2022-08-13 10:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_assignment_expir_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assignment',
            name='expir_at',
        ),
    ]
