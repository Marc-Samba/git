#importation des bibliotheques
import pygame
#initialisation des modules
pygame.init() 
#constantes

WIDTH=400
HEIGHT=300
SCREEN_COLOR=(0,0,0)
SNAKE_COLOR=(0,255,0)
WHITE=(255,255,255)
FPS=20
TILE_SIZE=20
LINE=HEIGHT//TILE_SIZE
COLUMN=WIDTH//TILE_SIZE

#création de l'écran
screen=pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()

#snake de départ
snake=[(5,10),(6,10),(7,10)]

running=True #flag
while running:

    clock.tick(FPS)

    for event in pygame.event.get():   #s'il y a un évènement 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running=False
        elif event.type==pygame.QUIT:
            running=False

    #affichage de l'écran
    screen.fill( SCREEN_COLOR ) 
    #dessin du checkboard
    for i in range(LINE):
        for j in range(COLUMN):
            if (i+j)%2==0:
                new_rect=pygame.Rect((j*TILE_SIZE,i*TILE_SIZE,TILE_SIZE,TILE_SIZE))
                pygame.draw.rect(screen,WHITE,new_rect)
    
    #affichage du serpent
    for elem in snake :
        point=pygame.Rect(elem[0]*TILE_SIZE,elem[1]*TILE_SIZE,TILE_SIZE,TILE_SIZE)
        pygame.draw.rect(screen,SNAKE_COLOR,point)

        
    
    #mise à jour de l'écran
    pygame.display.update()