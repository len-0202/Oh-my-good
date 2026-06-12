import time
import gpiozero

SW_PIN0 = 17
SW_PIN1 = 18

sw0 = gpiozero.DigitalInputDevice(SW_PIN0, pull_up = False) #オレンジ
sw1 = gpiozero.DigitalInputDevice(SW_PIN1, pull_up = False) #緑

while True:
    if sw0.value == 1:
        Camera_judge += CAMERA() #カメラの画像認識
    Sleepy_judge += Sleepy(Camera_judge) #居眠りの判定
    
    if Sleepy_judge >= 1: #居眠り中か判断
        print("居眠り中\n")
        print("アームに信号を送信")

        #アームに信号を送信
        time.sleep(10) #10秒待機
         


while Mode_button == 0:


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