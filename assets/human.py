# importar librarias necessarias.
import numpy as np
import pickle

class Human():
    """Criação da entidade humano"""
    
    # O símbolo é X ou 0
    def __init__(self, symbol):
        self.symbol = symbol

    def make_move(self, environment):
        """Função responsável por executar jogadas"""

        while True:
            
            move = input("Please, choose your next play (row, column): ")
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