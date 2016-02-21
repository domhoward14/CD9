#!/bin/python
from gcm import *

gcm = GCM("AIzaSyDnYlTUqmET3vg4zUbuLHhOX6HW-6cQ2EE")
data = {'message': 'I hope that daniel see this !!', 'param2':'value2'}

reg_id = 'cFB5VC4vZVo:APA91bHpB3HxyCLrMXBtE3W-rqVJLFKenDB_X_1nOBp0mZ-70PvXVpJZbymsD_e96K7Bqnhh-9lVeSI6WZfATy_yfWbU82cR5sxSyCzPxnt43WfWrt2nrmuusLXA67IAa4txWqT1zHpZ'

gcm.plaintext_request(registration_id=reg_id, data=data)
