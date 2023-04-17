from django.utils import timezone  #used tp access timezone and store time wile timezone is active in django
from django.shortcuts import render
from .models import Customer

# Create your views here.
def landingpage(request):
    return render(request, "landingpage.html")

def signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        fname = request.POST["fname"]
        lname = request.POST["lname"]
        password = request.POST["password"]
        c_password = request.POST["c_password"]
        email = request.POST["email"]

        if password == c_password:
            if Customer.objects.filter(customer_email = email).exists(): #checks weather email is used or not
                print("Email is already in use.")
            if Customer.objects.filter(customer_username = username).exists(): #checks weather username is used or not
                print("Username is already taken.")
            else:
                user = Customer(customer_fname = fname, customer_lname = lname, customer_username = username, customer_email = email, customer_password = password, customer_login_history = timezone.now())
                user.save()
                print("User Account created successfully")
        else:
            print("Confirmation password mismatched")
    return render(request, "signup.html")

def signin(request):
    if request.method == "POST":
        u_username = request.POST['username']
        u_password = request.POST['password']

        s_details = Customer.objects.all()
        for s in s_details:
            if(s.customer_username == u_username and s.customer_password == u_password):
                time = Customer.objects.get(id=s.id)
                time.customer_login_history = timezone.now()
                time.save()
                return render(request,"home.html")

        else:
            print("Invalid credentials")

    return render(request,"signin.html")