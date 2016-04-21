from googleapiclient import discovery
import httplib2
import json
import random
from string import digits, ascii_uppercase, ascii_lowercase
import datetime, calendar, string
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
from rest_framework.serializers import ModelSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from serializers import *
from models import *
from rest_framework import generics
from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from gcm import *
import re
import os
from forms import *
from django.http import HttpResponseRedirect
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from rest_framework_bulk import ListBulkCreateUpdateDestroyAPIView
from apiclient import discovery
from django.utils import timezone
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
import logging

DATUM_KEY = "dc648e604c7cc671609af14835c73152"
_42MATTERS_URL = "https://42matters.com/api/1/apps/query.json?access_token=538cc092cf6325f0c0c6d9ab27ead07c759a82b3"
TEXT_ANALYZER_URL = "http://api.datumbox.com/1.0/TwitterSentimentAnalysis.json"
TEXT_EXTRACTION_URL = "http://api.datumbox.com/1.0/TextExtraction.json"
CATEGORY_URL = "http://api.datumbox.com/1.0/TopicClassification.json"
GCM_KEY = "AIzaSyDnYlTUqmET3vg4zUbuLHhOX6HW-6cQ2EE"
CLIENT_SECRET_FILE = str(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + "/client_secret.json"
CD9_APP_SECRET = "87b2da14fffc70104a079c7598230b82"
CD9_APP_ID = "193476894336866"
FB_TOKEN_EXTENDER_URL = "https://graph.facebook.com/oauth/access_token"
FB_USER_NEWSFEED = "https://graph.facebook.com/me/feed"
FB_ME = "https://graph.facebook.com/me"
FB_GRAPH = "https://graph.facebook.com/"

C_TEXTS = 0
C_APPS = 1
C_WEBSITES = 2
C_NUMBER = 3
C_FB = 4
C_EMAIL = 5

C_Arts = 0
C_Business= 1
C_Computers = 2
C_Health = 3
C_Home =4
C_News = 5
C_Recreation = 6
C_Reference = 7
C_Science = 8
C_Shopping = 9
C_Society = 10
C_Sports = 11

triggerWord = models.CharField(max_length=100)
dataType = models.IntegerField(default=6)
owner = models.ForeignKey('auth.User', related_name='Flags')

def create_flag(triggerWord, dataType, owner):
    flag = Flags(triggerWord=triggerWord, dataType=dataType, owner=owner)
    flag.save()

def test(request):
    user = request.user
    parent_profile = user.User
    if(request.method == "POST"):
        form = SocialMediaForm(request.POST)
        if (form.is_valid()):
            #THIS IS WHERE THERE WILL NEED TO BE A SWITCH TO ROUTE TO THE CORRECT FORM
            data = form.cleaned_data
            print data.keys()
            print data.values()
            #website alert
            if (data.get("form_type") == 1):
                create_flag(data.get("triggerWord"), data.get("form_type"), user)
                if(data.get("active") == "select1") :
                    parent_profile.websites_active_monitoring = True
                else:
                    parent_profile.websites_active_monitoring = False
                parent_profile.save()

            if (data.get("form_type") == 2):
                create_flag(data.get("triggerWord"), data.get("form_type"), user)
                if(data.get("active") == "select1") :
                    parent_profile.apps_active_monitoring = True
                else:
                    parent_profile.apps_active_monitoring = False
                parent_profile.save()

            if (data.get("form_type") == 3):
                create_flag(data.get("triggerWord"), data.get("form_type"), user)
                if(data.get("active") == "select1") :
                    parent_profile.calls_active_monitoring = True
                else:
                    parent_profile.calls_active_monitoring = False
                parent_profile.save()

            if (data.get("form_type") == 4):
                create_flag(data.get("triggerWord"), data.get("form_type"), user)
                if(data.get("active") == "select1") :
                    parent_profile.numbers_active_monitoring = True
                else:
                    parent_profile.numbers_active_monitoring = False
                parent_profile.save()

            if (data.get("form_type") == 5):
                create_flag(data.get("triggerWord"), data.get("form_type"), user)
                if(data.get("active") == "select1") :
                    parent_profile.social_active_monitoring = True
                else:
                    parent_profile.social_active_monitoring = False
                parent_profile.save()

            return HttpResponse("yay")
        else:
            return HttpResponse("Invalid Selection !")
    else:
        texts_form = TextsForm()
        context_dict = {'texts_form': texts_form}
        context_dict['social_media_form'] = SocialMediaForm()
        context_dict['calls_form'] = CallsForm()
        context_dict['apps_form'] = AppsForm()
        context_dict['sites_form'] = SitesForm()
        return render(request, 'settings.html', context_dict)

def alert_overview(request, clear_id="null"):

    user = request.user
    is_teen = True
    if(user.User.isTeenager):
        teen = user.User
    else:
        teen = UserProfile.objects.filter(parent=user)[0]
        is_teen = False

    if(request.method == "POST"):
        teen_id = request.POST.get("teen_id")
        if(teen_id):
            print teen_id
            teen = UserProfile.objects.get(id=teen_id)
        elif(not clear_id=="null"):
            clear_teen = UserProfile.objects.get(id=clear_id)
            Alerts.objects.filter(teen=clear_teen).delete()

    context_dict = {'all_alerts': Alerts.objects.filter(teen=teen)}
    parent = teen.parent
    context_dict["parents_teens"] = UserProfile.objects.filter(parent=parent)
    context_dict["is_teen"] = is_teen
    context_dict["teen"] = teen
    return render(request, 'Alert_overview_table.html', context_dict)

def alert_processing(request, alert_id):
    user = request.user
    alert = Alerts.objects.get(id=alert_id)
    alert.isProcessed =True
    alert.save()
    print "the type is "
    print alert.type
    context_dict = {"name":request.user.username}
    context_dict["alert_count"] = 1
    return render(request, 'index.html', context_dict)



@login_required
def index(request, alert_id="null"):
    user = request.user
    is_teen = True
    if(user.User.isTeenager):
        teen = user.User
    else:
        teen = UserProfile.objects.filter(parent=user)[0]
        is_teen = False

    if(request.method == "POST"):
        print "the alert is " + alert_id
        if(not alert_id == "null"):
            alert = Alerts.objects.get(id=alert_id)
            alert.isProcessed = True
            alert.save()
        else:
            teen_id = request.POST.get("teen_id")
            if(teen_id):
                print teen_id
                teen = UserProfile.objects.get(id=teen_id)


    context_dict = addCalendar(teen)
    parent = teen.parent
    context_dict["parents_teens"] = UserProfile.objects.filter(parent=parent)
    context_dict["name"] = request.user.username
    sites = Web_History.objects.filter(owner = teen.user)
    alerts = Alerts.objects.filter(teen = teen)
    context_dict["sites"] = sites
    context_dict["alerts"] = alerts
    context_dict["is_teen"] = is_teen
    context_dict["alert_json"] = mark_safe(json.dumps(get_alert_json(alerts)))
    context_dict["web_json"] = mark_safe(json.dumps(get_web_json(sites)))
    context_dict["app_list"] = App_list.objects.filter(owner=teen.user)
    context_dict["teen"] = teen
    alert_list = Alerts.objects.filter(teen=teen, isProcessed=False)
    context_dict["alert_count"] = len(alert_list)
    if(context_dict["alert_count"] > 1):
        context_dict["alert_list"] = alert_list[1:]
        context_dict["first_alert"] = alert_list[:1][0]
    elif(context_dict["alert_count"] == 1) :
        context_dict["first_alert"] = alert_list[0]
        context_dict["alert_list"] = alert_list
    context_dict["alert_range"] = range(context_dict["alert_count"] + 1)[1:]

    context_dict["call_log_list"] = Phone_Calls.objects.filter(owner=teen.user)
    #print len(context_dict)
    log_list = context_dict["call_log_list"]


    #print len(log_list)

    #for i in context_dict["call_log_list"]:
        #if i.contact == "Unknown":
        #    print "this is null"
        #else:
            #print i.contact


    context_dict["text_list"] = Texts.objects.filter(owner=teen.user)
    context_dict["social_media_list"] = FbPosts.objects.filter(owner=teen.user)
    print "the social media list is "
    print context_dict["social_media_list"]
    context_dict["call_logs_list"] = Phone_Calls.objects.filter(owner=teen.user)

    text_list = context_dict["text_list"]
    social_media_list = context_dict["social_media_list"]
    call_logs_list = context_dict["call_logs_list"]

    #print len(text_list)

    # loop through the texts, if there is no associated contact, get the address
    context_dict["text_address_list_to"] = []
    context_dict["text_address_list_from"] = []

    addresses = []
    address_dict = {}
    myaddress = address(0,0,0,0,0,0,0)
    address_dict_from = {}

    # need address object

#parsing the text list
    for i in text_list:

        #print i.contact
        # if text is sent from teen
        if i.text_type == 2 or i.text_type == 5:
            myaddress = address(0,0,0,0,0,0,0)

            # if there is no name association with the text
            if i.contact is None:
                myaddress.name = str(i.number)
            else:
                myaddress.name = i.contact

            if myaddress.name in address_dict:
                address_dict[myaddress.name].to_text_count += 1
                if i.date > address_dict[myaddress.name].date:
                    address_dict[myaddress.name].date = i.date
            else:
                myaddress.to_text_count = 1
                myaddress.date = i.date
                address_dict[myaddress.name] = myaddress


        elif i.text_type == 1:
            myaddress = address(0,0,0,0,0,0,0)

            if i.contact is None:
                myaddress.name = str(i.number)
            else:
                myaddress.name = i.contact

            if myaddress.name in address_dict_from:
                address_dict_from[myaddress.name].from_text_count += 1
                if i.date > address_dict_from[myaddress.name].date:
                    address_dict_from[myaddress.name].date = i.date
            else:
                myaddress.from_text_count=1
                myaddress.date = i.date
                address_dict_from[myaddress.name] = myaddress

#parsing the social_media_list
    for i in social_media_list:
        print "++++++++++++++++++++++++++++++++++++++++"
        print "The username and the creator respectively are " + str(user.username) + str(i.creator)
        print "++++++++++++++++++++++++++++++++++++++++"
        # if Post is not sent from teen
        if user.username != i.creator:
            myaddress = address(0,0,0,0,0,0,0)

            # if there is no name association with the text
            myaddress.name = i.creator

            if myaddress.name in address_dict:
                address_dict[myaddress.name].to_social_count += 1
                if i.date_created > address_dict[myaddress.name].date:
                    address_dict[myaddress.name].date = i.date_created
            else:
                myaddress.to_social_count = 1
                myaddress.date = i.date_created
                address_dict[myaddress.name] = myaddress

#parsing the call_log list
    for i in call_logs_list:
        #print i.contact
        # if call is sent from teen
        if i.call_type == str(2):
            myaddress = address(0,0,0,0,0,0,0)

            # if there is no name association with the text
            if i.contact.lower() == "unknown":
                #print "this call is by unknown "
                myaddress.name = str(i.number)
            else:
                myaddress.name = i.contact

            if myaddress.name in address_dict:
                address_dict[myaddress.name].to_call_count += 1
                if i.date > address_dict[myaddress.name].date:
                    address_dict[myaddress.name].date = i.date
            else:
                myaddress.to_call_count = 1
                myaddress.date = i.date
                address_dict[myaddress.name] = myaddress

        elif i.call_type == str(1):
            myaddress = address(0,0,0,0,0,0,0)

            if i.contact.lower() == "unknown":
                myaddress.name = str(i.number)
            else:
                myaddress.name = i.contact

            if myaddress.name in address_dict_from:
                address_dict_from[myaddress.name].from_call_count += 1
                if i.date > address_dict_from[myaddress.name].date:
                    address_dict_from[myaddress.name].date = i.date
            else:
                myaddress.from_call_count=1
                myaddress.date = i.date
                address_dict_from[myaddress.name] = myaddress

    t_count = 0
    s_count = 0
    c_count = 0

    #print(len(addresses))
    context_dict["my_addresses"] = address_dict
    context_dict["my_from_addresses"] = address_dict_from

    for key, value in address_dict.iteritems():
        #print "the text count is " + str(value.to_text_count)
        #print "the social count is " + str(value.to_social_count)
        #print "the call count is " + str(value.to_call_count)

        # code for graph generation
        t_count += value.to_text_count
        s_count += value.to_social_count
        c_count += value.to_call_count


    context_dict["total_count"] = True
    if(t_count == 0 and s_count == 0 and c_count == 0):
        context_dict["total_count"] = False

    context_dict["interactions_to_json"] = mark_safe(json.dumps(make_interaction_pie(t_count, s_count, c_count)))

    #for key, value in address_dict_from.iteritems():
        #print "the text count is " + str(value.from_text_count)
        #print "the call count is " + str(value.from_call_count)

    #print address_dict_from.viewkeys()
    #print ""
    #print address_dict_from.viewvalues()
    print "##############################################"
    print "The dates are "
    print "##############################################"

    for key, value in address_dict.iteritems():
        value.date = str(value.date)
    for key, value in address_dict_from.iteritems():
        value.date = str(value.date)
    return render(request, 'index.html', context_dict)


def addCalendar(teen):
    currentDay = datetime.date.today().strftime("%d")
    year = int(datetime.date.today().strftime("%y"))
    monthNumber = datetime.date.today().strftime("%m")
    month = getMonthProperties(monthNumber,year)[2]
    nextAddress = "/CD9/Calendar/"+str((int(monthNumber) + 1))+"-"+str(year)
    prevAddress = "/CD9/Calendar/"+str(int(monthNumber) - 1)+"-"+str(year)
    fstDayOfMonth = int(calendar.monthrange(year,int(monthNumber))[0])
    secondWkSp = 7 - fstDayOfMonth
    daysInMonth = calendar.monthrange(year,int(monthNumber))[1]
    UncutDaysInMonth = daysInMonth
    daysInMonth = range(daysInMonth+1)[secondWkSp:]
    startingPoints = [secondWkSp, secondWkSp+7, secondWkSp+14, secondWkSp+21]
    endingPoints = [secondWkSp+6, secondWkSp+13, secondWkSp+20, secondWkSp+27]
    actionUrl = "/CD9/Calendar/" + str(monthNumber) + "-" + str(year) +"/"
    context_dict = {'monthstr':month, 'yearstr':year, 'currentDay':int(currentDay), 'fstDayOfMonth':range(fstDayOfMonth+1), 'daysInMonth':daysInMonth}
    context_dict['leftOver'] = range(secondWkSp)[1:]
    context_dict['startingPoints'] = startingPoints
    context_dict['endingPoints'] = endingPoints
    context_dict['next'] = nextAddress
    context_dict['prev'] = prevAddress
    context_dict['actionUrl'] = actionUrl
    context_dict['month'] = monthNumber
    context_dict['year'] = year + 2000

    emo_scores = get_monthly_emo_scores(range(UncutDaysInMonth), context_dict['year'], monthNumber, teen.user)
    print emo_scores
    leftOver_list = []
    daysInMonth_list = []
    for day in context_dict['leftOver']:
        leftOver_list.append(dict(day=day, pic=emo_scores[day-1].get("pic")))
    for day in context_dict['daysInMonth']:
        daysInMonth_list.append(dict(day=day, pic=emo_scores[day-1].get("pic")))
    context_dict["daysInMonth_list"] = daysInMonth_list
    context_dict["leftOver_list"] = leftOver_list

    return context_dict

def login (request):
   return render(request, 'login.html')

def app_detail (request,app_id):
    app = App_list.objects.get(id=app_id)
    return render(request, 'app_detail.html', {"app":app})

#TEsting now, but will need to be dynamic, and allow the acknowledge button to only show if
#the instance is not already set true for is processed
def alert_details (request,alert_id):
        alert = Alerts.objects.get(id=alert_id)
        context_dict = {"alert":alert}
        return render(request, 'alert_details.html', context_dict)

def settings (request, triggerword_id=''):

    if(request.user.User.isTeenager):
        return HttpResponse("Unauthorized Access !")
    user = request.user
    parent_profile = user.User

    if(request.method == "POST"):
        form = SocialMediaForm(request.POST)
        if (form.is_valid()):
            #THIS IS WHERE THERE WILL NEED TO BE A SWITCH TO ROUTE TO THE CORRECT FORM
            data = form.cleaned_data
            print data.keys()
            print data.values()
            #website alert
            if (data.get("form_type") == 1):
                create_flag(data.get("triggerWord"), C_WEBSITES, user)
                if(data.get("active") == "select1") :
                    parent_profile.websites_active_monitoring = True
                else:
                    parent_profile.websites_active_monitoring = False
                parent_profile.save()

            if (data.get("form_type") == 2):
                create_flag(data.get("triggerWord"), C_APPS, user)
                if(data.get("active") == "select1") :
                    parent_profile.apps_active_monitoring = True
                else:
                    parent_profile.apps_active_monitoring = False
                parent_profile.save()

            if (data.get("form_type") == 3):
                create_flag(data.get("triggerWord"), C_NUMBER, user)
                if(data.get("active") == "select1") :
                    parent_profile.calls_active_monitoring = True
                else:
                    parent_profile.calls_active_monitoring = False
                parent_profile.save()

            if (data.get("form_type") == 4):
                create_flag(data.get("triggerWord"), C_TEXTS, user)
                if(data.get("active") == "select1") :
                    parent_profile.numbers_active_monitoring = True
                else:
                    parent_profile.numbers_active_monitoring = False
                parent_profile.save()

            if (data.get("form_type") == 5):
                create_flag(data.get("triggerWord"), C_FB, user)

                if(data.get("active") == "select1") :
                    parent_profile.social_active_monitoring = True
                else:
                    parent_profile.social_active_monitoring = False
                parent_profile.save()

        else:
            return HttpResponse("nooooo")

    if(triggerword_id):
        try:
            flag = Flags.objects.get(id = triggerword_id)
            flag.delete()
        except Exception as e:
            print e

    context_dict = {'texts_form': TextsForm()}
    context_dict['social_media_form'] = SocialMediaForm()
    context_dict['calls_form'] = CallsForm()
    context_dict['apps_form'] = AppsForm()
    context_dict['sites_form'] = SitesForm()
    context_dict['sites'] = Flags.objects.filter(owner=request.user, dataType=C_WEBSITES)
    context_dict['apps'] = Flags.objects.filter(owner=request.user, dataType=C_APPS)
    context_dict['numbers'] = Flags.objects.filter(owner=request.user, dataType=C_NUMBER)
    context_dict['texts'] = Flags.objects.filter(owner=request.user, dataType=C_TEXTS)
    context_dict['social_posts'] = Flags.objects.filter(owner=request.user, dataType=C_FB)
    return render(request, 'settings.html', context_dict)

@login_required
def user_logout(request):
    logout(request)
    return render(request, 'login.html')

def daniel (request):
   return render(request, 'dan_index.html')

def daniel2 (request):
   return render(request, 'danfile2.html')

def getAlertCount(alerts):
    alert_count = []
    for i in range(6):
        alert_count.append(0)
    for alert in alerts:
        i = 0
        for i in range(6):
             if(alert.type == i):
                 alert_count[i] += 1
                 break
             i += 1
    return alert_count

def getSiteCount(sites):
    categories = ["Arts", "Business & Economy", "Computers & Technology", "Health", "Home & Domestic Life",
    "News", "Recreation & Activities", "Reference & Education", "Science", "Shopping", "Society", "Sports"]
    site_count = []
    for i in range(12):
        site_count.append(0)
    for site in sites:
        i = 0
        for category in categories:
             if(site.category == category):
                 site_count[i] += 1
                 break
             i += 1
    return site_count

def make_web_pie(site_count):
    categories = ["Arts", "Business & Economy", "Computers & Technology", "Health", "Home & Domestic Life",
    "News", "Recreation & Activities", "Reference & Education", "Science", "Shopping", "Society", "Sports"]
    total_sites = sum(site_count)
    percentages = []
    colors = ["#0000FF", "#46BFBD", "BDB768", "9932CC", "8B0000", "00CED1", "#556B2F", "#46BFBD", "BDB768", "9932CC", "8B0000", "00CED1"]
    dictionaries = [dict(value = 0, color="", highlight="", label="") for x in range(12)]
    if(total_sites != 0):
        for i in range(12):
            percentages.append(int(round(site_count[i]/float(total_sites) * 100)))
        for i in range(12):
            dictionaries[i]["value"] = percentages[i]
            dictionaries[i]["color"] = "#46BFBD"
            dictionaries[i]["highlight"] = "#46BFBD"
            dictionaries[i]["label"] = categories[i]
    return dictionaries

def make_alert_pie(site_count):
    alerts = ["Texts", "Apps", "Websites", "Number", "Social Media", "Email"]
    colors = ["#0000FF", "#46BFBD", "BDB768", "9932CC", "8B0000", "00CED1", "#556B2F"]
    total_sites = sum(site_count)
    percentages = []
    dictionaries = [dict(value = 0, color="", highlight="", label="") for x in range(6)]
    if(total_sites != 0):
        for i in range(6):
            percentages.append(int(round(site_count[i]/float(total_sites) * 100)))
        for i in range(6):
            dictionaries[i]["value"] = percentages[i]
            dictionaries[i]["color"] = "#46BFBD"
            dictionaries[i]["highlight"] = "#46BFBD"
            dictionaries[i]["label"] = alerts[i]
    return dictionaries

def make_interaction_pie(text_count, social_media_count,call_count):
    alerts = ["Texts", "Social Media", "Calls"]
    colors = ["#0000FF", "#46BFBD", "BDB768"]
    percentages = []
    dictionaries = [dict(value = 0, color="", highlight="", label="") for x in range(3)]

    percentages.append(text_count)
    percentages.append(social_media_count)
    percentages.append(call_count)

    for i in range(3):
        dictionaries[i]["value"] = percentages[i]
        dictionaries[i]["color"] = "#46BFBD"
        dictionaries[i]["highlight"] = "#46BFBD"
        dictionaries[i]["label"] = alerts[i]
    return dictionaries

def get_web_json(list):
    site_count = getSiteCount(list)
    return make_web_pie(site_count)

def get_alert_json(list):
    site_count = getAlertCount(list)
    return make_alert_pie(site_count)

def createAlert(color, alert_string, icon, type, date_created, isProcessed, content, teen, from_who='', id=''):
    if(type == C_FB):
        alert = Alerts(color= color, alert_string=alert_string, icon=icon, type=type, date_created=timezone.now(), from_who=from_who, isProcessed=isProcessed, content=content, teen=teen, id=id)
    else:
        alert = Alerts(color= color, alert_string=alert_string, icon=icon, type=type, date_created=timezone.now(), from_who=from_who, isProcessed=isProcessed, content=content, teen=teen)
    try:
        alert.save()
    except Exception as e:
        print str(e)

def sendGcmAlert(userProfile, alert_message):
    gcm = GCM(GCM_KEY)
    parent_profile = userProfile.parent.User
    registration_ids = []
    ids = [userProfile.gcm_reg_id, parent_profile.gcm_reg_id]
    for id in ids:
        if(not id == "null"):
            registration_ids.append(id)
    notification = {'alert' : alert_message, 'name':userProfile.user.username}
    try:
       response = gcm.json_request(registration_ids=registration_ids,data=notification, delay_while_idle=False)
       print "the gcm response is " + str(response)
    except Exception as e:

       print e

def triggerCheck(dict):
#Make the data besides the apps get the data list from the function call
#so it is only checking the ones that are incoming in real time

    teenProf = dict.get("profile")
    print "Variable teeProf is " + str(teenProf)
    parent = teenProf.parent.User
    triggerType = dict.get("data_type", "nothing")
    print "the type is " + str(triggerType)
    data_set = dict.get("data_set")

    if(triggerType == C_APPS and parent.apps_active_monitoring ):
        apps = data_set
        trigger_list = Flags.objects.filter(owner=parent.user, dataType=C_APPS)
        for trigger in trigger_list:
            for app in apps:
                print "the app and the trigger word are " + str(app.appName) + " and " + str(trigger.triggerWord)

                triggerHit = re.search(trigger.triggerWord, app.appName, re.IGNORECASE)
                if(triggerHit):
                    sendGcmAlert(teenProf, "App Alert: Detected a app on the trigger list !")
                    alert = createAlert(color= "yellow", alert_string="App Alert !", icon="ion-social-android", type=C_APPS, date_created=timezone.now(),isProcessed=False, content=app.appName, teen=teenProf)

                    try:
                        alert.save()
                    except Exception as e:
                        print e
                    print "App Alert: Detected a app on the trigger list !"

    elif(triggerType == C_TEXTS ):
        #texts = dict.get("texts")
        texts = data_set
        trigger_list = Flags.objects.filter(owner=parent.user, dataType=C_TEXTS)
        print "the trigger list is " + str(trigger_list)
        print "the texts is " + str(texts)
        for trigger in trigger_list:
            for text in texts:
                print "++++++++++++++++++++++++++++++++++++++"
                print "the trigger word and the text respectively is " + str(trigger.triggerWord) + "" + str(text.content)
                print "++++++++++++++++++++++++++++++++++++++"
                triggerHit = re.search(trigger.triggerWord, text.content, re.IGNORECASE)
                if(triggerHit):

                    print "the trigger word is " + trigger.triggerWord
                    print "the text content is " + text.content
                    print "Text Alert: Detected a text with that contains a word from trigger list !"
                    sendGcmAlert(teenProf, "Text Alert: Detected a text with that contains a word from trigger list !")
                    alert = createAlert(color= "red", alert_string="Text Alert !", icon="ion-android-phone-portrait", type=C_TEXTS, from_who=text.number, date_created=timezone.now(), content=text.content, isProcessed=False, teen=teenProf)
		    try:
                       alert.save()
                    except Exception as e:
                       print e
        print " it got here and the dataset is " + str(data_set)

        trigger_list = Flags.objects.filter(owner=parent.user, dataType=C_NUMBER)
        for trigger in trigger_list:
            for number in texts:
                if( trigger.triggerWord.replace("-","") == str(number.number).replace("-", "")):
                    print "Text Alert: Detected a text from a number on the trigger list !"
                    sendGcmAlert(teenProf, "Text Alert: Detected a text from a number on the trigger list !")
                    alert = createAlert(color= "green", alert_string="Number Alert !", icon="ion-android-call", from_who=number.number, type=C_NUMBER, date_created=timezone.now(), content=text.number, isProcessed=False,  teen=teenProf)
		    try:
                       alert.save()
		    except Exception as e:
		       print e

    elif(triggerType == C_WEBSITES and parent.websites_active_monitoring ):
        websites = data_set
	print "the data set is " + str(data_set)
        trigger_list = Flags.objects.filter(owner=parent.user, dataType=C_WEBSITES)
	print "the trigger list is " + str(trigger_list)
        for trigger in trigger_list:
            for domain in websites:
                triggerHit = re.search(trigger.triggerWord, domain.site, re.IGNORECASE)
		print "the trigger word is " + trigger.triggerWord
                print "the text content is " + domain.site
                if(triggerHit):
                    print "Website Alert: Detected a visited site thats listed in trigger list !"
                    sendGcmAlert(teenProf, "Website Alert: Detected a visited site thats listed in trigger list !")
                    alert = createAlert(color= "blue", alert_string="Website Alert !", icon="ion-android-globe", type=C_WEBSITES, date_created=timezone.now(), content=domain.site, isProcessed=False, teen=teenProf)
		    try:
                       alert.save()
                    except Exception as e:
                       print e

    elif(triggerType == C_NUMBER and parent.numbers_active_monitoring  ):
        numbers = data_set
        trigger_list = Flags.objects.filter(owner=parent.user, dataType=C_NUMBER)
        for trigger in trigger_list:
            for number in numbers:
                #print "the number and the trigger word are " + str(number.number) + " and " + str(trigger.triggerWord)
                if( trigger.triggerWord.replace("-", "") == str(number.number).replace("-", "") ):
                    sendGcmAlert(teenProf, "Phone Call Alert: Detected a call from a number on the trigger list !")
                    alert = createAlert(color= "green", alert_string="Number Alert !", icon="ion-android-call", from_who=number.number, type=C_NUMBER, date_created=timezone.now(), content=text.number, isProcessed=False,  teen=teenProf)
		    try:
                       alert.save()
                    except Exception as e:
                       print e
                    print "Phone Call Alert: Detected a call from a number on the trigger list !"

"""
#Facebook data will not be analyzed here since it will not be sent from the phone
#it will be accessed and processed strictly from the server
    elif(triggerType == C_FB):
        #fb_posts = dict.get("fb_posts")
        fb_posts = FbPosts.objects.filter(owner=user)
        trigger_list = Flags.objects.filter(owner=user, dataType=C_FB)
        for trigger in trigger_list:
            for post in fb_posts:
                if(post.message):
                    triggerHit = re.search(trigger.triggerWord, post.message, re.IGNORECASE)
                    if(triggerHit):
                        print "Social Alert: Detected a Post with that contains a word from trigger list !"
                        sendGcmAlert(userProf, "Post Alert: Detected a Post with that contains a word from trigger list !")
"""

def getAppInfo(packageName):
    dict = {
              "query": {
                "_id": "56d1f962ea9e198b7963d678",
                "name": "",
                "platform": "android",
                "query_params": {
                  "sort": "number_ratings",
                  "from": 0,
                  "num": 100,
                  "i18n_lang": [],
                  "cat_int": [],
                  "content_rating": [],
                  "sort_order": "desc",
                  "downloads_lte": "",
                  "downloads_gte": "",
                  "full_text_term": "",
                  "title_exact_match": "true",
                  "include_full_text_desc": "true",
                  "package_name": [
                    packageName
                  ]
                },
                "user_id": "56d1f29ceb9e193d08855550"
              }
            }
    dict = json.dumps(dict)
    print str(dict)
    res = requests.post(_42MATTERS_URL, dict)
    try:
        result = res.json().get("results")[0]
        return result
    except Exception as e:
        print e
        print packageName
        print "There is no more api calls !!!"
        return {"successful" : False}

def fetchAndProcess(dict):
    data_set = dict.get("data_set", "nothing")
    data_type = dict.get("data_type")
    teenProfile = dict.get("profile")
    owner = None

    if(data_type == C_TEXTS):
        #ANALYZE TEXTS AND MARK PROCESSED TRUE
        for text in data_set:
            content = text.content
            resDict = analyzeText(str(content))
            text.emo_score = 0
            if(resDict.get("success") == True):
                print "it got to the api successfully"
                if(resDict.get("emo_score") == "negative"):
                    text.emo_score = -1
                elif(resDict.get("emo_score") == "positive"):
                    text.emo_score = 1
                text.isProcessed = True
                text.save()
        triggerCheck(dict)

    elif(data_type == C_APPS):
        for app in data_set:
            packageName = app.packageName
            appDict = getAppInfo(packageName)
            result = appDict.get("successful",True)
     	    app.isProcessed = True
            app.contentRating = appDict.get("content_rating", "N/A")
            app.appName  = appDict.get("title", "N/A")
            app.siteLink  = appDict.get("website", "N/A")
            app.description = appDict.get("description", "N/A")
            app.marketUrl = appDict.get("market_url", "N/A")
            #screenShot = appDict.get("screenshots", "nothing")[0]
            app.save()
        triggerCheck(dict)


    elif(data_type == C_WEBSITES):
        #ANALYZE_WEBSITES AND MARK PROCESSED TRUE
        for website in data_set:
            site = "http://"+website.site
            res = requests.get(site)
            reqDict = {"api_key":DATUM_KEY, "text":res.text}
            res = requests.post(TEXT_EXTRACTION_URL, reqDict)
            extractedText = res.json().get("output").get("result", "")
            reqDict["text"] = extractedText
	    res = requests.post(CATEGORY_URL, reqDict)
            website.category = res.json().get("output").get("result", "nothing")
            website.isProcessed = True
            website.save()
        triggerCheck(dict)

    elif(data_type == C_NUMBER):
        for number in data_set:
            number.isProcessed = True
            number.save()
        triggerCheck(dict)

class GetIds(generics.ListAPIView):

    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,BasicAuthentication)
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        user = self.request.user
        print user.User
        profile = user.User
        list = UserProfile.objects.filter(email=profile.email)
        print profile.user.email
        list2 = UserProfile.objects.filter(parent=user)
        qs = list | list2
        return qs



