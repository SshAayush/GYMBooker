from django.shortcuts import render
from .models import Customer, CustomerQuery, Class, Membership
from django.db.models import Q  #the Q object is used to create complex queries with logical operators such as OR and AND.
import random

from django.urls import reverse
from django.shortcuts import redirect

# used to send mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

# used tp access timezone and store time wile timezone is active in django
from django.utils import timezone
from datetime import timedelta, datetime

#Used to hash the password
from django.contrib.auth.hashers import check_password, make_password

# USed to destroy the session
from django.contrib.sessions.models import Session

# Create your views here.


def landingpage(request):
    fetchClass = Class.objects.all()
    memberships = Membership.objects.all()
    return render(request, "landingpage.html", {
        "classes" : fetchClass,
        "memberships" : memberships,
    })


def signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        fname = request.POST["fname"]
        lname = request.POST["lname"]
        password = request.POST["password"]
        c_password = request.POST["c_password"]
        email = request.POST["email"]
        hashed_pwd = make_password(password)

        if password == c_password:
            # checks weather email is used or not
            if Customer.objects.filter(customer_email=email).exists():
                print("Email is already in use.")
                msg = "Email is already in use"
                return render(request, "signup.html",{'acc_created': msg})
            # checks weather username is used or not
            elif Customer.objects.filter(customer_username=username).exists():
                print("Username is already taken.")
                msg = "Username is already taken"
                return render(request, "signup.html",{'acc_created': msg})
            else:
                # ph_hash = PasswordHasher()
                # hashed_password = ph_hash.hash(password)
                user = Customer(customer_fname= fname, customer_lname= lname, customer_username= username,
                                customer_email= email, customer_password= hashed_pwd, customer_login_history= timezone.now())
                user.save()
                print("User Account created successfully")
                msg = "User Account created successfully"
                return render(request, "signup.html",{'acc_created': msg})
        else:
            print("Confirmation password mismatched")
    return render(request, "signup.html")


def signin(request):
    if request.method == "POST":
        u_username = request.POST['username']
        u_password = request.POST['password']

        ss = Customer.objects.get(customer_username = u_username)
        if (ss.customer_username == u_username and check_password(u_password, ss.customer_password)):
                time = Customer.objects.get(id=ss.id)
                time.customer_login_history = timezone.now()
                time.save()
                request.session['username'] = u_username #set the session of their username after loggin in
                request.session.save() # start the session
                # current_user = request.session.get('username')
                # print(f'{current_user} yoyoyoyyo')
                return redirect('dashboard')

        else:
            print("Invalid credentials")
            msg = "Invalid credentials"
            return render(request, "signin.html",{'message': msg})
        
    return render(request, "signin.html")


def forget_pass(request):
    return render(request, "forget_pass.html")


def reset_code(request):
    if request.method == "POST":
        email = request.POST['email']
        print(email)  # in future we will send the code to the provided if it exist
        # generate code and send via email
        if Customer.objects.filter(customer_email=email).exists():
            random_float = random.randint(100000, 999999)
            print(random_float)
            c_details = Customer.objects.get(customer_email=email)

            # saving the generated password reset code to database
            c_details.customer_resetcode = random_float
            c_details.save()

            # creating the session to send email of user to change password in reset_passwordDone method
            request.session['customer_email'] = c_details.customer_email

            #sending forget password code to user mail

            user = Customer.objects.get(customer_email = email)

            subject = "Reset Password"
            html_content = render_to_string('forgetpass_email.html',{
                                            'fname': user.customer_fname, 'lname': user.customer_lname, 'email': user.customer_email,'code':random_float})
            from_email = 'team.bookex@gmail.com'
            to = [c_details.customer_email]

            text_content = strip_tags(html_content)
            email = EmailMultiAlternatives(
                subject,
                text_content,
                from_email,
                to,
            )
            email.attach_alternative(html_content, "text/html")
            email.send(fail_silently=False)

            return render(request, "code_reset.html", {'fname': c_details.customer_fname,'code':c_details.customer_resetcode})
        else:
            print("This email doesn't exist.")
    return render(request, "forget_pass.html")


