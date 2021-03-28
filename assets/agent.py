# importar librarias necessarias.
import numpy as np

class Agent():

    def __init__(self, symbol, epsilon = 0.05, learning_rate=0.2, name=None):
        self.name = name
        self.epsilon = epsilon
        self.learning_rate = learning_rate
        self.symbol = symbol
        self.history = []

    def value_function(self, V):
        self.V = V

    def make_move(self, environment):

        available_moves = []
        
        for row in range(3):
            for column in range(3):
                if environment.board[row,column] == 0:
                    available_moves.append((row,column))

        random_choice = np.random.random()

        if random_choice < self.epsilon:
            
            move_index = np.random.choice(len(available_moves))
            player_move = available_moves[move_index]
            
        else:
            board_list = []
            current_board = environment.board.copy()
            
            for move in available_moves:
                future_board = current_board.copy()
                future_board[move[0], move[1]] = self.symbol
                board_list.append(future_board.copy())
            
            states = [environment.game_status(board) for board in board_list]
            values = [self.V[state] for state in states]
            
            best_move = np.argmax(values)
            player_move = available_moves[best_move]
            
        environment.board[player_move[0], player_move[1]] = self.symbol
    
    def update_history(self, s):
        self.history.append(s)
        
    def update(self, environment):
        reward = environment.reward(self.symbol)
        target = reward
        
        for state in reversed(self.history):
            value = self.V[state] + self.learning_rate*(target - self.V[state])
            self.V[state] = value
            target = value
            
        self.history = []