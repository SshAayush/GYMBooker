from django.shortcuts import render
from .models import Customer, CustomerQuery
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
    return render(request, "landingpage.html")


def signup(request):  # Password need to be hashed
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

        #USed to store logged user full name
        customer_name = Customer.objects.get(customer_username = u_username)
        customer_fullName = customer_name.customer_fname + " " + customer_name.customer_lname

        s_details = Customer.objects.all()
        for s in s_details:
            if (s.customer_username == u_username and check_password(u_password, s.customer_password)):
                time = Customer.objects.get(id=s.id)
                time.customer_login_history = timezone.now()
                time.save()
                request.session['username'] = u_username #set the session of their username after loggin in
                request.session.save() # start the session
                # current_user = request.session.get['username']
                # print(current_user)
                return render(request, "dashboard.html", {'fullName': customer_fullName})

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
    username = request.session.get('username', None)
    if username is not None:
        print(f'Active user: {username}')
        return render(request, 'dashboard.html')
    else:
        print("None active user available")
        return render(request, "signin.html")

def logout(request):
    # get the session id
    session_id = request.session.session_key

    # delete the session from the database
    Session.objects.filter(session_key=session_id).delete()

    # flush the session data from memory
    request.session.flush()

    # remove the session cookie
    request.session.clear_expired()
    return render(request, 'landingpage.html')

