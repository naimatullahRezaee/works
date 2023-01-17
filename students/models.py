from django.db import models
from departments.models import Department, Semester
from accounts.models import User


class Student(models.Model):
    GENDER = (
        ("خانم", "خانم"),
        ("آقا", "آقا"),
    )
    STATUS = (
        ("فعال", "فعال"),
        ("تعجیل", "تعجیل"),
        ("چانس", "چانس"),
        ("محروم", "محروم"),
        ("ناکام", "ناکام"),
    )
    SECTION = (
        ("A", "A"),
        ("B", "B")
    )
    CART = (
        ("تذکره برقی", "تذکره برقی"),
        ("تذکره کاغذی", "تذکره کاغذی")
    )
    HOSTEL = (
        ("بلی", "بلی"),
        ("نخیر", "نخیر")
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    kankor_id  = models.CharField(max_length=200, unique=True)
    f_name = models.CharField(max_length=200)
    l_name = models.CharField(max_length=200)
    father_name = models.CharField(max_length=200)
    grand_father_name = models.CharField(max_length=200)
    school_name = models.CharField(max_length=200)
    score = models.IntegerField(default=0)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    province = models.CharField(max_length=200)
    gender = models.CharField(max_length=30, choices=GENDER, default="آقا")
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    section = models.CharField(max_length=30, choices=SECTION, default="A")
    status = models.CharField(max_length=30, choices=STATUS, default="فعال")

    adminssion_date = models.DateField(auto_now_add=True)

    phone = models.CharField(max_length=16, null=True , unique=True , blank=True )
    cart = models.CharField(max_length=30, choices=CART, default="تذکره برقی")
    cart_number = models.CharField(max_length=200, unique=True, null=True, blank=True)
    page_number = models.CharField(max_length=200, null=True, blank=True)
    register_number = models.CharField(max_length=200, null=True, blank=True)
    volume_number = models.CharField(max_length=200, null=True, blank=True)
    cart_image = models.ImageField(upload_to="images/cart", default="cart.jpg")

    # hostel
    hostel = models.CharField(max_length=20, choices=HOSTEL, default="نخیر")
    wing_number = models.IntegerField(null=True, blank=True)
    room_number = models.IntegerField(null=True, blank=True)
    graduated_from_school = models.DateField(null=True, blank=True)
    rel_with_std = models.CharField(max_length=200, null=True, blank=True)
    rel_name = models.CharField(max_length=200,null=True, blank=True)
    rel_job = models.CharField(max_length=200, null=True, blank=True)
    rel_phone1 = models.CharField(max_length=40, unique=True, null=True, blank=True)
    rel_phone2 = models.CharField(max_length=40, unique=True, null=True, blank=True)
    rel_current_address = models.CharField(max_length=255, null=True, blank=True)

    avatar = models.ImageField(upload_to="images/students", default="student.jpg")
    def __str__(self):
        return self.f_name

        

class StudentBulkUpload(models.Model):
    csv_file = models.FileField(upload_to="students/bulkupload/")
    date_uploaded = models.DateTimeField(auto_now=True)

