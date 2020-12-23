# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 17:54:13 2020

@author: ikhla
"""

from ortools.sat.python import cp_model
from random import *

def Level():
    level = eval(input("Choose a level between 1 and 5 "+
                       "(1 easy and 5 very hard) :"))
    assert (level in range(1,6))
    if level == 1 :
        nbcases = 50
    if level == 2 :
        nbcases = 40
    if level == 3 :
        nbcases = 33
    if level == 4 :
        nbcases = 26
    if level == 5 :
        nbcases = 17
    
    # Return the number of hidden cases
    return (81 - nbcases)   
  
        
    
def Sudoku(grilleinitiale = None):
    # Creates the model
    model = cp_model.CpModel()
    kBase = 9
    
    #Variable
    grille = [[model.NewIntVar(1, kBase, "") for i in range(9)] 
              for j in range(9)]
    
    # Constraints with a pre-filled grid
    if (grilleinitiale != None):
        for i in range(9):
            for j in range(9):
                if (grilleinitiale[i][j] != 0) : 
                    model.Add(grille[i][j] == grilleinitiale[i][j])
    
        
    #Constraints
        #Lines 
    for j in range(9):
        model.AddAllDifferent(grille[i][j] for i in range(9))
        #Columns
    for i in range(9):
        model.AddAllDifferent(grille[i][j] for j in range(9))
        
        #Squares
    C = []         
    for pasligne in range(0,7,3):       
        for pascolonne in range(0,7,3):
            for j in range(3):
                for i in range(3):
                    C.append(grille[pasligne+i][pascolonne+j])
            model.AddAllDifferent(C)
            C.clear()
    
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
        
    if (grilleinitiale != None) :
        if status == cp_model.FEASIBLE:
            # We hide some cells according to the difficulty
            limite = Level()
            count = 0
            incomplete = [[i for i in lignes] for lignes in grille]
            while(count < limite):
                ligne = randint(0,8)
                colonne = randint(0,8)
                if (incomplete[ligne][colonne] != 0) : 
                    incomplete[ligne][colonne] = 0
                    count += 1
                
            for i in range(9):
                print('')
                if (i%3 == 0 and i != 0) : print("- - - - - - - - - - - -")
                for j in range(9):
                   if (j%3 ==2) : print(solver.Value(incomplete[i][j]), end = " | ")
                   else : print(solver.Value(incomplete[i][j]), end = " ")
            print("\n")
            
            soluce = eval(input("Do you want a solution ? If yes, tap 1.\n"))
            if(soluce == 1) :
                for i in range(9):
                    print('')
                    if (i%3 == 0 and i != 0) : print("- - - - - - - - - - - -")
                    for j in range(9):
                       if (j%3 ==2) : print(solver.Value(grille[i][j]), end = " | ")
                       else : print(solver.Value(grille[i][j]), end = " ")                          
                print("\n")
    else :
        grilleinitiale = [[0 for i in range(9)] for j in range(9)]
        grilleinitiale[0][8] = randint(0,9)
        grilleinitiale[4][4] = randint(0,9)
        grilleinitiale[8][0] = randint(0,9)
        Sudoku(grilleinitiale)


test_grille = [[0, 0, 0, 0, 0, 0, 0, 0, 6], [0, 0, 6, 0, 2, 0, 7, 0, 0],
        [7, 8, 9, 4, 5, 0, 1, 0, 3], [0, 0, 0, 8, 0, 7, 0, 0, 4],
        [0, 0, 0, 0, 3, 0, 0, 0, 0], [0, 9, 0, 0, 0, 4, 2, 0, 1],
        [3, 1, 2, 9, 7, 0, 0, 4, 0], [0, 4, 0, 0, 1, 2, 0, 7, 8],
        [9, 0, 8, 0, 0, 0, 0, 0, 0]]

if __name__=="__main__" :
    Sudoku()



    