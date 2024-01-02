#importing libraries

import argparse
import pygame
import logging
import copy


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




def create_self.current_state(state_file):
   

def count_neighbors(i,j,self.current_state):
    """receives the position of a cell and the self.current_state associated to the state of the game and return the number of living cells around it."""
    
    m=len(self.current_state)
    n=len(self.current_state[0])
    S=0

    #processing the corner cells
    if i==0 and j==0: #top left cell
        S+=self.current_state[0][1]+self.current_state[1][0]+self.current_state[1][1]
    elif i==0 and j==n-1: #top right cell
        S+=self.current_state[0][n-2]+self.current_state[1][n-2]+self.current_state[1][n-1]
    elif i==m-1 and j==0: #bottom left cell
        S+=self.current_state[m-2][0]+self.current_state[m-2][1]+self.current_state[m-1][1]
    elif i==m-1 and j==n-1: #bottom right cell
        S+=self.current_state[m-1][n-2]+self.current_state[m-2][n-2]+self.current_state[m-2][n-1]
    
    #processing the side cells
    
    #cells on top
    elif i==0 and 0<j<n-1: 
        S+=self.current_state[0][j-1]+self.current_state[1][j-1]+self.current_state[1][j]+self.current_state[1][j+1]+self.current_state[0][j+1]
    
    #cells on the bottom
    elif i==m-1 and 0<j<n-1: 
        S+=self.current_state[m-1][j-1]+self.current_state[m-2][j-1]+self.current_state[m-2][j]+self.current_state[m-2][j+1]+self.current_state[m-1][j+1]

    #cells on the left side
    elif j==0 and 0<i<m-1:
        S+=self.current_state[i-1][0]+self.current_state[i-1][1]+self.current_state[i][1]+self.current_state[i+1][1]+self.current_state[i+1][0]
    
    #cells on the right side
    elif j==n-1 and 0<i<m-1:
        S+=self.current_state[i-1][n-1]+self.current_state[i-1][n-2]+self.current_state[i][n-2]+self.current_state[i+1][n-2]+self.current_state[i+1][n-1]

    #processing the rest of the cells

    else :
        S+=self.current_state[i-1][j-1]+self.current_state[i][j-1]+self.current_state[i+1][j-1]+self.current_state[i+1][j]+self.current_state[i+1][j+1]+self.current_state[i][j+1]+self.current_state[i-1][j+1]+self.current_state[i-1][j]                              
    
    return(S)


def rules(ind_ligne,ind_col,Mat):
    """reçoit une cellule indiquée par sa position ainsi que la matrice associée à l'état actuel du jeu et renvoie l'état ( 0 ou 1 ) de la nouvelle cellule en appliquant les règles """
    if Mat[ind_ligne][ind_col]==1: #the cell is alive
        if 1<count_neighbors(ind_ligne,ind_col,Mat)<4:
            return(1) #the cell stays alive
        else:
            return(0) #the cell dies
    else : # the cell is dead
        if count_neighbors(ind_ligne,ind_col,Mat)==3:
            return(1) #the cell becomes a living cell



def new_mat(self.current_state):
    """receives the self.current_state associated to the state of the game and return the new self.current_state having applied the rules"""
    m=len(self.current_state)
    n=len(self.current_state[0])
    M=copy.deepcopy(self.current_state) #we copy the self.current_state because we don't want to modify it. We need the same self.current_state to apply the rules() fucntion every time
    for i in range (m):
        for j in range(n):
            M[i][j]=rules(i,j,self.current_state) 
    return (M)


def empty_file(file):
    with open(file, 'r') as fichier:
        ligne = fichier.readline()
        return ligne == "" #return true if the file is empty
    
def output_file(self.current_state,o_file):
    """reçoit la matrice correspondant au nouvelle état et modifie le fichier de sortie"""
    m=len(self.current_state)
    n=len(self.current_state[0])

    if empty_file(o_file):                 #the file is empty : after step 1
        with open(o_file, 'w') as fichier: #opening o_file in writing mode
            for i in range (m):
                new_line=''                #creating a new line
                for j in range(n):
                    new_line=new_line+str(self.current_state[i][j])  #adding all the 0 and 1 from the line on by one
                fichier.write(new_line+'\n')

    #the file is already filed we modify it 
    else:
        with open(o_file,'w') as fichier:          #opening o_file in writing mode
            fichier.write('')                      #on vide de fichier de l'état précédent
            for ligne in self.current_state :
                new_line= ''.join(map(str, ligne)) #on convertit les éléments de la liste en str et on les concatène
                fichier.write(new_line+'\n')       #on ajoute la nouvelle ligne au fichier de sorti


