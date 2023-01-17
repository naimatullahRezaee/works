import csv
import os
from io import StringIO

from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from departments.models import Department, Semester
from .models import Subject, SubjectBulkUpload
import random
import string
from django.utils.text import slugify


def random_subject_slug():
    return "".join(random.choice(string.ascii_letters+ string.digits) for _ in range(6))


@receiver(post_save, sender=SubjectBulkUpload)
def create_bulk_student(sender, created, instance, *args, **kwargs):
    if created:
        opened = StringIO(instance.csv_file.read().decode())
        reading = csv.DictReader(opened, delimiter=",")
        subjects = []
        for row in reading:
            if "subject" in row and row["subject"]:
                subject = row["subject"]
                code = row["code"] if "code" in row and row["code"] else ""
                credit = (
                    row["credit"] if "credit" in row and row["credit"] else ""
                )
                semester = (
                    row["semester"]
                    if "semester" in row and row["semester"]
                    else ""
                )
                subject_type = (
                    (row["subject_type"]).lower() if "subject_type" in row and row["subject_type"] else ""
                )
                description = (
                    row["description"]
                    if "description" in row and row["description"]
                    else ""
                )
                
                department = (
                    row["department"]
                    if "department" in row and row["department"]
                    else ""
                )
                
                if department:
                    theclass, kind = Department.objects.get_or_create(
                        name=department
                    )
                    
                if semester:
                    print("i am here")
                    sem = Semester.objects.get(
                        semester_name = semester
                    )
                    print("another problm", sem)
                check = Subject.objects.filter(subject=subject).exists()
                if not check:
                    subjects.append(
                        Subject(
                            subject=subject,
                            code=code,
                            credit=credit,
                            semester=sem,
                            slug=random_subject_slug(),
                            subject_type=subject_type,
                            department=theclass,
                        )
                    )

        Subject.objects.bulk_create(subjects)
        instance.csv_file.close()
        instance.delete()