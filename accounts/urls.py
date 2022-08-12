from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.myAccount),
    path('registerUser/',views.registerUser, name='registerUser'),   #when registerUser/ comes in path registerUser method in views trigger
    path('registerVendor/', views.registerVendor, name='registerVendor'),

    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('myAccount/', views.myAccount, name='myAccount'),   #for checking if user is cust/vendor
    path('custDashboard/', views.custDashboard, name='custDashboard'),
    path('vendorDashboard/', views.vendorDashboard, name='vendorDashboard'),

    path('activate/<uidb64>/<token>/', views.activate, name='activate'),  #for activating user


    path('forgot_password/', views.forgot_password, name='forgot_password'), #for forgot password
    path('reset_password_validate/<uidb64>/<token>/', views.reset_password_validate, name='reset_password_validate'),
    path('reset_password/', views.reset_password, name='reset_password'),  #user will reset his password in this page

    path('vendor/', include('vendor.urls')),
]