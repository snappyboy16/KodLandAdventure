from pgzero.actor import Actor
from hero import Hero
from enemy import Alien, Bat

hero = Hero()
alien = Alien()
bat = Bat()
background_menu_day = Actor('menu/background/menu_background_day')
start_btn = Actor('menu/button/start_btn', (400, 200))
settings_btn = Actor('menu/button/settings_btn', (400, 300))
exit_btn = Actor('menu/button/exit_btn', (400, 400))
on_music_btn = Actor('menu/button/on_music_btn', (400, 200))
off_music_btn = Actor('menu/button/off_music_btn', (400, 200))
on_sounds_btn = Actor('menu/button/on_sounds_btn', (400, 300))
off_sounds_btn = Actor('menu/button/off_sounds_btn', (400, 300))
close_btn = Actor('menu/button/close_btn', (400, 400))
faq_btn = Actor('menu/button/faq_btn', (760, 35))


def draw_main_menu():
    background_menu_day.draw()
    faq_btn.draw()
    start_btn.draw()
    settings_btn.draw()
    exit_btn.draw()
    hero.draw()
    alien.draw()


def draw_settings_menu(music, sounds):
    background_menu_day.draw()
    faq_btn.draw()
    if music:
        off_music_btn.draw()
    else:
        on_music_btn.draw()
    if sounds:
        off_sounds_btn.draw()
    else:
        on_sounds_btn.draw()
    close_btn.draw()
    hero.draw()
    alien.draw()