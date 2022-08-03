from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models.fields.related import ForeignKey, OneToOneField

# Create your models here.
class UserManager(BaseUserManager):  
    def create_user(self, first_name, last_name, username, email, password=None):  #self is used if a fn is created inside a class
        if not email:
            raise ValueError('User must have an email address')

        if not username:
            raise ValueError('User must have an username')


        user = self.model( 
            email = self.normalize_email(email),   #takes email-address from us and converts upper to lower if contains!!
            username = username,
            first_name = first_name,
            last_name = last_name,
        )
        user.set_password(password)
        user.save(using=self._db)     #mention which db django should use(We have only one DB, so no prob)
        return user





    def create_superuser(self, first_name, last_name, username, email, password=None):
        user = self.create_user(          #first make him a user then we can make him to super user
            email = self.normalize_email(email),   #takes email-address from us and converts upper to lower if contains!!
            username = username,
            password = password,
            first_name = first_name,
            last_name = last_name,
        )     
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user





class User(AbstractBaseUser):
    VENDOR = 1       #For seperating customer with vendor(rest owner)
    CUSTOMER = 2

    ROLE_CHOICE = (
        (VENDOR,'Vendor'),
        (CUSTOMER, 'Customer'),
    )

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100,unique=True)
    phone_number = models.CharField(max_length=12,blank=True) #phone number is optional
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICE, blank=True, null = True)


    #required fields
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    created_data = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    #django only takes username for login purposes we need to overwrite it

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = UserManager()


    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):     #Returns True for active and superusers
        return True                            #Returns False for inactive users

    def get_role(self):
        if self.role == 1:
            user_role = 'Vendor'
        elif self.role == 2:
            user_role = 'Customer'
        return user_role
    
class UserProfile(models.Model):
    user = OneToOneField(User, on_delete=models.CASCADE,blank=True, null=True)      #one user can have only one account
    profile_picture = models.ImageField(upload_to='users/profile_pictures', blank=True, null=True)
    cover_photo = models.ImageField(upload_to='users/cover_photos', blank=True, null=True)
    address_line_1 = models.CharField(max_length=50, blank=True, null=True)
    address_line_2 = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=15, blank=True, null=True)
    state = models.CharField(max_length=15, blank=True, null=True)
    city = models.CharField(max_length=15, blank=True, null=True)
    pin_code = models.CharField(max_length=6, blank=True, null=True)
    latitude = models.CharField(max_length=20, blank=True, null=True)
    longitude = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email




