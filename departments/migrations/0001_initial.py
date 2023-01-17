# Generated by Django 4.0.5 on 2022-07-01 08:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Semester',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('semester_number', models.PositiveIntegerField(default=1)),
                ('semester_name', models.CharField(choices=[('اول', 'اول'), ('دوم', 'دوم'), ('سوم', 'سوم'), ('چهارم', 'چهارم'), ('پنجم', 'پنجم'), ('ششم', 'ششم'), ('هفتم', 'هفتم'), ('هشتم', 'هشتم')], default='اول', max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=200, unique=True)),
                ('publish_date', models.DateField()),
                ('status', models.CharField(choices=[('فعال', 'فعال'), ('غیر فعال', 'غیر فعال')], default='فعال', max_length=20)),
                ('about', models.TextField(blank=True, null=True)),
                ('loan', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='dep_loan', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
