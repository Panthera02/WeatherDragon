import http.client
import urllib
import time
import random
from sense_emu import SenseHat

sense = SenseHat()

#get temperature
current_temp = sense.get_temperature()
            
#get humidity
current_humidity = sense.get_humidity()
            
# API KEY
key = "KQ0RK384JWCSS3MJ"  # Put your API Key here

# Body: data to send
params = urllib.parse.urlencode({'field1': current_temp, 'field2': current_humidity, 'key':key }) #change input

# Headers
headers = {"Content-type": "application/x-www-form-urlencoded"}

# Create the connection
conn = http.client.HTTPConnection("api.thingspeak.com:80")

# Make the request: GET, POST, DELETE
conn.request("POST", "/update", params, headers)

# Get the response
response = conn.getresponse()

# Print the response
print(response.status, response.reason)
data = response.read()
print (data)

# Close the connection
conn.close()