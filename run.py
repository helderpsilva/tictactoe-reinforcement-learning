import argparse
import sys
import os

from tqdm import trange, tqdm
import matplotlib.pyplot as plt

import numpy as np
import random
import pickle

from assets.game import Tictactoe, play_game
from assets.agent import Agent
from assets.human import Human
from assets.value_function import status_and_winners_matrix, value_function


def main():
    parser = argparse.ArgumentParser(
    prog="TIC-TAC-TOE:",
    add_help=True,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description="""
     Implementation of the TIC-TAC-TOE game leveraging reinforcement learning for an adversarial game.
                """,
    epilog=""" 

           """)

    # Processo de treino
    parser.add_argument('-t',dest='train',action="store", type=int ,help='Definir o número de jogos que queremos treinar o nosso agente (default:1000)')
    parser.add_argument('-r',dest='random',action="store_true",help='Treinar agente contra jogador aleatório')

    # Processo de jogo contra humano
    parser.add_argument('-p',dest='agent',action="store",help='Jogar contra um agente treinado')
    
    # Processo competição entre Agentes
    parser.add_argument('-g',dest='gym',action="store_true",help='Competição entre agentes')



    args = parser.parse_args()


    if not args.train == None:
        train(args.train, args.random)
       
    elif not args.agent == None:
        play_human_to_agent(args.agent)
    
    elif args.gym:
        create_gym()


def train (iteration,random = False):
    #create a new game
    name = input("\nPlease chose a name for this Agent:  ")
    game = Tictactoe()
    print('\n[INFO]: Checking all possible moves combinations.\n')
    winner_matrix = status_and_winners_matrix(game)

    v1 = value_function(game,winner_matrix, 1)
    v2 = value_function(game,winner_matrix, -1)

    player_turn = int(input("Please chose your agent turn? (1/2):  "))
    symbol = input("Please chose the symbol for the Agent (X or O):  ")
    print(f'\n[INFO]: Creating agent {name} with symbol {symbol}\n')
    
    agent_turn = player_turn 
    
    player_turn = (1 if player_turn == 2 else 2)
    
    if symbol =="x" or symbol =="X":
        if random:
            p1 = Agent(1, epsilon = 1) # O
        else:
            p1 = Agent(1) # O
        p1.value_function(v1)
        
        p2 = Agent(-1) # X
        p2.value_function(v2)
    
    elif symbol =="o" or symbol =="O":
        if random:
            p1 = Agent(-1, epsilon = 1) # x
        else:
            p1 = Agent(-1) # x
        p1.value_function(v2)
        
        p2 = Agent(1) # O
        p2.value_function(v1)

    iterations = trange(iteration, desc='Victory:0 | Losses:0', leave=True)
    losses = 0
    victories = 0

    for i in iterations:
        game = Tictactoe()
        play_game(p1,p2,player_turn,game)

        if game.winner == p2.symbol:
            victories +=1
        losses = i-victories

        iterations.set_description(f'Victory:{victories} | Losses:{losses}')
        iterations.refresh() # to show immediately the update
    
    if random:
        agent_name =f'{name}_{symbol}_{agent_turn}_{iteration}_randon'
    else:
        agent_name =f'{name}_{symbol}_{agent_turn}_{iteration}'

    print(f'\n[INFO]: Saving agent: {agent_name}')

    
    agent_information = {}

    agent_information["symbol"] = symbol
    agent_information["player_turn"] = agent_turn
    agent_information["V"] = p2.V

    save_agent(agent_name=agent_name, agent_information=agent_information)

    print(f'[INFO]: New agent was saved sucessfully\n')
    print(f'[INFO]: To play against the new created Agent, you can run the command:\n \tpython run.py -p {agent_name}\n')


def get_agent(agent_name):
    with open(f'./trained_agents/{agent_name}.pickle', 'rb') as handle:
        return pickle.load(handle)

def save_agent(agent_name, agent_information):
    with open(f'./trained_agents/{agent_name}.pickle', 'wb') as handle:
        pickle.dump(agent_information, handle, protocol=pickle.HIGHEST_PROTOCOL)


