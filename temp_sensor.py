import Adafruit_DHT
import RPi.GPIO as GPIO
from time import sleep

"""
a simple wrapper for the DHT11 temperature and humidity sensor
"""
class temp_sensor():

    def __init__(self, mqc, pin):
        GPIO.setmode(GPIO.BCM)
        self.mqc = mqc
        self.pin = pin
        self.sensor = Adafruit_DHT.DHT11

    def __publish(self, topic, payload):
        print("---- publishing topic {} payload {}".format(topic, payload))
        rc = self.mqc.publish(topic, payload, 0)
        sleep(5)
        print("---- rc = {} mid = {} is_published = {}".format(rc.rc, rc.mid, rc.is_published()))

    def check_temp(self):
        topic = "garage/environment"

        h,t = Adafruit_DHT.read(self.sensor, self.pin)

        if h is not None and t is not None:
            f = t * (9 / 5) + 32
            payload = "C:{0:0.1f}, F:{1:0.1f}, H:{2:0.1f}%".format(t, f, h)
        else:
            payload = "C:X, F:X, H:X"

        self.__publish(topic, payload)
