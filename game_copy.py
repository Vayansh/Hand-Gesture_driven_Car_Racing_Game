import pygame
pygame.init()
gray=(119,118,110)
black=(0,0,0)
red=(255,0,0)
green=(0,200,0)
blue=(0,0,200)
bright_red=(255,0,0)
bright_green=(0,255,0)
bright_blue=(0,0,255)
display_width=800
display_height=600
import time
import random
import cv2
import numpy as np
import os
import threading

# from yolo_predictions import YOLO_Pred



cap=cv2.VideoCapture(0)
# yolo = YOLO_Pred(r"/home/gourav/Desktop/vss/edge-embedded/best.onnx")

def prediction_key():
    global cap
    _, image = cap.read()

    image = cv2.flip(image, 1)
    # image = yolo.predictions(image)    
    cv2.imshow("camera",image)




gamedisplays=pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption("car game")
clock=pygame.time.Clock()
carimg=pygame.image.load('images/car1.jpg')
backgroundpic=pygame.image.load("images/grass.jpg")
yellow_strip=pygame.image.load("images/yellow_strip.jpg")
strip=pygame.image.load("images/strip.jpg")
intro_background=pygame.image.load("images/background.jpg")
instruction_background=pygame.image.load("images/background2.jpg")
car_width=56
pause=False

def capture_screen():
    screen_shot = pygame.surfarray.array3d(gamedisplays)
    # Convert RGB to BGR (OpenCV uses BGR)
    screen_shot = np.swapaxes(screen_shot, 0, 1)
    return cv2.cvtColor(screen_shot, cv2.COLOR_RGB2BGR)

def obstacle(obs_startx,obs_starty,obs):
    if obs==0:
        obs_pic=pygame.image.load("images/car1.jpg")
    elif obs==1:
        obs_pic=pygame.image.load("images/car2.jpg")
    elif obs==2:
        obs_pic=pygame.image.load("images/car2.jpg")
    elif obs==3:
        obs_pic=pygame.image.load("images/car4.jpg")
    elif obs==4:
        obs_pic=pygame.image.load("images/car5.jpg")
    elif obs==5:
        obs_pic=pygame.image.load("images/car6.jpg")
    elif obs==6:
        obs_pic=pygame.image.load("images/car7.jpg")
    gamedisplays.blit(obs_pic,(obs_startx,obs_starty))

def score_system(passed,score):
    font=pygame.font.SysFont(None,25)
    text=font.render("Passed"+str(passed),True,black)
    score=font.render("Score"+str(score),True,red)
    gamedisplays.blit(text,(0,50))
    gamedisplays.blit(score,(0,30))


def text_objects(text,font):
    textsurface=font.render(text,True,black)
    return textsurface,textsurface.get_rect()

def message_display(text):
    largetext=pygame.font.Font("freesansbold.ttf",80)
    textsurf,textrect=text_objects(text,largetext)
    textrect.center=((display_width/2),(display_height/2))
    gamedisplays.blit(textsurf,textrect)
    pygame.display.update()
    cv2.imshow("window",capture_screen())
    cv2.waitKey(1)
    time.sleep(3)
    game_loop()


def crash():
    message_display("YOU CRASHED")


def background():
    gamedisplays.blit(backgroundpic,(0,0))
    gamedisplays.blit(backgroundpic,(0,200))
    gamedisplays.blit(backgroundpic,(0,400))
    gamedisplays.blit(backgroundpic,(700,0))
    gamedisplays.blit(backgroundpic,(700,200))
    gamedisplays.blit(backgroundpic,(700,400))
    gamedisplays.blit(yellow_strip,(400,0))
    gamedisplays.blit(yellow_strip,(400,100))
    gamedisplays.blit(yellow_strip,(400,200))
    gamedisplays.blit(yellow_strip,(400,300))
    gamedisplays.blit(yellow_strip,(400,400))
    gamedisplays.blit(yellow_strip,(400,500))
    gamedisplays.blit(strip,(120,0))
    gamedisplays.blit(strip,(120,100))
    gamedisplays.blit(strip,(120,200))
    gamedisplays.blit(strip,(680,0))
    gamedisplays.blit(strip,(680,100))
    gamedisplays.blit(strip,(680,200))

