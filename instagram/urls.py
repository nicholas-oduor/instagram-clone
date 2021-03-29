from django.conf.urls import url
from . import views
from django.conf import settings
from django.urls import path,re_path
from django.conf.urls.static import static


from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

from django.conf.urls import url


from .views import UserView, signup

app_name = 'instagram'

urlpatterns = [
    path('', views.index, name='instag'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/accounts/login'), name='logout'),
    path('profile/',  login_required(UserView.as_view()), name='profile'),
    path('signup/', signup, name='signup'),
    path('search/', views.search_results, name='search_results'),
    path('new/comment/', views.new_comment, name='new_comment'),
    path('new/post/', views.new_post, name='new_post'),
    path('accounts/profile/', views.new_profile, name='new_profile'),
    path('image/(\d+)', views.get_image, name='image_results'),
    path('like/<int:pk>/', views.like_image, name='like_post'),
    
]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
