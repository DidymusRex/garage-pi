# garage-pi

This project is designed to use a Raspberry Pi (Zero W) to manage a garage. Using
MQTT as an interface to the system.

1. Manage overhead doors
    a. Distance sensor to determin door position
    b. Relay to trigger door button
2. Report environment (temp/humidity)
    a. DHT-11 sensor
3. Display inside of garage
    a. snapshot
    b. streaming video
4. Interface with Home Assistant using MQTT

# To Do
Camera management
Home Assistant integration

# BOM
Raspberry Pi Zero W or compatible
3v3 to 5v level shifter
HC-SR04 distance sensor
DHT-11 temperature and humidity sensor
Dual relay control board
Circuit board
Much wire

Home Assistant server
MQTT broker