"""
Add a parent to a teenager profile

def AddParent(request):
    json_data = request.body
    dict = json.loads(json_data)
    username = dict.get("username")
    password = dict.get("password")
    if(username and password):
            #do work
    else:
            raise Http404("Client did not send either the password or the username.")
"""

"""
Utility function to make a quick secure password. More of a
dummy password since all the authentication is done via social
media
"""
def generatePassword():
    charset = digits + ascii_uppercase + ascii_lowercase
    return ''.join(random.choice(charset) for _ in range(50))

def generateId():
    return ''.join(random.choice(digits) for _ in range(15))

"""
Responsible for creating the django authentication token for
the validated user.
"""
def createToken(user):
    token = Token.objects.create(user=user)
    token_dictionaries = {"token" : token.key}
    return token_dictionaries

def getToken(request):
    json_data = request.body
    parsed_data = json.loads(json_data)
    return {"password" : parsed_data.get("password","Nothing"), "token" : parsed_data.get("token", "Nothing")}

def tokenVerifier(token):
    dict = {'fields' : 'name, email', 'access_token' : token}
    r = requests.get('https://graph.facebook.com/me', params=dict)
    parsed_data = json.loads(r.text)
    if (r.status_code == 200):
        return {"isVerified" : True, "facebook_dict" : parsed_data}
    else:
        return {"isVerified" : False}

