#importing libraries

import argparse
import pygame
import logging
import copy

                
class GameOfLife:
    def __init__(self, input, output, d, m, f, width, height):
        self.input = input
        self.output = output
        self._d = d
        self._m = m
        self._f = f
        self._width = width
        self._height = height
        self._current_state = None
        self._step=0 #count the number of steps
        

    def _create_matrice(self):
        """this function returns the matrice associated to the initial state of the game"""
        #initializing the matrix
        M = [[0 for _ in range(self._width)] for _ in range(self._height)]

        with open(self.input, 'r') as fichier:
            for i, ligne in enumerate(fichier):
                # Get rid of '\n'
                read_line = ligne.strip()

                # Add zeroes and ones to the matrix using index
                for j, car in enumerate(read_line):
                    M[i][j] = int(car)
        return(M)

            



    def _read_initial_state(self):
        """initialize the state of the game"""
        self._current_state = self._create_matrice()
        logging.info("Initial state read successfully.")
    
    def _count_neighbors(self, i, j):
        """receives the position of a cell and the matrice associated to the state of the game and return the number of living cells around it."""
    
        m=len(self._current_state)
        n=len(self._current_state[0])
        S=0

        #processing the corner cells
        if i==0 and j==0: #top left cell
            S+=self._current_state[0][1]+self._current_state[1][0]+self._current_state[1][1]
        elif i==0 and j==n-1: #top right cell
            S+=self._current_state[0][n-2]+self._current_state[1][n-2]+self._current_state[1][n-1]
        elif i==m-1 and j==0: #bottom left cell
            S+=self._current_state[m-2][0]+self._current_state[m-2][1]+self._current_state[m-1][1]
        elif i==m-1 and j==n-1: #bottom right cell
            S+=self._current_state[m-1][n-2]+self._current_state[m-2][n-2]+self._current_state[m-2][n-1]
        
        #processing the side cells
        
        #cells on top
        elif i==0 and 0<j<n-1: 
            S+=self._current_state[0][j-1]+self._current_state[1][j-1]+self._current_state[1][j]+self._current_state[1][j+1]+self._current_state[0][j+1]
        
        #cells on the bottom
        elif i==m-1 and 0<j<n-1: 
            S+=self._current_state[m-1][j-1]+self._current_state[m-2][j-1]+self._current_state[m-2][j]+self._current_state[m-2][j+1]+self._current_state[m-1][j+1]

        #cells on the left side
        elif j==0 and 0<i<m-1:
            S+=self._current_state[i-1][0]+self._current_state[i-1][1]+self._current_state[i][1]+self._current_state[i+1][1]+self._current_state[i+1][0]
        
        #cells on the right side
        elif j==n-1 and 0<i<m-1:
            S+=self._current_state[i-1][n-1]+self._current_state[i-1][n-2]+self._current_state[i][n-2]+self._current_state[i+1][n-2]+self._current_state[i+1][n-1]

        #processing the rest of the cells

        else :
            S+=self._current_state[i-1][j-1]+self._current_state[i][j-1]+self._current_state[i+1][j-1]+self._current_state[i+1][j]+self._current_state[i+1][j+1]+self._current_state[i][j+1]+self._current_state[i-1][j+1]+self._current_state[i-1][j]                              
        
        return(S)

    def _apply_rules(self, i, j):
        """returns the new state of a cell"""
        if self._current_state[i][j]==1: #the cell is alive
            if 1<self._count_neighbors(i,j)<4:
                return(1) #the cell stays alive
            else:
                return(0) #the cell dies
        else : # the cell is dead
            if self._count_neighbors(i,j)==3:
                return(1) #the cell becomes a living cell

    def _generate_next_state(self):
        """receives the current state of the game and return the new state having applied the rules"""
        m=len(self._current_state)
        n=len(self._current_state[0])
        M=copy.deepcopy(self._current_state) #we copy the matrix associated to the current state because we don't want to modify it. We need the same matrice to apply the rules every time
        for i in range (m):
            for j in range(n):
                M[i][j]=self._apply_rules(self._current_state,i,j) 
        #new state
        self._current_state=M
    
    def _empty_file(self):
        """return true if the file is empty or false if it isn't"""
        with open(self.output, 'r') as fichier:
            ligne = fichier.readline()
            return ligne == "" #return true if the output file is empty

    def _output_file(self):
        """takes the current state of the game and modifies the output file"""
        m=len(self._current_state)
        n=len(self._current_state[0])

        #if the file is empty : after step 1
        if self._empty_file():                                            
            with open(self.output, 'w') as fichier:                       #opening the output file in writing mode
                for i in range (m):
                    new_line=''                                           #creating a new line
                    for j in range(n):
                        new_line=new_line+str(self._current_state[i][j])  #adding all the 0 and 1 from the line on by one
                    fichier.write(new_line+'\n')
            logging.info("Output file completed.")

        #the file is already filed we modify it 
        else:
            with open(self.output,'w') as fichier:     #opening o_file in writing mode
                fichier.write('')                      #on vide de fichier de l'état précédent
                for ligne in self._current_state :
                    new_line= ''.join(map(str, ligne)) #on convertit les éléments de la liste en str et on les concatène
                    fichier.write(new_line+'\n')       #on ajoute la nouvelle ligne au fichier de sorti
            logging.info("Output file modified.")

    def run(self):
        self._read_initial_state()
        while self._step<self._m: #while the number of steps is inferior to the number of steps to run
            self._generate_next_state()
            self._output_file()
            self._step=self._step+1
            logging.info(f"Step {self._step} completed.")

