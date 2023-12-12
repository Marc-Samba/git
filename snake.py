#importation des bibliothèques
import pygame
import argparse
import logging
import sys
import random as rd
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
FPS=10
TILE_SIZE=20
LINE=HEIGHT//TILE_SIZE
COLUMN=WIDTH//TILE_SIZE
UP=(0,-1) #la ligne 0 est en haut donc il faut retrancher 1 pour monter 
DOWN=(0,1)
RIGHT=(1,0)
LEFT=(-1,0)

#configuration du root logger 
logger = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stderr)
logger.addHandler(handler)
logger.setLevel(logging.INFO)
logger.setLevel(logging.DEBUG)

def read_args(): 
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
    parser.add_argument('--tile-size', type=int,default=TILE_SIZE, help='size of a square tile')
    parser.add_argument('--gameover-on-exit',help='quit the game if the snake is out of screen')

    #ajout argument debug 
    parser.add_argument('-g','--debug', help='débogage')

    args=parser.parse_args()
    print(args)

    #on vérifie les conditions

    if [(args.height)%(args.tile_size) !=0] or args.height//(args.tile_size)<12:
        raise ValueError
        logger.debug("la hauteur de l'écran n'est pas bonne.") 

    elif [(args.width)%(args.tile_size) !=0] or args.widht//(args.tile_size)<20:
        raise ValueError
        logger.debug("la largeur de l'écran n'est pas bonne.") 

    elif args.snake_length < 2:
        raise ValueError
        logger.warning("le serpent initial est trop court.")

    elif args.snake_color==args.bg_color_1 or args.snake_color==args.bg_color_2:
        raise ValueError
        logger.warning('la couleur du serpent est identique à celle du damier.')



