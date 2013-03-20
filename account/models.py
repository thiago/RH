# -- coding: utf-8 --
from django.conf import settings
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.sites.models import Site
from django.db import models
from django.db.models.signals import post_save

from sorl.thumbnail import ImageField, get_thumbnail

from .settings import ACCOUNT_DEFAULT_IMG_PROFILE, ACCOUNT_SIZES, ACCOUNT_SIZE_DEFAULT, ACCOUNT_ANONYMOUS_NAME

class UserProfile(models.Model):
	user 				= models.OneToOneField(User)
	sites 				= models.ManyToManyField(Site)
	picture				= ImageField(upload_to='account/profile', null=True, blank=True)
	biography			= models.TextField(null=True, blank=True)
	birth_date			= models.DateField(null=True, blank=True)

	def get_avatar(self, type=None):
		image_url			= ACCOUNT_DEFAULT_IMG_PROFILE if not self.picture else self.picture.file.name

		if ACCOUNT_SIZES.has_key(type):
			size				= 	ACCOUNT_SIZES[type]
		else:
			size				= 	ACCOUNT_SIZES[ACCOUNT_SIZE_DEFAULT] if ACCOUNT_SIZES.has_key(ACCOUNT_SIZE_DEFAULT) else ACCOUNT_SIZES[list(ACCOUNT_SIZES)[0]]
		size_string			= '%d' % size[0] if size[0] > 0 else ''
		size_string			+= 'x%d' % size[1] if size[1] > 0 else ''
		image				= get_thumbnail(image_url, size_string, crop='center').url
		return image

	@property
	def avatar(self):
		return self.get_avatar()

	@property
	def get_full_name(self):
		if self.user.is_anonymous():
			return ACCOUNT_ANONYMOUS_NAME
		return (u'%s %s' % (self.user.first_name, self.user.last_name)) if self.user.first_name else self.user.username

	def get_info(self, key=None):
		if not key:
			return self.information.all().order_by('order')
		data    = self.information.filter(label__key=key).order_by('order').values_list('value', flat=True)
		rtn     = []
		if key == 'email' and self.user.email:
			rtn.append(self.user.email)
		rtn.extend(data)
		return rtn

	def __unicode__(self):
		return self.user.__unicode__()

	def __str__(self):
		return self.get_full_name

	class Meta:
		ordering 				= ['id']
		verbose_name 			= 'Perfil'
		verbose_name_plural		= 'Perfis'

class UserInfoAttr(models.Model):
	label					= models.CharField(max_length=60)
	key						= models.SlugField(max_length=60)

	def __unicode__(self):
		return self.key

	def __str__(self):
		return self.label

	class Meta:
		ordering 				= ['label', 'key', 'id']
		verbose_name 			= 'Atributo'
		verbose_name_plural		= 'Atributos'

class UserInfo(models.Model):
	order					= models.IntegerField(default=0)
	label					= models.ForeignKey(UserInfoAttr, related_name='information')
	value					= models.CharField(max_length=255)
	user					= models.ForeignKey(UserProfile, related_name='information')

	def __unicode__(self):
		return self.label.__unicode__() + ': ' + self.value

	def __str__(self):
		return self.label.__str__() + ': ' + self.value

	class Meta:
		ordering 				= ['label', 'id']
		verbose_name 			= 'Informação'
		verbose_name_plural		= 'Informações'


def create_user_profile(sender, instance, created, **kwargs):
	if created:
		user		= UserProfile.objects.get_or_create(user=instance)[0]
		try:
			user.sites.add(Site.objects.get_current())
			user.save()
		except :
			pass

post_save.connect(create_user_profile, sender=User)
User.profile 		= property(lambda u: UserProfile.objects.get_or_create(user=u)[0])

AnonymousUser.username					= ACCOUNT_ANONYMOUS_NAME
AnonymousUser.get_full_name 			= ACCOUNT_ANONYMOUS_NAME
AnonymousUser.profile 					= UserProfile()