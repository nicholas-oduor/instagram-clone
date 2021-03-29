from django.shortcuts import render,redirect,get_object_or_404
from django.http  import HttpResponse,Http404,HttpResponseRedirect
import datetime as dt
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from django.urls import reverse


from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from . import forms
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages


from django.views.generic.detail import DetailView

from .forms import SignUpForm


class UserView(DetailView):
    template_name = 'users/profile.html'

    def get_object(self):
        return self.request.user


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(request, email=user.email, password=raw_password)
            if user is not None:
                login(request, user)
            else:
                print("user is not authenticated")
            return redirect('users:profile')
    else:
        form = SignUpForm()
    return render(request, 'users/signup.html', {'form': form})


# Create your views here.
# @login_required(login_url='/accounts/login/')
def index(request):
    images = Image.objects.all()
    date = dt.date.today()
    current_user = request.user
    users = Profile.objects.all()
    
    
    
    
    if request.method == 'POST':
        form = NewsLetterForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['your_name']
            email = form.cleaned_data['email']

            recipient = NewsLetterRecipients(name = name,email = email)
            recipient.save()
            send_welcome_email(name,email)

            HttpResponseRedirect('instag')
    else:
        form = NewsLetterForm()
    return render(request, 'home.html', {"date": date,"images":images, "users":users, "form": form})


@login_required(login_url='/accounts/login/')
def new_post(request):
    current_user = request.user
    if request.method == 'POST':
        form = NewPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.Author = current_user
            post.save()
        return redirect('instag')

    else:
        form = NewPostForm()
    return render(request, 'new_post.html', {"form": form})

@login_required(login_url='/accounts/login/')
def new_profile(request):
    current_user = request.user
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = current_user
            post.save()
        return redirect('instag')

    else:
        form = ProfileForm()
    return render(request, 'profile.html', {"form": form})

@login_required(login_url='/accounts/login/')
def search_results(request):

    if 'Author' in request.GET and request.GET["Author"]:
        Author = request.GET.get("Author")
        Author = Image.search_by_author(Author)
        message = f"{Author}"

        return render(request, 'search.html',{"message":message,"Author":Author})

    else:
        message = "You haven't searched for any term"
        return render(request, 'search.html',{"message":message})
    
    
@login_required(login_url='/accounts/login/')
def new_comment(request):
    current_user = request.user
    if request.method == 'POST':
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.Author = current_user
            post.save()
        return redirect('instag')

    else:
        form = CommentForm()
    return render(request, 'new_comment.html', {"form": form})

@login_required(login_url='/accounts/login/')
def get_image(request, id):
    comments = Comment.get_comment()

    try:
        image = Image.objects.get(pk = id)        
        
    except ObjectDoesNotExist:
        raise Http404()
    
    current_user = request.user 
    if request.method == 'POST':
        form = CommentForm(request.POST, auto_id=False)
        img_id = request.POST['image_id']
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = current_user
            image = Image.get_image(img_id)
            comment.image = image
            comment.save()
            return redirect(f'/image/{img_id}',)
    else:
        form = CommentForm(auto_id=False)
    
    return render(request, "images.html", {"image":image, "form":form, "comments":comments})

def like_image(request, pk):
    post= get_object_or_404(Image, id=request.POST.get('post_id'))
    post.likes.add(request.user)
    return HttpResponseRedirect(reverse('instag', args=[str(pk)]))
