import pygame as py
from pygame import mixer as mx
import random as r
import copy as c
import math
py.init()

#game_over is the variable that controlls if the game window is running
game_over = False

score = 0

textx = 10
texty = 5


didcollisionhappen = 0
didcollisionhappen1 = 0
didcollisionhappen2 = 0
didcollisionhappen3 = 0

font0 = py.font.Font("freesansbold.ttf",32)

#screen is the variable of the display
screen = py.display.set_mode((700,700))

#the variable that controlls the name of the window
caption = py.display.set_caption("Space invaders")



#loading in the music
mx.init()
mx.music.load(r"background.wav")
mx.music.set_volume(0.5)
mx.music.play()

#loading in the background image, icon image and setting them to be the same
Bg = py.image.load("background.png")
Bg = py.transform.scale(Bg,(700,700))

icon_image = py.image.load("ufo.png")
icon = py.display.set_icon(icon_image)

#these are the coords of the player on the x axis and y axis
coordsx = 325
coordsy = 600

# ecoordsx = r.randint(1,700)
# ecoordsy = r.randint(1,100)

#these are the starting coords of the enemy
ecoordsx = 100
ecoordsy = 0

#loading in the images for the bullet, enemy and player
ammo = py.image.load(r"bullet.png")
enem = py.image.load(r"enemy.png")
rocket =  py.image.load(r"player.png")

#making functions to put them on the screen
def player(image,x,y):
    screen.blit(image,(x,y))
playerxchange = 0

def bullet(image,x,y):
    screen.blit(image,(x,y))
    bullet_state = 0
bulletychange = 0
bullet_state = 0
n_coordsy = 625

def enemy(image,x,y):
    screen.blit(image,(x,y))
enemyxchange = 5
enemyychange = 0

font1 = py.font.SysFont("COMIC.TTF", 100)


def scoreboard(textx,texty,gameOverMessage):
    tex = font0.render("score:" + str(gameOverMessage),True,(255,255,255))
    screen.blit(tex,(textx,texty))


def game_message():
    text = font1.render("Game Over",True,(255,255,255))
    screen.blit(text,(150,300))

def collision(enemyX,bulletX,enemyY,bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2)+ math.pow(enemyY - bulletY, 2))
    if distance <= 50:
        return 1
    else:
        return 0

#the game loop, this makes the game run
while game_over is not True:
    screen.blit(Bg,(0,0))
    
    #getting the events
    for event in py.event.get():
    
        #if the event is quit (if the red cross is pressed), game_over = true
        if event.type == py.QUIT:
            game_over = True
    
        #checking for the keys pressed
        if event.type == py.KEYDOWN:
    
            #if the key pressed is the left arrow, the player coordsx -= 1 and if the right key is pressed, players coordsx is += 1
            if event.key == py.K_LEFT:
                playerxchange = -1
                rocket = py.transform.rotate(rocket,90)
                screen.blit(rocket,(coordsx,coordsy))
            if event.key == py.K_RIGHT:
                playerxchange = 1
                rocket = py.transform.rotate(rocket,-90)
                screen.blit(rocket,(coordsx,coordsy))
    
            #if the event is space, n_coordsx = coordsx
            if event.key == py.K_SPACE:
                bullet_state = 1
                if bullet_state == 1:
                    n_coordsx = coordsx
                mx.music.load(r"laser.wav")
                mx.music.set_volume(1)
                mx.music.play()
    
        #checking events for when the key goes up
        elif event.type == py.KEYUP:
            if (event.key == py.K_LEFT) or (event.key == py.K_RIGHT):
                playerxchange = 0
            if event.key == py.K_LEFT:
                rocket = py.transform.rotate(rocket,-90)
                screen.blit(rocket,(coordsx,coordsy))

            if event.key == py.K_RIGHT:
                rocket = py.transform.rotate(rocket,90)
                screen.blit(rocket,(coordsx,coordsy))


    #making coordsx += or -= 1 depeding on what key was pressed
    coordsx = coordsx+playerxchange
    
    didcollisionhappen = collision(ecoordsx,coordsx,ecoordsy,n_coordsy)
    if score > 10:
        didcollisionhappen1 = collision(ecoordsx*1.4 - 40,coordsx,ecoordsy*1.3 + 35, n_coordsy)
    if score > 20:
        didcollisionhappen2 = collision(ecoordsx*0.6 + 50,coordsx,ecoordsy*0.69 + 35,n_coordsy)
    if score > 35:
        didcollisionhappen3 = collision(ecoordsx*0.4,coordsx,ecoordsy*0.3 + 5,n_coordsy)
    # didcollisionhappen = collision(ecoordsx*0.04 - 4,coordsx,ecoordsy*0.03 + 3,n_coordsy)
    # didcollisionhappen = collision(ecoordsx*1.8 - 40,coordsx,ecoordsy*1.7 + 35,n_coordsy)
    if (didcollisionhappen == 1) or (didcollisionhappen1 == 1) or (didcollisionhappen2 == 1) or (didcollisionhappen3 == 1):
        mx.music.load(r"explosion.wav")
        mx.music.set_volume(1)
        mx.music.play()
        score += 1



    scoreboard(textx,texty,score)
    #making sure the player can't leave the game window
    if coordsx < 50:
        coordsx = 50
    if coordsx > 650:
        coordsx = 650
    
    #putting the player on the screen
    player(rocket,coordsx,coordsy)
    
    #enemy logic
    ecoordsx = ecoordsx + enemyxchange
    if ecoordsx < 0:
        enemyxchange = 5
        ecoordsy = ecoordsy + 50
    if ecoordsx > 625:
        enemyxchange = -5
        ecoordsy = ecoordsy + 50
    
    if bullet_state == 1:
        #n_coordsy = coordsy
        bullet(ammo,n_coordsx+36.5,n_coordsy+10)
        bullet(ammo,n_coordsx-5,n_coordsy+10)
        n_coordsy -= 10
        if n_coordsy <= 0:
            bullet_state = 0
            # n_coordsy = coordsx
            n_coordsy = coordsy

    #putting the enemy and bullets on the screen
    enemy(enem,ecoordsx,ecoordsy)
    bullet(ammo,coordsx-5,coordsy+5)
    bullet(ammo,coordsx+36.5,coordsy+5)
    if score >= 10:
        enemy(enem,ecoordsx*1.4 - 40,ecoordsy*1.3 + 35)
    if score >= 20:
        enemy(enem,ecoordsx*0.6 + 50,ecoordsy*0.69 + 35)
    if score >= 35:
        enemy(enem,ecoordsx*0.4,ecoordsy*0.3 + 5)

    # if ecoordsy or (ecoordsy*1.3 + 35) or (ecoordsy*0.69 + 35) or (ecoordsy*0.3 + 5) > 800:
        # print("game over")
    if ecoordsy > 650:
        game_message()
    # if score >= 50:
    #     enemy(enem,ecoordsx*0.04 - 4,ecoordsy*0.03 + 3)
    # if score >= 60:
    #     enemy(enem,ecoordsx*1.8 - 40,ecoordsy*1.7 + 35)
    #updating display




    py.display.update()