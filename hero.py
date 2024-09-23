from pgzero.actor import Actor
from pgzero.loaders import sounds


class Hero:
    def __init__(self):
        self.hero = Actor('hero/player_idle_right', (105, 355))
        self.bullet = Actor('hero/player_bullets')
        self.hearts = 3
        self.speed = 5
        self.jump_strength = 15  # высота прыжка
        self.gravity = 0.8  # гравитация
        self.vertical_speed = 0  # скорость по y
        self.bullets = []
        self.bullet_time = 0
        self.is_jumping = False  # прыгнул
        self.is_grounded = True  # стоит
        self.is_crouching = False  # присел
        self.direction = 'right'  # направление
        self.ground_level = 355  # уровень земли
        self.animations = {
            'idle_right': ['hero/player_idle_right', 'hero/player_cheer_right', 'hero/player_cheer_right_1'],
            'idle_left': ['hero/player_idle_left', 'hero/player_cheer_left', 'hero/player_cheer_left_1'],
            'walk_right': ['hero/player_walk_right_1', 'hero/player_walk_right_2'],
            'walk_left': ['hero/player_walk_left_1', 'hero/player_walk_left_2'],
            'down_right': 'hero/player_down_right',
            'down_left': 'hero/player_down_left',
            'jump_right': 'hero/player_jump_right',
            'jump_left': 'hero/player_jump_left',
        }
        self.is_idle = True  # стоит на месте
        self.walk_index = 0
        self.idle_index = 0
        self.down_index = 0
        self.animation_delay = 10
        self.frame_count = 0
        self.run_sound = sounds.load('hero/run.mp3')
        self.sound_playing = False

    def move(self, keys, sound):  # перемещение героя
        self.is_idle = False
        if keys.left and not self.is_crouching:
            if self.hero.x < 50:
                self.hero.x = self.hero.x
            else:
                self.hero.x -= self.speed
                self.direction = 'left'
                self.animate_walk()
                self.attack(keys)
                self.play_run_sound(sound)
        elif keys.right and not self.is_crouching:
            if self.hero.x > 750:
                self.hero.x = self.hero.x
            else:
                self.hero.x += self.speed
                self.direction = 'right'
                self.animate_walk()
                self.attack(keys)
                self.play_run_sound(sound)
        elif keys.down and not self.is_jumping:
            self.is_crouching = True
            self.animate_down()
        else:
            self.is_crouching = False
            self.is_idle = True
            self.animate_idle()
            self.attack(keys)
            self.stop_run_sound(sound)

        if keys.up and not self.is_jumping and self.is_grounded and not self.is_crouching:
            self.jump()
        else:
            self.apply_gravity()

    def animate_walk(self):  # анимация ходьбы
        if self.frame_count % self.animation_delay == 0:
            self.walk_index = (self.walk_index + 1) % len(self.animations[f'walk_{self.direction}'])
            self.hero.image = self.animations[f'walk_{self.direction}'][self.walk_index]
        self.frame_count += 1

    def animate_idle(self):  # анимация, когда герой стоит на месте
        if self.frame_count % self.animation_delay == 0:
            self.idle_index = (self.idle_index + 1) % len(self.animations[f'idle_{self.direction}'])
            self.hero.image = self.animations[f'idle_{self.direction}'][self.idle_index]
        self.frame_count += 1

    def animate_down(self):  # анимация приседания
        self.hero.image = self.animations[f'down_{self.direction}']

    def jump(self):  # прыжок
        self.is_jumping = True
        self.is_grounded = False
        self.vertical_speed = -self.jump_strength
        self.hero.image = self.animations[f'jump_{self.direction}']

    def apply_gravity(self):  # гравитация, если прыжка нет, то падает на землю
        if not self.is_grounded:
            self.vertical_speed += self.gravity
            self.hero.y += self.vertical_speed
            if self.hero.y >= self.ground_level:
                self.hero.y = self.ground_level
                self.is_jumping = False
                self.is_grounded = True
                self.vertical_speed = 0
                self.animate_idle()

    def attack(self, keys):  # выпускание пуль
        if self.bullet_time == 0:
            if keys.space:
                self.bullet.angle = self.hero.angle
                self.bullet.x = self.hero.x
                self.bullet.y = self.hero.y
                self.bullets.append(self.bullet)
                self.bullet_time = 70
        else:
            self.bullet_time = self.bullet_time - 1

    def play_run_sound(self, sound):  # включение звука перемещения
        if not self.sound_playing and sound:
            self.run_sound.play(-1)
            self.sound_playing = True

    def stop_run_sound(self, sound):  # отключение звука перемещения
        if self.sound_playing and sound:
            self.run_sound.stop()
            self.sound_playing = False

    def draw(self):
        self.hero.draw()
        for bullet in self.bullets:
            bullet.draw()
