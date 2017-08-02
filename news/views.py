from django.shortcuts import render

# Create your views here.
from news.models import News, Comments, Apps, Shows
from news.serializers import NewsDetailSerializer, CommentSerializer, NewsListSerializer
from rest_framework import generics
# for register
from rest_framework import generics, viewsets, mixins, status, permissions
from django.contrib.auth import login, logout
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.http import HttpResponse
from rest_framework.response import Response
import re


def IsPasswordValid(password):
    return re.match(r'^(?=.*[A-Za-z])(?=.*[0-9])\w{6,}$', password)


def IsEmailValid(email):
    return re.match(r"[-_\w\.]{0,64}@([-\w]{1,63}\.)*[-\w]{1,63}", email)


def Index(request):
    return render(request, template_name='index.html')


from rest_framework import pagination


class NewsPagination(pagination.PageNumberPagination):
    page_size = 6


# from django_filter
class NewsList(generics.ListAPIView):
    queryset = News.objects.all()
    serializer_class = NewsListSerializer
    pagination_class = NewsPagination

    def list(self, request, *args, **kwargs):
        newsType = request.GET.get('newstype', None)
        print(newsType)
        if newsType:
            queryset = News.objects.filter(newsType=newsType)
            print(queryset)
        else:
            queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class NewsTypeList(generics.ListAPIView):
    queryset = News.objects.all()
    serializer_class = NewsListSerializer
    pagination_class = NewsPagination

    def list(self, request, *args, **kwargs):
        # queryset = self.filter_queryset(self.get_queryset())
        newsType = request.GET.get('newstype', None)
        if newsType:
            queryset = News.objects.filter(newsType=newsType)
        else:
            queryset = None
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


def convertDelta(createdTime):
    chunks = (
        (60 * 60 * 24 * 365, '年'),
        (60 * 60 * 24 * 30, '个月'),
        (60 * 60 * 24 * 7, '周'),
        (60 * 60 * 24, '天'),
        (60 * 60, '小时'),
        (60, '分钟'),
    )
    delta = datetime.datetime.now() - createdTime
    secDelta = delta.total_seconds()
    secDelta = round(secDelta)
    if secDelta < 60:
        return '刚刚'
    for seconds, unit in chunks:
        count = secDelta // seconds
        if count != 0:
            break
    return str(count) + unit + "前"


class NewsDetail(generics.RetrieveAPIView):
    queryset = News.objects.all()
    serializer_class = NewsDetailSerializer


from django.views.generic import ListView, DetailView


class NewsShare(DetailView):
    model = News
    # template_name = 'newsShow2.html'
    template_name = 'Untitled-9.html'
    def get_context_data(self, **kwargs):
        context = super(NewsShare, self).get_context_data(**kwargs)
        lastApp = Apps.objects.all()[0]
        context['appQrcode'] = lastApp.qrcode.url
        context['appurl'] = lastApp.app.url
        shows = Shows.objects.all()[0]
        context['logo'] = shows.logo.url
        context['avatar'] = shows.avatar.url

        return context


from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.contrib.auth.models import User
from rest_framework import authentication
from rest_framework import exceptions


class CommentsPagination(pagination.PageNumberPagination):
    page_size = 999
    # page_size_query_param = 'page_size'
    # max_page_size = 1000


# from news.serializers import UserFingerSerializer
# class UserFinger(generics.ListAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserFingerSerializer



class NewsComments(generics.ListCreateAPIView):
    # queryset = Comments.objects.all()
    queryset = Comments.objects.all()
    serializer_class = CommentSerializer
    # 验证方式为Token，在settings中说明
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    pagination_class = CommentsPagination

    def list(self, request, *args, **kwargs):
        # queryset = self.filter_queryset(self.get_queryset())
        queryset = Comments.objects.filter(news=self.kwargs['pk'])
        # 为了改上一句，设定filter。下面的都是按照原格式抄上的
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            # print(serializer.data)
            setList = []
            # 为了显示评论距离现在的时间，把每个q的数据重写
            for p in page:
                tempSet = {'id': p.id, 'timeDelta': convertDelta(p.createdTime), 'text': p.text,
                           'user': p.user.username}
                # 因为queryset是预先排序的set，所以按顺序迭代之后append仍是排序的
                setList.append(tempSet)
            return self.get_paginated_response(setList)
        # serializer = self.get_serializer(queryset, many=True)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        # self.kwargs传入的是正则提取的参数，也就是post的url指明了往哪里post
        # self.request.user 因为user是认证信息，在head里面
        # 当评论创建的时候，要手动更新所属文章、用户
        username = self.request.user
        user = User.objects.get(username=username)
        user.last_login = datetime.datetime.now()
        user.save()
        # , timeDelta = convertDelta()
        serializer.save(news_id=self.kwargs['pk'], user=user)
        n = News.objects.get(id=self.kwargs['pk'])
        n.commentCount = Comments.objects.filter(news_id=self.kwargs['pk']).count()
        n.save()


# from django.views.decorators.csrf import csrf_exempt
# @csrf_exempt
# def logoutView(request):
#     logout(request)
#     return Response("logout success")

from news.serializers import UserRegisterSerializer, UserLoginSerializer, UserResetSerializer
import datetime


# from django.contrib import auth

