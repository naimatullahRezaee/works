# Generated by Django 4.1.2 on 2022-11-27 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('departments', '0003_alter_semester_semester_name_departmentprogramlevel_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]