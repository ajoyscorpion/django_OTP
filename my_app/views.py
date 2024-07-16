from django.shortcuts import render,redirect
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.decorators import login_required
from .models import Users
from django.contrib import messages
from django.contrib.auth import login,logout
from django.db.models import Q
import random
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from django.conf import settings
from sms import send_sms

def home(request):
    
    print(request.user.is_authenticated)

    if request.user.is_authenticated:
        print(request.user.name)
        name = request.user.name
        first_name = request.user.first_name
        last_name = request.user.last_name
        print(first_name)
    else:
        name = ""

    data = {
        'name' : name,
        'first_name' : first_name,
        'last_name' : last_name
    }

    return render(request,"base.html", {'data':data})

def register(request):
    print(request)
    if request.method == 'POST':
        name = request.POST.get("name")
        print(name)
        email = request.POST.get("email")
        print(email)
        phone = request.POST.get("phone")
        print(phone)
        password = request.POST.get('password')

        if Users.objects.filter(name=name,email=email,phone_number=phone):
            print("User already exists")
            messages.error(request,"User Already Exits")
        else :
            user_profile = Users.objects.create_user(name=name,email=email,phone_number=phone)
            print(user_profile)
            # user_profile.save
            messages.success(request,"User Successfully Registered")
            login(request,user_profile,backend='django.contrib.auth.backends.ModelBackend')
            return redirect("home")
    return render(request,"register.html")

# def signIn(request):

    is_otpGenerated = False

    if request.method == 'POST':

        email = request.POST.get("email")
        phone = request.POST.get('phone')

        print(email)
        print(phone)

        if Users.objects.filter(Q(email=email) | Q(phone_number=phone)):
            print("User Found")
            user = Users.objects.get(Q(email=email) | Q(phone_number=phone))

            user.max_otp_try = 3    

            if user.max_otp_try == 0:
                print("OTP maximum reached")
                return render(request,"signIn.html")

            otp = random.randint(1000,9999)
            otp_expiry = timezone.now() + timedelta(3)
            max_otp_try = user.max_otp_try

            user.otp = otp
            user.otp_duration = otp_expiry
            user.max_otp_try = max_otp_try
            user.save()

            if phone:
                send_otp(phone,otp)
                is_otpGenerated = True
            elif email:
                send_otp(email,otp)
                is_otpGenerated = True
            else:
                print("Failed to send OTP")

            print(max_otp_try)
            print(otp_expiry)
            print(user)
            print(otp)    

        else:
            print("User Not Found. Please Register")

    return render(request,"signIn.html",{"is_otpGenerated":is_otpGenerated})



def logout_view(request):
    logout(request)
    return redirect("home")




def send_otp(destination,otp):
    if '@' in destination:
        subject = 'Your OTP Code'
        message = f'Your OTP code is {otp}. It will expire in 3 minutes'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [destination]
        send_mail(subject,message,email_from,recipient_list)
    else:
        send_sms(
            'Your OTP code is {otp}. It will expire in 3 minutes',
            '+918113000923',
            '+91{destination}',
            fail_silently=False
        )
        print("OTP send to the {destination}")


# def verify_otp(request):
    # if request.method == 'POST':
    #     entered_otp = request.POST.get('otp')
    #     print(entered_otp)
    #     email = Users.
    #     phone = user.phone
    #     print(email)
    #     print(phone)

    #     user = Users.objects.get(Q(email=email) | Q(phone_number=phone))
    #     otp = user.otp

    #     if entered_otp == otp:
    #         print("The user has been verified")
    #         user.otp = None
    #         user.max_otp_try = 3
    #         user.otp_duration = None
    #         redirect("home")
    #     else:
    #         print("Failed to verify the User")
    # return render(request,"signIn.html")
        




def signInOrVerifyOTP(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        phone = request.POST.get('phone')
        otp = request.POST.get('otp')

        print(email)
        print(otp)

        if Users.objects.filter(Q(email=email) | Q(phone_number=phone)):
            user = Users.objects.get(Q(email=email) | Q(phone_number=phone))

            if otp:  # OTP verification
                saved_otp = user.otp
                if saved_otp and otp == saved_otp:
                    # Clear OTP-related fields after successful verification
                    user.otp = None
                    user.otp_duration = None
                    user.max_otp_try = 3
                    user.save()
                    login(request,user,backend='django.contrib.auth.backends.ModelBackend')
                    return redirect("home")
                else:
                    messages.error(request, "Incorrect OTP. Please try again.")
                    return render(request, "signIn.html", {"is_otpGenerated": True, "email": email, "phone": phone})

            else:  # Generating OTP
                if user.max_otp_try > 0:
                    otp = random.randint(1000, 9999)
                    otp_expiry = timezone.now() + timedelta(minutes=3)
                    user.otp = otp
                    user.otp_duration = otp_expiry
                    user.max_otp_try -= 1
                    user.save()

                    if phone:
                        send_otp(phone, otp)
                    elif email:
                        send_otp(email, otp)

                    return render(request, "signIn.html", {"is_otpGenerated": True, "email": email, "phone": phone})
                else:
                    messages.error(request, "OTP maximum attempts reached. Please try again later.")
                    return render(request, "signIn.html", {"email": email, "phone": phone})

        else:
            messages.error(request, "User not found. Please register.")
            return render(request, "signIn.html", {"email": email, "phone": phone})

    return render(request, "signIn.html")