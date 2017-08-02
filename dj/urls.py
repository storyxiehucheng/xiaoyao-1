"""dj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from news import views
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf import settings
from django.conf.urls.static import static

# from rest_framework.authtoken import views as rviews
urlpatterns = [
                  url(r'^$', views.Index),
                  url(r'^admin/', admin.site.urls),
                  url(r'^register/$', views.UserRegister.as_view()),
                  url(r'^login/$', views.UserLogin.as_view()),
                  url(r'^reset/$', views.UserReset.as_view()),
                  # url(r'^reset/avatar/(?P<user>.+)$',views.UserAvatar.as_view()),
                  # url(r'^reset/avatar/$',views.UserAvatar.as_view()),
                  url(r'^news/$', views.NewsList.as_view()),
                  url(r'^news/(?P<pk>[0-9]+)/$', views.NewsShare.as_view()),
                  url(r'^news/(?P<pk>[0-9]+)/detail/$', views.NewsDetail.as_view()),
                  url(r'^news/(?P<pk>[0-9]+)/comments/$', views.NewsComments.as_view()),
                  url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')),
                  # url(r'^api-token-auth/', rviews.obtain_auth_token),
                  url(r'^update/$', views.AppsList.as_view()),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = format_suffix_patterns(urlpatterns)
handler404 = views.page_not_found