"""
This is the view function that handles the request
to update the token. It also updates the long lived token so its good for another 60 days.
"""
@csrf_exempt
def TokenUpdater(request):
    token_dict = getToken(request)
    token = token_dict.get("token", "Nothing")
    verify_results = tokenVerifier(token)
    if(verify_results["isVerified"]):
        email = verify_results["facebook_dict"].get("email","Nothing")
        """
        This part may be revised if we find that there may be any
        security risks with only accepting the token as authenticating input
        """
        user_dict = getUser(email)
        if(user_dict.get("success") != True):
            raise Http404("email associated with this token is not valid.")
        user = user_dict.get("user")
        ext_token = internalExtendToken(token)
        res_dict = updateToken(user)
        if(ext_token.get("success")):
            user.fb_token = ext_token.get("token")
            user.save()
            res_dict.update({"success":True})
            return JsonResponse(res_dict)
        else:
            res_dict.update({"success":False})
            return JsonResponse(res_dict)
    else:
        raise Http404("There was an error in verifying the access token")

"""
This is the helper function for TokenUpdater
"""
def updateToken(user):

    token = Token.objects.get(user=user)
    token.delete()
    token = createToken(user=user)
    return token

def getUser(email):

    try:
        user = User.objects.get(email=email)

    except Exception as e:
        dict = {"success" : False}
        return dict

    dict = {"success" : True, "user" : user}
    return dict




