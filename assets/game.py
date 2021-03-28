# importar librarias necessarias.
import numpy as np

class Tictactoe():

    def __init__(self):
        self.ROWS = 3
        self.COLUMNS = 3
        self.board = np.zeros( (self.ROWS,self.COLUMNS) )
        self.winner = None
        self.finished = False
        self.x = -1
        self.o = 1

    def reward (self, player):
        """Reward based on a particular state"""
        
        # check if game is over, if not return 0.
        if not self.finished:
            return 0
        elif self.winner == player:
            return 1
        else:
            return 0
    
    def game_status(self, board = None):
        """Return a tuple containing the current game status"""
        
        game_status = []
        
        for row in range(self.ROWS):
            for column in range(self.COLUMNS):
                if not np.any(board == None):
                    game_status.append(board[row, column])
                else:
                    game_status.append(self.board[row,column])
        return tuple(game_status)

    def check__winner(self):
        """Function to check if we have a winner in a given board"""

        winner = False
        
        # check for winner in the lines:
        for row in range(self.ROWS):
            if self.board[row,0] != 0:
                if (self.board[row,0] == (np.sum(self.board[row,:])/3)):
                    self.winner = self.board[row,0]
                    winner = True

        # check for winner in the columns:
        for column in range(self.COLUMNS):
            if self.board[0,column] != 0:
                if (self.board[0,column] == (np.sum(self.board[:,column])/3)):
                    self.winner = self.board[0,column]
                    winner = True
                
        # check for winner diagonally:
        if self.board[0,0] != 0:
            if self.board[0,0] == ((self.board[0,0] + self.board[1,1] + self.board[2,2])/3):
                self.winner = self.board[0,0]
                winner = True
        
        if self.board[2,0] != 0:
            if self.board[2,0] == ((self.board[2,0] + self.board[1,1] + self.board[0,2])/3):
                self.winner = self.board[2,0]
                winner = True

        return winner
    
    def check_finished(self):
        if self.check__winner():
            self.finished = True
            return True
        elif (np.sum(self.board == 0)==0):
            self.finished = True
            return True
        else:
            return False

    def print_board(self):
        """Prints the game board to the terminal."""

        print_board = np.array([["","",""],["","",""],["","",""]])

        for row in range(self.ROWS):
            for column in range(self.COLUMNS):
                if self.board[row][column] == 1.0:
                    print_board[row][column] = "O"
                elif self.board[row][column] == -1.0:
                    print_board[row][column] = "X"
                elif self.board[row][column] == 0.0:
                    print_board[row][column] = " "
        
        print("\n")
        print('      0   1   2  ')
        print('    -------------')
        print(' 0  | {} | {} | {} |'.format(print_board[0][0], print_board[0][1], print_board[0][2]))
        print('    -------------')
        print(' 1  | {} | {} | {} |'.format(print_board[1][0], print_board[1][1], print_board[1][2]))
        print('    -------------')
        print(' 2  | {} | {} | {} |'.format(print_board[2][0], print_board[2][1], print_board[2][2]))
        print('    -------------')
        print("\n")

            

def play_game(p1, p2, player_turn, environment, draw_board=False):

    current_player = None
    while not environment.check_finished():

        if current_player == p1:
            current_player = p2
        else:
            if current_player == None:
                if player_turn == 1:
                    current_player = p1
                elif player_turn == 2:
                    current_player = p2
            else:
                current_player = p1

        if draw_board:
            if draw_board == 1 and current_player == p1:
                environment.print_board()
                
            if draw_board == 1 and current_player == p2:
                environment.print_board()
                

        current_player.make_move(environment)

        state = environment.game_status()
        p1.update_history(state)
        p2.update_history(state)

    if draw_board:
        environment.print_board()
        if environment.winner:
            if environment.winner == environment.x:
                print('    - Winner: X -')
                environment.print_board()
            else:
                print('    - Winner: O -')
        else: 
            print('    ---- TIE ----')


    p1.update(environment)
    p2.update(environment)