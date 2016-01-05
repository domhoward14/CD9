from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("This is where the Parent Dashboard will be located")