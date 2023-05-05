from django.db import models

# Create your models here.
class Customer(models.Model):
    customer_fname = models.CharField(max_length=50)
    customer_lname = models.CharField(max_length=50)
    customer_username = models.CharField(max_length=50)
    customer_email = models.EmailField(max_length=25)
    customer_password = models.CharField(max_length=125)
    customer_login_history = models.DateTimeField(auto_now_add=False)
    customer_resetcode = models.IntegerField(null=True)

    def __str__(self):
        return self.customer_fname + " " +self.customer_lname

class CustomerQuery(models.Model):
    Cquery_name = models.CharField(max_length=100)
    Cquery_email = models.EmailField(max_length=100)
    Cquery_class = models.CharField(max_length=100)
    Cquery_comment = models.CharField(max_length=1000)

    def __str__(self):
        return self.Cquery_name



    