from django.conf.urls import patterns, url
from CD9 import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'))
