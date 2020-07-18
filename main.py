import sys
from pygame import *
import time as timePython

# main configs
init()

width = 640
height = 480

bgColor = (35, 30, 105) #rgb format

fps = time.Clock()

key.set_repeat(1)

score = 0
lifes = 3
waitOut = True

#ball
class Ball(sprite.Sprite):
    def __init__(self):
        sprite.Sprite.__init__(self)
        # load image/sprite
        self.image = image.load('resources/ball.png')
        # get object
        self.rect = self.image.get_rect()
        #center
        self.rect.centery = height / 2
        self.rect.centerx = width / 2
        # assign main speed
        self.speed = [3,3]

    def update(self):
        # check if the ball its outside the limits
        if self.rect.top <= 0:
            self.speed[1] = -self.speed[1]
        elif self.rect.right >= width or self.rect.left <= 0:
            self.speed[0] = -self.speed[0]
        # move in base to a actual pos and speed
        self.rect.move_ip(self.speed)

class Platform(sprite.Sprite):
    def __init__(self):
        sprite.Sprite.__init__(self)
        # load image/sprite
        self.image = image.load('resources/platform.png')
        # get object
        self.rect = self.image.get_rect()
        # intial pos
        self.rect.midbottom = (width / 2, height - 20)
        # assign main speed
        self.speed = [0, 0]

    def update(self, event):
        if event.key == K_LEFT and self.rect.left > 0:
            self.speed = [-5, 0]
        elif event.key == K_RIGHT and self.rect.right < width:
            self.speed = [5, 0]
        else:
            self.speed = [0, 0]
        self.rect.move_ip(self.speed)

class Brick(sprite.Sprite):
    def __init__(self, position):
        sprite.Sprite.__init__(self)
        # load image
        self.image = image.load('resources/brick.png')
        self.rect = self.image.get_rect()
        # first position
        self.rect.topleft = position

class Wall(sprite.Group):
    def __init__(self, quantity):
        sprite.Group.__init__(self)

        posX = 0
        posY = 20

        for _ in range(quantity):
            brick = Brick((posX, posY))
            self.add(brick)

            posX += brick.rect.width

            if posX >= width:
                posX = 0
                posY += brick.rect.height

def gameOver():
    fontConfig = font.SysFont('Arial', 72)
    text = fontConfig.render('Game Over!', True, (255, 255, 255))
    textRect = text.get_rect()
    textRect.center = [width / 2, height / 2]
    window.blit(text, textRect)
    display.flip()
    timePython.sleep(3)
    sys.exit()

def showScore():
    fontConfig = font.SysFont('Consolas', 20)
    text = fontConfig.render(str(score).zfill(5), True, (255, 255, 255))
    textRect = text.get_rect()
    textRect.topleft = [width / 2, 5]
    window.blit(text, textRect)
    display.flip()

def showLifes():
    fontConfig = font.SysFont('Consolas', 20)
    string = f'Lifes: {lifes}'
    text = fontConfig.render(string, True, (255, 255, 255))
    textRect = text.get_rect()
    textRect.topright = [width, 0]
    window.blit(text, textRect)
    display.flip()


# initialize
window = display.set_mode((width, height))
display.set_caption('breakout game')

ball = Ball()
platform = Platform()
wall = Wall(100)

# keep the display
while True:
    # set the fps cap
    fps.tick(60)

    for events in event.get():
        if events.type == QUIT:
            sys.exit()
        elif events.type == KEYDOWN:
            platform.update(events)
            if waitOut == True and events.key == K_SPACE:
                waitOut = False
                if ball.rect.centerx < width / 2:
                    ball.speed = [3, -3]
                else:
                    ball.speed = [3, 3]

    # update the pos in display
    if waitOut == False:
        ball.update()
    else:
        ball.rect.midbottom = platform.rect.midtop

    # collision
    if sprite.collide_rect(ball, platform):
        ball.speed[1] = -ball.speed[1]

    listCollide = sprite.spritecollide(ball, wall, False)
    if listCollide:
        brick = listCollide[0]
        cx = ball.rect.centerx
        if cx < brick.rect.left or cx > brick.rect.right:
            ball.speed[0] = -ball.speed[0]
        else:
            ball.speed[1] = -ball.speed[1]
        wall.remove(brick)
        score += 1

    # check if the ball is out of the borders
    if ball.rect.top > height:
        lifes -= 1
        waitOut = True

    # change the bg color
    window.fill(bgColor)

    #show score and lifes
    showScore()
    showLifes()

    # draw the ball in the display
    window.blit(ball.image, ball.rect)
    window.blit(platform.image, platform.rect)
    # draw bricks
    wall.draw(window)

    display.flip()

    if lifes <= 0:
        gameOver()