from django.db import models
from accounts.models import User
from departments.models import Department

# employee general information
class Employee(models.Model):
    
    STATUS = (
        ('فعال', 'فعال'),
        ('غیر فعال', 'غیر فعال'),
    )
    CART = (
        ('تذکره کاغذی', 'تذکره کاغذی'),
        ('تذکره برقی', 'تذکره برقی'),
    )
    GENDER = (
        ("خانم", "خانم",),
        ("آقا", "آقا"),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    emp_unique_id = models.CharField(max_length=200, unique=True)
    f_name = models.CharField(max_length=200)
    l_name = models.CharField(max_length=200)
    father_name = models.CharField(max_length=200)
    gender = models.CharField(max_length=20, choices=GENDER, default="مرد")
    dob = models.DateField(null=True, blank=True)
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, related_name="department", null=True, blank=True)

    
    phone_number = models.CharField(max_length=20)
    bio = models.TextField(null=True, blank=True)
    address = models.CharField(max_length=500, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS, default="فعال")
    avatar = models.ImageField(upload_to="staff/avatar", default="employee.jpg")

    def __str__(self):
        return f"{self.user.username}'s Employee profile"


# employee id cart
class EmployeeNationalityCart(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE)
    cart_type = models.CharField(max_length=200, default="تذکره")
    passport_back = models.ImageField(upload_to="employee/cart", null=True, blank=True)
    passport_front = models.ImageField(upload_to="employee/cart", null=True, blank=True)
    nationality_back = models.ImageField(upload_to="employee/cart", null=True, blank=True)
    nationality_front = models.ImageField(upload_to="employee/cart", null=True, blank=True)

    def __str__(self):
        return self.cart_type



# employee eduaction background
class Education(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    university = models.CharField(max_length=200)
    start_date = models.DateField()
    finish_date = models.DateField()
    diploma = models.ImageField(upload_to="eudcation/")
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title

# employee work experiences


class Experience(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    org = models.CharField(max_length=200)
    position = models.CharField(max_length=200)
    from_date = models.DateField()
    finish_date = models.DateField()
    description = models.TextField(blank=True)
    document = models.ImageField(upload_to="background/")
    
    def __str__(self):
        return self.org


