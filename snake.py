#importation des bibliotheques
import pygame
import argparse
#initialisation des modules
pygame.init() 

#constantes
WIDTH=400
HEIGHT=300
SCREEN_COLOR1=(0,0,0)
SCREEN_COLOR2=(255,255,255)
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


#on ajoute tous les arguments 
parser = argparse.ArgumentParser(description='Some description.')
parser.add_argument('--bg-color-1',default=SCREEN_COLOR1, help=' first color of the background checkerboard.')
parser.add_argument('--bg-color-2',default=SCREEN_COLOR2,help='second color of the background checkerboard')
parser.add_argument('--height',default=HEIGHT,type=int, help='window height')
parser.add_argument('--width',default=WIDTH,type=int, help='window width')
parser.add_argument('--fps',type=int,default=FPS, help='number of frames per second')
parser.add_argument('--fruit-color',default=FRUIT_COLOR,help='color of the fruit')
parser.add_argument('--snake-color',default=SNAKE_COLOR,help='snake color')
parser.add_argument('--snake-length',type=int, help='initial length of the snake')
parser.add_argument('--tile-size', type=int, help='size of a square tile')
parser.add_argument('--gameover-on-exit',help='quit the game if the snake is out of screen and ')
args=parser.parse_args()
print(args)

#on vérifie les conditions

if [(args.height)%(args.tile_size) !=0] or args.height//(args.tile_size)<12:
    raise ValueError
elif [(args.width)%(args.tile_size) !=0] or args.widht//(args.tile_size)<20:
    raise ValueError
elif args.snake_length < 2:
    raise ValueError
elif args.snake_color==args.bg_color_1 or args.snake_color==args.bg_color_2:
    raise ValueError




#fruits pour l'étape où le serpent mange successivement deux fruits prédéfinis
fruit1=(3,3)
fruit2=(15,10)

#création de l'écran
screen=pygame.display.set_mode((args.width,args.height))
clock = pygame.time.Clock()
pygame.display.set_caption("Snake - Score: 0")
#état initial
snake=[(5,10),(6,10),(7,10)]
direction=RIGHT
fruit=fruit1
Score=0

running=True #flag
while running:

    clock.tick(args.fps)

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
    screen.fill( args.bg_color_1 ) 

    #dessin du checkboard
    for i in range(LINE):
        for j in range(COLUMN):
            if (i+j)%2==0:
                new_rect=pygame.Rect((j*args.tile_size,i*args.tile_size,args.tile_size,args.tile_size))
                pygame.draw.rect(screen,args.bg_color_2,new_rect)
    
    #affichage du fruit
    fruit_rect=pygame.Rect(fruit[0]*args.tile_size,fruit[1]*args.tile_size,args.tile_size,args.tile_size)
    pygame.draw.rect(screen,args.fruit_color,fruit_rect)
    
    
    #affichage du serpent
    for elem in snake :
        point=pygame.Rect(elem[0]*args.tile_size,elem[1]*args.tile_size,args.tile_size,args.tile_size)
        pygame.draw.rect(screen,args.snake_color,point)
    
    
    #mise à jour de l'écran
    pygame.display.update()