"""
This is the helper function for TokenExtender. This is one of two
functions that extend a token, but this one is made to directly respond to a http client.
"""
def extendToken(token):
    verify_results = tokenVerifier(token)
    if(verify_results["isVerified"]):
        email = verify_results["facebook_dict"].get("email","Nothing")
        """
        This is where the authentication token will be used to retrieve the logged in users
        email so it can then be compared to the one received from facebook to ensure that the person
        whoe sent the token is the same as the one logged in
        """
        dict = {"client_id" : CD9_APP_ID, "client_secret" : CD9_APP_SECRET, "grant_type" : "fb_exchange_token", "fb_exchange_token" : token}
        response = requests.get(FB_TOKEN_EXTENDER_URL, params=dict)
        if(response.status_code == 200):
            token = response.text.split("=")[1].split("&")[0]
            """"
            This is where the token would be saved in the users database
            """
            user = UserProfile.objects.get(email=email)
            user.fb_token = token
            user.save()
            return HttpResponse("The token was successfully updated and saved !")
        else:
            raise Http404("There was an error while creating a long life token")
    else:
        raise Http404("There was an error while authenticating the token")

@csrf_exempt
def TokenExtender(request):
    token_dict = getToken(request)
    return extendToken(token_dict.get("token","Nothing"))

