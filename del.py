import http.client
import urllib
import time
import json

key = "xx"    # Put your PROFILE API Key here
url = "api.thingspeak.com:80"
channel_id = "1565209"         # Put your channel ID

#All values
path = "/channels/"+channel_id+".json"

params = urllib.parse.urlencode({'key':key}) 

headers = {"Content-type": "application/x-www-form-urlencoded"}

conn = http.client.HTTPConnection(url)

# DELETE Method
conn.request("DELETE", path, params, headers)

response = conn.getresponse()

print(response.status, response.reason)

data = response.read()

data2=json.loads(data)
print(json.dumps(data2,indent=4,sort_keys=True))

conn.close()