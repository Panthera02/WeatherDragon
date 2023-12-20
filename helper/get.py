import http.client
import urllib
import time
import json
from sense_emu import SenseHat

sense = SenseHat()


key = "U5ZYAESQI38IZE0K"          # Put your API Key here
channel = "2345712"            # Put your channel ID
url = "api.thingspeak.com:80"  # URL provided by Thingspeak

# Path
# All values
path = "/channels/"+channel+"/feeds"
# Last value
# path = "/channels/"+channel+"/feeds/last"
# Specific Field
# field_id = "2"
# path = "/channels/"+channel+"/fields/"+field_id

# Body
params = urllib.parse.urlencode({'key':key}) 

# If you have a lot of values, you can filter by date, for example:
#params = urllib.parse.urlencode({'key':key, "start": "2021-11-09%19:05:16"}) 

# Headers
headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}

# Create the connection
conn = http.client.HTTPConnection(url)

# Make the request: GET, POST, DELETE
conn.request("GET", path, params, headers)

# Get the response
response = conn.getresponse()

# Print the response
print(response.status, response.reason)
data = response.read()
data2=json.loads(data)
#print(json.dumps(data2,indent=4,sort_keys=True))
t=json.dumps(data2["feeds"][-1]["field1"],indent=4,sort_keys=True)
h=json.dumps(data2["feeds"][-1]["field2"],indent=4,sort_keys=True)
print(t)
print(h)

sense.show_message("T"+t+" H"+h)

#penultimate
t=json.dumps(data2["feeds"][-2]["field1"],indent=4,sort_keys=True)
h=json.dumps(data2["feeds"][-2]["field2"],indent=4,sort_keys=True)
print(t)
print(h)

sense.show_message("T"+t+" H"+h)

# Close the connection
conn.close()