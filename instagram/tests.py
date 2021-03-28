from django.test import TestCase
from .models import Image,Comment,Profile
import datetime as dt
from django.contrib.auth.models import User

# Create your tests here.
class ImageTestClass(TestCase):

    def setUp(self):
        # Creating a new profile and saving it
        self.nicholas = User.objects.create_user('nicholas', 'nicks@gmail.com', 'nickspass')
        self.profile = Profile(id=1,user=self.nicholas,bio="software developer")
        self.profile.save_profile()

        

        self.new_image= Image(id=1, image_name='image',description="awesome",pub_date="2021-03-04",Author=self.nicholas,author_profile=self.profile,likes="yes")
        self.new_image.save()
        
        # Creating a new comment and saving it
        self.comment = Comment(id=1,image=self.new_image,pub_date="28-03-2021",comment="nice",author=self.nicholas)
        self.comment.save_comment()

        # Testing  instance
    def test_instance(self):
        self.assertTrue(isinstance(self.new_image,Image))
        
    def test_save_method(self):
        self.new_image.save_image()
        new_image = Image.objects.all()      
        self.assertTrue(len(new_image) >0)
        
    def test_delete_image(self):
        self.new_image.delete_image()
        image = Image.objects.all()
        self.assertTrue(len(image)== 0)
        
    def test_update_image(self):
        self.new_image.save_image()
        self.new_image.update_image(self.new_image.id, 'photos/test.jpg')
        changed_img = Image.objects.filter(image='photos/test.jpg')
        self.assertTrue(len(changed_img) > 0)