class Pygame:
    def __init__(self,game_of_life):

        self.instance_gameoflife=game_of_life   #retrieve all the attributs and methods from the class GameOfLife
        
        pygame.init()

        self._screen = pygame.display.set_mode((self.instance_gameoflife._width, self.instance_gameoflife._height))

        self._clock = pygame.time.Clock()

        self._board = self._draw_board()

        self._run = True




    def _taillecase(self):
        taillecase=self.instance_gameoflife._height//len(self.instance_gameoflife._current_state) #provided that screen size and the file are appropriate (each cell is a square and all the cell cover the entire screen). We will have to check that 
        return taillecase
    
    def _cell_color(self,cell):
        """returns the white color if the cell is dead and black if it is alive"""
        if cell==0:     #the cell is dead we return white 
            return((255,255,255))                           
        else:           #the cell is alive we return black
            return((0,0,0))

    def _draw_board(self):
        """draws the current state using pygame"""
        m=len(self.instance_gameoflife._current_state)
        n=len(self.instance_gameoflife._current_state[0])
        SIZE=self._taillecase()
        for i in range (m):
            for j in range (n):
                new_rect=pygame.Rect((j*SIZE,i*SIZE,SIZE,SIZE))
                pygame.draw.rect(self._screen,self._cell_color(self.instance_gameoflife._current_state[i][j]),new_rect)
        logging.debug("Board drawn.")


    def _process_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._run=False
    
    def _update_display(self):
        #draw the state of the game
        self._draw_board()

        #update title with the current step 
        pygame.display.set_caption(f"My Pygame Window - Step: {self.instance_gameoflife._step}")

        #update display
        pygame.display.update()


    def start(self):
        """If d is activated start displays each state of the game"""

        #initialising the game
        self.instance_gameoflife._read_initial_state()

        while self.instance_gameoflife._step<self._m and self._run: #while the number of steps is inferior to the number of steps to run and run==True
            
            self._clock.tick(self.instance_gameoflife._f)
            #processing event
            self._process_event()

            #generating the next state
            self.instance_gameoflife._generate_next_state()

            #modifying the output file
            self.instance_gameoflife._output_file()
            
            #updating the number of step
            self.instance_gameoflife_step=self.instance_gameoflife_step+1

            #updating display
            self._update_display()

            logging.info(f"Display updated for step {self.instance_gameoflife._step}.")

        pygame.quit()



def read_args():

    #parser definition
    parser = argparse.ArgumentParser(description="An implementation of game of life")
    #adding all arguments

    parser.add_argument('--input', type=str, help='Path to the initial state file.')
    parser.add_argument('--output', type=str, help='Path to the output file.')
    parser.add_argument('-d',action='store_true', help='display flag')
    parser.add_argument('-m', default=20, help='Set the number of steps to run when display is off.')
    parser.add_argument('-f',default=10,help='number of frames per second to use with pygame.')
    parser.add_argument('--width',default=800, help='Set the width of the screen.')
    parser.add_argument('--height',default=600,help='Set the height of the screen')

    args = parser.parse_args()

    return args
    

def main():
    args = read_args()
    
    if args.d: 
        game_of_life= GameOfLife(args.input, args.output, args.d, args.m, args.f, args.width, args.height)
        game=Pygame(game_of_life)
        game.start()
    else :
        game = GameOfLife(args.input, args.output, args.d, args.m, args.f, args.width, args.height)
        game.run()

#configuring logging
logging.basicConfig(level=logging.DEBUG)

#Create a logger for this module
logger = logging.getLogger(__name__)

if __name__=="__main__": 
    main()

