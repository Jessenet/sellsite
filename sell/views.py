from django.shortcuts import render, get_object_or_404,redirect,HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required  
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post,City,Province
from django import forms
from .forms import PostForm
from datetime import datetime
from django.http import JsonResponse

from geoip import geolite2
import requests
from django.contrib.gis.geoip2 import GeoIP2
import geoip2.database
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))



def home(request):
    my_ip=requests.get('https://api.ipify.org').text
    reader=geoip2.database.Reader('C:\workspace\djstartup\mktvenv\Lib\site-packages\geoip2\GeoLite2-City.mmdb')
    response=reader.city('210.2.31.255')
    #response=reader.city(my_ip)
    Province=response.subdivisions.most_specific.names['zh-CN']


    return HttpResponse(Province)

    #context = {
     #   'posts': Post.objects.all()
    #}
    #return render(request, 'sell/home.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'sell/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 9

    def get_queryset(self):
        my_ip=requests.get('https://api.ipify.org').text
        DIR = os.path.join(BASE_DIR,'mktvenv', 'lib','site-packages','geoip2','GeoLite2-City.mmdb')
        reader=geoip2.database.Reader(DIR)
        response=reader.city(my_ip)
        provinces=response.subdivisions.most_specific.names['zh-CN']
        count=Post.objects.filter(province__name=provinces)
        if not provinces:
            return Post.objects.all().order_by('-date_posted')
        elif not count:
            return Post.objects.all().order_by('-date_posted')
        else:
            return Post.objects.filter(province__name=provinces).order_by('-date_posted')


class UserPostListView(ListView):
    model = Post
    template_name = 'sell/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 9

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

class SearchTitleListView(ListView):
    model = Post
    template_name = 'sell/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'


    def get_queryset(self):
        title = self.request.GET.get('title')
        my_ip=requests.get('https://api.ipify.org').text
        DIR = os.path.join(BASE_DIR,'mktvenv', 'lib','site-packages','geoip2','GeoLite2-City.mmdb')
        reader=geoip2.database.Reader(DIR)
        response=reader.city(my_ip)
        provinces=response.subdivisions.most_specific.names['zh-CN']
        count=Post.objects.filter(title__contains=title,province__name=provinces)
        if not provinces:
            return Post.objects.filter(title__contains=title).order_by('-date_posted')
        elif not count:
            return Post.objects.filter(title__contains=title).order_by('-date_posted')
        else:
            return Post.objects.filter(title__contains=title,province__name=provinces).order_by('-date_posted')



class PostDetailView(DetailView):
    model = Post


#class PostCreateView(LoginRequiredMixin, CreateView):
    #form_class = PostForm 

   # def form_valid(self, form):
    #    form.instance.author = self.request.user
    #    return super().form_valid(form)

@login_required
def PostCreateView(request):
    p_form=PostForm()
    if request.method=='POST':
        p_form=PostForm(request.POST,request.FILES)
        if p_form.is_valid():
            post=p_form.save(commit=False)
            post.date_posted= datetime.now() 
            post.author=request.user
            post.save()
            messages.success(request, f'你的物品信息已发布!')
            return redirect('/')
    else:
        p_form =PostForm()
    context={'form':p_form}

    return render(request, 'sell/post_form.html', context)





class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'sell/about.html', {'title': 'About'})



class ItemFilter_electronic(ListView):
    model = Post
    template_name = 'sell/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 9

    def get_queryset(self):
        my_ip=requests.get('https://api.ipify.org').text
        DIR = os.path.join(BASE_DIR,'mktvenv', 'lib','site-packages','geoip2','GeoLite2-City.mmdb')
        reader=geoip2.database.Reader(DIR)
        response=reader.city(my_ip)
        provinces=response.subdivisions.most_specific.names['zh-CN']
        count=Post.objects.filter(category='电子产品',province__name=provinces)
        if not provinces:
            return Post.objects.filter(category='电子产品').order_by('-date_posted')
        elif not count:
            return Post.objects.filter(category='电子产品').order_by('-date_posted')
        else:
            return Post.objects.filter(category='电子产品',province__name=provinces).order_by('-date_posted')

class ItemFilter_car(ListView):
    model = Post
    template_name = 'sell/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 9

    def get_queryset(self):
        my_ip=requests.get('https://api.ipify.org').text
        DIR = os.path.join(BASE_DIR,'mktvenv', 'lib','site-packages','geoip2','GeoLite2-City.mmdb')
        reader=geoip2.database.Reader(DIR)
        response=reader.city(my_ip)
        provinces=response.subdivisions.most_specific.names['zh-CN']
        count=Post.objects.filter(category='汽车',province__name=provinces)
        if not provinces:
            return Post.objects.filter(category='汽车').order_by('-date_posted')
        elif not count:
            return Post.objects.filter(category='汽车').order_by('-date_posted')
        else:
            return Post.objects.filter(category='汽车',province__name=provinces).order_by('-date_posted')




