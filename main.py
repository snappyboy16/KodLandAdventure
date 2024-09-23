import random
import pgzrun
from pgzero.actor import Actor
from pgzero.constants import mouse
from pgzero.loaders import sounds
from pgzero.keyboard import keyboard
import menu
from hero import Hero
from enemy import Alien, Bat

WIDTH = 800
HEIGHT = 480
TITLE = "Kodland Adventures"
state = 'menu'
music = False
music_playing = False
sound = True
hearts = Hero().hearts
book_count = 0
books = []
enemies = []

enemy_spawn_delay = 200
frame_count = 0

background_game = Actor('map/day/map_day_start')
map_day = [Actor('map/day/map_day_1'), Actor('map/day/map_day_2'), Actor('map/day/map_day_3')]
hearts_img = [Actor('bonus/heart_full', (35, 30)), Actor('bonus/heart_full', (85, 30)),
              Actor('bonus/heart_full', (135, 30))]

hero_start_position = (100, 355)
menu.hero.hero.pos = hero_start_position


def draw():
    if state == 'menu':
        menu.draw_main_menu()
    elif state == 'settings':
        menu.draw_settings_menu(music, sound)
    elif state == 'faq':
        menu.draw_faq_menu()
    elif state == 'exit':
        exit()
    elif state == 'start':
        background_game.draw()
        for i in range(hearts):  # Отрисовываем оставшиеся жизни
            hearts_img[i].draw()
        for enemy in enemies:
            enemy.draw()
        menu.hero.draw()
        for book in books:
            book.draw()  # Отрисовка книг
        for bullet in menu.hero.bullets:
            bullet.draw()  # Отрисовываем пули героя


def on_mouse_down(button, pos):
    global state, music, sound
    if button == mouse.LEFT:
        sounds.load('button/click_button.mp3').play() if sound else False
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
            elif not sound and menu.on_sounds_btn.collidepoint(pos):
                sound = True
            elif sounds and menu.off_sounds_btn.collidepoint(pos):
                sound = False
            elif menu.close_btn.collidepoint(pos):
                state = 'menu'
        elif state == 'faq':
            if menu.faq_btn.collidepoint(pos):
                state = 'menu'


def on_music_off():
    global music_playing
    if music and not music_playing:
        sounds.load("background_music.mp3").play(-1)
        music_playing = True
    elif not music and music_playing:
        sounds.load('background_music.mp3').stop()
        music_playing = False


def spawn_enemy():  # рандомно появляются враги
    if random.choice([True, False]):
        new_enemy = Alien(position=(WIDTH, 368))
    else:
        random_height = random.randint(250, 350)
        new_enemy = Bat(position=(WIDTH, random_height))

    enemies.append(new_enemy)


def spawn_book():  # рандомно появляются книги
    x_position = random.randint(50, WIDTH - 50)
    new_book = Actor('bonus/book', (x_position, 368))
    books.append(new_book)


def check_collision_with_books():  # сбор книг
    global book_count
    for book in books:
        if menu.hero.hero.colliderect(book):
            books.remove(book)
            book_count += 1
            if book_count == 5:
                change_map()


def change_map():
    global background_game
    background_game = random.choice(map_day)  # меняем карту на случайную


def check_collision_with_enemies():
    global hearts
    for enemy in enemies:
        if menu.hero.hero.colliderect(enemy.enemy):
            hearts -= 1
            enemies.remove(enemy)
            if hearts <= 0:
                game_over()


def game_over():  # конец игры
    global state
    print("Game Over")
    state = 'menu'
    reset_game()


def reset_game():  # перезагрузка игры
    global hearts, book_count, enemies, books, frame_count, background_game
    hearts = 3
    book_count = 0
    enemies.clear()
    books.clear()
    frame_count = 0
    background_game = Actor('map/day/map_day_start')
    sounds.load('hero/run.mp3').stop()
    menu.hero.hero.pos = hero_start_position


def update():
    on_music_off()
    global frame_count, enemies, books
    if state == 'start':
        frame_count += 1
        if sound:
            menu.hero.move(keyboard, sound)
            if frame_count % enemy_spawn_delay == 0:
                spawn_enemy()
                spawn_book()
            for enemy in enemies:
                enemy.move()
            for bullet in menu.hero.bullets:
                if bullet.angle == 0:
                    bullet.x += 5
                elif bullet.angle == 90:
                    bullet.y -= 5
                elif bullet.angle == 180:
                    bullet.x -= 5
                elif bullet.angle == 270:
                    bullet.y += 5
                for enemy in enemies:
                    if bullet.colliderect(enemy.enemy):
                        if isinstance(enemy, Alien):
                            enemy.life -= 1
                            if enemy.life <= 0:
                                enemies.remove(enemy)
                        elif isinstance(enemy, Bat):
                            enemies.remove(enemy)
                        menu.hero.bullets.remove(bullet)

            # проверка столкновений с книгами и врагами
            check_collision_with_books()
            check_collision_with_enemies()

            # удаление вышедших за экран врагов и книг
            enemies = [enemy for enemy in enemies if not enemy.is_off_screen()]
            books = [book for book in books if book.x > 0]
        else:
            menu.hero.move(keyboard, sound)
            if frame_count % enemy_spawn_delay == 0:
                spawn_enemy()
                spawn_book()
            for enemy in enemies:
                enemy.move()

            # проверка на попадание пули во врага
            for bullet in menu.hero.bullets:
                if bullet.angle == 0:
                    bullet.x += 5
                elif bullet.angle == 90:
                    bullet.y -= 5
                elif bullet.angle == 180:
                    bullet.x -= 5
                elif bullet.angle == 270:
                    bullet.y += 5
                for enemy in enemies:
                    if bullet.colliderect(enemy.enemy):
                        if isinstance(enemy, Alien):
                            enemy.life -= 1  # уменьшаем жизнь у Alien на 1
                            if enemy.life <= 0:
                                enemies.remove(enemy)
                        elif isinstance(enemy, Bat):
                            enemies.remove(enemy)  # удаляем Bat при попадании
                        menu.hero.bullets.remove(bullet)  # удаляем пулю после попадания

            # проверка столкновений с книгами и врагами
            check_collision_with_books()
            check_collision_with_enemies()

            # удаление вышедших за экран врагов и книг
            enemies = [enemy for enemy in enemies if not enemy.is_off_screen()]
            books = [book for book in books if book.x > 0]
    if state == 'menu' or state == 'settings' or state == 'faq':
        menu.hero.animate_idle()
        menu.alien.draw()


pgzrun.go()
