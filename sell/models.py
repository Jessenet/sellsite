from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image

class Category(models.Model):
    name=models.CharField(max_length=100,verbose_name='类别')

    def __str__(self):
        return self.name

class Province(models.Model):
    name = models.CharField(max_length=30)
    def __str__(self):
        return self.name

class City(models.Model):
    province = models.ForeignKey(Province, on_delete=models.CASCADE)
    name = models.CharField(max_length=10)
    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=30,verbose_name='标题')
    content = models.TextField(verbose_name='详细信息(物品信息/联系方式等)')
    date_posted = models.DateTimeField(default=timezone.now,verbose_name='发布日期')
    author = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name='作者')

    category=models.CharField(max_length=50,verbose_name='分类')
    price=models.IntegerField(verbose_name='价格')
    address=models.CharField(max_length=100,verbose_name='地址')
    image=models.ImageField(upload_to="product_pics",verbose_name='图片')

    province = models.ForeignKey(Province, on_delete=models.CASCADE,verbose_name='省')
    #city = models.ForeignKey(City, on_delete=models.CASCADE,verbose_name='城市')
    city = models.CharField(max_length=10,verbose_name='城市')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        super(Post, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)



