from django.urls import path
from . import views

urlpatterns = [
    path('registerUser/',views.registerUser, name='registerUser'),   #when registerUser/ comes in path registerUser method in views trigger
    path('registerVendor/', views.registerVendor, name='registerVendor'),

    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('myAccount/', views.myAccount, name='myAccount'),   #for checking if user is cust/vendor
    path('custDashboard/', views.custDashboard, name='custDashboard'),
    path('vendorDashboard/', views.vendorDashboard, name='vendorDashboard')
]