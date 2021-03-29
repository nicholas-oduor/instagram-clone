from __future__ import unicode_literals

from django.db import models
import cloudinary
from cloudinary.models import CloudinaryField
from tinymce.models import HTMLField
import datetime as dt
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _

# Create your models here.
class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        print("email...",email)
        print("password...",password)
        return self._create_user(email, password=password, **extra_fields)




class Profile(models.Model):
    # form.instance.user = Profile.objects.get(user=self.request.user)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    photo = CloudinaryField('image')
    
    def save_profile(self):
        self.save()
        
    def delete_profile(self):
        self.delete()
        
    
    @classmethod
    def get_profile(request, id):
        try:
            profile = Profile.objects.get(pk = id)
            print(image)
            
        except ObjectDoesNotExist:
            raise Http404()
        
        return profile
        
    @classmethod
    def update_profile(cls, id, value):
        cls.objects.filter(id=id).update(name = value)
        
    def __str__(self):
        return self.bio 

class Image(models.Model):
    image = CloudinaryField('image')
    image_name = models.CharField(max_length=255)
    description = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    Author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    author_profile = models.ForeignKey(Profile,on_delete=models.CASCADE, null=True)
    likes = models.ManyToManyField(User, related_name = 'likes', blank = True)
    
    
    def save_image(self):
        self.save()
    
    def delete_image(self):
        self.delete()
        
    def total_likes(self):
        return self.likes.count()
        
    @classmethod
    def update_image(cls, id, value):
        cls.objects.filter(id=id).update(image=value)
    
    @classmethod
    def get_image(request, id):
        try:
            image = Image.objects.get(pk = id)
            print(image)
            
        except ObjectDoesNotExist:
            raise Http404()
        
        return image
    
    @classmethod
    def search_by_author(cls, Author):
        images = cls.objects.filter(Author__user__icontains=Author)
        return images

  
    def __str__(self):
        return self.image_name 

class Comment(models.Model):
    comment = models.TextField(blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE )
    pub_date = models.DateTimeField(auto_now_add=True)
    
    def save_comment(self):
        self.save()
        
    def delete_comment(self):
        self.delete()
        
    @classmethod
    def update_comment(cls, id, value):
        cls.objects.filter(id=id).update(name = value)
        
    def __str__(self):
        return self.comment