def reset_password(request):

    email = request.session.get('customer_email') # accessing the session
    customer_detail = Customer.objects.get(customer_email=email)

    if request.method == "POST":
        username = request.POST['username']
        code = request.POST['code']
        print(customer_detail.customer_username)
        if (int(customer_detail.customer_resetcode) == int(code) and customer_detail.customer_username == username):  # validate the generated code and user type code
            customer_detail.customer_resetcode = None
            customer_detail.save()
            return render(request, "reset_password.html")
        else:
            print("Invalid Code provided")
    return render(request, "code_reset.html")


def reset_passwordDone(request):
    if request.method == "POST":
        password = request.POST['password']
        c_password = request.POST['c_password']
        email = request.session.get('customer_email')
        # now we can access every data of that user via email
        customer_detail = Customer.objects.get(customer_email=email)

        if password == c_password:
            if password != customer_detail.customer_password:
                customer_detail.customer_password = make_password(password)
                customer_detail.save()
                print("Password Updated")
                return render(request, "signin.html")
            else:
                print("Password can't be same with old one")
        else:
            print("Confirm password didn't match")
    return render(request, "reset_password.html")


def send_offerEmail(request):
    # threshold_time = timezone.now() - timedelta(hours=1)
    # inactive_users = Customer.objects.filter(
    #     customer_login_history__lt=threshold_time)
    threshold_date = timezone.now() - timedelta(hours=1)
    print(threshold_date)
    inactive_users = Customer.objects.filter(customer_login_history__lt=threshold_date)
    print(inactive_users)
    emails = []
    for user in inactive_users:
        emails.append(user.customer_email)

        subject = "Haven't Seen You Lately!"
        html_content = render_to_string('offer_mail.html',{
                                        'fname': user.customer_fname, 'lname': user.customer_lname, 'email': user.customer_email})
        from_email = 'team.bookex@gmail.com'
        print(user.customer_fname)
        to = [user.customer_email]

        text_content = strip_tags(html_content)
        email = EmailMultiAlternatives(
            subject,
            text_content,
            from_email,
            to,
        )
        email.attach_alternative(html_content, "text/html")
        email.send(fail_silently=False)
    # return render(request, "signin.html")
    return redirect('/admin/GYMBookerapp/customer/')

