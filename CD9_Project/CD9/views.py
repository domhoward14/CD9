import json
import random
from string import digits, ascii_uppercase, ascii_lowercase
import datetime
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from serializers import UserProfileSerializer, TextSerializer, AppSerializer, PhotoMessagesSerializer, \
    PhoneCallSerializer, WebHistorySerializer, UserSerializer
from models import UserProfile, Texts, App_list, Phone_Calls, Photo_Messages, Web_History, FbPosts
from rest_framework import generics
from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from gcm import *
import logging

DATUM_KEY = "dc648e604c7cc671609af14835c73152"
TEXT_ANALYZER_URL = "http://api.datumbox.com/1.0/TwitterSentimentAnalysis.json"
GCM_KEY = "AIzaSyCdH4wLDGgv6PZKRb_pPWpoGwcL9itHCgc"
CD9_APP_SECRET = "87b2da14fffc70104a079c7598230b82"
CD9_APP_ID = "193476894336866"
FB_TOKEN_EXTENDER_URL = "https://graph.facebook.com/oauth/access_token"
FB_USER_NEWSFEED = "https://graph.facebook.com/me/feed"
FB_GRAPH = "https://graph.facebook.com/"

def index(request):
    return render(request,'index.html')

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
"""
Will need to add functionality to make a user profile for
the parent as well
"""
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


"""
class Texts(APIView):

    def post(self, request, format=None):
        serializer = TextSerializer(data=request.data)
"""

class TextsUpdate(generics.UpdateAPIView):

    """
    def update(self, request, *args, **kwargs):
        data = request.data
        text_instance = Texts.objects.get(pk=1)
        serializer = TextSerializer(text_instance, data=data, many=True)

        if serializer.is_valid():
            serializer.save()

        return Response(serializer.data)
    """
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    queryset = Texts.objects.all()
    serializer_class = TextSerializer

class Texts(generics.CreateAPIView):

    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    def perform_create(self, serializer):
        text = serializer.validated_data['content']
        dict = analyzeText(str(text))
        score = 0
        if(dict.get("success") == True):
            if(dict.get("emo_score") == "negative"):
                score = -1
            elif(dict.get("emo_score") == "positive"):
                score = 1
        serializer.save(owner=self.request.user, emo_score=score)

    queryset = Texts.objects.all()
    serializer_class = TextSerializer

class Apps(generics.CreateAPIView):

    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    #When the authentication step is ready
    #permission_classes = (permissions.IsAuthenticated,)
    queryset = App_list.objects.all()
    serializer_class = AppSerializer

class PhoneCall(generics.CreateAPIView):

    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

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

    #When the authentication step is ready
    #permission_classes = (permissions.IsAuthenticated,)
    queryset = Web_History.objects.all()
    serializer_class = WebHistorySerializer
"""
This needs to be turned into the token updater
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
"""

"""
This is the initial endpoint that all new user go through for account creation.
Sends back the token for django authentication, and a flag letting the client
know if the token was successfully extended or not.
"""
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
            res_dict.update({"sucess":True})
            return JsonResponse(res_dict)
        else:
            res_dict.update({"sucess":False})
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
"""
def getFbData(user_profile):
    access_token = user_profile.fb_token
    now = datetime.datetime.now()
    dict = {"access_token":access_token,"since":now,"limit":"1000"}
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
        score = 0
        if(dict.get("success") == True):
            if(dict.get("emo_score") == "negative"):
                score = -1
            elif(dict.get("emo_score") == "positive"):
                score = 1
        try:
            FbPosts.objects.update_or_create(creator=name, date_created=date, emo_score=int(score), id=str(id))
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