from django.db import models

# Create your models here.

class Days(models.Model):
    day = models.CharField(max_length=9, blank=True, null= True)

    def __str__(self):
        return self.day
class Class(models.Model):
    class_name = models.CharField(max_length=100)
    class_instructor = models.CharField(max_length=100)
    class_time = models.TimeField(auto_now_add=False)
    class_image = models.ImageField(upload_to='static/image/classes/')
    class_info = models.CharField(max_length=1000)
    class_day = models.ManyToManyField(Days, blank = True)

    def __str__(self):
        return self.class_name

class CustomerQuery(models.Model):
    Cquery_name = models.CharField(max_length=100)
    Cquery_email = models.EmailField(max_length=100)
    Cquery_class = models.CharField(max_length=100)
    Cquery_comment = models.CharField(max_length=1000)

    def __str__(self):
        return self.Cquery_name
    
class Facility(models.Model):
    facility_name = models.CharField(max_length=100)

    def __str__(self):
        return self.facility_name


class Membership(models.Model):
    membership_name = models.CharField(max_length=100)
    membership_price = models.IntegerField(null= False)
    membership_fac1 = models.ForeignKey(Facility, on_delete=models.CASCADE, blank= True, null= True, related_name='membership_fac1_set')
    membership_fac2 = models.ForeignKey(Facility, on_delete=models.CASCADE, blank= True, null= True, related_name='membership_fac2_set')
    membership_fac3 = models.ForeignKey(Facility, on_delete=models.CASCADE, blank= True, null= True, related_name='membership_fac3_set')
    membership_fac4 = models.ForeignKey(Facility, on_delete=models.CASCADE, blank= True, null= True, related_name='membership_fac4_set')
    membership_fac5 = models.ForeignKey(Facility, on_delete=models.CASCADE, blank= True, null= True, related_name='membership_fac5_set')
    membership_image = models.ImageField(upload_to='static/image/membership/')
    
    def __str__(self):
        return self.membership_name
    

class Customer(models.Model):
    customer_image = models.ImageField(upload_to='static/image/customer_image/',blank = True,null = True)
    customer_fname = models.CharField(max_length=100)
    customer_lname = models.CharField(max_length=100)
    customer_username = models.CharField(max_length=100)
    customer_email = models.EmailField(max_length=100)
    customer_password = models.CharField(max_length=250)
    customer_login_history = models.DateTimeField(auto_now_add=False, blank = True,null = True)
    customer_dob = models.DateField(auto_now_add=False, blank = True,null = True)
    customer_resetcode = models.IntegerField(blank=True, null=True)
    joined_class = models.ManyToManyField(Class, blank = True)
    customer_age = models.IntegerField(blank=True, null = True)
    gender_choice = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Others', 'Others'),
    )
    customer_gender = models.CharField(max_length = 6, choices = gender_choice,blank=True)
    customer_phone = models.BigIntegerField(null = True,blank=True)
    customer_address = models.CharField(max_length=500, blank=True)
    customer_height = models.IntegerField(blank=True, null = True,default=0)
    customer_currheight = models.IntegerField(blank=True, null = True,default=0)
    customer_weight = models.IntegerField(blank=True, null = True,default=0)
    customer_currweight = models.IntegerField(blank=True, null = True,default=0)
    customer_bmi = models.IntegerField(blank=True, null = True)
    customer_membership = models.ForeignKey(Membership, on_delete=models.CASCADE, blank= True, null= True)
    customer_membership_joinedDate = models.DateField(auto_now_add=False, blank = True,null = True)
    customer_membership_exipredDate = models.DateField(auto_now_add=False, blank = True,null = True)
    is_active = models.BooleanField(default = False)
    is_confirmed = models.BooleanField(default = False)
    customer_count = models.IntegerField(blank=True, null = True,default=0)
    customer_startbmi = models.IntegerField(blank=True, null = True,default=0)
    customer_bmidiff = models.IntegerField(blank=True, null = True,default=0)
    
    def __str__(self):
        return self.customer_fname + " " +self.customer_lname
