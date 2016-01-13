from django.db import models

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
    isDomain =  models.BooleanField()

#Options for the parent to customize some of the monitoring features
class Data_Options(models.Model):
    Monitoring_Feature = (
        ('App', 'Installed Apps'),
        ('Phone', 'Logged Phone Calls'),
        ('Text', 'SMS/MMS'),
        ('Pics', 'Photo Messaging'),
        ('Web', 'Web History'),
    )
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

class Phone_Calls(models.Model):
    number = models.IntegerField()
    convoTime = models.IntegerField()
    Date = models.DateTimeField()

class Texts(models.Model):
    number = models.IntegerField()
    Date = models.DateTimeField()

class Photo_Messages(models.Model):
    number = models.IntegerField()
    Date = models.DateTimeField()

class Web_History(models.Model):
    site = models.CharField(max_length=100)
    rating = models.IntegerField(null=True)
    Date = models.DateTimeField()

class Social_Media(models.Model):
    socialActivity =(
        ('inPost','Inbound Post'),
        ('outPost','Outbound Post'),
        ('msg','Text Messages'),
        ('tag','Tagged'),
        ('friends','Friend Requests'),
    )
    date = Date = models.DateTimeField()

class Total(models.Model):
    totalApps = models.IntegerField()
    totalPhoneCalls = models.IntegerField()
    totalTexts = models.IntegerField()
    totalPhotos = models.IntegerField()
    totalSites = models.IntegerField()
