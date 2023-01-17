from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CourseDetail, Course

from accounts.models import User

@receiver(post_save, sender=Course)
def create_course_detail(sender, instance, created, **kwargs):
    if created:
        CourseDetail.objects.create(course=instance)


@receiver(post_save, sender=Course)
def save_course_detail(sender, instance, **kwargs):
    instance.coursedetail.save()