from django.db import models
from accounts.models import User
from students.models import Student
from employees.models import Employee
# Create your models here.

class Evaluation(models.Model):
    luncher = models.ForeignKey(User, on_delete=models.CASCADE)
    teacher = models.ForeignKey(
        Employee, 
        on_delete=models.CASCADE, 
        verbose_name="نام استاد که ارزیابی میشود"
    )

    def __str__(self):
        return f"{self.teacher.user.first_name}'s evaluation "


class InstructorEvaluation(models.Model):
    CHOICES = (
        ("کاملا مخالف", "کاملا مخالف"),
        ("مخالف", "مخالف"),
        ("بعضی اوقات", "بعضی اوقات"),
        ("موافق", "موافق"),
        ("کاملا موافق", "کاملا موافق"),

    )
    evaluation = models.ForeignKey(Evaluation, on_delete=models.CASCADE)
    skill = models.CharField(
        verbose_name="استاد تسلط کامل بر موضوعی که تدریس میکند دارد.",
        choices=CHOICES, 
        max_length=200
    )
    descipline = models.CharField(
        max_length=200, 
        verbose_name="استاد در وقت معین به صنف آمده و خارج میشود و نهایت استفاده را از ساعت درسی میکند.",
        choices=CHOICES
    )
    ability_to_explain = models.CharField(
        max_length=200, 
        verbose_name="با آنکه میدانم استاد تسلط کامل بالای موضوع دارد ولی نحوه تدریس شان قابل فهم نیست.",
        choices=CHOICES
    )
    coaporation_with_students = models.CharField(
        max_length=200, 
        choices=CHOICES, 
        verbose_name="نحوه تدریس استاد مشارکتی نیست و شاگردان مشارکتی در درس ها ندارد."
    )
    expectations = models.CharField(
        max_length=200,
        choices=CHOICES, 
        verbose_name="توقع استاد بیشتر از چیزی هست که با شاگردان تدریس میکند."
    )
    discriminations = models.CharField(
        max_length=255, 
        choices=CHOICES, 
        verbose_name="استاد هیچ گونه تمایلی به تبعیض قایل شدن بین شاگردان اش نیست و شاگردان را به هم پذیری دعوت میکند."
    )

    ethics = models.CharField(
        max_length=255, 
        choices=CHOICES, 
        verbose_name="استاد از اخلاق نیکو و پسندیده ای برخوردار نیست."
    )

    
    description = models.TextField(blank=True, verbose_name="توضیحات اضافی")

    student = models.ForeignKey(Student, on_delete=models.CASCADE)