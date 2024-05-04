import pygame
import time
import random
import cv2
import numpy as np
import os
import cvzone
import math
from ultralytics import YOLO
from server import server

cap=cv2.VideoCapture(0)
model = YOLO('best.pt')
className = ['left','right']

ip_add = input("Enter the IP address Where you want to stream")

server_c = server(ip_add)


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
    server_c.place_frame(capture_screen())

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

def get_predictions(img):
    results = model(img,stream= True)
    ultimate_cls = -1
    max_conf = 0
    for r in results:
        boxes = r.boxes
        for box in boxes:
            x1,y1,x2,y2 =  box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            cvzone.cornerRect(img,(x1,y1,(x2-x1),(y2-y1)),8,colorR=(255,0,0),colorC=(0,255,0))
            cls = className[int(box.cls[0])]
            conf = math.ceil(box.conf[0]*100)/100
            cvzone.putTextRect(img,f'{cls} {conf}',(max(0,x1),max(35,y1-20)),
                               scale=0.8, thickness=1)
            if max_conf < conf:
                max_conf = conf
                ultimate_cls = cls
    return img, ultimate_cls

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
        #     if event.type==pygame.KEYDOWN:
        #         if event.key==pygame.K_LEFT:
        #             x_change=-5
        #         if event.key==pygame.K_RIGHT:
        #             x_change=5
        #         if event.key==pygame.K_a:
        #             obstacle_speed+=2
        #         if event.key==pygame.K_b:
        #             obstacle_speed-=2
       
        #     if event.type==pygame.KEYUP:
        #         if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT:
        #             x_change=0

        _, image = cap.read()
        image = cv2.flip(image, 1)
        image, direction = get_predictions(image)    
        cv2.imshow("camera",image)
        cv2.waitKey(1)
        
        if direction == 'left':
            x_change=-5
        elif direction == 'right':
            x_change=5
        else:   
            x_change = 0
        
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
        pygame.display.update()
        clock.tick(60)
        server_c.place_frame(capture_screen())


if __name__ == '__main__':
    game_loop()
    pygame.quit()
    quit()
