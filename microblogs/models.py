from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from libgravatar import Gravatar




# Create your models here.

class User(AbstractUser):
    username = models.CharField(max_length=20,unique=True)
    email = models.EmailField(unique=True,blank=False)
    first_name = models.CharField(max_length=50,blank=False)
    last_name = models.CharField(max_length=50,blank=False)
    bio = models.CharField(max_length=520,blank=True)
    followers = models.ManyToManyField('self', symmetrical=False, related_name='followees',blank=True)

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def gravatar(self,size=120):
        gravatar_object = Gravatar(self.email)
        gravatar_url = gravatar_object.get_image(size=size, default='mp')
        return gravatar_url
    
    def mini_gravatar(self):
        return self.gravatar(size=40)
    
    def toggle_follow(self,followee):
        if followee == self:
            return

        if self.is_following(followee):
            followee.followers.remove(self)
        else:
            followee.followers.add(self)
    
    def is_following(self,user):
        return user in self.followees.all()
   
    def follower_count(self):
        return self.followers.count()
    
    def followee_count(self):
        return self.followees.count()
    class Meta:
        ordering = ['last_name','first_name']

    
class Post(models.Model):

    author = models.ForeignKey(User,on_delete=models.CASCADE)
    text = models.CharField(max_length=280)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']