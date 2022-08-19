from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from vendor.models import Vendor
from menu.models import Category, FoodItem
from django.db.models import Prefetch
from .context_processors import get_cart_counter,  get_cart_amounts
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D # ``D`` is a shortcut for ``Distance``
from django.contrib.gis.db.models.functions import Distance

from .models import Cart
# Create your views here.
def marketplace(request):
    vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)      #getting vendors and looping thru
    vendor_count = vendors.count()  #to find number of vendors
    context = {
        'vendors': vendors,
        'vendor_count': vendor_count,
    }
    return render(request, 'marketplace/listings.html', context)

def vendor_detail(request, vendor_slug):
    vendor = get_object_or_404(Vendor, vendor_slug=vendor_slug)


    categories = Category.objects.filter(vendor=vendor).prefetch_related(                   #prefetch_related for reverse look -up using the foriegn keyed values
        Prefetch(
            'fooditems',
            queryset = FoodItem.objects.filter(is_available=True)
        )
    )

    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        cart_items = None   #Not Logged-in

    context = {
        'vendor': vendor,
        'categories': categories,
        'cart_items': cart_items,
    }
    return render(request, 'marketplace/vendor_detail.html', context)



def add_to_cart(request, food_id):
    if request.user.is_authenticated:
        #if request.is_ajax(): (django 4 removed this way of checking ajax request)
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # Check if the food item exists
            try:
                fooditem = FoodItem.objects.get(id=food_id)
                # Check if the user has already added that food to the cart
                try:
                    chkCart = Cart.objects.get(user=request.user, fooditem=fooditem)    #request.user is authenticated user
                    # Increase the cart quantity
                    chkCart.quantity += 1
                    chkCart.save()
                    return JsonResponse({'status': 'Success', 'message': 'Increased the cart quantity', 'cart_counter': get_cart_counter(request), 'qty': chkCart.quantity, 'cart_amount': get_cart_amounts(request)})  #get_cart_counter is the context processor we wrote to get nuber of qty
                except:                                                                                                                                                      #'qty' to print the qty of that food pushed to cart between + and -
                    #if the food_item is not present in cart we need to add it
                    chkCart = Cart.objects.create(user=request.user, fooditem=fooditem, quantity=1)
                    return JsonResponse({'status': 'Success', 'message': 'Added the food to the cart', 'cart_counter': get_cart_counter(request), 'qty': chkCart.quantity, 'cart_amount': get_cart_amounts(request)})
            except:
                return JsonResponse({'status': 'Failed', 'message': 'This food does not exist!'})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid request!'})
    else:
        return JsonResponse({'status': 'login_required', 'message': 'Please login to continue'})




def decrease_cart(request, food_id):
    if request.user.is_authenticated:
        #if request.is_ajax(): (django 4 removed this way of checking ajax request)
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # Check if the food item exists
            try:
                fooditem = FoodItem.objects.get(id=food_id)
                # Check if the user has already added that food to the cart
                try:
                    chkCart = Cart.objects.get(user=request.user, fooditem=fooditem)
                    if chkCart.quantity > 1:
                        # decrease the cart quantity
                        chkCart.quantity -= 1
                        chkCart.save()
                    else:
                        chkCart.delete()
                        chkCart.quantity = 0
                    return JsonResponse({'status': 'Success', 'cart_counter': get_cart_counter(request), 'qty': chkCart.quantity, 'cart_amount': get_cart_amounts(request)})
                except:                                                                                                                                                     
                    #if the food_item is not present in cart we need to add it
                    return JsonResponse({'status': 'Failed', 'message': 'You do not have this item in your cart!'})
            except:
                return JsonResponse({'status': 'Failed', 'message': 'This food does not exist!'})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid request!'})
    else:
        return JsonResponse({'status': 'login_required', 'message': 'Please login to continue'})




@login_required(login_url = 'login')                   #if user is logged-out and types the cart url-path, he will be re-directed to the home page!!
def cart(request):
    cart_items = Cart.objects.filter(user=request.user).order_by('created_at')
    context = {
        'cart_items': cart_items,
    }
    return render(request, 'marketplace/cart.html', context)



def delete_cart(request, cart_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                # Check if the cart item exists
                cart_item = Cart.objects.get(user=request.user, id=cart_id)
                if cart_item:
                    cart_item.delete()
                    return JsonResponse({'status': 'Success', 'message': 'Cart item has been deleted!', 'cart_counter': get_cart_counter(request), 'cart_amount': get_cart_amounts(request)})
            except:
                return JsonResponse({'status': 'Failed', 'message': 'Cart Item does not exist!'})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid request!'})





def search(request):

    if not 'address' in request.GET:
        return redirect('marketplace')

    else:

        address = request.GET['address']   #'address'  is from <input type="text" name="address" class="location-field-text filter" id="id_address" required placeholder="All Locations">
        latitude = request.GET['lat']
        longitude = request.GET['lng']
        radius = request.GET['radius']
        keyword = request.GET['keyword'] #rest-name

        # get vendor ids that has the food item the user is looking for
        fetch_vendors_by_fooditems = FoodItem.objects.filter(food_title__icontains=keyword, is_available=True).values_list('vendor', flat=True)   #provides list of ID's of vendors!!

        #FoodItem.objects.filter(food_title__icontains=keyword, is_available=True) willl give the food-items itself, but we need the list of vendors
        #values_list('vendor', flat=True) gives list of venodr

        vendors = Vendor.objects.filter(Q(id__in=fetch_vendors_by_fooditems) | Q(vendor_name__icontains=keyword, is_approved=True, user__is_active=True))   #Q-object is user for complex quering. Since ware using "OR"!!!
        #vendors = Vendor.objects.filter(vendor_name__icontains=keyword, is_approved=True, user__is_active=True)  #search user with the "restaurant_name" given in the search!!
        #here we are getting vendors from both "rest-name" as well as "food-item"


        if latitude and longitude and radius:  #ONLY RESTAURANTS HAVE Lat and LONG
            pnt = GEOSGeometry('POINT(%s %s)' % (longitude, latitude))   #%s for string representation technique of dynamic-values

            vendors = Vendor.objects.filter(Q(id__in=fetch_vendors_by_fooditems) | Q(vendor_name__icontains=keyword, is_approved=True, user__is_active=True),
            user_profile__location__distance_lte=(pnt, D(km=radius)) #find all restaurants having distance less than equal to the radius
            ).annotate(distance=Distance("user_profile__location", pnt)).order_by("distance")  #using the in-built geodjango Disatance function
            #annotate gets the summary from the db
        
            for v in vendors:
                v.kms = round(v.distance.km, 1)    #distance is not a field but we define it in the prev step, km --> kilometre
                #round upto to 1 decimal
        
        vendor_count = vendors.count()
        context = {
            'vendors': vendors,
            'vendor_count': vendor_count,
            'source_location': address,
        }

        return render(request, 'marketplace/listings.html', context)