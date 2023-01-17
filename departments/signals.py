from django.db.models.signals import  post_save
from django.dispatch import receiver
from .models import DepartmentProgramLevel, Semester


@receiver(post_save, sender=DepartmentProgramLevel)
def create_semester_programatically(sender, created, instance, *args, **kwargs):
    semesters = ["اول", "دوم", "سوم", "چهارم", "پنجم", "ششم", "هفتم" , "هشتم"]
    
    if created:
        if instance.level == "لیسانس":
            for i in range(8):
                Semester.objects.create(
                    program=instance,
                    semester_number=i+1, 
                    semester_name=f"سمستر {semesters[i]} {instance.department.name}"
                )
        elif instance.level == "ماستری":
            for i in range(5):
                Semester.objects.create(
                    program=instance,
                    semester_number=i+1, 
                    semester_name=f"سمستر {semesters[i]}"
                )
    
