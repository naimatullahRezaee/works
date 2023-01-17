import csv
import os
from io import StringIO


from django.db.models.signals import  post_save
from django.dispatch import receiver
from results.models import Result, ResultBulkUpload
from subjects.models import Subject
from students.models import Student
from employees.models import Employee
from .models import User


@receiver(post_save, sender=User)
def create_superuser_profile(sender, created, instance, *args, **kwargs):
    if created:
        if instance.is_staff == True:
            Employee.objects.create(user=instance)



@receiver(post_save, sender=ResultBulkUpload)
def create_bulk_result(sender, created, instance, *args, **kwargs):
    if created:
        opened = StringIO(instance.csv_file.read().decode())
        reading = csv.DictReader(opened, delimiter=",")
        results = []

        for row in reading:
            if "subject" in row and row["subject"]:
                subject = row["subject"]
                student = (row["student"] if "student" in row and row["student"] else "")
                student_ID = (row["student_ID"] if "student_ID" in row and row["student_ID"] else "")
                mid_term = (row["mid_term"] if "mid_term" in row and row["mid_term"] else "")
                final = (row["final"] if "final" in row and row["final"] else "")
                chances = (row["chances"] if "chances" in row and row["chances"] else "")
                assignment = (row["assignment"] if "assignment" in row and row["assignment"] else "")
                
                if student and student_ID:
                    std = Student.objects.get(kankor_id=student_ID)
                if subject:
                    sub = Subject.objects.get(subject=subject)

                check = Result.objects.filter(student=Student.objects.get(pk=std.pk), subject=Subject.objects.get(pk=sub.pk)).exists()
                if not check:
                    results.append(
                        Result(
                            subject=sub, 
                            student=std, 
                            class_activity=0, 
                            assignment=assignment, 
                            mid_term=mid_term, 
                            final=final, 
                            chances=chances, 
                            project=0,
                        )
                    )
                elif check:
                    result = Result.objects.get(student=std, subject=sub)
                    result.class_activity=float(0)
                    result.assignment=float(assignment)
                    result.mid_term=float(mid_term)
                    result.final=float(final)
                    result.chances=chances
                    result.project=float(0)
                    result.save()
        
        Result.objects.bulk_create(results)
        instance.csv_file.close()
        instance.delete()