class UserLogin(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        username = self.request.data.get('username')
        password = self.request.data.get('password')
        try:
            if re.match(r"[-_\w\.]{0,64}@([-\w]{1,63}\.)*[-\w]{1,63}", username):
                # print('by email:')
                olduser = User.objects.get(email=username)
            else:
                # print('by username:')
                olduser = User.objects.get(username=username)
            if olduser.is_active:
                if olduser.check_password(password):
                    if not olduser.is_active:
                        return Response({'username': ['请先登录邮箱激活']}, status=status.HTTP_400_BAD_REQUEST)
                    # 验证通过
                    # 修改最后登录时间
                    olduser.last_login = datetime.datetime.utcnow()
                    olduser.save()
                    # 获取token
                    token = Token.objects.get_or_create(user=olduser)
                    # 登录成功，给token用于以后评论
                    return Response(
                        # {'username': olduser.username, 'token': token[0].key, 'avatar': olduser.myuser.avatar.url},
                        {'username': olduser.username, 'token': token[0].key},
                        status=status.HTTP_200_OK)
                return Response({'password': ['您输入的帐号和密码不符']}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'username': ['该帐号未注册']}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'username': ['该帐号未注册']}, status=status.HTTP_400_BAD_REQUEST)


import json
from news.serializers import SendToken
from django.views.decorators.csrf import csrf_exempt

import random


class UserRegister(generics.ListCreateAPIView):
    # queryset = User.objects.all()
    serializer_class = UserRegisterSerializer

    def get(self, request, *args, **kwargs):
        email = request.GET.get('email', None)
        if email:
            if IsEmailValid(email=email):
                try:
                    user = User.objects.get(email=email)
                except User.DoesNotExist:
                    username = "user_{}".format(random.randint(1000, 9999))
                    password = "password000000"
                    user = User.objects.create_user(username=username, password=password, email=email)
                    user.is_active = False
                    user.is_staff = False
                    user.save()
                if user.is_active:
                    return Response('该邮箱已被注册', status=status.HTTP_400_BAD_REQUEST)
                if SendToken(user=user, message='帐号激活'):
                    return Response('验证码已发送，请登录邮箱查看', status=status.HTTP_200_OK)
                return Response('验证请求频繁，请稍候再试', status=status.HTTP_400_BAD_REQUEST)
            return Response('email格式不正确', status=status.HTTP_400_BAD_REQUEST)
        return Response('参数缺失', status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        username = request.data.get('username')
        password = request.data.get('password')
        last_name = request.data.get('last_name')
        have_user = User.objects.filter(username=username)
        if len(have_user) != 0:
            return Response('该用户名已被注册', status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(email=email)
            if last_name == user.last_name:
                delta = datetime.datetime.now().timestamp() - user.last_login.timestamp()
                if delta < 600:
                    user.username = username
                    user.set_password(password)
                    user.is_active = True
                    user.is_staff = True
                    user.save()
                    token = Token.objects.get_or_create(user=user)
                    return Response({'username': user.username, 'token': token[0].key}, status=status.HTTP_201_CREATED)
                else:
                    return Response('验证码失效', status=status.HTTP_400_BAD_REQUEST)
            return Response('验证码错误', status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response('邮箱错误', status=status.HTTP_400_BAD_REQUEST)


from django.shortcuts import render, render_to_response, Http404
# from news.serializers import UserAvatarSerializer
from news.models import MyUser


# user avatar update
# class UserAvatar(generics.RetrieveAPIView):
#     queryset = MyUser.objects.all()
#     # queryset = User.objects.all()
#     serializer_class = UserAvatarSerializer
#     lookup_field = 'user'
#     # permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
#     def get(self, request, *args, **kwargs):
#         return Response(str(self.get_queryset()))


class UserReset(generics.CreateAPIView):
    # queryset = User.objects.all()
    serializer_class = UserResetSerializer

    def get(self, request, *args, **kwargs):
        email = request.GET.get('email', None)
        if email:
            if IsEmailValid(email=email):
                try:
                    user = User.objects.get(email=email)
                    if SendToken(user=user, message='密码重置'):
                        return Response('验证已发送，请登录邮箱查看', status=status.HTTP_200_OK)
                    return Response('验证请求频繁，请稍候再试', status=status.HTTP_400_BAD_REQUEST)
                except User.DoesNotExist:
                    return Response('帐号不存在', status=status.HTTP_400_BAD_REQUEST)
            return Response('email格式不正确', status=status.HTTP_400_BAD_REQUEST)
        return Response('参数缺失', status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        last_name = request.data.get('last_name')
        try:
            user = User.objects.get(email=email)
            if user.is_active:
                if last_name == user.last_name:
                    delta = datetime.datetime.now().timestamp() - user.last_login.timestamp()
                    if delta < 600:
                        user.set_password(password)
                        user.save()
                        return Response('密码已重置', status=status.HTTP_200_OK)
                    else:
                        return Response('验证码失效', status=status.HTTP_400_BAD_REQUEST)
                return Response('验证码错误', status=status.HTTP_400_BAD_REQUEST)
            return Response('帐号不存在', status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response('帐号不存在', status=status.HTTP_400_BAD_REQUEST)


from news.models import Apps
from news.serializers import AppsSerializer


class AppsList(generics.ListAPIView):
    # 注意！！ 这里的切片方式！ 不要直接用objects.all[0]
    queryset = Apps.objects.all()[:1]
    serializer_class = AppsSerializer

    # def get(self, request, *args, **kwargs):
    #     lastApp = Apps.objects.all()[0]
    #     print(lastApp)
    #     return Response(serializers., status=status.HTTP_200_OK)
    # return self.list(request, *args, **kwargs)


def page_not_found(request):
    return render_to_response('404.html', status=status.HTTP_404_NOT_FOUND)