class UserList(generics.ListCreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

"""
This is the other token extending function that is used internally for other functions.
This one is only made to return a token that will later be saved in the function that calls this one.
"""
def internalExtendToken(token):
    verify_results = tokenVerifier(token)
    if(verify_results["isVerified"]):
        email = verify_results["facebook_dict"].get("email","Nothing")
        """
        This is where the authentication token will be used to retrieve the logged in users
        email so it can then be compared to the one received from facebook to ensure that the person
        whoe sent the token is the same as the one logged in
        """
        dict = {"client_id" : CD9_APP_ID, "client_secret" : CD9_APP_SECRET, "grant_type" : "fb_exchange_token", "fb_exchange_token" : token}
        response = requests.get(FB_TOKEN_EXTENDER_URL, params=dict)
        if(response.status_code == 200):
            token = response.text.split("=")[1].split("&")[0]
            return {"success" : True, "token" : token}
        else:
            return {"success" : False}

"""
reset the data back to now when done testing

In future enable logging in case of UNIQUE constraint errors

This is a hourly cronjob
"""
def getFbData(teens):

    for user_profile in teens:
        _user = user_profile.parent
        access_token = user_profile.fb_token
        x = requests.get(FB_ME, params={'access_token':access_token})
        if (x.status_code == 200):
            #Due to lack of current activity on my account makeing the date earlier, but after testing revert back to original today variable
            #today = str(datetime.date.today())
            dict = {"access_token":access_token,"since":"2014-04-20","limit":"1000"}
            response = requests.get(FB_USER_NEWSFEED,params=dict)
            res = response.json()
            data = res.get("data")
            #profile = UserProfile.objects.all()[0]
            user_name = str(user_profile.user)
            print data
            for i in range(len(data)):
                #save to the database first
                #then query the set and process only the ones that aren't processed
                id = data[i].get("id")
                name = getFrom(access_token, id)
                date = data[i].get("created_time")
                day = int(date.split("-")[2].split("T")[0])
                month = int(date.split("-")[1])
                year = int(date.split("-")[0])
                date = datetime.date(year,month,day)
                message = data[i].get("message")
                dict = analyzeText(str(message))
                score = 0
                trigger_list = Flags.objects.filter(owner=_user, dataType=C_FB)

                if(dict.get("success") == True and message and user_profile.parent.social_active_monitoring ):
                    #checking for Trigger words in the posts
                    for trigger in trigger_list:
                        print("The trigger word and the message respectively are " + str(trigger.triggerWord) + " "+ str(message))
                        triggerHit = re.search(trigger.triggerWord, message, re.IGNORECASE)
                        if(triggerHit):
                            print "Social Alert: Detected a Post with that contains a word from trigger list !"
                            sendGcmAlert(user_profile, "Post Alert: Detected a Post with that contains a word from trigger list !")
                            createAlert(color= "yellow", alert_string="Social Media Alert !", icon="ion-social-facebook", type=C_FB, date_created=timezone.now(),isProcessed=False, content=message, teen=user_profile, from_who=name, id=int(id.split('_',1)[0]))

                    #analyzing the post messages
                    if(dict.get("emo_score") == "negative"):
                        score = -1
                    elif(dict.get("emo_score") == "positive"):
                        score = 1

                try:
                    FbPosts.objects.update_or_create(creator=name, date_created=date, emo_score=int(score), id=str(id), owner=user_profile.user, message=message)
                except Exception as e:
                    print e.message
        else:
            sendGcmAlert(user_profile, "Warning: Facebook Token Update Needed !")

"""
def testgetFbData(user_profile):
    access_token = user_profile.fb_token
    now = timezone.now()
    dict = {"access_token":access_token,"since":"2015-1-1","limit":"1000"}
    response = requests.get(FB_USER_NEWSFEED,params=dict)
    res = response.json()
    data = res.get("data")
    profile = UserProfile.objects.all()[0]
    user_name = str(profile.user)
    for i in range(len(data)):
        id = data[i].get("id")
        name = getFrom(access_token, id)
        date = data[i].get("created_time")
        day = int(date.split("-")[2].split("T")[0])
        month = int(date.split("-")[1])
        year = int(date.split("-")[0])
        date = datetime.date(year,month,day)
        message = data[i].get("message")
        dict = analyzeText(str(message))
        if(dict.get("emo_score") == "negative"):
            score = -1
            print "this is working"
        elif(dict.get("emo_score") == "positive"):
            score = 1
            print "this is working"
        else:
            score = 0
"""

#android code is setup to access key name message
def sendGcmMsg(user_profile, message, alert_type=None):
    gcm = GCM("AIzaSyDnYlTUqmET3vg4zUbuLHhOX6HW-6cQ2EE")
    data = {'message': message, 'alert_type': alert_type}
    reg_id = user_profile.google_token
    gcm.plaintext_request(registration_id=reg_id, data=data)

def getFrom(access_token, id):
    dict = {"access_token":access_token, "fields" : "from"}
    response = requests.get(FB_GRAPH + id,params=dict)
    post = response.json()
    return post.get("from").get("name", "unknown")

def analyzeText(text):
    dict={"api_key":DATUM_KEY, "text":text}
    res = requests.post(TEXT_ANALYZER_URL,dict)
    if(res.status_code == 200):
        return {"success":True, "emo_score" : res.json().get("output").get("result")}
    else:
        return {"success":False}

class UserProfiles(generics.CreateAPIView):

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class UpdateUserProfile(generics.UpdateAPIView):

    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, BasicAuthentication)
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
#Will need to add functionality to make a user profile for
#the parent as well

