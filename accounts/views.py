from doctest import FAIL_FAST
from django.forms import PasswordInput
from django.http import HttpResponse
from django.shortcuts import redirect, render

from vendor.forms import VendorForm
from .forms import UserForm
from .models import User, UserProfile
from django.contrib import messages #for prompting user with messages in webpage
# Create your views here.

def registerUser(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():

            #Creating the user using the form
            # password=form.cleaned_data['password']
            # user=form.save(commit=False)
            # user.set_password(password) #will be saved but not be commited in db
            # user.role = User.CUSTOMER
            # user.save()

            #Creating the user using create_user_method
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email = email,password=password)
            user.role = User.CUSTOMER
            user.save()
            messages.success(request, 'Your account has been registered succesfully')
            return redirect('registerUser')
        else:
            print('Invalid form')
            print(form.errors)  #for field errors like char>maxchar etc...
    else: 
        form = UserForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/registerUser.html', context)


#REGISTRATION FOR VENDORS

def registerVendor(request):
    if request.method == 'POST':
        #store the data and create the vendor
        form = UserForm(request.POST)
        v_form = VendorForm(request.POST, request.FILES)# for reciveing files(licesnse)
        if form.is_valid() and v_form.is_valid:
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email = email,password=password)
            user.role = User.VENDOR
            user.save()
            vendor = v_form.save(commit=False)  #need to provide user and userprofile before posting in db(commit=false)
            vendor.user = user
            user_profile = UserProfile.objects.get(user=user)    #signals will create user_profile
            vendor.user_profile = user_profile
            vendor.save()
            messages.success(request, 'Your account has been registered succesfully! Please wait for the approval.')
            return redirect('registerVendor')
        else:
            print(form.errors)
    else: #get request(LIKE REFRESHING THE PAGE  IS NOT POSTING)
        form = UserForm()
        v_form = VendorForm()

    context = {
        'form':form,
        'v_form':v_form,
    }

    return render(request, 'accounts/registerVendor.html', context)