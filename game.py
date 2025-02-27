#pygame
import pygame
from pygame import  *
from random import randint
from time import time as timer
#loading font
font.init() 
font1 = font.SysFont("Arial", 80)
font2 = font.SysFont("Arial", 36)
win = font1.render("YOU WIN!!!", True, (43,134,235))
lose = font1.render("You Lose", True, (255, 0,0))
score = 0
goal = 30
miss = 0
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image,(self.rect.x, self.rect.y))
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet("bullet.png", self.rect.centerx - 10, self.rect.top, 15,20,15)
        bullets.add(bullet)


class Enemy(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed, is_asteroid):
        super().__init__(player_image, player_x, player_y, size_x, size_y, player_speed)
        self.is_asteroid = is_asteroid

    def update(self):
        global miss
        self.rect.y += self.speed
        if self.rect.y > win_height and self.is_asteroid == False:
            self.rect.x = randint(80, win_width-80)
            self.rect.y = 0
            miss = miss + 1
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()
#window size
win_width = 700
win_height = 500
image_player = "Player.png"
image_background = "background.png"
display.set_caption("Shooter game")
background = transform.scale(image.load(image_background), (win_width, win_height))
window = display.set_mode((win_width,win_height))
player = Player("Player.png", 5, win_height - 100, 80,100, 20)
asteroids = sprite.Group()
for i in range(5):
    asteroid = Enemy("asteroid.png", randint(80, win_width-80), 0, 80, 50, randint(1,10), True)
    asteroids.add(asteroid)
ufos = sprite.Group()
for i in range(5):
    ufo = Enemy("UFO.png", randint(80, win_width-80), 0, 80, 50, randint(1,5), False)
    ufos.add(ufo)
bullets = sprite.Group()

game = True
finish = False
reload_time = False
num_fire = 5
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire > 0 and reload_time == False:
                    num_fire -= 1
                    player.fire()

                if num_fire == 0:
                    last_time = timer()
                    reload_time = True
    if not finish:
        window.blit(background, (0,0))
        text = font2.render("Score:" + str(score), 1, (243,34, 12))
        window.blit(text,(10, 20))
        text2 = font2.render("Miss:" + str(miss), 1, (243, 34, 12))
        window.blit(text2, (10, 40))
        player.update()
        player.reset()
        ufos.update()
        ufos.draw(window)
        asteroids.update()
        asteroids.draw(window)
        bullets.update()
        bullets.draw(window)

        if reload_time == True:
            now_time = timer()
            if now_time - last_time < 3:
                reload_text = font2.render("Wait, reload...", 1 , (243,183,33))
                window.blit(reload_text,(250,450))
            else:
                num_fire = 5
                reload_time = False
        collides = sprite.groupcollide(ufos, bullets, True, True)
        for asteroid in asteroids:
            if sprite.spritecollide(player,asteroids, False):
                finish = True
                window.blit(lose, (200,200))
        for collide in collides:
            score += 1
            ufo = Enemy("UFO.png", randint(80, win_width - 80), 0, 80, 50, randint(1, 5), False)
            ufos.add(ufo)

        if sprite.spritecollide(player, ufos, False ) or miss > 3:
            finish = True
            window.blit(lose, (200, 200))
        if score >= goal:
            finish = True
            window.blit(win, (200,200))
        display.update()

    else:
        #reset the game
        finish = False
        score = 0
        miss = 0
        num_fire = 5
        for bullet in bullets:
            bullet.kill()
        for m in ufos:
            m.kill()
        for a in asteroids:
            a.kill()
        time.delay(3000)

        for i in range(5):
            ufo = Enemy("UFO.png", randint(80, win_width - 80), 0, 80, 50, randint(1, 5), False)
            ufos.add(ufo)
        for i in range(5):
            asteroid = Enemy("asteroid.png", randint(80, win_width-80), 0, 80, 50, randint(1,10), True)
            asteroids.add(asteroid)

    time.delay(50)

