from django.contrib import admin
from django.contrib.admin import site
from sorl.thumbnail.admin import AdminImageMixin
from .models import *

class UserInfoInline(admin.TabularInline):
	model 		= UserInfo
	extra		= 2

class UserProfileAdmin(AdminImageMixin, admin.ModelAdmin):
	inlines 	= [
		UserInfoInline,
	]

class UserInfoAttrAdmin(admin.ModelAdmin):
	prepopulated_fields		= {"key": ("label",)}

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(UserInfoAttr, UserInfoAttrAdmin)