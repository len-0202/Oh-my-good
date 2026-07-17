import time
from gpiozero import Button
import cv2
import os
os.environ["SDL_AUDIODRIVER"] = "alsa"
os.environ["AUDIODEV"] = "hw:3,0"
import pygame
import pygame
import threading
import face_detect
from music import music

button = Button(18, pull_up=False, bounce_time=0.05)

mode = False

threading.Thread(
    target=face_detect.CAMERA, 
    daemon=True 
).start()

pygame.mixer.init()

while True:

    # ボタンが押された瞬間
    if button.is_pressed: 
        mode = not mode 

        if mode: 
            print("監視開始") 
        else: 
            print("監視終了") 
        
        while button.is_pressed: 
            time.sleep(0.01)

    if mode:
        if face_detect.get_camera_status() == 1:

            print("居眠り中")
            print("アームに信号を送信")

            # アーム制御
            time.sleep(10)
            music() # 音楽再生
            time.sleep(10)

            face_detect.stop_camera()
            mode = False
            print("監視終了")
            print("ボタンを押すと監視を再開します")

    time.sleep(0.1)