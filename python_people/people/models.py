# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.gis.db import models

from django.db.models.signals import post_save


SEXO_CHOICES = (
    (1, 'Male'),
    (2, 'Female'),
)


class PythonFrameWorks(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(null=True, blank=True )
    site_project = models.URLField()
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
        
#class Occupation(models,Model):
#    name = models.CharField(max_length=60)
    
     
class UserProfile(models.Model):
    """
    User Profile data
    """
    user = models.ForeignKey(User, unique=True)
    
    name = models.CharField(max_length=60 , blank=True, null=True )
    gender = models.SmallIntegerField(choices=SEXO_CHOICES, blank=True, null=True)
    
    point = models.PointField(srid=settings.SRID, blank=True, null=True)
    python_frameworks = models.ManyToManyField(PythonFrameWorks, blank=True, null=True, help_text="Select one or more choices")
    
    #google address format
    locality = models.CharField(max_length=60 , blank=True, null=True )
    administrative_area_level_1 = models.CharField(max_length=60 , blank=True, null=True )
    country = models.CharField(max_length=6 , blank=True, null=True )
        
    #occupation = models.ManyToManyField(Occupation) 
    #organization =  models.CharField(max_length=60 , blank=True, null=True )
    #organization_site = models.URLField()
    
    #blog = models.URLField(verify_exists=True, blank=True, null=True )
    #site = models.URLField(verify_exists=True, blank=True, null=True )
    #twitter = models.CharField(blank=True, null=True )

    #bio  = models.TextField( blank=True, null=True , blank=True, null=True )
    
    objects = models.GeoManager()
    
    
    def __unicode__(self):
        return self.user.username

def create_profile(sender, instance=None, **kwargs):
    if instance is None:
        return
    profile, created = UserProfile.objects.get_or_create(user=instance)


post_save.connect(create_profile, sender=User)

class PythonGroup(models.Model):
    
    name = models.CharField( max_length=60, blank=False, null=False )
    description = models.TextField( blank=True, null=True )
    site_url = models.URLField(verify_exists=True, blank=True, null=True )
    contact = models.EmailField( blank=False, null=False )
    mailing_list_url = models.URLField(verify_exists=True, blank=True, null=True )
    
    point = models.PointField( srid=settings.SRID, blank=False, null=False )
    #google address format
    locality = models.CharField( max_length=60 , blank=True, null=True )
    administrative_area_level_1 = models.CharField( max_length=60 , blank=True, null=True )
    country = models.CharField( max_length=6 , blank=False, null=False )
    
    date_add = models.DateField( auto_now_add=True )
    date_upd = models.DateField( auto_now=True )
    user = models.ForeignKey( User )
    
    objects = models.GeoManager()