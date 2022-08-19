from django.db import models
from accounts.models import User, UserProfile
from accounts.utils import send_notification
# Create your models here.


class Vendor(models.Model):
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)                      #on_delete=...... deletes the referred  object as well as the objects that have rerference to it {like if u delete a blog comments also gets deleted}
    user_profile = models.OneToOneField(UserProfile, related_name='userprofile', on_delete=models.CASCADE)
    vendor_name = models.CharField(max_length=50)
    vendor_slug = models.SlugField(max_length=100, unique=True)
    vendor_license = models.ImageField(upload_to='vendor/license')
    is_approved = models.BooleanField(default=False)   #false because admin should approve to pusblish his rest details
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.vendor_name


#APPROVING THE VENDOR BY ADMIN
    def save(self, *args, **kwargs):
        if self.pk is not None:   #THIS IS UPDATE(URL CONTAINS A NUMBER(PRIMARY_KEY))
            orig = Vendor.objects.get(pk=self.pk)
            if orig.is_approved != self.is_approved:   #if is_approved is changed
                mail_template = 'accounts/emails/admin_approval_email.html'
                context = {                                 #to provide data to the HTML file
                    'user': self.user,
                    'is_approved': self.is_approved,
                    'to_email': self.user.email,
                }
                if self.is_approved == True: 
                    mail_subject = "Congratulations! Your restaurant has been approved."
                    send_notification(mail_subject, mail_template, context)
                else:
                    mail_subject = "We're sorry! You are not eligible for publishing your food menu on our marketplace."
                    send_notification(mail_subject, mail_template, context)
        return super(Vendor, self).save(*args, **kwargs)         #THIS IS A DEFINED SYNTAC FOR ACCESSING THE SAVE button in the model

    