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
from django.http import HttpResponse
import uuid, requests, json

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
                return render(request, 
                              "signup.html",{'acc_created': msg}
                              )
        else:
            print("Confirmation password mismatched")
            msg = "Confirmation password mismatched"
            return render(request, 
                            "signup.html",{'acc_created': msg}
                            )
    return render(request, "signup.html")


def signin(request):
    if request.method == "POST":
        u_username = request.POST['username']
        u_password = request.POST['password']

        ss = Customer.objects.get(customer_username = u_username)
        if (ss.customer_username == u_username and check_password(u_password, ss.customer_password)):
            if(ss.is_active):
                time = Customer.objects.get(id=ss.id)
                time.customer_login_history = timezone.now()
                time.save()
                request.session['username'] = u_username #set the session of their username after loggin in
                request.session.save() # start the session
                # current_user = request.session.get('username')
                # print(f'{current_user} yoyoyoyyo')
                return redirect('dashboard')
            else:
                print("Your account is not active")
                msg = "Your account is not active"
                return render(request, "signin.html",{'message': msg})
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
            from_email = 'xayush.tc@gmail.com'
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
            message = "This email doesn't exist."
            print("This email doesn't exist.")
    return render(request, "forget_pass.html",{
        "message" : message,
    })


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
            message = "Invalid Code provided"
            print("Invalid Code provided")
    return render(request, "code_reset.html", {
        "message" : message,
    })


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
                message = "Password can't be same with old one"
        else:
            print("Confirm password didn't match")
            message = "Password can't be same with old one"
    return render(request, "reset_password.html",{
        "message" : message,
    })


