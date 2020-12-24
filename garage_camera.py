from time import sleep
from picamera import PiCamera

"""
a wrapper for the pi camera functions
"""
class garage_camera():

    def __init__(self, mqc):
        self.mqc = mqc

        self.camera = PiCamera()
        self.camera.resolution = (1024, 768)
        self.camera.start_preview()

    def __publish(self, topic, payload):
        print("---- publishing topic {} still image".format(topic))
        rc = self.mqc.publish(topic, payload, 0)
        sleep(5)
        print("---- rc = {} mid = {} is_published = {}".format(rc.rc, rc.mid, rc.is_published()))

    def take_still(self):
        topic = "garage/environment/still"

        self.camera.capture('foo.jpg')
        f=open("foo.jpg", "rb")
        fileContent = f.read()
        payload = bytearray(fileContent)

        self.__publish(topic, payload)
