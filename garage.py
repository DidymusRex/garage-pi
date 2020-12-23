from datetime import datetime
from gpiozero import DistanceSensor
from garage_door import garage_door
from garage_camera import garage_camera
import paho.mqtt.client as mqtt
from temp_sensor import temp_sensor
from time import sleep

"""
GPIO pin assignments:
    relays
    range finder sensor (echo passes thru voltage converter)
    DHT11 temperature/huidity sensor
"""
GPIO_Pins = {'temp_1':21, 'relay_1':6, 'relay_2':12, 'trig_1':17,'echo_1':18, 'trig_2':22,'echo_2':23}

"""
MQTT values
"""
mqtt_broker = "ubuntu-mini.local"
mqtt_account = ""
mqtt_passwd = ""
mqtt_topic = "garage/command"

"""
MQTT connect callback
    Subscribing in on_connect() means that if we lose the connection and
    reconnect then subscriptions will be renewed.
"""
def on_connect(client, userdata, flags, rc):
    client.subscribe(mqtt_topic)

"""
MQTT receive message callback (garage/command)
    Take action on a subject
"""
def on_message(client, userdata, msg):
    print("message received ", str(msg.payload.decode("utf-8")))
    print("message topic=", msg.topic)
    print("message qos=", msg.qos)
    print("message retain flag=", msg.retain)

    cmd = str(msg.payload.decode("utf-8")).split(",")
    if len(cmd) == 2:
        (subject, action) = cmd

        if subject in garage_doors:
            if action == "open":
                garage_doors[subject].open()
            elif action == "close":
                garage_doors[subject].close()
            elif action == "check":
                garage_doors[subject].get_position()
            else:
                print("Invalid command {}".format(action))
        elif subject == "dht11":
            dht11.check_temp()
        elif subject == "still":
            garage_cam.take_still()
        else:
            print("invalid subject {}".format(subject))
    else:
        print("Invalid payload")
"""
MQTT publish callback
    Mainly for debugging
"""
def on_publish(client, userdata, mid):
    print("message id {} published".format(mid))

"""
Just in case
"""
def main():
    pass

"""
Create client and connect it to the MQTT broker
"""
mqc = mqtt.Client("garage-pi", clean_session=True)
mqc.on_connect = on_connect
mqc.on_message = on_message
mqc.on_publish = on_publish

mqc.username_pw_set(mqtt_account, mqtt_passwd)
mqc.connect(mqtt_broker)
mqc.loop_start()
mqc.publish("garage/foo", "go!")

"""
Create temperature sensor object
"""
dht11 = temp_sensor(mqc, GPIO_Pins['temp_1'])

"""
Create garage camera object
"""
garage_cam = garage_camera(mqc)

"""
Create garage door objects
"""
garage_doors = dict()
garage_doors["left"] = garage_door(mqc, "left", GPIO_Pins['relay_1'], GPIO_Pins['echo_1'], GPIO_Pins['trig_1'])
garage_doors["right"] = garage_door(mqc, "right", GPIO_Pins['relay_2'], GPIO_Pins['echo_2'], GPIO_Pins['trig_2'])

if __name__ == "__main__":
    main()
