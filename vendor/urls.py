from django.urls import path, include
from . import views
from accounts import views as AccountViews                             #CAN ACCESS THE views.py from accounts app



urlpatterns = [
    path('', AccountViews.vendorDashboard, name='vendor'),
    path('profile/', views.vprofile, name='vprofile'),
]