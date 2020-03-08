from django.forms import ModelForm
from .models import Post,Category,Province,City
from django import forms
from django.db import models


class PostForm(ModelForm):  
    title = models.CharField(max_length=100,verbose_name='标题')
    image=models.ImageField(upload_to="product_pics",verbose_name='图片')
    category=models.CharField(max_length=50,verbose_name='分类')
    price=models.IntegerField(verbose_name='价格')
    address=models.CharField(max_length=100,verbose_name='地址')
    content = models.TextField(verbose_name='详细信息')

    category = forms.ModelChoiceField(queryset=Category.objects.all(),label='分类')



    class Meta:
        model = Post
        fields = ['title','image',"category", "price",'province','city',"address",'content']



        
