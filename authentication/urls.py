from django.urls import path
from authentication.views import *
from authentication.constants import (SIGNIN_URL, SIGNOUT_URL,SIGNUP_URL)
urlpatterns = [
    path(SIGNIN_URL + "/", signin, name="signin"),
    path(SIGNUP_URL + "/", signup, name="signup"),
    path(SIGNOUT_URL + "/", signout, name="signout"),
    path("activate/<uidb64>/<token>", activateUser, name="activate"),
]
