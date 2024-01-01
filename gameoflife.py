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




def create_matrice(state_file):
    """this function returns the matrice associated to the state of the game"""

    with open(state_file, 'r') as fichier:
        #get the number of line
        lignes=state_file.read_line()
        N=len(lignes)
        #creating the matrice
        M=[[] for i in range (N)]
        c=0
        for ligne in state_file:
            # getting rid of /n
            read_line = ligne.strip()
            for car in read_line :
                M[c].append(int(car))
            c+=1
        return M

def count_neighbors(i,j,Matrice):
    """receives the position of a cell and the Matrice associated to the state of the game and return the number of living cells around it."""
    
    m=len(Matrice)
    n=len(Matrice[0])
    S=0

    #processing the corner cells
    if i==0 and j==0: #top left cell
        S+=Matrice[0][1]+Matrice[1][0]+Matrice[1][1]
    elif i==0 and j==n-1: #top right cell
        S+=Matrice[0][n-2]+Matrice[1][n-2]+Matrice[1][n-1]
    elif i==m-1 and j==0: #bottom left cell
        S+=Matrice[m-2][0]+Matrice[m-2][1]+Matrice[m-1][1]
    elif i==m-1 and j==n-1: #bottom right cell
        S+=Matrice[m-1][n-2]+Matrice[m-2][n-2]+Matrice[m-2][n-1]
    
    #processing the side cells
    
    #cells on top
    elif i==0 and 0<j<n-1: 
        S+=Matrice[0][j-1]+Matrice[1][j-1]+Matrice[1][j]+Matrice[1][j+1]+Matrice[0][j+1]
    
    #cells on the bottom
    elif i==m-1 and 0<j<n-1: 
        S+=Matrice[m-1][j-1]+Matrice[m-2][j-1]+Matrice[m-2][j]+Matrice[m-2][j+1]+Matrice[m-1][j+1]

    #cells on the left side
    elif j==0 and 0<i<m-1:
        S+=Matrice[i-1][0]+Matrice[i-1][1]+Matrice[i][1]+Matrice[i+1][1]+Matrice[i+1][0]
    
    #cells on the right side
    elif j==n-1 and 0<i<m-1:
        S+=Matrice[i-1][n-1]+Matrice[i-1][n-2]+Matrice[i][n-2]+Matrice[i+1][n-2]+Matrice[i+1][n-1]

    #processing the rest of the cells

    else :
        S+=Matrice[i-1][j-1]+Matrice[i][j-1]+Matrice[i+1][j-1]+Matrice[i+1][j]+Matrice[i+1][j+1]+Matrice[i][j+1]+Matrice[i-1][j+1]+Matrice[i-1][j]                              
    
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



def new_mat(Matrice):
    """receives the matrice associated to the state of the game and return the new matrice having applied the rules"""
    m=len(Matrice)
    n=len(Matrice[0])
    M=copy.deepcopy(Matrice) #we copy the Matrice because we don't want to modify it. We need the same Matrice to apply the rules() fucntion every time
    for i in range (m):
        for j in range(n):
            M[i][j]=rules(i,j,Matrice) 
    return (M)


def empty_file(file):
    with open(file, 'r') as fichier:
        ligne = fichier.readline()
        return ligne == "" #return true if the file is empty
    
def output_file(Matrice,o_file):
    """reçoit la matrice correspondant au nouvelle état et modifie le fichier de sortie"""
    m=len(Matrice)
    n=len(Matrice[0])

    if empty_file(o_file):                 #the file is empty : after step 1
        with open(o_file, 'w') as fichier: #opening o_file in writing mode
            for i in range (m):
                new_line=''                #creating a new line
                for j in range(n):
                    new_line=new_line+str(Matrice[i][j])  #adding all the 0 and 1 from the line on by one
                fichier.write(new_line+'\n')

    #the file is already filed we modify it 
    else:
        with open(o_file,'w') as fichier:          #opening o_file in writing mode
            fichier.write('')                      #on vide de fichier de l'état précédent
            for ligne in Matrice :
                new_line= ''.join(map(str, ligne)) #on convertit les éléments de la liste en str et on les concatène
                fichier.write(new_line+'\n')       #on ajoute la nouvelle ligne au fichier de sorti

#il reste a :
                
#afficher chaque étape avec pygame si d est activé 
#run en tant que module avec main 
#faire des classes 
#utiliser logging
#tester les classes et les fonctions avec pytest
#tester la simulation avec des patterns et un certain nombre d'étape et checker si c'est bon
#using OOP to Store data only inside private members (start with underscore character). This means no direct access to internal data.

