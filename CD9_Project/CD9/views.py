import json
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
    PhoneCallSerializer, WebHistorySerializer
from models import UserProfile, Texts, App_list, Phone_Calls, Photo_Messages, Web_History
from rest_framework import generics
from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token



CD9_APP_SECRET = "87b2da14fffc70104a079c7598230b82"
CD9_APP_ID = "193476894336866"
FB_TOKEN_EXTENDER_URL = "https://graph.facebook.com/oauth/access_token"

def index(request):
    return HttpResponse("This is where the Parent Dashboard will be located")

class UserProfileList(generics.CreateAPIView):

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
        serializer.save(owner=self.request.user)

    #When the authentication step is ready
    #permission_classes = (permissions.IsAuthenticated,)
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
@csrf_exempt
def CreateNewUser(request):
    token_dict = getToken(request)
    password = token_dict.get("password","Nothing")
    token = token_dict.get("token", "Nothing")
    if(token == "Nothing" or password == "Nothing"):
        return Http404("There was no token or password sent in the JSON Object.")
    else:
        verify_results = tokenVerifier(token)
        if(verify_results["isVerified"]):
            dict = verify_results["facebook_dict"]
            email = dict.get("email","")
            name = dict.get("name","")
            try:
                user = User.objects.create(username=name,password=password, email=email)
                UserProfile.objects.create(user=user, email=email, isTeenager=True, fb_token=token)
            except Exception as e:
                error = e.message
                return Http404("The profile was not successfully created. Error : " + error)
        else:
            return Http404("There was an error in verifying the access token")
        return JsonResponse(createToken())

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
to update the token.
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
            return Http404("email associated with this token is not valid.")
        user = user_dict.get("user")
        return JsonResponse(updateToken(user))
    else:
        return Http404("There was an error in verifying the access token")

"""
This is the helper function for TokenUpdater
"""
def updateToken(user):

    token = Token.objects.get(user=user)
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
            return HttpResponse("This is where the token would be saved to the database and the client recieves a successful code. The token saved is : " + token)
        else:
            return Http404("There was an error while creating a long life token")
    else:
        return Http404("There was an error while authenticating the token")

@csrf_exempt
def TokenExtender(request):
    token_dict = getToken(request)
    return extendToken(token_dict.get("token","Nothing"))

class UserList(generics.ListCreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

