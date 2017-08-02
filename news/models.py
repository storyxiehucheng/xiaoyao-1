from django.db import models

from django.contrib import auth


# Create your models here.
class News(models.Model):
    createdTime = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100)
    contentText = models.TextField()
    analysisText = models.TextField()
    img = models.ImageField(upload_to='img')
    tf = models.BooleanField(default=False)
    NEWS_TYPE_CHOICES = (
        ('health', '健康'),
        ('tech', '科学'),
        ('eat', '饮食'),
    )
    newsType = models.CharField(max_length=10, choices=NEWS_TYPE_CHOICES)
    commentCount = models.IntegerField()

    # users = models.ForeignKey('auth.User', related_name='news', null=True)
    # 未添加收藏以及顶
    # users = models.ManyToManyField('auth.User', related_name='news')

    class Meta:
        # 前面加-表示倒序，新闻从新开始看
        ordering = ('-id',)


class Comments(models.Model):
    user = models.ForeignKey('auth.User', related_name='comments', null=True)
    news = models.ForeignKey('News', related_name='comments', null=True)
    createdTime = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=200)

    class Meta:
        # 评论从旧开始看
        ordering = ('createdTime',)


# class Followers(models.Model):

# 应用于在服务器存储更新文件
class Apps(models.Model):
    title = models.CharField(max_length=100)
    version = models.CharField(max_length=100)
    info = models.TextField(null=True)
    app = models.FileField(upload_to='apps')
    qrcode = models.ImageField(upload_to='apps')
    createdTime = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-createdTime',)


class Shows(models.Model):
    logo = models.ImageField(upload_to='apps')
    avatar = models.ImageField(upload_to='apps')


# class


from django.contrib.auth.models import User


class MyUser(models.Model):
    user = models.OneToOneField(User)
    avatar = models.ImageField(upload_to='avatar')
