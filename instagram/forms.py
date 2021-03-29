from django import forms
from .models import *

from django.contrib.auth.forms import UserCreationForm
# from .models import User
 
class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email',)

    
class NewPostForm(forms.ModelForm):
    class Meta:
        model = Image
        exclude = ['pub_date', 'Author', 'author_profile','likes']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']

class NewsLetterForm(forms.Form):
    your_name = forms.CharField(label='First Name',max_length=30)
    email = forms.EmailField(label='Email')

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ['pub_date', 'author', 'image']
