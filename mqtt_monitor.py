import paho.mqtt.client as mqtt
"""
A simple, generic MQTT client to monitor MQTT commands and
results
"""

"""
MQTT values
"""
mqtt_broker = "ubuntu-mini.local"
mqtt_account = ""
mqtt_passwd = ""
mqtt_topic = "garage/#"

"""
MQTT connect callback
    Subscribing in on_connect() means that if we lose the connection and
    reconnect then subscriptions will be renewed.
"""
def on_connect(client, userdata, flags, rc):
    client.subscribe(mqtt_topic)

"""
MQTT receive message callback
"""
def on_message(client, userdata, msg):
    print("message received " ,str(msg.payload.decode("utf-8")))
    print("message topic=",msg.topic)
    print("message qos=",msg.qos)
    print("message retain flag=",msg.retain)
    print("-" * 40)

mqc = mqtt.Client("monitor")
mqc.on_connect = on_connect
mqc.on_message = on_message

mqc.username_pw_set(mqtt_account, mqtt_passwd)
mqc.connect(mqtt_broker)

mqc.loop_forever()
