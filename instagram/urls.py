from django.conf.urls import url
from . import views
from django.conf import settings
from django.urls import path,re_path
from django.conf.urls.static import static


urlpatterns =[
    path('search/', views.search_results, name='search_results'),
    path('new/comment/', views.new_comment, name='new_comment'),
    path('new/post/', views.new_post, name='new_post'),
    path('accounts/profile/', views.new_profile, name='new_profile'),
    path('image/(\d+)', views.get_image, name='image_results'),
    path('like/<int:pk>/', views.like_image, name='like_post'),
    
]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