class AddAnotherTeen(generics.UpdateAPIView):

    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, BasicAuthentication)
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def update(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        parent = UserProfile.objects.get(pk=pk)
        teenager = UserProfile.objects.get(email=self.request.user.email)
        teenager.parent = parent.user
        teenager.save()
        return HttpResponse("SUCCESSFUL")
        #super(AddAnotherTeen, self).update(request, *args, **kwargs)

class AddParent(generics.CreateAPIView):

    def perform_create(self, serializer):
        parent = serializer.save()
        parent.set_password(parent.password)
        parent.save()
        profile = UserProfile.objects.create(user=parent, email=parent.email, id=generateId())
        teenager = UserProfile.objects.get(email=self.request.user.email)
        teenager.parent = parent
        teenager.save()
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ping(generics.CreateAPIView):
    #Endpoint responsible for taking the pings from the users
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    queryset = Pings.objects.all()
    serializer_class = PingSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user, time=timezone.now(), hit=True)
        for ping in Pings.objects.filter(owner=self.request.user, hit=False):
            ping.delete()

def ping_checker(request):
        x = timezone.now()
        regx =  str(x).split(':', 1)[0]
        #Check if the teen pinged this hour, Then check if they have 3 or more
        #misses
        try:
            for teen in UserProfile.objects.filter(isTeenager=True):
                if(not Pings.objects.filter(time__regex=regx,owner=teen.user, hit=True)):
                        y = Pings(hit=False, owner=teen.user, time=timezone.now())
                        y.save()
                if(len(Pings.objects.filter(hit=False, owner=teen.user)) >= 3):
                    print "Potential App Bypass Warning ! :"
                    sendGcmAlert(teen, "Potential App Bypass Warning ! : The app has been unresponsive for the past three hours")
        except Exception as e:
            print e
        return HttpResponse("successfully checked pings for entire database !")

class Texts_View(generics.CreateAPIView):

    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        data_set = Texts.objects.filter(isProcessed=False)
        #dict = {'data_set' : data_set}
        #dict["data_type"] = C_TEXTS
        #dict["profile"] = self.request.user.User
        #print "the user profile at the api is " + str(self.request.user.User)
        #fetchAndProcess(dict)

    def get_serializer(self, *args, **kwargs):
        if "data" in kwargs:
            data = kwargs["data"]
            if isinstance(data, list):
                kwargs["many"] = True
        return super(Texts_View, self).get_serializer(*args, **kwargs)

    queryset = Texts.objects.all()
    serializer_class = TextSerializer


class Apps(generics.CreateAPIView):

    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        data_set = App_list.objects.filter(isProcessed=False)
        #dict = {'data_set' : data_set}
        #dict["data_type"] = C_APPS
        #dict["profile"] = self.request.user.User
        #fetchAndProcess(dict)

    def get_serializer(self, *args, **kwargs):
        if "data" in kwargs:
            data = kwargs["data"]
            if isinstance(data, list):
                kwargs["many"] = True
        return super(Apps, self).get_serializer(*args, **kwargs)

    queryset = App_list.objects.all()
    serializer_class = AppSerializer


class PhoneCall(generics.CreateAPIView):

    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        data_set = Phone_Calls.objects.filter(isProcessed=False)
        #dict = {'data_set' : data_set}
        #dict["data_type"] = C_NUMBER
        #dict["profile"] = self.request.user.User
        #fetchAndProcess(dict)

    def get_serializer(self, *args, **kwargs):
        if "data" in kwargs:
            data = kwargs["data"]
            if isinstance(data, list):
                kwargs["many"] = True
        return super(PhoneCall, self).get_serializer(*args, **kwargs)

    #When the authentication step is ready
    #permission_classes = (permissions.IsAuthenticated,)
    queryset = Phone_Calls.objects.all()
    serializer_class = PhoneCallSerializer

class PhotoMessages(generics.CreateAPIView):

    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    #When the authentication step is ready
    #permission_classes = (permissions.IsAuthenticated,)
    queryset = Photo_Messages.objects.all()
    serializer_class = PhotoMessagesSerializer

class WebHistory(generics.CreateAPIView):

    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        data_set = Web_History.objects.filter(isProcessed=False)
        #dict = {'data_set' : data_set}
        #dict["data_type"] = C_WEBSITES
        #dict["profile"] = self.request.user.User
        #fetchAndProcess(dict)

    def get_serializer(self, *args, **kwargs):
        if "data" in kwargs:
            data = kwargs["data"]
            if isinstance(data, list):
                kwargs["many"] = True
        return super(WebHistory, self).get_serializer(*args, **kwargs)

    queryset = Web_History.objects.all()
    serializer_class = WebHistorySerializer


#This needs to be turned into the token updater

@csrf_exempt
def tokenAuthenticator(request):
    json_data = request.body
    parsed_data = json.loads(json_data)
    token = parsed_data.get("token", "There was no token !")
    password = parsed_data.get("password", "")
    dict = {'fields' : 'name, email', 'access_token' : token}
    r = requests.get('https://graph.facebook.com/me', params=dict)
    parsed_data = json.loads(r.text)
    email = parsed_data.get("email","There was an error getting the email from the dictionaries")
    name = parsed_data.get("name","error error")
    first_name = name.split()[0]
    last_name = name.split()[1]
    #profile = UserProfile.objects.get_or_create(email=email)
    try:
        profile = User.objects.get(email=email)
    except:
        try:
            profile = User.objects.create(first_name=first_name,last_name=last_name,email=email,password=password)
            UserProfile.objects.create()
        except:
            return("Profile was not successfully created !")
    if (r.status_code == 200):

        return HttpResponse(str(parsed_data))
    else:
        return HttpResponse("There was an error with the facebook graph request.")

#This is the initial endpoint that all new user go through for account creation.
#Sends back the token for django authentication, and a flag letting the client
#know if the token was successfully extended or not.

@csrf_exempt
def CreateNewUser(request):
    token_dict = getToken(request)
    """
    **Current flow design does not require a password input from the client**
    password = token_dict.get("password","Nothing")
    """
    token = token_dict.get("token", "Nothing")
    if(token == "Nothing"):
        raise Http404("There was no token sent in the JSON Object.")
    else:
        print token
        verify_results = tokenVerifier(token)
        if(verify_results["isVerified"]):
            dict = verify_results["facebook_dict"]
            email = dict.get("email","")
            name = dict.get("name","")
            ext_token = internalExtendToken(token)
            try:
                password = generatePassword()
                id = generateId()
                user = User.objects.create(username=name,password=password, email=email)
                user.set_password(password)
                user.save()
                UserProfile.objects.create(user=user, email=email, isTeenager=True, id=id, fb_token=ext_token.get("token", token), update_needed=True)
            except Exception as e:
                error = e.message
                raise Http404("The profile was not successfully created. Error : " + error)
        else:
            raise Http404("There was an error in verifying the access token")
        res_dict = createToken(user)
        if(ext_token.get("success")):
            UserProfile.fb_token = ext_token.get("token")
            res_dict.update({"success": True})
        else:
            res_dict.update({"success": False})
        res_dict.update({"password":password})
        return JsonResponse(res_dict)

