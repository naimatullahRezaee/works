# Generated by Django 4.1.2 on 2022-11-25 17:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmployeeNationalityCart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cart_type', models.CharField(default='تذکره', max_length=200)),
                ('passport_back', models.ImageField(blank=True, null=True, upload_to='employee/cart')),
                ('passport_front', models.ImageField(blank=True, null=True, upload_to='employee/cart')),
                ('nationality_back', models.ImageField(blank=True, null=True, upload_to='employee/cart')),
                ('nationality_front', models.ImageField(blank=True, null=True, upload_to='employee/cart')),
                ('employee', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='employees.employee')),
            ],
        ),
    ]
