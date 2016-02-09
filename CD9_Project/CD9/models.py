from django.db import models
from django.contrib.auth.models import User


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

class App_list(models.Model):
    appName = models.CharField(max_length=50)
    installDate = models.DateTimeField()
    owner = models.ForeignKey('auth.User', related_name='App_list')


#Also see how feasible it is to include contact names for texts, calls, etc ...

class Phone_Calls(models.Model):
    number = models.IntegerField()
    convoTime = models.IntegerField()
    date = models.DateTimeField()
    owner = models.ForeignKey('auth.User', related_name='Phone_Calls')

class Texts(models.Model):
    number = models.IntegerField()
    date = models.DateTimeField()
    content = models.CharField(max_length=160, default='default_text')
    owner = models.ForeignKey('auth.User', related_name='Texts')

class Photo_Messages(models.Model):
    number = models.IntegerField()
    date = models.DateTimeField()
    owner = models.ForeignKey('auth.User', related_name='Photo_Messages')

class Web_History(models.Model):
    site = models.CharField(max_length=100)
    rating = models.IntegerField(null=True)
    date = models.DateTimeField()
    owner = models.ForeignKey('auth.User', related_name='Web_History')

class Social_Media(models.Model):
    socialActivity =(
        ('inPost','Inbound Post'),
        ('outPost','Outbound Post'),
        ('msg','Text Messages'),
        ('tag','Tagged'),
        ('friends','Friend Requests'),
    )
    date = models.DateTimeField()
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

    def __unicode__(self):
        return self.user.username

