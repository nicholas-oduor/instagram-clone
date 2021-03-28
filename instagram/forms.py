from django import forms
from .models import Image,Profile,Comment
from django_registration.forms import RegistrationForm

    
class NewPostForm(forms.ModelForm):
    class Meta:
        model = Image
        exclude = ['pub_date', 'Author', 'author_profile','likes']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']
