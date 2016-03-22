LIENT_SECRET_FILE

from apiclient import discovery
import httplib2
from oauth2client import client
import os


auth_code = "nLLIpv_yDHecvUC_uzrR2rw02MYS3Ly3jeeKECW878s"
CLIENT_SECRET_FILE = str(os.getcwd()) + "/client_secret.json" 

credentials = client.credentials_from_clientsecrets_and_code(
    CLIENT_SECRET_FILE,
    ['https://www.googleapis.com/auth/gmail.readonly'],
    auth_code)


#http = credentials.authorize(httplib2.Http())
#gmail_service = discovery.build('gmail', 'v1', http=http)

