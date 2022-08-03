from doctest import FAIL_FAST
from django.forms import PasswordInput
from django.http import HttpResponse
from django.shortcuts import redirect, render
from .utils import detectUser
from vendor.forms import VendorForm
from .forms import UserForm
from .models import User, UserProfile
from django.contrib import messages,auth #for prompting user with messages in webpage
from django.contrib.auth.decorators import login_required,user_passes_test  #for decorator
from django.core.exceptions import PermissionDenied


# Restrict the vendor from accessing the customer page
def check_role_vendor(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied


#Restrict the customer from accessing the vendor page
def check_role_customer(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied







def registerUser(request):
    if request.user.is_authenticated:                 #when user is logged-in and goes to /login path in web-url this will trigger
        messages.warning(request, 'You are already logged in!')
        return redirect('dashboard')


    elif request.method == 'POST':
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
    if request.user.is_authenticated:                 #when user is logged-in and goes to /login path in web-url this will trigger
        messages.warning(request, 'You are already logged in!')
        return redirect('dashboard')

    elif request.method == 'POST':
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


def login(request):                                     #whenever user wants to come in the login page this method is invoked
    
    
    if request.user.is_authenticated:                 #when user is logged-in and goes to /login path in web-url this will trigger
        messages.warning(request, 'You are already logged in!')
        return redirect('myAccount')

        
    elif request.method == 'POST':
        email = request.POST['email']   #'email' is the name of html name=email should be same
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)  #django inbuilt check for uniqueness in email and password
        
        if user is not None:   #if line 88 is crct we can log-in him by this
            auth.login(request, user)  #user is logged-in
            messages.success(request, 'You are now logged in.')
            return redirect('myAccount')
                                                                            #messages.succes, messages.error all are the customized bootstrap prompt we made
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('login')


    return render(request, 'accounts/login.html')

def logout(request):
    auth.logout(request)
    messages.info(request, 'You are logged out.')
    return redirect('login')



@login_required(login_url='login')     #If the user is not logged in and clicks this he will be re-directed to the login page using this decorator function
def myAccount(request):                #returns if ur customer/vendor/superadmin
    user = request.user       #request.user is the user who is currently logged in*****
    redirectUrl = detectUser(user)
    return redirect(redirectUrl)


@login_required(login_url='login')
@user_passes_test(check_role_customer)
def custDashboard(request):
    return render(request, 'accounts/custDashboard.html')


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vendorDashboard(request):
    return render(request, 'accounts/vendorDashboard.html')