class GameOfLife:
    def __init__(self, input, output, d, m, f, width, height):
        self.input = input
        self.output = output
        self.d = d
        self.m = m
        self.f = f
        self.width = width
        self.height = height
        self.current_state = None

    def create_matrice(self):
        """this function returns the matrice associated to the initial state of the game"""
        with open(self.input, 'r') as fichier:
            #get the number of line
            lignes=fichier.readline()
            N=len(lignes)
            #creating the self.current_state
            M=[[] for i in range (N)]
            c=0
            for ligne in self.input:
                # getting rid of /n
                read_line = ligne.strip()
                for car in read_line :
                    M[c].append(int(car))
                c+=1
        return(M)



    def read_initial_state(self):
        """initialize the state of the game"""
        self.current_state = self.create_matrice()

    
    def count_neighbors(self, i, j):
        """receives the position of a cell and the matrice associated to the state of the game and return the number of living cells around it."""
    
        m=len(self.current_state)
        n=len(self.current_state[0])
        S=0

        #processing the corner cells
        if i==0 and j==0: #top left cell
            S+=self.current_state[0][1]+self.current_state[1][0]+self.current_state[1][1]
        elif i==0 and j==n-1: #top right cell
            S+=self.current_state[0][n-2]+self.current_state[1][n-2]+self.current_state[1][n-1]
        elif i==m-1 and j==0: #bottom left cell
            S+=self.current_state[m-2][0]+self.current_state[m-2][1]+self.current_state[m-1][1]
        elif i==m-1 and j==n-1: #bottom right cell
            S+=self.current_state[m-1][n-2]+self.current_state[m-2][n-2]+self.current_state[m-2][n-1]
        
        #processing the side cells
        
        #cells on top
        elif i==0 and 0<j<n-1: 
            S+=self.current_state[0][j-1]+self.current_state[1][j-1]+self.current_state[1][j]+self.current_state[1][j+1]+self.current_state[0][j+1]
        
        #cells on the bottom
        elif i==m-1 and 0<j<n-1: 
            S+=self.current_state[m-1][j-1]+self.current_state[m-2][j-1]+self.current_state[m-2][j]+self.current_state[m-2][j+1]+self.current_state[m-1][j+1]

        #cells on the left side
        elif j==0 and 0<i<m-1:
            S+=self.current_state[i-1][0]+self.current_state[i-1][1]+self.current_state[i][1]+self.current_state[i+1][1]+self.current_state[i+1][0]
        
        #cells on the right side
        elif j==n-1 and 0<i<m-1:
            S+=self.current_state[i-1][n-1]+self.current_state[i-1][n-2]+self.current_state[i][n-2]+self.current_state[i+1][n-2]+self.current_state[i+1][n-1]

        #processing the rest of the cells

        else :
            S+=self.current_state[i-1][j-1]+self.current_state[i][j-1]+self.current_state[i+1][j-1]+self.current_state[i+1][j]+self.current_state[i+1][j+1]+self.current_state[i][j+1]+self.current_state[i-1][j+1]+self.current_state[i-1][j]                              
        
        return(S)


    def apply_rules(self, i, j):
        """returns the new state of a cell"""
        if self.current_state[i][j]==1: #the cell is alive
            if 1<self.count_neighbors(i,j,self.current_state)<4:
                return(1) #the cell stays alive
            else:
                return(0) #the cell dies
        else : # the cell is dead
            if self.count_neighbors(i,j,self.current_state)==3:
                return(1) #the cell becomes a living cell

    def generate_next_state(self):
        """receives the current state of the game and return the new state having applied the rules"""
        m=len(self.current_state)
        n=len(self.current_state[0])
        M=copy.deepcopy(self.current_state) #we copy the matrix associated to the current state because we don't want to modify it. We need the same matrice to apply the rules every time
        for i in range (m):
            for j in range(n):
                M[i][j]=self.apply_rules(self.current_state,i,j) 
        self.current_state=M
    
    def empty_file(self):
        """return true if the file is empty or false if it isn't"""
        with open(self.output, 'r') as fichier:
            ligne = fichier.readline()
            return ligne == "" #return true if the output file is empty

    def output_file(self):
        """takes the current state of the game and modifies the output file"""
        m=len(self.current_state)
        n=len(self.current_state[0])

        if self.empty_file():                 #if the file is empty : after step 1
            with open(self.output, 'w') as fichier: #opening the output file in writing mode
                for i in range (m):
                    new_line=''                #creating a new line
                    for j in range(n):
                        new_line=new_line+str(self.current_state[i][j])  #adding all the 0 and 1 from the line on by one
                    fichier.write(new_line+'\n')

        #the file is already filed we modify it 
        else:
            with open(self.output,'w') as fichier:          #opening o_file in writing mode
                fichier.write('')                      #on vide de fichier de l'état précédent
                for ligne in self.current_state :
                    new_line= ''.join(map(str, ligne)) #on convertit les éléments de la liste en str et on les concatène
                    fichier.write(new_line+'\n')       #on ajoute la nouvelle ligne au fichier de sorti

    def run(self):
        self.read_initial_state()
        step=0
        while step<self.m: #while the number of steps is inferior to the number of steps to run
            self.generate_next_state()
            self.output_file()
            step+=1

def main():
    args = read_args()
    game = GameOfLife(args.input, args.output, args.d, args.m, args.f, args.width, args.height)
    game.run()

if __name__=="__main__":
    main()

#il reste a :
                
#afficher chaque étape avec pygame si d est activé : x
#run en tant que module avec main : v
#faire des classes : v
#utiliser logging : x
#tester les classes et les fonctions avec pytest : x
#tester la simulation avec des patterns et un certain nombre d'étape et checker si c'est bon : x
#using OOP to Store data only inside private members (start with underscore character). This means no direct access to internal data. : x

