from django.contrib import admin
from django.urls import path, include
from home.views import *
from authentication.views import *

urlpatterns = [
    path("", include("home.urls")),
    path("", include("authentication.urls")),
]
