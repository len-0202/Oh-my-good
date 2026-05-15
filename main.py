import time

while Mode_button == 1:
    Camera_judge += CAMERA() #カメラの画像認識
    Sleepy_judge += Sleepy(Camera_judge) #居眠りの判定
    
    if Sleepy_judge >= 1: #居眠り中か判断
        print("居眠り中\n")
        print("アームに信号を送信")

        #アームに信号を送信
        time.sleep(10) #10秒待機
         


while Mode_button == 0:
