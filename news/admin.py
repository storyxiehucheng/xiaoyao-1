from django.contrib import admin
from news import models


# Register your models here.
class NewsPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'id','newsType', 'tf', 'createdTime',)


admin.site.register(models.News, NewsPostAdmin)


# Register your models here.
class CommentsPostAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'createdTime',)


admin.site.register(models.Comments, CommentsPostAdmin)


class AppsPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'version', 'app', 'createdTime',)


admin.site.register(models.Apps, AppsPostAdmin)

# for my user class
# from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from news.models import MyUser


# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class EmployeeInline(admin.StackedInline):
    model = MyUser
    can_delete = False
    verbose_name_plural = 'myuser'


# Define a new User admin
class MyUserAdmin(UserAdmin):
    inlines = (EmployeeInline,)


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)
admin.site.register(models.Shows)