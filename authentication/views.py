from django.http import HttpResponse
from django.shortcuts import redirect, render
from core import settings

from django.contrib import messages
from django.contrib.auth.models import User

from django.core.mail import EmailMessage, send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth import authenticate, login, logout
from .token import generate_token
from .constants import (SIGNIN_TEMPLATE,
                        EMAIL_CONFIRMATION_TEMPLATE, 
                        EMAIL_WELCOME_TEMPLATE, 
                        ERROR_ACTIVATION_INVALID, 
                        ERROR_ALREADY_REGISTERED, 
                        ERROR_BAD_CREDENTIALS, 
                        ERROR_PASSWORDS_NOT_MATCH, 
                        SIGNIN_URL, SIGNUP_URL,
                        SIGNUP_TEMPLATE, 
                        SUCCESS_LOGIN, 
                        SUCCESS_LOGOUT, 
                        SUCCESS_ACCOUNT_CREATED,
                        SUCCESS_ACTIVATED,)


def signin(request):
    if request.method == "POST":
        username = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            firstName = user.first_name
            messages.success(request, SUCCESS_LOGIN)
            return render(request, "homePage.html", {"firstName": firstName})
        else:
            messages.error(request, ERROR_BAD_CREDENTIALS)
            return redirect(SIGNIN_URL)
    return render(
        request,
        SIGNIN_TEMPLATE,
    )


def signup(request):
    if request.method == "POST":
        username = request.POST["email"]
        firstName = request.POST["firstName"]
        lastName = request.POST["lastName"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmPassword = request.POST["confirmPassword"]

        if User.objects.filter(email=email).exists():
            messages.error(request,ERROR_ALREADY_REGISTERED,)
            return redirect(SIGNUP_URL)

        elif password != confirmPassword:
            messages.error(request, ERROR_PASSWORDS_NOT_MATCH)
            return redirect(SIGNUP_URL)

        else:
            myuser = User.objects.create_user(username, email, password)
            myuser.first_name = firstName
            myuser.last_name = lastName
            myuser.is_active = False
            myuser.save()
            messages.success(request,SUCCESS_ACCOUNT_CREATED,)

            # Welcome Email
            welcome_subject = "Welcome to vRemember!!"
            welcomeMessage = render_to_string(EMAIL_WELCOME_TEMPLATE)
            from_email = settings.EMAIL_HOST_USER
            to_list = [myuser.email]
            send_mail(
                welcome_subject, welcomeMessage, from_email, to_list, fail_silently=True
            )

            # Email Address Confirmation Email
            current_site = get_current_site(request)
            confirmation_subject = "Verify your Email "
            confirmationMail = render_to_string(
                EMAIL_CONFIRMATION_TEMPLATE,
                {
                    "name": myuser.first_name,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(myuser.pk)),
                    "token": generate_token.make_token(myuser),
                },
            )
            email = EmailMessage(
                confirmation_subject,
                confirmationMail,
                settings.EMAIL_HOST_USER,
                [myuser.email],
            )
            email.fail_silently = True
            email.send()

            return redirect(SIGNIN_URL)
    return render(request, SIGNUP_TEMPLATE)


def activateUser(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True
        myuser.save()
        login(request, myuser)
        messages.success(request, SUCCESS_ACTIVATED)
        return redirect(SIGNIN_URL)
    else:
        return HttpResponse(ERROR_ACTIVATION_INVALID)


def signout(request):
    logout(request)
    messages.success(request, SUCCESS_LOGOUT)
    return redirect(SIGNIN_URL)
