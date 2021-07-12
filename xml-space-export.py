import requests
import shutil
from time import sleep
from requests import Session
from requests.auth import HTTPBasicAuth
from zeep import Client
from zeep.transports import Transport

user = "admin"
password = "admin"

session = Session()
session.auth = HTTPBasicAuth(user, password)
client = Client('http://localhost:1990/confluence/rpc/soap-axis/confluenceservice-v2?WSDL',
    transport=Transport(session=session))

print("Logging in...")
token = client.service.login(user, password)
print("Getting Spaces")
spaces = client.service.getSpaces(token)
numSpaces = len(spaces)
for index, space in enumerate(spaces):
    print("Exporting space {} of {} - {} using URL:".format(index+1, numSpaces, space.key))
    siteExportUrl = client.service.exportSpace(token, space.key, "TYPE_XML")
    print(siteExportUrl)
    filename = siteExportUrl.split('/')[-1]
    print("Saving as: " + filename)
    r = session.get(siteExportUrl, stream=True)
    with open(filename, 'wb') as f:
        shutil.copyfileobj(r.raw, f)
    sleep(5)
