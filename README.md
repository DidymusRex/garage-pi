# garage-pi v 0.1

This project is designed to use a Raspberry Pi (Zero W) to manage a garage. Using
MQTT as an interface to the Home Assistant server.

## Main features / tasks
1. Manage overhead doors
    a. Distance sensor to determine door position
    b. Relay to trigger door button
2. Report environment (temp/humidity)
    a. DHT-11 sensor
3. Display inside of garage
    a. snapshot
    b. streaming video
4. Interface with Home Assistant

# To Do
- [ ] Camera management
- [ ] Home Assistant integration
- [ ] Custom PCB

# BOM
1. Raspberry Pi Zero W or compatible
2. 3v3 to 5v level shifter
3. HC-SR04 distance sensor (1 per garage door)
4. DHT-11 temperature and humidity sensor
5. Relay control board (1 relay per door)
6. Circuit board
7. Much wire

# Other software
- Home Assistant server
- MQTT broker
