import csv
import os
from io import StringIO
from django.db.models.signals import  post_save
from django.dispatch import receiver
from results.models import Result, CourseResultUpload
from courses.models import Course 
from students.models import Student
from subjects.models import Subject


@receiver(post_save, sender=CourseResultUpload)
def create_course_result(sender , created, instance ,  *args, **kwargs ):
    if created:
        opened = StringIO(instance.csv_file.read().decode())
        reading = csv.DictReader(opened , delimiter=",")
        results = []

        f_name = ""
        father_name = ""
        subject = ""
        mid_term_score = 0
        final_score = 0
        activity_score = 0
        project_score = 0
        homework_score = 0
        chance = 1

        for row in reading:
            if "f_name" in row and row["f_name"]:
                f_name = row["f_name"]
                father_name = (row["father_name"] if "father_name" in row and row["father_name"] else "" )
                subject = (row["subject"] if "subject" in row and row["subject"] else "")
                mid_term_score = (row["mid_term_score"] if "mid_term_score" in row and row["mid_term_score"] else "")
                final_score = (row["final_score"] if "final_score" in row and row["final_score"] else "")
                activity_score = (row["activity_score"] if "activity_score" in row and row["activity_score"] else "")
                project_score = (row["project_score"] if "project_score" in row and row["project_score"] else "")
                homework_score = (row["homework_score"] if "homework_score" in row and row["homework_score"] else "")
                chance = (row["chance"] if "chance" in row and row["chance"] else "")
                
                if f_name and father_name:
                    student = Student.objects.get(f_name=f_name, father_name=father_name)
                    
                subject_id = 0
                if subject:
                    sub = Subject.objects.get(subject=subject)
                    subject_id  = sub.id
                    
                check = Result.objects.filter(student=Student.objects.get(pk=student.pk), subject=Subject.objects.get(pk=subject_id)).exists()
                if not check:
                    results.append(
                        Result(
                            student=student,
                            subject=Subject.objects.get(id=subject_id),
                            mid_term=mid_term_score,
                            final=final_score,
                            class_activity=activity_score,
                            project=project_score,
                            assignment=homework_score,
                            chances=chance,
                        )
                    ) 
                elif check:
                    result = Result.objects.get(student=student, subject=sub)
                    result.delete()
                    results.append(
                        Result(
                            student=student,
                            subject=Subject.objects.get(id=subject_id),
                            mid_term=mid_term_score,
                            final=final_score,
                            class_activity=activity_score,
                            project=project_score,
                            assignment=homework_score,
                            chances=chance,
                        )
                    )
        Result.objects.bulk_create(results)
        instance.csv_file.close()
        instance.delete()


        

