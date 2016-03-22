#!/bin/bash
from CD9.views import *
from CD9.models import *


eric = UserProfile.objects.all()[1]
eric.auth_code = "4/PCYhGO2oaEcksDqMhbi0QiTQP7vBWbpuvg3tG_8mZJU"
eric.save()
cred = getCredentials(eric)
