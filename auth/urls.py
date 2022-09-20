from django.contrib import admin
from django.urls import path
from .views import index, login, ad_callback

urlpatterns = [
    path("", index, name="index"),
    path("login/", login, name="login"),
    path("getAToken/", ad_callback, name="ad_callback"),
]
