from django.contrib import admin
from .models import Category, FoodItem

# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('category_name',)}    #fields that get filled-automatically, once its parent field gets filled
    list_display = ('category_name', 'vendor', 'updated_at')  #what columns of data should be present in the display/outer page
    search_fields = ('category_name', 'vendor__vendor_name') #provides search function where user can search!!!!!
    #vendor__vendor_name because, it is a foriegn key for the Category model, to access the attributes of vendor model we do this!!!!


class FoodItemAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('food_title',)}
    list_display = ('food_title', 'category', 'vendor', 'price', 'is_available', 'updated_at')
    search_fields = ('food_title', 'category__category_name', 'vendor__vendor_name', 'price')
    list_filter = ('is_available',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(FoodItem, FoodItemAdmin)