#fonction qui termine le jeu si gameover on exit est passé en ligne de commande et loupe le snake sinon
def status_game(gameover_on_exit,serpent,hauteur,largeur,taillecase,run):
    if gameover_on_exit:
        #si on dépasse en haut ou en bas on quitte le jeu
        if serpent[-1][0]>=hauteur//taillecase or serpent[-1][0]<0:
            run=False
            logger.error('vous êtes sorti de la fenêtre de jeu')
        #si on dépasse sur les côtés on quitte le jeu
        elif serpent[-1][1]>=largeur//taillecase or serpent[-1][1]<0:
            run=False
            logger.error('vous êtes sorti de la fenêtre de jeu')
    else :
        #si on va trop bas on remonte la tête à la première ligne
        if serpent[-1][0]>=hauteur//taillecase: 
            head=(0,serpent[-1][1])
            serpent.pop()
            serpent.append(head)

        #si on va trop haut on redescend la tête à la dernière ligne
        elif serpent[-1][0] < 0 :  
            head=(hauteur//taillecase-1,serpent[-1][1])
            serpent.pop()
            serpent.append(head)

        #si on va trop à droite on ramène la tête tout à gauche
        elif serpent[-1][1]>=largeur//taillecase:
            head=(serpent[-1][0],0)
            serpent.pop()
            serpent.append(head)
        
        #si on va trop à gauche on ramène la tête tout à droite 
        elif serpent[-1][1]<0:
            head=(serpent[-1][0],largeur//taillecase-1)
            serpent.pop()
            serpent.append(head)

def collision(run, serpent):
    #copie du nouveau serpent
    snake_copy=serpent.copy() 

    #on extrait la nouvelle tête et on la supprime de la copie du snake
    new_headd=snake_copy.pop() 

    #on vérifie que la nouvelle tête ne partage pas la même case qu'un autre bout du corps
    if new_headd in snake_copy : 
        run=False

def draw_checkerboard(ecran,color1, color2,largeur,hauteur,taillecase):
    """affichage de l'écran"""
    #affichage de l'écran
    ecran.fill( color1 ) 
    m=hauteur//taillecase
    n=largeur//taillecase
    #dessin du checkboard
    for i in range(m):
        for j in range(n):
            if (i+j)%2==0:
                new_rect=pygame.Rect((j*taillecase,i*taillecase,taillecase,taillecase))
                pygame.draw.rect(ecran,color2,new_rect)

def draw_fruit(ecran,color_fruit,taillecase,Fruit):
    """affichage du fruit"""
    fruit_rect=pygame.Rect(Fruit[0]*taillecase,Fruit[1]*taillecase,taillecase,taillecase)
    pygame.draw.rect(ecran,color_fruit,fruit_rect)

def draw_snake(ecran,serpent,taillecase,couleur_serpent):
    """affichage du serpent"""
    for elem in serpent :
        point=pygame.Rect(elem[0]*taillecase,elem[1]*taillecase,taillecase,taillecase)
        pygame.draw.rect(ecran,couleur_serpent,point)
    
def draw(ecran,color1, color2,color_fruit,couleur_serpent,largeur,hauteur,taillecase,Fruit,serpent):
    #on appelle toutes les fonctions draw_* en leur passant leurs arguments respectifs
    
    #d'abord le checkerboard
    draw_checkerboard(color1, color2,largeur,hauteur,taillecase)

    #ensuite le fruit
    draw_fruit(ecran,color_fruit,taillecase,Fruit)

    #ensuite le serpent
    draw_snake(ecran,serpent,taillecase,couleur_serpent)


def process_event(run,Direction):
    for event in pygame.event.get():   #s'il y a un évènement 
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_q:
                run=False  #on quitte le jeu si q est pressé
                logger.critical('Vous avez quitté le jeu.')
            elif event.key==pygame.K_UP:
                Direction=UP
            elif event.key==pygame.K_DOWN:
                Direction=DOWN
            elif event.key==pygame.K_RIGHT:
                Direction=RIGHT
            elif event.key==pygame.K_LEFT:
                Direction=LEFT
        elif event.type==pygame.QUIT:
            run=False
            logger.critical('Vous avez quitté le jeu.')


def move_snake(serpent,Fruit,Direction):
    """on déplace le serpent"""
    if serpent[-1][0]==Fruit[0] and serpent[-1][1]==Fruit[1]: #si on rencontre le fruit on grandit donc on ne retire pas le dernier carré et on en ajoute un nouveau.
        new_head=tuple(x+y for x,y in zip(serpent[-1],Direction))
        serpent.append(new_head)
    else : #si on ne rencontre pas de fruit on fait avancer le serpent
        serpent.pop(0) 
        new_head=tuple(x+y for x,y in zip(serpent[-1],Direction))
        serpent.append(new_head)

def update_fruit(serpent,Fruit,hauteur,largeur):
    """créer aléatoirement un nouveau fruit quand le serpent en mange un """
    if serpent[-1][0]==Fruit[0] and serpent[-1][1]==Fruit[1]:
        Fruit[0]=rd.randint(0,hauteur-1)
        Fruit[1]=rd.randint(0,largeur-1)
        #on a update le fruit donc on renvoie vrai
        return True
    else:
        #on a pas update le fruit on renvoie faux
        return False

def get_score(booleen, score):
    #si on a update le fruit alors on modifie le score
    if booleen==True:
        score+=1
        

def update_display(ecran,color1, color2,color_fruit,couleur_serpent,largeur,hauteur,taillecase,Fruit,serpent,score):
    draw(ecran,color1, color2,color_fruit,couleur_serpent,largeur,hauteur,taillecase,Fruit,serpent)
    pygame.display.set_caption("Snake Pygame - Score: {}".format(score)) #mise à jour du score
    pygame.display.update() #mise à jour de l'écran

def main():
    #on lit les arguments et on vérifie les conditions
    read_args()
    #création de l'écran
    screen=pygame.display.set_mode((args.width,args.height))
    clock = pygame.time.Clock()
    pygame.display.set_caption("Snake - Score: 0")
    #état initial
    snake=[(5,10),(6,10),(7,10)]
    direction=RIGHT
    fruit=[3,3]
    Score=0
    running=True #flag
    while running:

        clock.tick(args.fps)
        #on process tous les évènements
        process_event(running,direction)

        #on fait avancer le serpent
        move_snake(snake,fruit,direction)

        #on compute le nouveau score si le serpent a mangé un fruit
        get_score(update_fruit,Score) 

        #on appelle la fonction status_game pour terminer le jeu où modifier la tête du serpent selon que l'on a passé l'argument gameover on exit ou non
        status_game(args.gameover_on_exit,snake,args.height,args.width,args.tile_size,running)  

        #on appelle la fonction collision pour vérifier que l'on ne se marche pas sur la queue 
        collision(running,snake)

        #on appelle la fonction update_display qui appelle draw et met à jour l'écran
        update_display(screen,args.bg_color_1,args.bg_color_2,args.fruit_color,args.snake_color,args.width,args.heigth,args.tile_size,fruit,snake,Score)

#on appelle main
main()