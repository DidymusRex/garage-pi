from gpiozero import DistanceSensor
import RPi.GPIO as GPIO
from time import sleep
from datetime import datetime

class garage_door():
    """
    Create a garage door object with a relay and two sensors
        Triggering the relay opens or closes the door (reversing it's current position)
        The sensor should be mounted above the door to measure the distance from the 
            ceiling to the door. An open door is a shorter distance than a closed door
        Send events and receive commands from the MQTT broker
    """
    def __init__(self, mqc, name, relay, echo_1, trig_1):
        GPIO.setmode(GPIO.BCM)

        self.mqc = mqc
        self.relay = relay
        self.name = name
        GPIO.setup(relay, GPIO.OUT, initial=GPIO.HIGH)

        self.sensor = DistanceSensor(echo=echo_1, trigger=trig_1)

        self.position = 0
        self.position_list = ('error', 'open', 'closed')
        print("{} initialized".format(self.name))

    def __check_time(self):
        print("{} retrieving time".format(self.name))

        now = datetime.now() # current date and time
        date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
        return date_time

    def __publish(self, topic, payload):
        print("---- publishing topic {} payload {}".format(topic, payload))
        rc = self.mqc.publish(topic, payload, 0)
        sleep(5)
        print("---- rc = {} mid = {} is_published = {}".format(rc.rc, rc.mid, rc.is_published()))

    def __click_door(self):
        print("{} clicked".format(self.name))

        """
        Close relay for 1/2 second
        """
        GPIO.output(self.relay, GPIO.LOW)
        sleep(.5)
        GPIO.output(self.relay, GPIO.HIGH)
        sleep(.5)

        topic = "garage/door/{}/clicked".format(self.name)
        payload = self.__check_time()
        self.__publish(topic, payload)

    def get_position(self):
        print("{} get position".format(self.name))

        """
        Position: 0=error, 1=open, 2=closed
        """
        print("---- read sensor1")
        distance_1=self.sensor1.distance * 100

        if (distance_1 > 20):
            # Door is closed
            self.position = 2
        elif (distance_1 < 20):
            # Door is open
            self.position = 1

        topic = "garage/door/{}/position".format(self.name)
        payload = self.position_list[self.position]
        self.__publish(topic, payload)

    def open(self):
        print("{} close".format(self.name))
        """
        Only open a closed door
        """
        self.get_position()

        if (self.position == 2):
            self.__click_door()

        topic = "garage/door/{}/open".format(self.name)
        payload = self.__check_time()
        self.__publish(topic, payload)

    def close(self):
        print("{} open".format(self.name))
        """
        Only close an open door
        """
        self.get_position()

        if (self.position == 1):
            self.__click_door()

        topic = "garage/door/{}/close".format(self.name)
        payload = self.__check_time()
        self.__publish(topic, payload)
