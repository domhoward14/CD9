from django.shortcuts import render
from django.http import HttpResponse
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

