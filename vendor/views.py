from django.shortcuts import render
from .forms import VendorForm
from accounts.forms import UserProfileForm
from django.shortcuts import get_object_or_404, redirect

from accounts.models import UserProfile
from .models import Vendor

from django.contrib import messages

from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.views import check_role_vendor

# Create your views here.

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vprofile(request):

    profile = get_object_or_404(UserProfile, user=request.user)    #both these contains instance of the current vendor(user + his specific deatils)
    vendor = get_object_or_404(Vendor, user=request.user)

    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)   #getting the necessary files form vendor, UPLOADED IN MY RESTAUARANT
        vendor_form = VendorForm(request.POST, request.FILES, instance=vendor)
        if profile_form.is_valid() and vendor_form.is_valid():
            profile_form.save()
            vendor_form.save()
            messages.success(request, 'Settings updated.')
            return redirect('vprofile')
        else:
            print(profile_form.errors)
            print(vendor_form.errors)

    else:
        profile_form = UserProfileForm(instance = profile)
        vendor_form = VendorForm(instance=vendor)

    profile_form = UserProfileForm(instance=profile)        #LOADS THE EXISITNG CONTENT OF THE USER INSIDE THE FORM
    vendor_form = VendorForm(instance=vendor)
    context = {
        'profile_form': profile_form,
        'vendor_form': vendor_form,
        'profile': profile,
        'vendor': vendor,
    }
    return render(request, 'vendor/vprofile.html', context)   #we will get the form fields inside this context
