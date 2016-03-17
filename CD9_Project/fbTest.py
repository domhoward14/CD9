#!/bin/python 

from CD9.views import *
from CD9.models import *

incomingData = [{u'created_time': u'2015-07-06T21:29:30+0000', u'story': u'Laticia Howard added a new photo \u2014 with Eric Howard.', u'id': u'1140150502663872_1044589268886663'}, {u'created_time': u'2015-04-24T14:36:09+0000', u'story': u'Tom Hug added a new photo \u2014 with Bruce Howard and 3 others.', u'id': u'1140150502663872_1002960353049555'}, {u'created_time': u'2015-03-18T15:43:03+0000', u'story': u'Mark Roz and 4 others wrote on your Timeline.', u'id': u'1140150502663872_981202281892029'}, {u'created_time': u'2014-03-19T22:56:12+0000', u'message': u'Wow its been a minute since i posted on facebook but wanted to thank every one that showed me love yesterday for my b day!! much appreciated !!', u'id': u'1140150502663872_769104213101838'}, {u'created_time': u'2014-03-19T03:38:03+0000', u'story': u'Manny Baptiste and 10 others wrote on your Timeline.', u'id': u'1140150502663872_768721299806796'}]

def fbTest():
      for post in FbPosts.objects.all():
         print "the owner is " + str(post.owner)
         print "the creator is " + post.creator
         print "the emo_score is " + str(post.emo_score)
         print "the message is " + str(post.message)
         print "===================="

prof = UserProfile.objects.all()[1]
getFbData(prof)
FbPosts.objects.all()
fbTest()
