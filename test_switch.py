import gpiozero
import time

SW_PIN = 18

sw = gpiozero.DigitalInputDevice(SW_PIN)

while True:
    if(sw.value == 1):
        print("ON")
    else:
        print("OFF")

    time.sleep(0.5)