def makeCredentials(userProf):
    user = userProf.user
    flow = flow_from_clientsecrets(CLIENT_SECRET_FILE, 'https://www.googleapis.com/auth/gmail.readonly')
    flow.redirect_uri = "http://localhost"
    credentials = flow.step2_exchange(userProf.auth_code)
    credentials.id_token
    storage = Storage(CredentialsModel, 'id', user, 'credential')
    storage.put(credentials)

def callBack(request_id, response, exception):
    successful = True
    for msg in response.get("payload").get("headers"):

        if msg.get("name") == "From":
            from_ = msg.get("value")
            print msg.get("value")

        elif msg.get("name") == "Delivered-To":
            user_gmail = msg.get("value")
            print msg.get("value")

        elif msg.get("name") == "Message-ID":
            message_id = msg.get("value")
            print msg.get("value")

    try:
        userProf = UserProfile.objects.get(gmail=user_gmail)
    except Exception as e:
        print e
        successful = False

    if(successful):
            try:
                user = userProf.user
                gmail_record = Gmail(owner=user, _from=from_, date_created = datetime.date.today(), id = message_id)
                gmail_record.save()
            except Exception as e:
                print e
#put this back when done testing



def getGmail(teens):

    for userProf in teens:
        if(userProf.update_needed):
            makeCredentials(userProf)
            userProf.update_needed = False
            userProf.save()

        user = userProf.user
        date = datetime.datetime.today()
        query = date.strftime("%Y/%m/%d")
        storage = Storage(CredentialsModel, 'id', user, 'credential')
        credentials = storage.get()
        try:
            user_id = credentials.id_token.get("email")
            userProf.gmail = user_id
            userProf.save()
            print  "the users gmail is " + userProf.gmail
            http = credentials.authorize(httplib2.Http())
            service = discovery.build('gmail', 'v1', http=http)
            batch = service.new_batch_http_request()

            if(credentials.access_token_expired):
                credentials.refresh(httplib2.Http())
                userProf.refresh_token_uses += 1
                userProf.save()

            try:
                # Change the query back to the date
                message = service.users().messages().list(userId=user_id).execute()
                for msg_id in message.get("messages"):
                    batch.add(service.users().messages().get(userId = 'me', id = msg_id['id']), callback = callBack)
                    batch.execute()

            except Exception as e:
                print e.message
                sendGcmAlert(userProf, "Warning: Authorization Code Update Needed !")
                userProf.update_needed = True
                userProf.save()

        except Exception as e:
            print e

def processTexts(teens):

   for teen in teens:
      if teen.parent:
          texts = Texts.objects.filter(isProcessed=False, owner=teen.user)
          dict = {'data_set' : texts}
          dict["data_type"] = C_TEXTS
          dict["profile"] = teen
          fetchAndProcess(dict)

def processApps(teens):

   for teen in teens:
      if teen.parent:
          print "+++++++++++++++++++++++"
          print "the teen is " + str(teen)
          apps= App_list.objects.filter(isProcessed=False, owner=teen.user)
          dict = {'data_set' : apps}
          dict["data_type"] = C_APPS
          dict["profile"] = teen
          fetchAndProcess(dict)
   empties = [app for app in App_list.objects.all() if app.appName == None]
   for app in empties:
       app.delete()

def processSites(teens):

   for teen in teens:
      if teen.parent:
          sites = Web_History.objects.filter(isProcessed=False, owner=teen.user)
          dict = {'data_set' : sites }
          dict["data_type"] = C_WEBSITES
          dict["profile"] = teen
          fetchAndProcess(dict)

def processNumbers(teens):

   for teen in teens:
      if teen.parent:
          site= Phone_Calls.objects.filter(isProcessed=False, owner=teen.user)
          dict = {'data_set' : site}
          dict["data_type"] = 3
          dict["profile"] = teen
          fetchAndProcess(dict)

def getMonthProperties(monthNumber, year):
    monthNumber = int(monthNumber)
    if monthNumber == 1:
        fstDayAndNumOfDays = calendar.monthrange(year,int(monthNumber))
        month = "January"
        return fstDayAndNumOfDays + (month,)

    if monthNumber == 2:
        fstDayAndNumOfDays = calendar.monthrange(year,int(monthNumber))
        month = "Feburary"
        return fstDayAndNumOfDays + (month,)

    if monthNumber == 3:
        fstDayAndNumOfDays = calendar.monthrange(year,int(monthNumber))
        month = "March"
        return fstDayAndNumOfDays + (month,)

    if monthNumber == 4:
        fstDayAndNumOfDays = calendar.monthrange(year,int(monthNumber))
        month = "April"
        return fstDayAndNumOfDays + (month,)

    if monthNumber == 5:
        fstDayAndNumOfDays = calendar.monthrange(year,int(monthNumber))
        month = "May"
        return fstDayAndNumOfDays + (month,)

    if monthNumber == 6:
        fstDayAndNumOfDays = calendar.monthrange(year,int(monthNumber))
        month = "June"
        return fstDayAndNumOfDays + (month,)

    if monthNumber == 7:
        fstDayAndNumOfDays = calendar.monthrange(year,int(monthNumber))
        month = "July"
        return fstDayAndNumOfDays + (month,)

    if monthNumber == 8:
        fstDayAndNumOfDays = calendar.monthrange(year,int(monthNumber))
        month = "August"
        return fstDayAndNumOfDays + (month,)

    if monthNumber == 9:
        fstDayAndNumOfDays = calendar.monthrange(year,int(monthNumber))
        month = "September"
        return fstDayAndNumOfDays + (month,)

    if monthNumber == 10:
        fstDayAndNumOfDays = calendar.monthrange(year,int(monthNumber))
        month = "October"
        return fstDayAndNumOfDays + (month,)

    if monthNumber == 11:
        fstDayAndNumOfDays = calendar.monthrange(year,int(monthNumber))
        month = "November"
        return fstDayAndNumOfDays + (month,)

    if monthNumber == 12:
        fstDayAndNumOfDays = calendar.monthrange(year,int(monthNumber))
        month = "December"
        return fstDayAndNumOfDays + (month,)

    else:
        return "Undefined"

def calendar_np(request):
    currentDay = datetime.date.today().strftime("%d")
    year = int(datetime.date.today().strftime("%y"))
    monthNumber = datetime.date.today().strftime("%m")
    month = getMonthProperties(monthNumber,year)[2]
    nextAddress = "/CD9/Calendar/"+str((int(monthNumber) + 1))+"-"+str(year)
    prevAddress = "/CD9/Calendar/"+str(int(monthNumber) - 1)+"-"+str(year)
    fstDayOfMonth = int(calendar.monthrange(year,int(monthNumber))[0])
    secondWkSp = 7 - fstDayOfMonth
    daysInMonth = calendar.monthrange(year,int(monthNumber))[1]
    UncutDaysInMonth = daysInMonth
    daysInMonth = range(daysInMonth+1)[secondWkSp:]
    startingPoints = [secondWkSp, secondWkSp+7, secondWkSp+14, secondWkSp+21]
    endingPoints = [secondWkSp+6, secondWkSp+13, secondWkSp+20, secondWkSp+27]
    actionUrl = "/CD9/Calendar/" + str(monthNumber) + "-" + str(year) +"/"
    context_dict = {'monthstr':month, 'yearstr':year,'fstDayOfMonth':range(fstDayOfMonth+1), 'daysInMonth':daysInMonth}
    context_dict['leftOver'] = range(secondWkSp)[1:]
    context_dict['startingPoints'] = startingPoints
    context_dict['endingPoints'] = endingPoints
    context_dict['next'] = nextAddress
    context_dict['prev'] = prevAddress
    context_dict['actionUrl'] = actionUrl
    context_dict['month'] = monthNumber
    context_dict['currentDay'] = int(currentDay)
    context_dict['year'] = year + 2000
    user = request.user
    is_teen = True
    if(user.User.isTeenager):
        teen = user.User
    else:
        teen = UserProfile.objects.filter(parent=user)[0]
        is_teen = False

    emo_scores = get_monthly_emo_scores(range(UncutDaysInMonth), context_dict['year'], monthNumber, teen.user)
    print emo_scores
    leftOver_list = []
    daysInMonth_list = []
    for day in context_dict['leftOver']:
        leftOver_list.append(dict(day=day, pic=emo_scores[day-1].get("pic")))
    for day in context_dict['daysInMonth']:
        daysInMonth_list.append(dict(day=day, pic=emo_scores[day-1].get("pic")))
    context_dict["daysInMonth_list"] = daysInMonth_list
    context_dict["leftOver_list"] = leftOver_list

    context_dict["is_teen"] = emo_scores
    context_dict["emo_scores"] = is_teen
    return render(request, 'calendar.html', context_dict)

