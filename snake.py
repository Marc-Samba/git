#importation des bibliotheques
import pygame
#initialisation des modules
pygame.init() 
#constantes

WIDTH=400
HEIGHT=300
SCREEN_COLOR=(0,0,0)
SNAKE_COLOR=(0,255,0)
FRUIT_COLOR=(255,0,0)
WHITE=(255,255,255)
FPS=3
TILE_SIZE=20
LINE=HEIGHT//TILE_SIZE
COLUMN=WIDTH//TILE_SIZE
UP=(0,-1) #la ligne 0 est en haut donc il faut retrancher 1 pour monter 
DOWN=(0,1)
RIGHT=(1,0)
LEFT=(-1,0)

fruit1=(3,3)
fruit2=(15,10)

#création de l'écran
screen=pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Snake - Score: 0")
#état initial
snake=[(5,10),(6,10),(7,10)]
direction=RIGHT
fruit=fruit1
Score=0

running=True #flag
while running:

    clock.tick(FPS)

    for event in pygame.event.get():   #s'il y a un évènement 
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_q:
                running=False  #on quitte le jeu si q est pressé

            elif event.key==pygame.K_UP:
                direction=UP
            elif event.key==pygame.K_DOWN:
                direction=DOWN
            elif event.key==pygame.K_RIGHT:
                direction=RIGHT
            elif event.key==pygame.K_LEFT:
                direction=LEFT
        elif event.type==pygame.QUIT:
            running=False

    #nouveau serpent
    if snake[-1]==fruit1: #si on rencontre le fruit 1 on grandit donc on ne retire pas le dernier carré et on en ajoute un nouveau
        new_head=tuple(x+y for x,y in zip(snake[-1],direction))
        snake.append(new_head)
        fruit=fruit2
        Score+=1
        pygame.display.set_caption("Snake Pygame - Score: {}".format(Score)) #mise à jour du score

    elif snake[-1]==fruit2: #si on rencontre le fruit 2 on grandit donc on ne retire pas le dernier carré et on en ajoute un nouveau
        new_head=tuple(x+y for x,y in zip(snake[-1],direction))
        snake.append(new_head)
        fruit=fruit1
        Score+=1
        pygame.display.set_caption("Snake Pygame - Score: {}".format(Score)) #mise à jour du score
    
    else : 
        snake.pop(0) 
        new_head=tuple(x+y for x,y in zip(snake[-1],direction))
        snake.append(new_head)
        
    #affichage de l'écran
    screen.fill( SCREEN_COLOR ) 

    #dessin du checkboard
    for i in range(LINE):
        for j in range(COLUMN):
            if (i+j)%2==0:
                new_rect=pygame.Rect((j*TILE_SIZE,i*TILE_SIZE,TILE_SIZE,TILE_SIZE))
                pygame.draw.rect(screen,WHITE,new_rect)
    
    #affichage du fruit
    fruit_rect=pygame.Rect(fruit[0]*TILE_SIZE,fruit[1]*TILE_SIZE,TILE_SIZE,TILE_SIZE)
    pygame.draw.rect(screen,FRUIT_COLOR,fruit_rect)
    
    
    #affichage du serpent
    for elem in snake :
        point=pygame.Rect(elem[0]*TILE_SIZE,elem[1]*TILE_SIZE,TILE_SIZE,TILE_SIZE)
        pygame.draw.rect(screen,SNAKE_COLOR,point)
    
    
    #mise à jour de l'écran
    pygame.display.update()