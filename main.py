import pgzrun
from pgzero.constants import mouse

import menu

WIDTH = 800
HEIGHT = 480
TITLE = "Kodland Adventures"

state = 'menu'
music = False
sounds = False


def draw():
    if state == 'menu':
        menu.draw_main_menu()
    elif state == 'settings':
        menu.draw_settings_menu(music, sounds)
    elif state == 'faq':
        pass
    elif state == 'exit':
        exit()
    elif state == 'start':
        pass
    elif state == 'pause':
        pass


def on_mouse_down(button, pos):
    global state, music, sounds
    if button == mouse.LEFT:
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
        elif state == 'settings':
            if menu.faq_btn.collidepoint(pos):
                state = 'faq'
            elif not music and menu.on_music_btn.collidepoint(pos):
                music = True
            elif music and menu.off_music_btn.collidepoint(pos):
                music = False
            elif not sounds and menu.on_sounds_btn.collidepoint(pos):
                sounds = True
            elif sounds and menu.off_sounds_btn.collidepoint(pos):
                sounds = False
            elif menu.close_btn.collidepoint(pos):
                state = 'menu'


def update(dt):
    if music:
        if sounds:
            pass
        else:
            pass
    else:
        pass


pgzrun.go()
