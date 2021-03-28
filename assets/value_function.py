# importar librarias necessarias.
import numpy as np

def status_and_winners_matrix(environment, row=0, column=0):
    matrix = []
    
    for v in (0, environment.x, environment.o):
        environment.board[row,column] = v
        
        if column == 2:
            if row == 2:
                status = environment.game_status()
                finished = environment.check_finished()
                winner = environment.winner
                matrix.append((status, winner, finished))
            else:
                matrix += status_and_winners_matrix(environment, row + 1, 0)
        else:
            matrix += status_and_winners_matrix(environment, row , column + 1)

    return matrix


def value_function(environment, matrix, symbol): 
    V = {}
    for status, winner, finished in matrix:
        if finished:
            if winner == symbol:
                v = 1
            else:
                v = 0
        else:
            v = 0.5
        V[status] = v
    
    return V
