from django.utils import timezone  #used tp access timezone and store time wile timezone is active in django
from django.shortcuts import render
from .models import Customer
import random
from django.contrib import sessions

# Create your views here.
def landingpage(request):
    return render(request, "landingpage.html")

def signup(request): #Password need to be hashed
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
            elif Customer.objects.filter(customer_username = username).exists(): #checks weather username is used or not
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

def forget_pass(request):
    return render(request,"forget_pass.html")


def reset_code(request):
    if request.method == "POST":
        email = request.POST['email']
        print(email) #in future we will send the code to the provided if it exist
        #generate code and send via email
        if Customer.objects.filter(customer_email = email).exists():
            random_float = random.randint(000000,999999)
            print(random_float)
            request.session['random_float'] = random_float #creating the session to access this value from anywere
            return render(request,"code_reset.html")
        else:
            print("This email doesn't exist.")
    return render(request,"forget_pass.html")

def reset_password(request):
    random_float = request.session.get('random_float') #accessing the session
    if request.method == "POST":
        code = request.POST['code']
        if(int(random_float) == int(code)): #validate the generated code and user type code 
            return render(request,"reset_password.html")
        else:
            print("Invalid Code provided")
    return render(request,"code_reset.html")


