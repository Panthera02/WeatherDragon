import paho.mqtt.client as mqtt

client = mqtt.Client()

def on_message(client1, userdata, message):
    print("message received  ", str(message.payload.decode("utf-8")))
    
client.on_message = on_message

client.connect("broker.emqx.io", 1883, 60)

client.subscribe("/temperature")

client.loop_forever()