class ItemFilter_books(ListView):
    model = Post
    template_name = 'sell/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 9

    def get_queryset(self):
        my_ip=requests.get('https://api.ipify.org').text
        DIR = os.path.join(BASE_DIR,'mktvenv', 'lib','site-packages','geoip2','GeoLite2-City.mmdb')
        reader=geoip2.database.Reader(DIR)
        response=reader.city(my_ip)
        provinces=response.subdivisions.most_specific.names['zh-CN']
        count=Post.objects.filter(category='书籍',province__name=provinces)
        if not provinces:
            return Post.objects.filter(category='书籍').order_by('-date_posted')
        elif not count:
            return Post.objects.filter(category='书籍').order_by('-date_posted')
        else:
            return Post.objects.filter(category='书籍',province__name=provinces).order_by('-date_posted')


class ItemFilter_furniture(ListView):
    model = Post
    template_name = 'sell/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 9

    def get_queryset(self):
        my_ip=requests.get('https://api.ipify.org').text
        DIR = os.path.join(BASE_DIR,'mktvenv', 'lib','site-packages','geoip2','GeoLite2-City.mmdb')
        reader=geoip2.database.Reader(DIR)
        response=reader.city(my_ip)
        provinces=response.subdivisions.most_specific.names['zh-CN']
        count=Post.objects.filter(category='家具',province__name=provinces)
        if not provinces:
            return Post.objects.filter(category='家具').order_by('-date_posted')
        elif not count:
            return Post.objects.filter(category='家具').order_by('-date_posted')
        else:
            return Post.objects.filter(category='家具',province__name=provinces).order_by('-date_posted')


class ItemFilter_sports(ListView):
    model = Post
    template_name = 'sell/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 9

    def get_queryset(self):
        my_ip=requests.get('https://api.ipify.org').text
        DIR = os.path.join(BASE_DIR,'mktvenv', 'lib','site-packages','geoip2','GeoLite2-City.mmdb')
        reader=geoip2.database.Reader(DIR)
        response=reader.city(my_ip)
        provinces=response.subdivisions.most_specific.names['zh-CN']
        count=Post.objects.filter(category='运动',province__name=provinces)
        if not provinces:
            return Post.objects.filter(category='运动').order_by('-date_posted')
        elif not count:
            return Post.objects.filter(category='运动').order_by('-date_posted')
        else:
            return Post.objects.filter(category='运动',province__name=provinces).order_by('-date_posted')


class ItemFilter_clothes(ListView):
    model = Post
    template_name = 'sell/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 9

    def get_queryset(self):
        my_ip=requests.get('https://api.ipify.org').text
        DIR = os.path.join(BASE_DIR,'mktvenv', 'lib','site-packages','geoip2','GeoLite2-City.mmdb')
        reader=geoip2.database.Reader(DIR)
        response=reader.city(my_ip)
        provinces=response.subdivisions.most_specific.names['zh-CN']
        count=Post.objects.filter(category='衣服鞋',province__name=provinces)
        if not provinces:
            return Post.objects.filter(category='衣服鞋').order_by('-date_posted')
        elif not count:
            return Post.objects.filter(category='衣服鞋').order_by('-date_posted')
        else:
            return Post.objects.filter(category='衣服鞋',province__name=provinces).order_by('-date_posted')


class ItemFilter_free(ListView):
    model = Post
    template_name = 'sell/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 9

    def get_queryset(self):
        my_ip=requests.get('https://api.ipify.org').text
        DIR = os.path.join(BASE_DIR,'mktvenv', 'lib','site-packages','geoip2','GeoLite2-City.mmdb')
        reader=geoip2.database.Reader(DIR)
        response=reader.city(my_ip)
        provinces=response.subdivisions.most_specific.names['zh-CN']
        count=Post.objects.filter(category='免费')
        if not provinces:
            return Post.objects.filter(category='免费').order_by('-date_posted')
        elif not count:
            return Post.objects.filter(category='免费').order_by('-date_posted')
        else:
            return Post.objects.filter(category='免费',province__name=provinces).order_by('-date_posted')


class ItemFilter_others(ListView):
    model = Post
    template_name = 'sell/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 9

    def get_queryset(self):
        my_ip=requests.get('https://api.ipify.org').text
        DIR = os.path.join(BASE_DIR,'mktvenv', 'lib','site-packages','geoip2','GeoLite2-City.mmdb')
        reader=geoip2.database.Reader(DIR)
        response=reader.city(my_ip)
        provinces=response.subdivisions.most_specific.names['zh-CN']
        count=Post.objects.filter(category='其它')
        if not provinces:
            return Post.objects.filter(category='其它').order_by('-date_posted')
        elif not count:
            return Post.objects.filter(category='其它').order_by('-date_posted')
        else:
            return Post.objects.filter(category='其它',province__name=provinces).order_by('-date_posted')

    
class PostListViewCountry(ListView):
    model = Post
    template_name = 'sell/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 9





