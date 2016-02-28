from django.db import models
from django.contrib.auth.models import User

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
    triggerWord = models.CharField(max_length=50)
    isDomain = models.BooleanField(default=False)
    owner = models.ForeignKey('auth.User', related_name='Flags')

#Options for the parent to customize some of the monitoring features
class Data_Options(models.Model):
    Monitoring_Feature = (
        ('App', 'Installed Apps'),
        ('Phone', 'Logged Phone Calls'),
        ('Text', 'SMS/MMS'),
        ('Pics', 'Photo Messaging'),
        ('Web', 'Web History'),
    )
    owner = models.ForeignKey('auth.User', related_name='Data_Options')
    Status = models.BooleanField(default=True)
#   Threshold is still optional at this time
#   Threshold = (
#        ('Low', 'Passive'),
#        ('Med', 'Moderate'),
#        ('High', 'Conservative'),
#    )

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
    #screenShot = models.CharField(max_length=200, null=True)

#Also see how feasible it is to include contact names for texts, calls, etc ...
class Phone_Calls(models.Model):
    number = models.IntegerField()
    convoTime = models.IntegerField()
    date = models.DateField()
    owner = models.ForeignKey('auth.User', related_name='Phone_Calls')

class Texts(models.Model):
    number = models.IntegerField()
    date = models.DateField()
    content = models.CharField(max_length=160, default='default_text')
    owner = models.ForeignKey('auth.User', related_name='Texts')
    emo_score = models.IntegerField(default=0)

class Photo_Messages(models.Model):
    number = models.IntegerField()
    date = models.DateField()
    owner = models.ForeignKey('auth.User', related_name='Photo_Messages')

class Web_History(models.Model):
    site = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    installDate = models.DateTimeField()
    owner = models.ForeignKey('auth.User', related_name='Web_History')

class Social_Media(models.Model):
    socialActivity =(
        ('inPost','Inbound Post'),
        ('outPost','Outbound Post'),
        ('msg','Text Messages'),
        ('tag','Tagged'),
        ('friends','Friend Requests'),
    )
    date = models.DateField()
    owner = models.ForeignKey('auth.User', related_name='Social_Media')

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
    parent = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='parent')
    isTeenager = models.BooleanField(default=False)
    fb_token = models.CharField(null=True, default='default_text', max_length=512)
    google_token = models.CharField(null=True, default='default_text', max_length=512)
    id = models.IntegerField(unique=True, primary_key=True)

    def __unicode__(self):
        return self.user.username

class FbPosts(models.Model):
    creator = models.CharField(default="unknown", max_length=50, )
    date_created = models.DateField(null=True)
    emo_score = models.IntegerField(default=0)
    trigger_hit = models.BooleanField(default=False)
    message = models.CharField(max_length=300, null=True)
    id = models.CharField(unique=True, primary_key=True, max_length=200)
