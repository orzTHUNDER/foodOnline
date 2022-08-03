from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from .models import User, UserProfile



#DJANGO SIGNALS TO CREATE USER PROFILE!!!
@receiver(post_save, sender=User)
def post_save_create_profile_reciever(sender, instance, created, **kwargs):   #for reciever, created is flag, returns true if acc is created
    print(created)
    if created:
        #print('create the user profile')
        UserProfile.objects.create(user=instance) #user is intance so it creates user profile after user is created
    else:  #not creating but updating case
        
        try:                                                #if user is deleted in users but not in userprofiles
            profile=UserProfile.objects.get(user=instance)
            profile.save()
        except:
            UserProfile.objects.create(user=instance)   #create this user!!
#post_save.connect(post_save_create_profile_reciever, sender=User)    #using signals!!!!!(another way)


@receiver(pre_save, sender=User)
def pre_save_profile_receiver(sender, instance, **kwargs):
    pass
   