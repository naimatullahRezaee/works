import csv
import os
from io import StringIO

from django.db.models.signals import post_delete,  post_save
from django.dispatch import receiver
from accounts.models import User
from departments.models import Department, Semester
from .models import Student, StudentBulkUpload
from django.contrib.auth.models import Group
from django.contrib.auth.hashers import make_password

@receiver(post_save, sender=StudentBulkUpload)
def create_bulk_student(sender, created, instance, *args, **kwargs):
    if created:
        opened = StringIO(instance.csv_file.read().decode())
        reading = csv.DictReader(opened, delimiter=",")
        students = []
        for row in reading:
            if "kankor_id" in row and row["kankor_id"]:
                kankor_id = row["kankor_id"]
                f_name = row["f_name"] if "f_name" in row and row["f_name"] else ""
                l_name = (
                    row["l_name"] if "l_name" in row and row["l_name"] else ""
                )
                father_name = (
                    row["father_name"]
                    if "father_name" in row and row["father_name"]
                    else ""
                )
                grand_father_name = (
                    (row["grand_father_name"]).lower() if "grand_father_name" in row and row["grand_father_name"] else ""
                )
                school_name = (
                    row["school_name"]
                    if "school_name" in row and row["school_name"]
                    else ""
                )
                score = row["score"] if "score" in row and row["score"] else ""
                province = row["province"] if "province" in row and row["province"] else ""
                gender = row["gender"] if "gender" in row and row["gender"] else ""
                section = row["section"] if "section" in row and row["section"] else ""
                username = row["username"] if "username" in row and row["username"] else ""
                email = row["email"] if "email" in row and row["email"] else ""
                password = row["password"] if "password" in row and row["password"] else ""

                semester = row["semester"] if "semester" in row and row["semester"] else ""
                print("semester number ", semester)
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
                    sem = Semester.objects.get(
                        semester_name=semester
                    )
                    print(sem)

                if username and email and password:
                    user = User.objects.create(
                        username=username, 
                        email=email, 
                        password=make_password(password), 
                        is_student=True
                    )
                    group = Group.objects.get(name="students")
                    group.user_set.add(user)
                check = Student.objects.filter(kankor_id=kankor_id).exists()
                if not check:
                    students.append(
                        Student(
                            kankor_id=kankor_id,
                            f_name=f_name,
                            l_name=l_name,
                            father_name=father_name,
                            grand_father_name=grand_father_name,
                            school_name=school_name,
                            score=score,
                            province=province,
                            gender=gender,
                            semester=sem,
                            section=section,
                            user=user,
                            department=theclass,
                        )
                    )

        Student.objects.bulk_create(students)
        instance.csv_file.close()
        instance.delete()