def get_monthly_emo_scores(daysinmonth, year, month, owner):

    monthly_emo = []
    date = str(year)+"-"+str(month)

    for i in daysinmonth:
        monthly_emo.append(0)
    print daysinmonth
    for i in daysinmonth:
        if(i < 10):
           daily_emo = Texts.objects.filter(owner=owner, date__contains=date+"-0"+str(i+1))
           fb_daily_emo = FbPosts.objects.filter(owner=owner, date_created__contains=date+"-0"+str(i+1))
        else:
           daily_emo = Texts.objects.filter(owner=owner, date__contains=date+"-"+str(i+1))
           fb_daily_emo = FbPosts.objects.filter(owner=owner, date_created__contains=date+"-"+str(i+1))

        for score in daily_emo:
           monthly_emo[i] += score.emo_score

        for score in fb_daily_emo:
           monthly_emo[i] += score.emo_score

    expressions = []
    for i in daysinmonth:
        if(monthly_emo[i] > 0 ):
           expressions.append(dict(score=monthly_emo[i], pic="/static/smiley.jpg/"))
        if(monthly_emo[i] == 0 ):
           expressions.append(dict(score=monthly_emo[i], pic="/static/neutral.jpg/"))
        if(monthly_emo[i] < 0 ):
           expressions.append(dict(score=monthly_emo[i], pic="/static/sad.jpg/"))
    return expressions

def calendar_wp(request, Date):
    monthNumber = int(string.split(Date, "-")[0])
    year = int(string.split(Date, "-")[1])
    if(monthNumber == 13):
        monthNumber = 1
        year += 1
    if(monthNumber == 0):
        monthNumber = 12
        year -= 1
    month = getMonthProperties(monthNumber,year)[2]
    nextAddress = "/CD9/Calendar/"+str((int(monthNumber) + 1))+"-"+str(year)
    prevAddress = "/CD9/Calendar/"+str(int(monthNumber) - 1)+"-"+str(year)
    fstDayOfMonth = int(calendar.monthrange(year,int(monthNumber))[0])
    secondWkSp = 7 - fstDayOfMonth
    daysInMonth = calendar.monthrange(year,int(monthNumber))[1]
    daysInMonth = range(daysInMonth+1)[secondWkSp:]
    startingPoints = [secondWkSp, secondWkSp+7, secondWkSp+14, secondWkSp+21]
    endingPoints = [secondWkSp+6, secondWkSp+13, secondWkSp+20, secondWkSp+27]
    actionUrl = "/CD9/Calendar/" + str(monthNumber) + "-" + str(year) +"/"
    context_dict = {'monthstr':month, 'yearstr':year, 'fstDayOfMonth':range(fstDayOfMonth+1), 'daysInMonth':daysInMonth}
    context_dict['leftOver'] = range(secondWkSp)[1:]
    context_dict['startingPoints'] = startingPoints
    context_dict['endingPoints'] = endingPoints
    context_dict['next'] = nextAddress
    context_dict['prev'] = prevAddress
    context_dict['actionUrl'] = actionUrl
    context_dict['month'] = monthNumber
    context_dict['year'] = year + 2000
    user = request.user
    is_teen = True
    if(user.User.isTeenager):
        teen = user.User
    else:
        teen = UserProfile.objects.filter(parent=user)[0]
        is_teen = False
    context_dict["is_teen"] = is_teen
    return render(request, 'calendar.html', context_dict)

def processAllData(request):

   teens = UserProfile.objects.filter(isTeenager=True)
   print "Data would be getting processed right now"
   #processTexts(teens)
   processApps(teens)
   processSites(teens)
   processNumbers(teens)
   getFbData(teens)
   #getGmail(teens)
   return HttpResponse('success')

def loginUser(request):
    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        print request.POST.viewkeys()
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
                # We use request.POST.get('<variable>') as opposed to request.POST['<variable>'],
                # because the request.POST.get('<variable>') returns None, if the value does not exist,
                # while the request.POST['<variable>'] will raise key error exception
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            print "this worked !"
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                auth_login(request, user)
                return HttpResponseRedirect('/CD9/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your CD9 account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionaries object...
        return render(request, 'login.html', {})

class address:
    def __init__(self, name, to_text_count, from_text_count, date, from_call_count, to_call_count, to_social_count):
        self.name = name
        self.to_text_count = to_text_count
        self.from_text_count = from_text_count
        self.date = date
        self.from_call_count = from_call_count
        self.to_call_count = to_call_count
        self.to_social_count = to_social_count

def total_interactions(request):

    user = request.user
    is_teen = True
    if(user.User.isTeenager):
        teen = user.User
    else:
        teen = UserProfile.objects.filter(parent=user)[0]
        is_teen = False

    if(request.method == "POST"):
        teen_id = request.POST.get("teen_id")
        if(teen_id):
            print teen_id
            teen = UserProfile.objects.get(id=teen_id)

    parent = teen.parent
    context_dict = {"name":request.user.username}
    context_dict["parents_teens"] = UserProfile.objects.filter(parent=parent)
    context_dict["teen"] = teen
    context_dict["call_log_list"] = Phone_Calls.objects.filter(owner=teen.user)
    context_dict["is_teen"] = is_teen
    #print len(context_dict)
    log_list = context_dict["call_log_list"]
    #print len(log_list)
    #for i in context_dict["call_log_list"]:
    #    if i.contact == "Unknown":
            #print "this is null"
    #    else:
            #print i.contact

    context_dict["text_list"] = Texts.objects.filter(owner=teen.user)
    text_list = context_dict["text_list"]
    print len(text_list)
    # loop through the texts, if there is no associated contact, get the address
    context_dict["text_address_list_to"] = []
    context_dict["text_address_list_from"] = []
    addresses = []
    address_dict = {}
    myaddress = address(0,0,0,0,0,0,0)
    address_dict_from = {}
    # need address object
    for i in text_list:

        # if text is sent from teen
        if i.text_type == 2 or i.text_type == 5:
            myaddress = address(0,0,0,0,0,0,0)
            # if there is no name association with the text
            if i.contact is None:
                myaddress.name = str(i.number)
            else:
                myaddress.name = i.contact

            if myaddress.name in address_dict:
                address_dict[myaddress.name].to_text_count += 1
            else:
                myaddress.to_text_count = 1
                address_dict[myaddress.name] = myaddress
                context_dict["text_address_list_to"].append(myaddress.name)

                myaddress = address(0,0,0,0,0,0,0)

        elif i.text_type == 1:
            myaddress = address(0,0,0,0,0,0,0)

            if i.contact is None:
                myaddress.name = str(i.number)
            else:
                myaddress.name = i.contact

            if myaddress.name in address_dict_from:
                address_dict_from[myaddress.name].from_text_count += 1
            else:
                myaddress.from_text_count=1
                address_dict_from[myaddress.name] = myaddress




    #print(len(addresses))
    context_dict["my_addresses"] = address_dict
    context_dict["my_from_addresses"] = address_dict_from
    #for key, value in address_dict.iteritems():
        #print value.name, value.to_text_count

    #print(len(context_dict["my_addresses"]))
    return render(request, 'total_interactions.html', context_dict)
