# Generated by Django 4.0.5 on 2022-07-01 08:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('departments', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Experience',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('org', models.CharField(max_length=200)),
                ('position', models.CharField(max_length=200)),
                ('years', models.IntegerField(default=1)),
                ('from_date', models.DateField()),
                ('finish_date', models.DateField()),
                ('description', models.TextField(blank=True)),
                ('file', models.FileField(blank=True, null=True, upload_to='background/')),
                ('document', models.ImageField(upload_to='background/')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('emp_unique_id', models.CharField(max_length=200, unique=True)),
                ('f_name', models.CharField(max_length=200)),
                ('l_name', models.CharField(max_length=200)),
                ('father_name', models.CharField(max_length=200)),
                ('gender', models.CharField(choices=[('خانم', 'خانم'), ('آقا', 'آقا')], default='مرد', max_length=20)),
                ('dob', models.DateField(blank=True, null=True)),
                ('national_cart', models.CharField(choices=[('تذکره کاغذی', 'تذکره کاغذی'), ('تذکره برقی', 'تذکره برقی')], default='تذکره برقی', max_length=20)),
                ('cart_number', models.CharField(max_length=255)),
                ('page_number', models.IntegerField(blank=True, null=True)),
                ('register_number', models.IntegerField(blank=True, null=True)),
                ('volume', models.IntegerField(blank=True, null=True)),
                ('phone_number', models.CharField(max_length=20)),
                ('cart_image', models.ImageField(default='cart.jpg', upload_to='staff/')),
                ('bio', models.TextField(blank=True, null=True)),
                ('address', models.CharField(blank=True, max_length=500, null=True)),
                ('status', models.CharField(choices=[('فعال', 'فعال'), ('غیر فعال', 'غیر فعال')], default='فعال', max_length=20)),
                ('avatar', models.ImageField(default='employee.jpg', upload_to='staff/avatar')),
                ('department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='department', to='departments.department')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Education',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('university', models.CharField(max_length=200)),
                ('start_date', models.DateField()),
                ('finish_date', models.DateField()),
                ('diploma', models.ImageField(upload_to='eudcation/')),
                ('file', models.FileField(blank=True, null=True, upload_to='background/')),
                ('description', models.TextField(blank=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
