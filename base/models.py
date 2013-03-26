# -- coding: utf-8 --
from django.db import models
from django.db.models.signals import post_save
from django.contrib.sites.models import Site
from django.contrib.auth.models import User

class Department(models.Model):
    name = models.CharField(max_length=60)
    slug = models.SlugField(max_length=60)
    description = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']
        verbose_name = 'Departamento'
        verbose_name_plural = 'Departamentos'


class Role(models.Model):
    name = models.CharField(max_length=60)
    slug = models.SlugField(max_length=60)
    description = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']
        verbose_name = 'Cargo'
        verbose_name_plural = 'Cargos'


class ProfessionalProfile(models.Model):
    department = models.ForeignKey(Department)
    role = models.ForeignKey(Role)
    user = models.ForeignKey(User, related_name='professional_profile', unique=True)

    def user_profile(self):
        return self.user.profile.admin_display_related()

    user_profile.short_description = "Usuário"
    user_profile.allow_tags = True

    def __unicode__(self):
        return self.user.__unicode__()

    def __str__(self):
        return self.user.__str__()

    class Meta:
        ordering = ['id']
        verbose_name = 'Perfil Profissional'
        verbose_name_plural = 'Perfis Profissionais'


class Note(models.Model):
    profie = models.ForeignKey(
        ProfessionalProfile,
        related_name='notes')
    text = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_last_edited = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.text

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['id']
        verbose_name = 'Nota'
        verbose_name_plural = 'Notas'


#def create_user_profile(sender, instance, created, **kwargs):
#	if created:
#		user = ProfessionalProfile.objects.get_or_create(user=instance)[0]
#		try:
#			user.sites.add(Site.objects.get_current())
#			user.save()
#		except:
#			pass
#
#post_save.connect(create_user_profile, sender=User)
#User.profile = property(
#	lambda u: ProfessionalProfile.objects.get_or_create(
#		user=u)[
#	          0])