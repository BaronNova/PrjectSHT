#Создай собственный Шутер!

from pygame import *
from random import randint



windx = 700
windy = 500
FPS = 30
lost = 0
win = 0
overheat = 0
health = 3


window = display.set_mode((windx, windy))
display.set_caption('shooter')
background = image.load('galaxy.jpg') 

bullets = sprite.Group()

playing = True
finsh = False
clock = time.Clock()

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

fire1 = mixer.Sound('fire.ogg')

font.init()
font1 = font.Font(None, 36)

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (65, 65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if (keys[K_LEFT] or keys[K_a]) and self.rect.x > 5:
            self.rect.x -= self.speed
        if (keys[K_RIGHT] or keys[K_d]) and self.rect.x < 620:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, -15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > windy:
            self.rect.x = randint(80, windy - 80)
            self.rect.y = 0
            lost += 1
        

class Enemy2(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > windy:
            self.rect.x = randint(80, windy - 80)
            self.rect.y = 0

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

monsters = sprite.Group()

asteroids = sprite.Group()

for i in range(1,6):
    monetr = Enemy('ufo.png', randint(80, windx-80), -10, randint(1, 4))
    monsters.add(monetr)

player = Player('rocket.png', windx/2, windy - 65, 10)

meteor = Enemy2('asteroid.png', randint(80, windx-80), -10, 1)

asteroids.add(meteor)

cheat = False  

while playing:
    for e in event.get():
        if e.type == QUIT:
            playing = False
        if e.type == KEYDOWN:
            if overheat%5 != 0 or overheat == 0:
                if e.key == K_SPACE:
                    player.fire()
                    fire1.play()
                    overheat += 1
            if e.key == K_r:
                overheat = 0
            if e.key == K_1:
                cheat = True
            if e.key == K_2:
                cheat = False


    if not finsh:
        text_lose = font1.render('Пропущено: ' + str(lost), 1, (255,255,255))
        text = font1.render('Счет:' + str(win), 0 , (255,255,255))
        hp_bar = font1.render('Жизни: ' + str(health), 0 , (69,148,74))
        sprites_list = sprite.groupcollide(monsters, bullets, True, True)
        for i in sprites_list:
            win +=1
            monetr = Enemy('ufo.png', randint(80, windx-80), -10, randint(1, 4))
            monsters.add(monetr)
        asteroid_collide = sprite.groupcollide(asteroids, bullets, False, True)
        
        crash = sprite.spritecollide(player, monsters, True)
        for i in crash:
            health -= 1
        
        window.blit(background,(0,0))
        window.blit(text_lose, (0, 10))
        window.blit(text,(0, 40))
        window.blit(hp_bar,(570, 10))

        player.reset()
        player.update()
        if cheat == True:
            player.fire()
        monsters.draw(window)
        monsters.update()
        asteroids.draw(window)
        asteroids.update()
        bullets.draw(window)
        bullets.update()
        if lost == 3 or health == 0 or sprite.spritecollide(player, asteroids, False):
            text_proigral = font1.render('ИГРА ОКОНЧЕНА', 1, (255,0,0)) 
            window.blit(text_proigral,(250,225))
            finsh = True
        elif win == 2**64:
            text_win = font1.render('ТЫ ВЫЙГРАЛ!|\nМЕГАХОРОШ, ЛЕГЕНДАРЕН', 1, (255,0,0)) 
            window.blit(text_win,(100,100))
    else:
        finsh = True
        lost = 0
        win = 0
        health = 3
        overheat = 0
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
        for a in asteroids:
            a.kill()

        time.delay(10)

        for i in range(1,6):
            monetr = Enemy('ufo.png', randint(80, windx-80), -10, randint(1, 4))
            monsters.add(monetr)
        meteor = Enemy2('asteroid.png', randint(80, windx-80), -10, 1)
        asteroids.add(meteor)



    display.update()
    clock.tick(FPS)

    