def send_offerEmail(request):
    customer_uname = request.session.get('username')
    
    threshold_date = timezone.now() - timedelta(hours=1)
    print(threshold_date)
    inactive_users = Customer.objects.filter(customer_login_history__lt=threshold_date)
    print(inactive_users)
    emails = []
    for user in inactive_users:
        emails.append(user.customer_email)

        discount = random.randint(5,20)

        subject = "Haven't Seen You Lately!"
        html_content = render_to_string('offer_mail.html',{
                                        'fname': user.customer_fname, 
                                        'lname': user.customer_lname, 
                                        'email': user.customer_email,
                                        'discount': discount,
                                        })
        from_email = 'xayush.tc@gmail.com'
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
    fetchClasses = Class.objects.all()
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
    return render(request, 'joinClass.html',{
        'classes' : fetchClasses,
    })


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
        
        current_membership = customer_name.customer_membership

        return render(request, "dashboard.html", {
            'classes': classes,
            'count': count,
            'customer_name': customer_name,
            'joined_classes': customer_classes,
            'current_class':current_class,
            'membership': membership,
            'upcoming_classes':upcoming_classes,
            'current_membership': current_membership,
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
    # request.session.flush()

    # remove the session cookie
    # request.session.clear_expired()
    return redirect('landingpage')


def addclass(request, pk):
    customer_uname = request.session.get('username')
    if customer_uname is None:
        return redirect("signin")
    

    customer_name = Customer.objects.get(customer_username = customer_uname)

    # customer_classes = customer_name.joined_class.all()

    #take the id of the class that user have just clicked and store it inot many to many field

    classes = Class.objects.get(id=pk)
    customer_name.joined_class.add(classes)
    customer_name.save()

    return redirect('dashboard')
    

def leaveClass(request, pk):
    customer_uname = request.session.get('username')
    if customer_uname is None:
        return redirect("signin")
    
    customer_name = Customer.objects.get(customer_username = customer_uname)

    classes = Class.objects.get(id=pk)
    customer_name.joined_class.remove(classes)

    return redirect('dashboard')

def checkout(request):
    if request.method == "POST":
        subTotal = request.POST["subTotal"]
        uuid = request.POST["uuid"]
        return_url = request.POST["return_url"]
        
        shipping_inc = float(subTotal) + 10
        
        print("shipping inc",shipping_inc)
        
        subPaisa = (float(shipping_inc)) * 100
        
        user = request.user
        
        print(subPaisa)
        
        print("uuid",uuid)
        print("subTotal",subPaisa)
        print("return_url http://127.0.0.1:8000",return_url)
        print("user",user.username)
    
    url = "https://a.khalti.com/api/v2/epayment/initiate/"

    payload = json.dumps({
        "return_url": "http://127.0.0.1:8000" + return_url,
        "website_url": "http://127.0.0.1:8000",
        "amount": subPaisa,
        "purchase_order_id": uuid,
        "purchase_order_name": "test",
        "customer_info": {
        "name": user.username,
        "email": user.email,
        "phone": user.userprofile.Phone_Number
        }
    })
    headers = {
        'Authorization': 'key 07b52c0f30dc425ea9c53fd77e798e9d',
        'Content-Type': 'application/json',
    }

    response = requests.request("POST", url, headers=headers, data=payload)


    new_res = json.loads(response.text)
    print(new_res)

    # Save the transaction code in the db to validate transaction
    transaction_id = new_res['pidx']
    return redirect(new_res['payment_url'])


    # return redirect('dashboard')
    # return redirect(reverse('dashboard') + f'?containerName=membershipContainer')

def addmembership(request, pk):
    customer_uname = request.session.get('username')
    if customer_uname is None:
        return redirect("signin")
    
    currentdate = datetime.now().date()
    customer_uname = request.session.get('username')
    customer_name = Customer.objects.get(customer_username=customer_uname)

    membership = Membership.objects.get(id=pk)
    print(f'-----{membership}----')
    customer_name.customer_membership = membership

    print(f'Date:{currentdate}')
    customer_name.customer_membership_joinedDate = currentdate

    threshold_date = timezone.now() + timedelta(days=30)
    customer_name.customer_membership_expiredDate = threshold_date.date()

    customer_name.save()
    
    subTotal = membership.membership_price
    uid = str(uuid.uuid4()) # Convert UUID object to string
    
    shipping_inc = float(subTotal) + 10
    subPaisa = (float(shipping_inc)) * 100
    
    user = request.user
    
    print(subPaisa)
    print("uuid", uid)
    print("subTotal", subPaisa)
    print("return_url http://127.0.0.1:8000/dashboard")
    print("user", "Aashish")
    
    url = "https://a.khalti.com/api/v2/epayment/initiate/"

    payload = json.dumps({
        "return_url": "http://127.0.0.1:8000/dashboard",
        "website_url": "http://127.0.0.1",
        "amount": subPaisa,
        "purchase_order_id": uid,
        "purchase_order_name": "test",
        "customer_info": {
            "name": "Aashish",
            "email": "aashsish@gmail.com",
            "phone": "9800000004"
        }
    })
    headers = {
        'Authorization': 'key live_secret_key_68791341fdd94846a146f0457ff7b455',
        'Content-Type': 'application/json',
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    new_res = json.loads(response.text)
    print(new_res)
    return redirect(new_res['payment_url'])


def cancelmembership(request):
    customer_uname = request.session.get('username')
    if customer_uname is None:
        return redirect("signin")
    
    customer_name = Customer.objects.get(customer_username = customer_uname)

    customer_name.customer_membership = None  # Set the membership to None
    customer_name.customer_membership_joinedDate = None
    customer_name.customer_membership_exipredDate = None
    customer_name.is_confirmed = False

    customer_name.save()

    return redirect(reverse('dashboard') + f'?containerName=membershipContainer')

def update_profile(request):
    customer_uname = request.session.get('username')
    if customer_uname is None:
        return redirect("signin")
    

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

    age = todayDate.year - customer_dob.year  
    #.year is added beacuse we need to convert the customer_dob to a datetime.date object 
    if todayDate.month < customer_dob.month or (todayDate.month == customer_dob.month and todayDate.day < customer_dob.day):
        age -= 1
    
    customer_name.customer_age = age
    customer_name.save()

    return redirect('dashboard')

def update_physical_info (request):
    customer_uname = request.session.get('username')
    if customer_uname is None:
        return redirect("signin")
    
    customer_name = Customer.objects.get(customer_username = customer_uname)

    if request.method == "POST":
        weight = request.POST['weight']
        height = request.POST['height']

        if weight == '' or height == '':
            print("Height or Weight cannot be empty")
        
        else:
            if customer_name.customer_count == 0:
                customer_name.customer_currheight = height
                customer_name.customer_currweight = weight
                customer_name.customer_height = height
                customer_name.customer_weight = weight
            else:
                customer_name.customer_currheight = height
                customer_name.customer_currweight = weight
                #calculate BMI
                bmi = int(customer_name.customer_weight) / (int(customer_name.customer_height)/100)**2
                customer_name.customer_startbmi = round(bmi, 2)
                cbmi = int(customer_name.customer_currweight) / (int(customer_name.customer_currheight)/100)**2
                customer_name.customer_bmi = round(cbmi, 2)
                customer_name.customer_bmidiff = int(customer_name.customer_startbmi)- int(customer_name.customer_bmi)
                customer_name.customer_count = int(customer_name.customer_currweight) - int(customer_name.customer_weight)

            customer_name.save()
            # customer_name.save()


    return redirect(dashboard)

def update_image(request):
    customer_uname = request.session.get('username')
    if customer_uname is None:
        return redirect("signin")
    
    if request.method == "POST":
        image = request.FILES.get("image")
        
        updateCustomer_image = Customer.objects.get(customer_username = customer_uname)
        updateCustomer_image.customer_image = image

        updateCustomer_image.save()
        
    return redirect(dashboard)

def delete_account (request):
    customer_uname = request.session.get('username')
    if customer_uname is None:
        return redirect("signin")
    
    customer_name = Customer.objects.get(customer_username = customer_uname)

    #delete customer account
    print(f'{customer_name} is deleted')
    customer_name.delete()

    return redirect('signin')

def request_membership(request):
    customer_uname = request.session.get('username')
    if customer_uname is None:
        return redirect("signin")
    
    return render(request, "request_membership.html")

def change_membershipFrom(request):
    customer_uname = request.session.get('username')
    if customer_uname:

        if request.method == 'POST':
            name = request.POST['name']
            email = request.POST['email']
            classInfo = request.POST['Select Class']
            comment = request.POST['Reason']
            
            customer_query = CustomerQuery.objects.create(
                Cquery_name=name,
                Cquery_email=email,
                Cquery_class=classInfo,
                Cquery_comment=comment
            )
            customer_query.save()
        return redirect('dashboard')
    print("Not logged in")
    return redirect('signin')

def delete_image(request):
    customer_uname = request.session.get('username')
    customer_name = Customer.objects.get(customer_username = customer_uname)

    print(f'{customer_name} profile image is deleted')
    customer_name.customer_image.delete()

    return redirect('dashboard')

def search(request):
    customer_uname = request.session.get('username')
    if customer_uname is None:
        return redirect("signin")
    
    if request.method == "POST":
        search_r = request.POST["search"]
        print(search_r)

        #Used to store logged user full name
        u_username = request.session.get('username')
        customer_name = Customer.objects.get(customer_username = u_username)

        #acessing ManytoMany field
        customer_classes = customer_name.joined_class.all()
        #Query to search for all rowa/name in models and present those result
        searchClass = Class.objects.filter(
            Q(class_name__icontains = search_r) | Q(class_instructor__icontains = search_r) | 
            Q(class_time__icontains = search_r)
            )
        
        print(f'Serach Result:{searchClass}')

    return render(request, "search_result.html", {
        "classResult" : searchClass,
        "joined_classes" : customer_classes,
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