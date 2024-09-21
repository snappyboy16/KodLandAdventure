from pgzero.actor import Actor
class Enemy:
    def __init__(self, image_left, image_right, walk_left, walk_right, position, speed=3, life=1):
        self.enemy = Actor(image_left, position)
        self.life = life
        self.speed = speed
        self.direction = 'left'
        self.animations = {
            'move_left': [image_left],
            'move_right': [image_right],
            'walk_left': walk_left,
            'walk_right': walk_right,
        }
        self.walk_index = 0
        self.animation_delay = 10
        self.frame_count = 0

    def move(self):
        # Движение врага влево
        self.enemy.x -= self.speed
        if self.enemy.x < 0:
            self.enemy.x = 730  # Вернем врага в начальную позицию справа

        self.animate_move()

    def animate_move(self):
        # Анимация движения
        if self.frame_count % self.animation_delay == 0:
            # Переключение между анимационными кадрами
            if self.direction == 'left':
                animation_frames = self.animations['walk_left']
            else:
                animation_frames = self.animations['walk_right']

            self.walk_index = (self.walk_index + 1) % len(animation_frames)
            self.enemy.image = animation_frames[self.walk_index]

        self.frame_count += 1

    def draw(self):
        self.enemy.draw()

    def is_off_screen(self):
        # Проверка, вышел ли враг за пределы экрана
        return self.enemy.x < 0

# Класс для Alien
class Alien(Enemy):
    def __init__(self, position=(730, 368), speed=4, life=2):
        super().__init__('enemy/alien/alien_green_left', 'enemy/alien/alien_green_right', ['enemy/alien/alien_green_walk_left_1', 'enemy/alien/alien_green_walk_left_2'], ['enemy/alien/alien_green_right_walk_1', 'enemy/alien/alien_green_right_walk_2'], position, speed, life)

class Bat(Enemy):
    def __init__(self, position=(730, 250), speed=3, life=1):
        super().__init__('enemy/bat/bat_left', 'enemy/bat/bat_right', 'enemy/bat/bat_fly_left', 'enemy/bat/bat_fly_right',
                         position, speed, life)