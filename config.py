from sense_hat import SenseHat
import http.client
import urllib
import paho.mqtt.client as mqtt
import board
import adafruit_si7021
import adafruit_bmp3xx

## Generell
level = 0

RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

## Sensors
# temp & humid
sensor = adafruit_si7021.SI7021(board.I2C())
#https://github.com/davidrazmadzeExtra/Si_7021_Temp_Humidity

# temp & pres
bmp = adafruit_bmp3xx.BMP3XX_I2C(board.I2C())
#https://learn.adafruit.com/adafruit-bmp388-bmp390-bmp3xx/python-circuitpython


## SenseHat
sense = SenseHat()



### ThingSpeak Stuff
# API KEY
key = "FQLYNG5P6AOIPVZV"

# Headers
headers = {"Content-type": "application/x-www-form-urlencoded"}

# Create the connection
conn = http.client.HTTPConnection("api.thingspeak.com:80")


## MQTT Stuff
broker_address = "broker.emqx.io"

client = mqtt.Client()
client.connect(broker_address, 1883, 60)
client.loop_start()


## LOOP
while True:
    # Sense Data
    temp3 = round(bmp.temperature, 2)
    temp2 = round(sensor.temperature, 2)
    temp = round(sense.get_temperature(), 2)
    hum = round(sense.get_humidity(), 2)
    prss = round(sense.get_pressure(), 2)
    
    ## Upload Data
    # Body: data to send
    params = urllib.parse.urlencode({'field1': temp, 'field2': hum, 'field3': prss, 'key':key })
    
    # Make the request: GET, POST, DELETE
    conn.request("POST", "/update", params, headers)

    # Get the response
    response = conn.getresponse()
    
    # Print the response
    print(response.status, response.reason)
    data = response.read()
    print (data)
    
    
    ## SenseHat Stuff
    # Change Text Color
    if hum<60: hum_color = RED
    elif hum>80: hum_color = BLUE
    else: hum_color = GREEN

    if prss>1018: prss_color = RED
    elif prss>1008: prss_color = GREEN
    else: prss_color = BLUE

    if temp>20: temp_color = RED
    elif temp>10: temp_color = GREEN
    else: temp_color = BLUE
    
    for event in sense.stick.get_events():
        if event.direction == "up" and event.action == "pressed" :
            level = (level+1)%3
        if event.direction == "down" and event.action == "pressed" :
            level = (level-1)%3
    if level == 0 :
        sense.show_message("T"+str(temp)+"ºC", text_colour = temp_color)
        print("SenseHat: " + str(temp) + "; Sensor: " + str(temp2) + "; Sensor2: " + str(temp3))
    if level == 1 :
        sense.show_message("H"+str(hum)+"%", text_colour = hum_color)
    if level == 2 :
        sense.show_message("P"+str(prss)+"mbar", text_colour = prss_color)
    
    
    ## Publishing for phone
    client.publish("/temperature", temp)


## unreachable closing
# close MQTT client
client.disconnect()
client.loop_stop()

# Close the connection
conn.close()
        
    


        
        
        
