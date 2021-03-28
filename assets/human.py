# importar librarias necessarias.
import numpy as np
import pickle

class Human():

    def __init__(self, symbol):
        self.symbol = symbol

    def make_move(self, environment):
        while True:
            
            move = input("Insere as coordenadas lina,coluna da próxima jogada (l,c=0..2): ")
            row, column = move.split(',')
            row = int(row)
            column = int(column)
            
            try:
                player_move = environment.board[row,column]
            except:
                player_move = -1
                
            if player_move == 0:
                environment.board[row, column] = self.symbol
                break

    def update(self, environment):
        pass

    def update_history(self, s):
        pass