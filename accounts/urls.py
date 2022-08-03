from django.urls import path
from . import views

urlpatterns = [
    path('registerUser/',views.registerUser, name='registerUser'),   #when registerUser/ comes in path registerUser method in views trigger
    path('registerVendor/', views.registerVendor, name='registerVendor'),
]