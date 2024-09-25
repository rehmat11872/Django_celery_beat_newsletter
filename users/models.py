from django.db import models
from django.contrib.auth.models import User
from django.templatetags.static import static
from django.conf import settings

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='avatars/', null=True, blank=True)
    displayname = models.CharField(max_length=50, null=True, blank=True)
    info = models.TextField(null=True, blank=True)
    newsletter_subscribed = models.BooleanField(default=True)

    def __str__(self):
        return str(self.user)
    
    @property
    def name(self):
        if self.displayname:
            return self.displayname
        return self.user.username 
    
    @property
    def avatar(self):
        if self.image:
            return self.image.url
        return f'{settings.STATIC_URL}images/avatar.svg'
    
    # @property
    # def name(self):
    #     if self.displayname:
    #         name = self.displayname
    #     else:
    #         name = self.name
    #     return name        
    
    # @property
    # def image(self):
    #     try:
    #         avatar = self.image.url
    #     except:
    #         avatar = static('images/avatar.svg')    
    #     return avatar        