#This function is used for customer Query
def joinclass(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        classInfo = request.POST['Select Class']
        comment = request.POST['comment']
        
        customer_query = CustomerQuery.objects.create(
            Cquery_name=name,
            Cquery_email=email,
            Cquery_class=classInfo,
            Cquery_comment=comment
        )
        customer_query.save()
    return render(request, 'joinClass.html')


def dashboard(request):
    #dashboard
    username = request.session.get('username')
    print(username)
    if username is not None:
        print(f'Active user: {username}')
        classes = Class.objects.all()

        #Used to store logged user full name
        u_username = request.session.get('username')
        customer_name = Customer.objects.get(customer_username = u_username)

        #acessing ManytoMany field
        customer_classes = customer_name.joined_class.all()
        #fetch upcoming classes
        current_day = datetime.now().strftime('%a')  # Get abbreviated day name (e.g., Mon, Tue)
        current_time = datetime.now().time()
        current_date = datetime.now().date()

        #views for Scheduled class on dashboard
        # upcoming_classes = ""

        classes = Class.objects.all()

        count = 0
        # for cls in customer_classes:
        #     print(cls)
        #     count += 1


        current_hour = current_time.hour
        current_hour_add = current_time.hour+1
        # # print(type(current_hour))
        # # print(f'----{current_hour}----')
        current_class= []
        upcoming_classes=[]
        
        for cls in customer_classes:
            count += 1
            print(f"------{cls.class_name}-----")
            print(f"------{cls.class_time}-----")
            
            class_days = cls.class_day.all()  # Access the ManyToManyField related objects
            
            
            class_hour = cls.class_time.hour
            # print(f'++{class_hour}++')
            # print(f'++{current_hour}++')
            # print(f'++{current_day}++')

            # join
            if class_hour >= current_hour and class_hour < current_hour_add:
                print(f'++{class_hour}++')
                print(f'++{current_hour}++')
                print(f'++{current_hour_add}++')
                for day in class_days:
                    print(day.day)  # Access the 'day' attribute of the 'Days' model
                    if day.day == current_day:
                        current_class.append(cls.class_name)
                        print("Current Class")
                        print(f'+++{current_class}++')

            # schedule
            if class_hour > current_hour:
                for day in class_days:
                    if day.day == current_day:
                        upcoming_classes.append(cls.class_name)
                        # print(upcoming_classes)
                        # print("upcoming_classes")
                        # print(f'++{upcoming_classes}++')

        #Membership Page
        membership = Membership.objects.all()

        #Check for Membership expiry date
        # Check membership expiry date
        membership_expiry_date = customer_name.customer_membership_exipredDate if customer_name.customer_membership else None
        
        if membership_expiry_date and membership_expiry_date >= current_date:
            # Membership is active
            is_membership_active = True
        else:
            # Membership is expired or not available
            is_membership_active = False
            customer_name.customer_membership = None
            customer_name.save()
        
            

        return render(request, "dashboard.html", {
            'classes': classes,
            'count': count,
            'customer_name': customer_name,
            'joined_classes': customer_classes,
            'current_class':current_class,
            'membership': membership,
            'upcoming_classes':upcoming_classes,
        })
    else:
        print("None active user available")
        return render(request, "signin.html")
    # return render(request, 'dashboard.html')

    
#have to remove only his session not whole server session
def logout(request):
    # get the session id
    session_id = request.session.session_key

    # delete the session from the database
    Session.objects.filter(session_key=session_id).delete()

    # flush the session data from memory
    request.session.flush()

    # remove the session cookie
    request.session.clear_expired()
    return redirect('landingpage')


def addclass(request, pk):
    customer_uname = request.session.get('username')
    customer_name = Customer.objects.get(customer_username = customer_uname)

    # customer_classes = customer_name.joined_class.all()

    #take the id of the class that user have just clicked and store it inot many to many field

    classes = Class.objects.get(id=pk)
    customer_name.joined_class.add(classes)

    return redirect('dashboard')

def leaveClass(request, pk):
    customer_uname = request.session.get('username')
    customer_name = Customer.objects.get(customer_username = customer_uname)

    classes = Class.objects.get(id=pk)
    customer_name.joined_class.remove(classes)

    return redirect('dashboard')

def addmembership(request,pk):
    currentdate = datetime.now().date()

    customer_uname = request.session.get('username')
    customer_name = Customer.objects.get(customer_username = customer_uname)

    membership = Membership.objects.get(id=pk)  # Retrieve a customer object by its primary key
    print(f'-----{membership}----')
    # customer_name.customer_membership.add(membership)
    customer_name.customer_membership = membership

    print(f'Date:{currentdate}')
    customer_name.customer_membership_joinedDate = currentdate

    threshold_date = timezone.now() + timedelta(days=30)
    # threshold_date = timezone.now() + timedelta(days=1)
    customer_name.customer_membership_exipredDate = threshold_date.date()

    customer_name.save()
    return redirect('dashboard')

def cancelmembership(request):

    customer_uname = request.session.get('username')
    customer_name = Customer.objects.get(customer_username = customer_uname)

    customer_name.customer_membership = None  # Set the membership to None
    customer_name.customer_membership_joinedDate = None
    customer_name.customer_membership_exipredDate = None

    customer_name.save()

    return redirect('dashboard')

def update_profile(request):
    customer_uname = request.session.get('username')
    customer_name = Customer.objects.get(customer_username = customer_uname)

    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        phone = request.POST['phone']
        dob = request.POST['dob']
        address = request.POST['address']
        

        if fname == "" or lname == "":
            print("Name cannot be empty")
        
        elif email == '':
            print("Email cannot be empty")
        
        elif phone == '':
            print("Phone cannot be empty")
        
        else:
            customer_name.customer_fname = fname
            customer_name.customer_lname = lname
            customer_name.customer_email = email
            customer_name.customer_phone = phone
            customer_name.customer_dob = dob
            customer_name.customer_address = address
            customer_name.save()
    
    customer_dob = datetime.strptime(customer_name.customer_dob, "%Y-%m-%d")
    todayDate = datetime.now().date()
    # print(todayDate.year)
    # print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    # print(customer_dob.year)

    age = todayDate.year - customer_dob.year  
    #.year is added beacuse we need to convert the customer_dob to a datetime.date object 
    if todayDate.month < customer_dob.month or (todayDate.month == customer_dob.month and todayDate.day < customer_dob.day):
        age -= 1
    
    customer_name.customer_age = age
    customer_name.save()

    return redirect('dashboard')

def update_physical_info (request):
    customer_uname = request.session.get('username')
    customer_name = Customer.objects.get(customer_username = customer_uname)

    if request.method == "POST":
        weight = request.POST['weight']
        height = request.POST['height']

        if weight == '' or height == '':
            print("Height or Weight cannot be empty")
        
        else:
            customer_name.customer_height = height
            customer_name.customer_weight = weight
            #calculate BMI
            bmi = int(customer_name.customer_weight) / (int(customer_name.customer_height)/100)**2
            customer_name.customer_bmi = round(bmi, 2)
            customer_name.save()
            # customer_name.save()


    return redirect(dashboard)

def update_image(request):
    customer_uname = request.session.get('username')
    if request.method == "POST":
        image = request.FILES.get("image")
        
        updateCustomer_image = Customer.objects.get(customer_username = customer_uname)
        updateCustomer_image.customer_image = image

        updateCustomer_image.save()
    return redirect(dashboard)

def delete_account (request):
    customer_uname = request.session.get('username')
    customer_name = Customer.objects.get(customer_username = customer_uname)

    #delete customer account
    print(f'{customer_name} is deleted')
    customer_name.delete()

    return redirect('signin')

def request_membership(request):
    return render(request, "request_membership.html")

def delete_image(request):
    customer_uname = request.session.get('username')
    customer_name = Customer.objects.get(customer_username = customer_uname)

    print(f'{customer_name} profile image is deleted')
    customer_name.customer_image.delete()

    return redirect('dashboard')

def search(request):
    if request.method == "POST":
        search_r = request.POST["search"]
        print(search_r)

        #Query to search for all rowa/name in models and present those result
        searchClass = Class.objects.filter(
            Q(class_name__icontains = search_r) | Q(class_instructor__icontains = search_r) | 
            Q(class_time__icontains = search_r) | Q(class_info__icontains = search_r)
            )

    return render(request, "search_result.html", {
        "classResult" : searchClass,
        })

def userreset_password(request):
    customer_uname = request.session.get('username')
    customer_detail = Customer.objects.get(customer_username = customer_uname)

    if customer_uname is None:
        return redirect("signin")
    else:
        if request.method == "POST":
            password = request.POST['password']
            c_password = request.POST['c_password']
            old_password = request.POST['old_password']
            if check_password(old_password, customer_detail.customer_password):
                if password == c_password and password != "":
                    if not check_password(password, customer_detail.customer_password):
                        customer_detail.customer_password = make_password(password)
                        customer_detail.save()
                        print("Password Updated")
                        return redirect("dashboard")
                    else:
                        return render(request, "userpassword_reset.html", {
                            "message" : "Password can't be same with old one",
                        })
                else:
                    return render(request, "userpassword_reset.html", {
                            "message" : "Confirm password didn't match / password cannot be empty",
                        })
            else:
                return render(request, "userpassword_reset.html", {
                            "message" : "Current password didn't matched",
                        })
        return render(request, "userpassword_reset.html")