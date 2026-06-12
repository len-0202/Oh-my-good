import RPi.GPIO as GPIO
import requests
import time

BUTTON = 18
URL = "http://PCのIPアドレス:5000/button"

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)

print("起動しました")

try:
    while True:
        if GPIO.input(BUTTON) == GPIO.LOW:
            print("ボタン押された！送信")
            try:
                requests.get(URL)
            except Exception as e:
                print("送信エラー:", e)

            time.sleep(0.5)  # チャタリング防止
        time.sleep(0.05)

except KeyboardInterrupt:
    GPIO.cleanup()