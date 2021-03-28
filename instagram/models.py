from django.db import models

# Create your models here.
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
