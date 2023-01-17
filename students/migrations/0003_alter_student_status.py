# Generated by Django 4.1.2 on 2022-11-26 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0002_student_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='status',
            field=models.CharField(choices=[('فعال', 'فعال'), ('تعجیل', 'تعجیل'), ('چانس', 'چانس'), ('محروم', 'محروم'), ('ناکام', 'ناکام')], default='فعال', max_length=30),
        ),
    ]
