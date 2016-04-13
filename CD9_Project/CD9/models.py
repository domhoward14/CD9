import datetime
from django.db import models
from django.contrib.auth.models import User
from django.db import models
from oauth2client.contrib.django_orm import CredentialsField, Storage

C_TEXTS = 0
C_APPS = 1
C_WEBSITES = 2
C_NUMBER = 3
C_FB = 4
C_EMAIL = 5
"""
update all of the models so that they are using the datetime field
instead of the date field
"""

#Making a prototye design of the database
#depending on what information is available via android
#Once the output for all monitoring features is documented and known we can
#more accurately define the classes for the input coming from the client

#TDL
#Make foreign keys for the users facebook
#Make a table for the parent
#When more research is done implement the emotional score table

#Class for parent to make custom alert triggers
#Currently made for the parents to be alerted from custom inputted
class Flags(models.Model):
    triggerWord = models.CharField(max_length=100)
    dataType = models.IntegerField(default=6)
    owner = models.ForeignKey('auth.User', related_name='Flags')

#may want to add screenshots when doing the web GUI
class App_list(models.Model):
    packageName = models.CharField(max_length=100)
    appName = models.CharField(max_length=200, null=True)
    contentRating = models.CharField(max_length=50, null=True)
    siteLink = models.CharField(max_length=200, null=True)
    marketUrl = models.CharField(max_length=200, null=True)
    description = models.CharField(max_length=1000, null=True)
    installDate = models.DateTimeField()
    owner = models.ForeignKey('auth.User', related_name='App_list')
    isProcessed = models.BooleanField(default=False)
    isAlert = models.BooleanField(default=False)
    active_monitoring = models.BooleanField(default=True)
    #screenShot = models.CharField(max_length=200, null=True)

#Also see how feasible it is to include contact names for texts, calls, etc ...
class Phone_Calls(models.Model):
    number = models.IntegerField()
    convoTime = models.IntegerField()
    date = models.DateTimeField()
    owner = models.ForeignKey('auth.User', related_name='Phone_Calls')
    isProcessed = models.BooleanField(default=False)
    contact = models.CharField(max_length=100, default="Unknown")
    call_type= models.CharField(max_length=5, default="0")
    active_monitoring = models.BooleanField(default=True)

class Texts(models.Model):
    number = models.IntegerField()
    date = models.DateTimeField()
    content = models.CharField(max_length=160, default='default_text')
    owner = models.ForeignKey('auth.User', related_name='Texts')
    emo_score = models.IntegerField(default=0)
    isProcessed = models.BooleanField(default=False)
    text_type = models.IntegerField(default=0)
    contact = models.CharField(max_length=100, null=True)
    active_monitoring = models.BooleanField(default=True)


class Photo_Messages(models.Model):
    number = models.IntegerField()
    date = models.DateTimeField()
    owner = models.ForeignKey('auth.User', related_name='Photo_Messages')

class Web_History(models.Model):
    site = models.CharField(max_length=1024)
    category = models.CharField(max_length=50)
    installDate = models.DateTimeField()
    owner = models.ForeignKey('auth.User', related_name='Web_History')
    isProcessed = models.BooleanField(default=False)
    title = models.CharField(max_length=1024)
    active_monitoring = models.BooleanField(default=True)

class Total(models.Model):
    totalApps = models.IntegerField()
    totalPhoneCalls = models.IntegerField()
    totalTexts = models.IntegerField()
    totalPhotos = models.IntegerField()
    totalSites = models.IntegerField()
    owner = models.ForeignKey('auth.User', related_name='Total')

class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='User')
    email = models.CharField(unique=True, max_length=100)
    gmail = models.CharField(unique=True, max_length=100, null=True)
    auth_code = models.CharField(null=True, max_length=512)
    parent = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='parent')
    isTeenager = models.BooleanField(default=False)
    fb_token = models.CharField(null=True, default='default_text', max_length=512)
    refresh_token_uses = models.IntegerField(default=1)
    update_needed = models.BooleanField(default=False)
    gcm_reg_id = models.CharField(default='null', max_length=512)
    id = models.IntegerField(unique=True, primary_key=True)

    def __unicode__(self):
        return self.user.username

class FbPosts(models.Model):
    owner = models.ForeignKey('auth.User', related_name='FbPosts')
    creator = models.CharField(default="unknown", max_length=50, )
    date_created = models.DateField(null=True)
    emo_score = models.IntegerField(default=0)
    trigger_hit = models.BooleanField(default=False)
    message = models.CharField(max_length=300, null=True)
    id = models.CharField(unique=True, primary_key=True, max_length=200)
    active_monitoring = models.BooleanField(default=True)

class Alerts(models.Model):
    type = models.IntegerField(default=10)
    date_created = models.DateTimeField(null=True)
    isProcessed = models.BooleanField(default=False)
    content = models.CharField(default="null", max_length=500, )
    parent = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner')
    from_who = models.CharField(default="null", max_length=50,)


class Gmail(models.Model):
    owner = models.ForeignKey('auth.User', related_name='GmailOwner')
    _from = models.CharField(default="unknown", max_length=50, )
    date_created = models.DateField(null=True)
    id = models.CharField(unique=True, primary_key=True, max_length=200)


class CredentialsModel(models.Model):
  id = models.ForeignKey(User, primary_key=True)
  credential = CredentialsField()

class Pings (models.Model):
  time = models.DateTimeField(default=datetime.datetime.now())
  hit = models.BooleanField(default=True)
  owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ping_owner')
