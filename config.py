from sense_hat import SenseHat
import http.client
import urllib
import paho.mqtt.client as mqtt
import board
import adafruit_si7021
import adafruit_bmp3xx
import RPi.GPIO as GPIO
from time import sleep

## Generell
level = 0

RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

minTemp = 15
maxTemp = 30
minHum = 30
maxHum = 60
minPrss = 900
maxPrss = 1000

# LED
LED_PIN = 21
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

def ledOn():
    GPIO.output(LED_PIN, GPIO.HIGH)
def ledOff():
    GPIO.output(LED_PIN, GPIO.LOW)
def ledBlink():
    ledOn()
    sleep(0.1)
    ledOff()


## Sensors
# temp & humid
si = adafruit_si7021.SI7021(board.I2C())
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
    # Sense Data from Sensors    
    temp = round((round(bmp.temperature,1) + round(si.temperature,1))/2, 1)
    hum = round(si.relative_humidity, 1)
    prss = round(bmp.pressure, 1)
    
    ## Upload Data
    # Body: data to send
    params = urllib.parse.urlencode({'field1': temp, 'field2': hum, 'field3': prss, 'key':key })
    
    # Make the request: GET, POST, DELETE
    conn.request("POST", "/update", params, headers)

    # Get the response
    response = conn.getresponse()
    
    # Print the response
    #print(response.status, response.reason)
    data = response.read()
    #print (data)
    
    
    ## SenseHat Stuff
    # Change Text Color
    if hum > maxHum:
        hum_color = RED
        ledBlink()
    elif hum > minHum:
        hum_color = GREEN
    else:
        hum_color = BLUE

    if prss > maxPrss:
        prss_color = RED
        ledBlink()
    elif prss > minPrss:
        prss_color = GREEN
    else:
        prss_color = BLUE

    if temp > maxTemp:
        temp_color = RED
        ledBlink()
    elif temp > minTemp:
        temp_color = GREEN
    else:
        temp_color = BLUE
    
    for event in sense.stick.get_events():
        if event.direction == "up" and event.action == "pressed" :
            level = (level+1)%3
        if event.direction == "down" and event.action == "pressed" :
            level = (level-1)%3
    if level == 0 :
        sense.show_message("T"+str(temp)+"C", text_colour = temp_color)
    if level == 1 :
        sense.show_message("H"+str(hum)+"%", text_colour = hum_color)
    if level == 2 :
        sense.show_message("P"+str(prss)+"mbar", text_colour = prss_color)
    
    
    ## Publishing for phone
    client.publish("/temperature", temp)
    client.publish("/humidity", hum)
    client.publish("/pressure", prss)


## unreachable closing
# close MQTT client
client.disconnect()
client.loop_stop()

# Close the connection
conn.close()
        
    


        
        
        