def play_human_to_agent(agent):

    print('\n[INFO]: Creating new game\n')
    print('\n[INFO]: Loading agent')

    agent_info = get_agent(agent)
    
    print(f'\n[ATENTION]: The agente loaded was trained with symbol {agent_info["symbol"]} for turn {agent_info["player_turn"]}')
    print('            Based on this information, choose your arguments for this game!\n')

    symbol = input("Please chose the symbol you want to play with (X or O):  ")
    player_turn = int(input("Please chose player turn? (1/2):  "))
    print(player_turn)
    
    if symbol == "o" or symbol == "O":
        p1 = Human(1)
        p2 = Agent(-1) # 0
    elif symbol == "x" or symbol == "X":
        p1 = Human(-1)
        p2 = Agent(1) # 0


    p2.value_function(agent_info["V"])

    game_loop = True

    while game_loop:
        game = Tictactoe()
        play_game(p1,p2,player_turn,game,draw_board=True)

        play_again = input("Do you want to play again (Y/N):  ")
        if play_again =="n" or play_again =="N":
            game_loop = False
    	    
            agent_info["V"] = p2.V
            
            try:
                save_agent(agent, agent_info)
                print('\n[INFO]: Agent saved sucessfuly')
                break
            except:
                print("\n[INFO]: Something went wrong while saving the agent")
            
        else:
            pass


def create_gym():
    print('\n[INFO]: Getting the board ready.')

    path = "./trained_agents"
    agents = os.listdir(path)

    print('\n[INFO]: Available agents:\n')
    choices = {}
    for agent in range(len(agents)):
        choices[agent+1] = agents[agent]

    for key, value in choices.items():
        print (key,":", value)
    first_agent = int(input("\nPlease choose the first agent: "))
    second_agent = int(input("Please choose the second agent: "))

    print(f'\n[INFO]: Loading agents: {choices[first_agent].strip(".pickle")} and {choices[second_agent].strip(".pickle")}\n')

    agent_1 = get_agent(choices[first_agent].strip(".pickle"))
    agent_2 = get_agent(choices[second_agent].strip(".pickle"))

    first_agent_symbol = input(f'\nPlease choose the symbol for agent {choices[first_agent].strip(".pickle")}: ')

    if first_agent_symbol == "o" or first_agent_symbol=="O":
        p1 = Agent(-1) # O
        p2 = Agent(1)  # X
    elif first_agent_symbol == "x" or first_agent_symbol=="X":
        p1 = Agent(1)  # X
        p2 = Agent(-1) # O
    
    p1.V = agent_1["V"]
    p2.V = agent_2["V"]

    iterations = int(input("Please choose the number of games: "))

    agent_1_victories = 0
    agent_2_victories = 0
    ties = 0

    for i in tqdm(range(iterations),  desc="Competing"):
        player_turn = random.randint(1,2)
        game = Tictactoe()
        play_game(p1,p2,player_turn,game)

        if game.winner == p1.symbol:
            agent_1_victories += 1
        elif game.winner == p2.symbol:
            agent_2_victories += 1
        else:
            ties += 1

    print(f'\n[GAME RESULTS]: Agent 1 | Victories: {agent_1_victories} | Losses: {iterations-agent_1_victories-ties} | Ties: {ties} | Agent: {choices[first_agent].strip(".pickle")}')
    print(f'[GAME RESULTS]: Agent 2 | Victories: {agent_2_victories} | Losses: {iterations-agent_2_victories-ties} | Ties: {ties} | Agent: {choices[second_agent].strip(".pickle")}')

    if agent_1_victories > agent_2_victories:
        winner_agent = agent_1_victories
        winner_agent_name = choices[first_agent].strip(".pickle")
    else:
        winner_agent = agent_2_victories
        winner_agent_name = choices[second_agent].strip(".pickle")

    data = {
        'Victories' : winner_agent,
        'Losses' : iterations-winner_agent-ties,
        "Ties" : ties
    }

    data_names = list(data.keys())
    data_values = list(data.values())


    plt.bar(data_names, data_values)
    plt.title(f'{winner_agent_name}')
    plt.show()


if __name__ == "__main__":
    main()