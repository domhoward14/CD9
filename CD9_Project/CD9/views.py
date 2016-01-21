import json
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponse
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



def index(request):
    return HttpResponse("This is where the Parent Dashboard will be located")

class UserProfileList(generics.CreateAPIView):

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    #When the authentication step is ready
    #permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class UpdateUserProfile(generics.UpdateAPIView):

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
    queryset = Texts.objects.all()
    serializer_class = TextSerializer

class Texts(generics.CreateAPIView):

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    #When the authentication step is ready
    #permission_classes = (permissions.IsAuthenticated,)
    queryset = Texts.objects.all()
    serializer_class = TextSerializer

class Apps(generics.CreateAPIView):

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    #When the authentication step is ready
    #permission_classes = (permissions.IsAuthenticated,)
    queryset = App_list.objects.all()
    serializer_class = AppSerializer

class PhoneCall(generics.CreateAPIView):

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    #When the authentication step is ready
    #permission_classes = (permissions.IsAuthenticated,)
    queryset = Phone_Calls.objects.all()
    serializer_class = PhoneCallSerializer

class PhotoMessages(generics.CreateAPIView):

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    #When the authentication step is ready
    #permission_classes = (permissions.IsAuthenticated,)
    queryset = Photo_Messages.objects.all()
    serializer_class = PhotoMessagesSerializer

class WebHistory(generics.CreateAPIView):

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
    json_data = request.body
    parsed_data = json.loads(json_data)
    password = parsed_data.get("password","Nothing")
    token = parsed_data.get("token", "Nothing")
    if(token == "Nothing" or password == "Nothing"):
        return HttpResponse("There was no token or password sent in the JSON Object.")
    else:
        verify_results = tokenVerifier(token)
        if(verify_results["isVerified"]):
            dict = verify_results["facebook_dict"]
            email = dict.get("email","")
            name = dict.get("name","")
            try:
                user = User.objects.create(username=name,password=password)
                UserProfile.objects.create(user=user, email=email, isTeenager=True, fb_token=token)
            except:
                return HttpResponse("The profile was not successfully created")
        else:
            return HttpResponse("There was an error in verifying the access token")
        #This is where the django authentication token is created
        return HttpResponse("This is the part where you would get a django authentication token")

def tokenVerifier(token):
    dict = {'fields' : 'name, email', 'access_token' : token}
    r = requests.get('https://graph.facebook.com/me', params=dict)
    parsed_data = json.loads(r.text)
    if (r.status_code == 200):

        return {"isVerified" : True, "facebook_dict" : parsed_data}
    else:
        return {"isVerified" : False}