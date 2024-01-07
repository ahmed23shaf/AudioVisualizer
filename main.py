import sys
import pygame
from pygame.locals import *
from visualizer import Visualizer

audio = "Audio Sweep.wav"

bars = 50
bar_height = 600
bar_width = 40
fps = 10

pygame.init()
file_name = sys.argv[0]
fps_clock = pygame.time.Clock()

screen = pygame.display.set_mode([int(bars * bar_width / 1.925), 50 + bar_height])
pygame.display.set_caption('Graphic Equalizer Display')

main_font = pygame.font.SysFont('consolas', 16)
freq_font = pygame.font.SysFont('consolas', 10)

pygame.mixer.init()
pygame.mixer.music.load(audio)
pygame.mixer.music.play()
pygame.mixer.music.set_endevent()
pygame.mixer.music.set_volume(0.2)

status = "Playing " + audio + "  " 

audio_visualizer = Visualizer(audio, bars, bar_height, bar_width, fps, screen, freq_font)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    # End check
    if audio_visualizer.current_frame <= 0:
        status = "stopped"

    name_text = main_font.render(file_name, True, (255, 255, 255))
    status_text = main_font.render(status.upper() + "" + audio_visualizer.get_current_time(), True, (255, 255, 255))

    screen.fill((0, 0, 0))

    screen.blit(name_text, (0, 0))
    screen.blit(status_text, (0, 18))

    fps_clock.tick(fps)

    audio_visualizer.update()
    pygame.display.update()