def car(x,y):
    gamedisplays.blit(carimg,(x,y))

def game_loop():
    global pause
    x=(display_width*0.45)
    y=(display_height*0.8)
    x_change=0
    obstacle_speed=9
    obs=0
    y_change=0
    obs_startx=random.randrange(200,(display_width-200))
    obs_starty=-750
    obs_width=56
    obs_height=125
    passed=0
    level=0
    score=0
    y2=7
    fps=120

    bumped=False
    while not bumped:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                cap.release()
                cv2.destroyAllWindows()
                pygame.quit()
                quit()

            # t1 = threading.Thread(target=prediction_key)
            # t1.start()
            # global cap
            
            # if k == ord('q'):
                # break

            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_LEFT:
                    x_change=-5
                if event.key==pygame.K_RIGHT:
                    x_change=5
                if event.key==pygame.K_a:
                    obstacle_speed+=2
                if event.key==pygame.K_b:
                    obstacle_speed-=2
       
            if event.type==pygame.KEYUP:
                if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT:
                    x_change=0
        _, image = cap.read()

        image = cv2.flip(image, 1)
        # image = yolo.predictions(image)    
        cv2.imshow("camera",image)
        # cv2.waitKey(1)
        x+=x_change
        pause=True
        gamedisplays.fill(gray)

        rel_y=y2%backgroundpic.get_rect().width
        gamedisplays.blit(backgroundpic,(0,rel_y-backgroundpic.get_rect().width))
        gamedisplays.blit(backgroundpic,(700,rel_y-backgroundpic.get_rect().width))
        if rel_y<800:
            gamedisplays.blit(backgroundpic,(0,rel_y))
            gamedisplays.blit(backgroundpic,(700,rel_y))
            gamedisplays.blit(yellow_strip,(400,rel_y))
            gamedisplays.blit(yellow_strip,(400,rel_y+100))
            gamedisplays.blit(yellow_strip,(400,rel_y+200))
            gamedisplays.blit(yellow_strip,(400,rel_y+300))
            gamedisplays.blit(yellow_strip,(400,rel_y+400))
            gamedisplays.blit(yellow_strip,(400,rel_y+500))
            gamedisplays.blit(yellow_strip,(400,rel_y-100))
            gamedisplays.blit(strip,(120,rel_y-200))
            gamedisplays.blit(strip,(120,rel_y+20))
            gamedisplays.blit(strip,(120,rel_y+30))
            gamedisplays.blit(strip,(680,rel_y-100))
            gamedisplays.blit(strip,(680,rel_y+20))
            gamedisplays.blit(strip,(680,rel_y+30))

        y2+=obstacle_speed




        obs_starty-=(obstacle_speed/4)
        obstacle(obs_startx,obs_starty,obs)
        obs_starty+=obstacle_speed
        car(x,y)
        score_system(passed,score)
        if x>690-car_width or x<110:
            crash()
        if x>display_width-(car_width+110) or x<110:
            crash()
        if obs_starty>display_height:
            obs_starty=0-obs_height
            obs_startx=random.randrange(170,(display_width-170))
            obs=random.randrange(0,7)
            passed=passed+1
            score=passed*10
            if int(passed)%10==0:
                level=level+1
                obstacle_speed+2
                largetext=pygame.font.Font("freesansbold.ttf",80)
                textsurf,textrect=text_objects("LEVEL"+str(level),largetext)
                textrect.center=((display_width/2),(display_height/2))
                gamedisplays.blit(textsurf,textrect)
                pygame.display.update()
                time.sleep(3)


        if y<obs_starty+obs_height:
            if x > obs_startx and x < obs_startx + obs_width or x+car_width > obs_startx and x+car_width < obs_startx+obs_width:
                crash()
        # button("Pause",650,0,150,50,blue,bright_blue,"pause")
        pygame.display.update()
        clock.tick(60)
        cv2.imshow("window",capture_screen())
        cv2.waitKey(1)


if __name__ == '__main__':
    game_loop()
    pygame.quit()
    quit()