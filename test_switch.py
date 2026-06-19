import gpiozero
import time

SW_PIN = 18

sw = gpiozero.DigitalInputDevice(SW_PIN, pull_up = False)

sw_old = 0
mode = False

while True:
    sw_new = sw.value  # ボタンの状態を取得 (0 or 1)

    # ボタンが押された瞬間
    if sw_new == 1 and sw_old == 0:
        mode = not mode  # モード切替
        print("ON")

    sw_old = sw_new

    if mode:
        print("モードA実行中")
    else:
        print("OFF")

    time.sleep(0.5)


