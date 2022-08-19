from django.db import models
from accounts.models import User
from menu.models import FoodItem


# Create your models here.
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)    #For adding into the cart, u need o be logged-in!!!(So, we need the user)
    fooditem = models.ForeignKey(FoodItem, on_delete=models.CASCADE) #Need FoodItem model, since, we need to choose food, which is present in FoodItem
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):     #Since, user is foriegn key and we are accessing his property, we use uincode
        return self.user


