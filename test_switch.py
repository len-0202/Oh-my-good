import gpiozero
import time

SW_PIN = 18

sw = gpiozero.DigitalInputDevice(SW_PIN, pull_up=False)

started = False

while True:
    # 一度でも押されたら started を True にする
    if sw.value == 1:
        started = True

    if started:
        print("実行中")
    else:
        print("待機中")

    time.sleep(0.5)