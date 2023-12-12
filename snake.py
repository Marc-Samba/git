#importation des bibliotheques
import pygame
#initialisation des modules
pygame.init() 
#constantes
WIDTH=400
HEIGHT=300
SCREEN_COLOR=(0,0,0)
FPS=20
#création de l'écran
screen=pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()

running=True #flag
while running:

    clock.tick(FPS)

    for event in pygame.event.get():   #s'il y a un évènement 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running=False
        elif event.type==pygame.QUIT:
            running=False

    
    screen.fill( SCREEN_COLOR ) #affichage de l'écran

    pygame.display.update()