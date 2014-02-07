from django import forms
from django.contrib.auth.models import User
from django.db import models
import datetime
from django.utils.timezone import utc
from allauth.account.models import EmailAddress
from allauth.socialaccount.models import SocialAccount
from djangotoolbox.fields import ListField

now = datetime.datetime.utcnow().replace(tzinfo=utc)
DEADLINE_DEFAULT = now + datetime.timedelta(weeks=1)
import hashlib

# Create your models here.

DEFAULT_FINE_FOR_WORD = 1


class Person(models.Model):
    name = models.CharField(max_length=128)
    email = models.EmailField(null=True)

    def __unicode__(self):
        return unicode(self.name)


class PayPalUser(models.Model):
    person = models.ForeignKey('Person')
    pre_approval_key = models.TextField(null=True)

    def __unicode__(self):
        return unicode(self.person.name) + ' ' + unicode(self.pre_approval_key)


class Challenge(models.Model):
    id = models.AutoField(primary_key=True, db_column='ID')
    start_date = models.DateTimeField(auto_now=True)
    end_date = models.DateTimeField(default=DEADLINE_DEFAULT)
    name = models.CharField(max_length=128)
    participant = models.ManyToManyField('Person', related_name='challenges')
    word1 = models.CharField(max_length=64, null=True, blank=True)
    word2 = models.CharField(max_length=64, null=True, blank=True)
    word3 = models.CharField(max_length=64, null=True, blank=True)


    def __unicode__(self):
        return unicode(self.name)


class Jar(models.Model):
    challenge = models.ForeignKey('Challenge', related_name='jar')
    current_sum = models.FloatField(default=0)

    def __unicode__(self):
        return unicode(self.challenge.name)+'_jar'


class ChargeEvent(models.Model):
    jar = models.ForeignKey('Jar')
    date_of_felony = models.DateTimeField(auto_now=True)
    felon = models.ForeignKey('Person')
    crime = models.CharField(max_length=128)
    evidence = models.URLField()

    def __unicode__(self):
        return unicode(self.felon) + \
               " " + unicode(self.crime) + \
               " " + unicode(self.date_of_felony)

class Word(models.Model):
    challenge = models.ForeignKey('Challenge')
    name = models.CharField(max_length=128, null=False)
    fine = models.IntegerField(default=DEFAULT_FINE_FOR_WORD)

    def __unicode__(self):
        return unicode(self.name)

    class Meta:
        unique_together = ('name', 'challenge')


class UserProfile(models.Model):
    id = models.AutoField(primary_key=True, db_column='ID')
    user = models.OneToOneField(User, related_name='profile')
    about_me = models.TextField(null=True, blank=True)
    person = models.ForeignKey('Person', null=True, related_name='profile')
    username = models.CharField(max_length=128)

    def __unicode__(self):
        return "{}'s profile".format(self.user.username)

    class Meta:
        db_table = 'user_profile'

    def profile_image_url(self):
        """
        Return the URL for the user's Facebook icon if the user is logged in via Facebook,
        otherwise return the user's Gravatar URL
        """
        fb_uid = SocialAccount.objects.filter(user_id=self.user.id, provider='facebook')



        if len(fb_uid):
            return "http://graph.beta.facebook.com/{}/picture?width=40&height=40".format(fb_uid[0].uid)

        return "http://www.gravatar.com/avatar/{}?s=40".format(
            hashlib.md5(self.user.email).hexdigest())

    def account_verified(self):
        """
        If the user is logged in and has verified hisser email address, return True,
        otherwise return False
        """
        if self.user.is_authenticated:
            result = EmailAddress.objects.filter(email=self.user.email)
            if len(result):
                return result[0].verified
        return False


User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])

