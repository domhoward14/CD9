from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from serializers import UserProfileSerializer, TextSerializer
from models import UserProfile, Texts
from rest_framework import generics
from rest_framework import permissions



def index(request):
    return HttpResponse("This is where the Parent Dashboard will be located")

class UserProfileList(APIView):

    def get(self, request, format=None):
        profiles = UserProfile.objects.all()
        serializer = UserProfileSerializer(profiles, many=True)
        return Response(serializer.data)
"""
class Texts(APIView):

    def post(self, request, format=None):
        serializer = TextSerializer(data=request.data)
"""

class Texts(generics.ListCreateAPIView):

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    #When the authentication step is ready
    #permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Texts.objects.all()
    serializer_class = TextSerializer
