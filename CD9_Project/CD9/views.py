from googleapiclient import discovery
import httplib2
import json
import random
from string import digits, ascii_uppercase, ascii_lowercase
import datetime
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
from serializers import UserProfileSerializer, TextSerializer, AppSerializer, PhotoMessagesSerializer, \
    PhoneCallSerializer, WebHistorySerializer, UserSerializer
from models import *
from rest_framework import generics
from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from gcm import *
import re
import os
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from rest_framework_bulk import ListBulkCreateUpdateDestroyAPIView
from apiclient import discovery
from django.utils import timezone
import logging


DATUM_KEY = "dc648e604c7cc671609af14835c73152"
_42MATTERS_URL = "https://42matters.com/api/1/apps/query.json?access_token=1f7b56972f7786671c41c6ea5e2eb529ce001140"
TEXT_ANALYZER_URL = "http://api.datumbox.com/1.0/TwitterSentimentAnalysis.json"
TEXT_EXTRACTION_URL = "http://api.datumbox.com/1.0/TextExtraction.json"
CATEGORY_URL = "http://api.datumbox.com/1.0/TopicClassification.json"
GCM_KEY = "AIzaSyDnYlTUqmET3vg4zUbuLHhOX6HW-6cQ2EE"
CLIENT_SECRET_FILE = str(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + "/client_secret.json"
CD9_APP_SECRET = "87b2da14fffc70104a079c7598230b82"
CD9_APP_ID = "193476894336866"
FB_TOKEN_EXTENDER_URL = "https://graph.facebook.com/oauth/access_token"
FB_USER_NEWSFEED = "https://graph.facebook.com/me/feed"
FB_GRAPH = "https://graph.facebook.com/"
C_TEXTS = 0
C_APPS = 1
C_WEBSITES = 2
C_NUMBER = 3
C_FB = 4
C_EMAIL = 5


def index():
    print CLIENT_SECRET_FILE

def createAlert(type, date_created, isProcessed, content, parent, from_who=''):
    alert = Alerts(type=type, date_created=timezone.now(), from_who=from_who, isProcessed=isProcessed, content=content, parent=parent)
    alert.save()

def sendGcmAlert(userProfile, alert_message):
    gcm = GCM(GCM_KEY)
    registration_ids = [userProfile.gcm_reg_id]
    if(userProfile.gcm_reg_id != "null"):
        registration_ids = [userProfile.gcm_reg_id]
        notification = {'alert' : alert_message}
        try:
	   response = gcm.json_request(registration_ids=registration_ids,
	   data=notification,
	   delay_while_idle=False)
	except Exception as e:
	   print e

    else:
        print userProfile.email + "does not have a gcm registration id"

def triggerCheck(dict):
#Make the data besides the apps get the data list from the function call
#so it is only checking the ones that are incoming in real time

    teenProf = dict.get("profile")
    print "Variable teeProf is " + str(teenProf)
    parent = teenProf.parent.User
    triggerType = dict.get("data_type", "nothing")
    print "the type is " + str(triggerType)
    data_set = dict.get("data_set")

    if(triggerType == C_APPS):
        apps = data_set
        trigger_list = Flags.objects.filter(owner=parent.user, dataType=C_APPS)
        for trigger in trigger_list:
            for app in apps:
                print "the app and the trigger word are " + app.packageName + " and " + trigger.triggerWord
		triggerHit = re.search(trigger.triggerWord, app.packageName, re.IGNORECASE)
                if(triggerHit):
                    sendGcmAlert(parent, "App Alert: Detected a app on the trigger list !")
                    alert = createAlert(type=C_APPS, date_created=datetime.datetime.now(),isProcessed=False, content=app.appName, parent=parent.user)
		    try:
                       alert.save()
                    except Exception as e:
		       print e
                    print "App Alert: Detected a app on the trigger list !"

    elif(triggerType == C_TEXTS):
        #texts = dict.get("texts")
        texts = data_set
        trigger_list = Flags.objects.filter(owner=parent.user, dataType=C_TEXTS)
        for trigger in trigger_list:
            for text in texts:
                triggerHit = re.search(trigger.triggerWord, text.content, re.IGNORECASE)
                if(triggerHit):
		    print "the trigger word is " + trigger.triggerWord
                    print "the text content is " + text.content
                    print "Text Alert: Detected a text with that contains a word from trigger list !"
                    sendGcmAlert(parent, "Text Alert: Detected a text with that contains a word from trigger list !")
                    alert = createAlert(type=C_TEXTS, from_who=text.number, date_created=datetime.datetime.now(), content=text.content, isProcessed=False, parent=parent.user)
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
                    sendGcmAlert(userProf, "Text Alert: Detected a text from a number on the trigger list !")
                    alert = createAlert(from_who=number.number, type=C_NUMBER, date_created=datetime.datetime.now(), content=text.number, isProcessed=False,  parent=parent.user)
		    try:
                       alert.save()
		    except Exception as e:
		       print e
		
    elif(triggerType == C_WEBSITES):
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
                    sendGcmAlert(parent, "Website Alert: Detected a visited site thats listed in trigger list !")
                    alert = createAlert(type=C_WEBSITES, date_created=datetime.datetime.now(), content=domain.site, isProcessed=False, parent=parent.user)
		    try:
                       alert.save()
                    except Exception as e:
                       print e

    elif(triggerType == C_NUMBER):
        numbers = data_set
        trigger_list = Flags.objects.filter(owner=parent.user, dataType=C_NUMBER)
        for trigger in trigger_list:
            for number in numbers:
                #print "the number and the trigger word are " + str(number.number) + " and " + str(trigger.triggerWord)
                if( trigger.triggerWord.replace("-", "") == str(number.number).replace("-", "") ):
                    sendGcmAlert(parent, "Phone Call Alert: Detected a call from a number on the trigger list !")
                    alert = createAlert(type=C_NUMBER,from_who=number.number, date_created=datetime.datetime.now(), content=number.number, isProcessed=False, parent=parent.user)
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
    res = requests.post(_42MATTERS_URL, dict)
    try:
        result = res.json().get("results")[0] 
        return result
    except Exception as e:
        print e
        print packageName
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
            if(result):
              app.content_rating = appDict.get("content_rating", "nothing")
              app.appName  = appDict.get("title", "nothing")
              app.siteLink  = appDict.get("website", "nothing")
              app.description = appDict.get("description", "nothing")
              app.marketUrl = appDict.get("market_url", "nothing")
              #screenShot = appDict.get("screenshots", "nothing")[0]
              app.isProcessed = True
              triggerCheck(dict)
	    app.save()   
 
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
    authentication_classes = (TokenAuthentication,)
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        user = self.request.user
        profile = UserProfile.objects.get(email=user.email)
        list = UserProfile.objects.filter(email=profile.email)
        print profile.parent.email
        list2 = UserProfile.objects.filter(email=profile.parent.email)
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
    token_dictionary = {"token" : token.key}
    return token_dictionary

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
This function will need to be retouched once we implement trigger checks &
emotional analysis to include that score in the model creation

reset the data back to now when done testing

In future enable logging in case of UNIQUE constraint errors

This is a hourly cronjob
"""
def getFbData(user_profile):
    _user = user_profile.user
    access_token = user_profile.fb_token
    now = datetime.datetime.now()
    dict = {"access_token":access_token,"since":"2014-03-16","limit":"1000"}
    response = requests.get(FB_USER_NEWSFEED,params=dict)
    res = response.json()
    data = res.get("data")
    #profile = UserProfile.objects.all()[0]
    user_name = str(user_profile.user)

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
        score = 0
        trigger_list = Flags.objects.filter(owner=_user, dataType=C_FB)

        if(dict.get("success") == True and message):
            #checking for Trigger words in the posts
            for trigger in trigger_list:
                #print("The trigger word and the message respectively are " + str(trigger.triggerWord) + str(message))
                triggerHit = re.search(trigger.triggerWord, message, re.IGNORECASE)
                if(triggerHit):
                    #print "Social Alert: Detected a Post with that contains a word from trigger list !"
                    sendGcmAlert(user_profile, "Post Alert: Detected a Post with that contains a word from trigger list !")
                    alert = createAlert(type=C_FB, date_created=datetime.datetime.now(), content=message, parent=user_profile.parent)
                    alert.save()

            #analyzing the post messages
            if(dict.get("emo_score") == "negative"):
                score = -1
            elif(dict.get("emo_score") == "positive"):
                score = 1

        try:
            FbPosts.objects.update_or_create(creator=name, date_created=date, emo_score=int(score), id=str(id), owner=_user, message=message)
        except Exception as e:
            print e.message
"""
def testgetFbData(user_profile):
    access_token = user_profile.fb_token
    now = datetime.datetime.now()
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


@csrf_exempt
def test(request):
    return HttpResponse(request.user)

class UserProfiles(generics.CreateAPIView):

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class UpdateUserProfile(generics.UpdateAPIView):

    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

#Will need to add functionality to make a user profile for
#the parent as well

class AddParent(generics.CreateAPIView):

    def perform_create(self, serializer):
        parent = serializer.save()
        profile = UserProfile.objects.create(user=parent, email=parent.email, id=generateId())
        teenager = UserProfile.objects.get(email=self.request.user.email)
        teenager.parent = parent
        teenager.save()
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    queryset = User.objects.all()
    serializer_class = UserSerializer


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
    email = parsed_data.get("email","There was an error getting the email from the dictionary")
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
                UserProfile.objects.create(user=user, email=email, isTeenager=True, id=id, fb_token=ext_token.get("token", token))
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
            user = userProf.user
            gmail_record = Gmail(owner=user, _from=from_, date_created = datetime.date.today(), id = message_id)
            gmail_record.save()




#put this back when done testing


def getGmail(userProf):

    if(userProf.update_needed):
        makeCredentials(userProf)
        userProf.update_needed = False
    
    user = userProf.user
    date = datetime.datetime.today()
    query = date.strftime("%Y/%m/%d")
    storage = Storage(CredentialsModel, 'id', user, 'credential')
    credentials = storage.get()
    user_id = credentials.id_token.get("email")
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)
    batch = service.new_batch_http_request()

    if(credentials.access_token_expired):
        credentials.refresh(httplib2.Http())
        userProf.refresh_token_uses += 1

    try:
        # Change the query back to the date
        message = service.users().messages().list(userId=user_id,q=query).execute()

        for msg_id in message.get("messages"):
            batch.add(service.users().messages().get(userId = 'me', id = msg_id['id']), callback = callBack)
            batch.execute()

    except Exception as e:
        print e
        sendGcmAlert(userProf, "Warning: Authorization Code Update Needed !")
        userProf.update_needed = True

def processTexts():
   
   for teen in teens:
      texts = Texts.objects.filter(isProcessed=False, owner=teen.user)
      dict = {'data_set' : texts}
      dict["data_type"] = C_TEXTS
      dict["profile"] = teen
      fetchAndProcess(dict)

def processApps():
   
   for teen in teens:
      apps= App_list.objects.filter(isProcessed=False, owner=teen.user)
      dict = {'data_set' : apps}
      dict["data_type"] = C_APPS
      dict["profile"] = teen
      fetchAndProcess(dict)

def processSites():

   for teen in teens:
      sites = Web_History.objects.filter(isProcessed=False, owner=teen.user)
      dict = {'data_set' : sites }
      dict["data_type"] = C_WEBSITES
      dict["profile"] = teen
      fetchAndProcess(dict)

def processNumbers():
  
   for teen in teens:
      site= Phone_Calls.objects.filter(isProcessed=False, owner=teen.user)
      dict = {'data_set' : site}
      dict["data_type"] = 3
      dict["profile"] = teen
      fetchAndProcess(dict)

def processAllData(request):

   print "Data would be getting processed right now"
   processTexts()
   processApps()
   processSites()
   processNumbers()
   return HttpResponse('success') 
