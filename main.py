import random
import pgzrun
from pgzero.constants import mouse
from pgzero.loaders import sounds
from pgzero.keyboard import keyboard
import menu

WIDTH = 800
HEIGHT = 480
TITLE = "Kodland Adventures"

state = 'menu'
music = False
music_playing = False
sound = True
books = []


def draw():
    if state == 'menu':
        menu.draw_main_menu()
    elif state == 'settings':
        menu.draw_settings_menu(music, sound)
    elif state == 'faq':
        pass
    elif state == 'exit':
        exit()
    elif state == 'start':
        pass
    elif state == 'pause':
        pass


def on_mouse_down(button, pos):
    global state, music, sound
    if button == mouse.LEFT:
        sounds.load('button/click_button.mp3').play() if sound else False
        print(pos)
        print(state)
        if state == 'menu':
            if menu.faq_btn.collidepoint(pos):
                state = 'faq'
            elif menu.start_btn.collidepoint(pos):
                state = 'start'
            elif menu.settings_btn.collidepoint(pos):
                state = 'settings'
            elif menu.exit_btn.collidepoint(pos):
                state = 'exit'
            elif menu.hero.hero.collidepoint(pos):
                pass
        elif state == 'settings':
            if menu.faq_btn.collidepoint(pos):
                state = 'faq'
            elif not music and menu.on_music_btn.collidepoint(pos):
                music = True
            elif music and menu.off_music_btn.collidepoint(pos):
                music = False
            elif not sound and menu.on_sounds_btn.collidepoint(pos):
                sound = True
            elif sounds and menu.off_sounds_btn.collidepoint(pos):
                sound = False
            elif menu.close_btn.collidepoint(pos):
                state = 'menu'


def on_music_off():
    global music_playing
    if music and not music_playing:
        sounds.load("background_music.mp3").play(-1)
        music_playing = True
    elif not music and music_playing:
        sounds.load('background_music.mp3').stop()
        music_playing = False

def update(dt):
    on_music_off()
    if sound:
        menu.hero.move(keyboard, sound)
        menu.alien.move()
        menu.bat.move()
        for bullet in menu.hero.bullets:
            if bullet.angle == 0:
                bullet.x = bullet.x + 5
            elif bullet.angle == 90:
                bullet.y = bullet.y - 5
            elif bullet.angle == 180:
                bullet.x = bullet.x - 5
            elif bullet.angle == 270:
                bullet.y = bullet.y + 5
    else:
        menu.hero.animate_idle()


pgzrun.go()
