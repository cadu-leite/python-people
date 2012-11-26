# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.gis.db import models


SEXO_CHOICES = (
    (1, 'Male'),
    (2, 'Female'),
)


class PythonFrameWorks(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(null=True, blank=True)
    site_project = models.URLField()

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class UserProfile(models.Model):
    """
    User Profile data
    """
    user = models.ForeignKey(User, unique=True)

    name = models.CharField(max_length=60, blank=True, null=True)
    gender = models.SmallIntegerField(choices=SEXO_CHOICES, blank=True, null=True)

    point = models.PointField(srid=settings.SRID, blank=True, null=True)
    python_frameworks = models.ManyToManyField(PythonFrameWorks, blank=True, null=True, help_text="Select one or more choices")

    #google address format
    locality = models.CharField(max_length=60, blank=True, null=True)
    administrative_area_level_1 = models.CharField(max_length=60, blank=True, null=True)
    country = models.CharField(max_length=6, blank=True, null=True)

    public_email = models.NullBooleanField('Public e-mail address ?', help_text="If 'yes', everyone may see your e-mail adress on your profile page.")

    bio = models.TextField()

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

    def get_absolute_url(self):
        return reverse('user-profile', args=[self.id])


class PythonGroup(models.Model):

    name = models.CharField(max_length=60, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    site_url = models.URLField(verify_exists=True, blank=True, null=True)
    contact = models.EmailField(blank=False, null=False)
    mailing_list_url = models.URLField(verify_exists=True, blank=True, null=True)

    point = models.PointField(srid=settings.SRID, blank=False, null=False)
    #google address format
    locality = models.CharField(max_length=60, blank=True, null=True)
    administrative_area_level_1 = models.CharField(max_length=60, blank=True, null=True)
    country = models.CharField(max_length=6, blank=False, null=False)

    date_add = models.DateField(auto_now_add=True)
    date_upd = models.DateField(auto_now=True)
    user = models.ForeignKey(User)

    objects = models.GeoManager()

    def __unicode__(self):
        return self.name

    def is_group_owner(self, user):
        '''return true if user is the owner or if it has no owner.'''
        return (self.user == user) or not self.user


class Survey(models.Model):
    choices_degree = (
        (1, "newbie"), (2, "novice"), (3, "apprentice"),  (4, "expert"), (5, "master")
        )

    choices_user_type = (
        (1, 'student'), (2, 'work as a developer'), (3, u'scientist / researcher'), (4, 'Other - (ex: geographer, lawyer ...)')
        )

    choices_main_context = (
        (1, "commercial"), (2, "academic / scientific research"), (3, "gov"), (4, "ngos"), (5, "help open source projects")
        )

    choices_main_environment = (
        (1, "web apps"), (2, "desktop apps"), (3, "scripts (server automation, small tools, plugins ...)"))

    choices_main_problem = (
        (1, u"as a glue language (ex: exchange data between applications, services ...)"),
        (2, u"financial tools"),
        (3, u"gis tools"),
        (4, u"graphical tools"),
        (5, u"IT Infrastructure (ex.:server automation, small tools)"),
        (6, u"just have fun programming"),
        (7, u"network tools"),
        (8, u"plugin"),
        (9, u"research"),
        (10, u"testing software"),
        (11, u"web applications development  - workflow process"),
        (12, u"web CMS"),
        (13, u"other"),
        )

    user = models.ManyToManyField(User)
    date_add = models.DateTimeField(u"Answers Date", auto_now_add=True)

    when_start = models.DateField(u"when do you start using python", null=True, blank=True)
    work = models.NullBooleanField(u"do you uses python at your work ?", null=True, blank=True)
    first = models.NullBooleanField(u"is python your first language ? not you like most, but you use most.", null=True, blank=True)
    degree = models.IntegerField(u"how much python do you know ? ", choices=choices_degree)
    why = models.TextField(u"Why python", null=True, blank=True)

    user_type = models.IntegerField(choices=choices_user_type, null=True, blank=True)
    user_type_description = models.CharField(u"Description", max_length=50, null=True, blank=True)

    context = models.IntegerField(u"main environment", choices=choices_main_context, null=True, blank=True)
    environment = models.IntegerField(u"main environment", choices=choices_main_environment, null=True, blank=True)

    problem = models.IntegerField(u"main environment", choices=choices_main_problem, null=True, blank=True)
    problem_description = models.CharField(u"Description", max_length=50, null=True, blank=True)

    def __unicode__(self):
        return self.date

    def is_survey_owner(self, user):
        '''return true if user is the owner or if it has no owner.
            to implement per user object check
        '''
        return (self.user == user) or not self.user
