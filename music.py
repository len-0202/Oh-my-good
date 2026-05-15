import pygame
import time

pygame.mixer.init()

pygame.mixer.music.load("test.mp3")
pygame.mixer.music.play()

while pygame.mixer.music.get_busy():
    time.sleep(1)

#上の6行目以降を編集
'''
#音を流すための関数
def play_sound():
    pygame.mixer.music.load("test.mp3")
    pygame.mixer.music.play()


pause()
'''