from django.db import models

# Create your models here.
class Customer(models.Model):
    customer_fname = models.CharField(max_length=100)
    customer_lname = models.CharField(max_length=100)
    customer_username = models.CharField(max_length=100)
    customer_email = models.EmailField(max_length=100)
    customer_password = models.CharField(max_length=250)
    customer_login_history = models.DateTimeField(auto_now_add=False)
    customer_resetcode = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.customer_fname + " " +self.customer_lname

class CustomerQuery(models.Model):
    Cquery_name = models.CharField(max_length=100)
    Cquery_email = models.EmailField(max_length=100)
    Cquery_class = models.CharField(max_length=100)
    Cquery_comment = models.CharField(max_length=1000)

    def __str__(self):
        return self.Cquery_name
    
class Class(models.Model):
    class_name = models.CharField(max_length=100)
    class_instructor = models.CharField(max_length=100)
    DAY_CHOICES = (
        ('Sun', 'Sunday'),
        ('Mon', 'Monday'),
        ('Tue', 'Tuesday'),
        ('Wed', 'Wednesday'),
        ('Thu', 'Thursday'),
        ('Fri', 'Friday'),
        ('Sat', 'Saturday'),
        ('Everyday', 'Everyday'),
        ('NONE', 'NONE'),
    )
    class_startDay = models.CharField(max_length=8, choices=DAY_CHOICES, default='Sun')
    class_endDay = models.CharField(max_length=8, choices=DAY_CHOICES, default='Sun')
    class_time = models.TimeField(auto_now_add=False)
    class_image = models.ImageField(upload_to='static/image/classes/')

    def __str__(self):
        return self.class_name