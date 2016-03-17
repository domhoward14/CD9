#!/bin/python

from CD9.views import *
from CD9.models import *

eric = UserProfile.objects.all()[0].user
dict = {"user" : eric}
dict["triggerType"] = 4
triggerCheck(dict)
