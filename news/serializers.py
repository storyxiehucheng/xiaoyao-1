# encoding: utf-8

'''

@author: Soofo

@license: (C) Copyright 2017-2018, IECAS Limited.

@contact: iecaser@163.com

@software: pycharm

@file: serializers.py

@time: 2017/4/12 13:09

@desc:

'''

from rest_framework import serializers
from news.models import News, Comments
from django.contrib.auth.models import User


class NewsDetailSerializer(serializers.ModelSerializer):
    # comments = serializers.PrimaryKeyRelatedField(many=True, queryset=Comments.objects.all())
    # comments = serializers.SlugRelatedField(many=True, slug_field='text',queryset=Comments.objects.all())
    # followers = serializers.SlugRelatedField(many=True)
    # users = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())

    class Meta:
        model = News
        fields = ('id', 'title', 'contentText', 'analysisText', 'img', 'newsType', 'tf', 'createdTime', 'commentCount')


class NewsListSerializer(serializers.ModelSerializer):
    # users = serializers.PrimaryKeyRelatedField(many=True,queryset=User.objects.all())
    class Meta:
        model = News
        fields = ('id', 'title', 'contentText', 'img', 'newsType', 'tf', 'commentCount',)


# class UserFingerSerializer(serializers.ModelSerializer):
#     news = serializers.ManyRelatedField(child_relation=News)
#     class Meta:
#         model = User
#         fields = ('news',)



from django.conf import settings as django_settings

import datetime
import json
from django.core.mail import send_mail
import random


def SendToken(user, message):
    now = datetime.datetime.now()
    if user.last_login is not None:
        delta = now.timestamp() - user.last_login.timestamp()
        if delta < 25:
            return False
    user.last_login = now
    user.last_name = random.randint(1000, 9999)
    user.save()
    send_mail('『消谣』{}说明'.format(message),
              '''
                      
  亲爱的用户，
  这封信是由 『消谣』 发送的。
  
  您收到这封邮件，是因为在我们的网站上这个邮箱地址被登记为用户邮箱，
  且该用户请求使用 Email{}功能所致。
                   
                   
  ------------------------------------------------
  您此次{}请求的验证码为 {} ,请再10分钟之内完成验证。
  重发则此验证码失效。




  ------------------------------------------------
  如果您没有提交{}的请求或不是我们网站的注册用户，请忽略
  并删除这封邮件。                  
          
              '''.format(message, message, user.last_name, message),
              'admin@soffo.top', [user.email], fail_silently=False)
    return True


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'last_name')


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password',)


from news.models import MyUser


# 头像设置
# class UserAvatarSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = MyUser
#         fields = ('user', 'avatar',)


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('id', 'email', 'last_name')


class UserResetSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'last_name',)


class CommentSerializer(serializers.ModelSerializer):
    news = serializers.ReadOnlyField(source='news.id')  # 所属news的id
    user = serializers.ReadOnlyField(source='user.username', )  # 评论人

    # follower = serializers.ReadOnlyField(source='')
    class Meta:
        model = Comments
        fields = ('id', 'text', 'createdTime', 'news', 'user')


from news.models import Apps


class AppsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Apps
        fields = ('id', 'title', 'version', 'app','qrcode', 'info', 'createdTime',)
