# Importação das bibliotecas necessárias 
# Interação com o OS 
import argparse
import sys
import os

# Apresentação gráfica de resultados 
from tqdm import trange, tqdm
import matplotlib.pyplot as plt

# Bibliotecas para computação de vetores e guardar resultados obtidos
import numpy as np
import random
import pickle

# Importação das funções criadas pelos autores
from assets.game import Tictactoe, play_game
from assets.agent import Agent
from assets.human import Human
from assets.value_function import status_and_winners_matrix, value_function

# A função main é responsável por lidar com os imputs do utilizador obtidos a partir do terminal
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

    # Parâmetros utilizados no processo de treino
    parser.add_argument('-t',dest='train',action="store", type=int ,help='Número de jogos que definimos para treinar o nosso agente')
    parser.add_argument('-r',dest='random',action="store_true",help='Uso de jogador aleatório para treino')

    # Parâmetro utilizado para jogos IA vs. Humano
    parser.add_argument('-p',dest='agent',action="store",help='Jogar contra um agente treinado')
    
    # Parâmetros para iniciar processo competição entre Agentes
    parser.add_argument('-g',dest='gym',action="store_true",help='Competição entre agentes')


    # Recolher os dados do utilizador
    args = parser.parse_args()

    # Processar os imputs do utilizador
    if not args.train == None:
        train(args.train, args.random)
       
    elif not args.agent == None:
        play_human_to_agent(args.agent)
    
    elif args.gym:
        create_gym()


def train (iteration,random = False):
    """Função responsável por treinar e guardar novos agentes""" 

    # Definição do nome do novo agente
    name = input("\nPlease choose a name for this Agent:  ")

    # Criar uma nova instância da classe Tic Tac Toe (Novo jogo)
    game = Tictactoe()

    # Calcular a matriz de estados e vencedores
    print('\n[INFO]: Checking all possible moves combinations.\n')
    winner_matrix = status_and_winners_matrix(game)

    # Cálculo da função v
    v1 = value_function(game,winner_matrix, 1)
    v2 = value_function(game,winner_matrix, -1)

    # Definição do símbolo e da ordem de jogo
    player_turn = int(input("Please chose your agent turn? (1/2):  "))
    symbol = input("Please choose the symbol for the Agent (X or O):  ")
    print(f'\n[INFO]: Creating agent {name} with symbol {symbol}\n')
    
    agent_turn = player_turn 
    
    player_turn = (1 if player_turn == 2 else 2)
    
    if symbol =="x" or symbol =="X":

        # Testa para a presença da flag -r. Se flag = TRUE converte o jogador em random
        if random:
            p1 = Agent(1, epsilon = 1) # O
        else:
            p1 = Agent(1) # O
        p1.value_function(v1)
        
        p2 = Agent(-1) # X
        p2.value_function(v2)
    
    elif symbol =="o" or symbol =="O":

        # Testa para a presença da flag -r. Se flag = TRUE converte o jogador em random
        if random:
            p1 = Agent(-1, epsilon = 1) # x
        else:
            p1 = Agent(-1) # x
        p1.value_function(v2)
        
        p2 = Agent(1) # O
        p2.value_function(v1)

    # Definição do número de jogadas com base no imput do utilizador
    iterations = trange(iteration, desc='Victory:0 | Losses:0', leave=True)

    # Variáveis para contagem do número de vitórios e derrotas do novo agente
    losses = 0
    victories = 0

    for i in iterations:
        game = Tictactoe()
        play_game(p1,p2,player_turn,game)

        if game.winner == p2.symbol:
            victories +=1
        losses = i-victories

        # Atualização dos resultados do treino em tempo real na barra de progresso 
        iterations.set_description(f'Victory:{victories} | Losses:{losses}')
        iterations.refresh() # to show immediately the update
    
    # Adiciona random ao nome do agente caso o adversário tenha sido random
    if random:
        agent_name =f'{name}_{symbol}_{agent_turn}_{iteration}_randon'
    else:
        agent_name =f'{name}_{symbol}_{agent_turn}_{iteration}'

    print(f'\n[INFO]: Saving agent: {agent_name}')

    # Recolher e guardar a informação do agente treinado
    agent_information = {}

    agent_information["symbol"] = symbol # guarda o símbolo para o qual o agente foi treinado
    agent_information["player_turn"] = agent_turn   # Guardar a ordem de jogadas
    agent_information["V"] = p2.V # Guardar o "cerébro" do jogador

    # Guardar o agente no computador em formato pickel "pasta trained_agents"
    save_agent(agent_name=agent_name, agent_information=agent_information)

    print(f'[INFO]: New agent was saved sucessfully\n')
    print(f'[INFO]: To play against the new created Agent, you can run the command:\n \tpython run.py -p {agent_name}\n')


def get_agent(agent_name):
    """ Função responsável por carregar agentes previamnete guardados"""

    with open(f'./trained_agents/{agent_name}.pickle', 'rb') as handle:
        return pickle.load(handle)

def save_agent(agent_name, agent_information):
    """ Função responsável por guardar novos agentes"""

    with open(f'./trained_agents/{agent_name}.pickle', 'wb') as handle:
        pickle.dump(agent_information, handle, protocol=pickle.HIGHEST_PROTOCOL)


def play_human_to_agent(agent):
    """Função responsável por iniciar um jogo entre humano e IA previamente treinada"""

    print('\n[INFO]: Creating new game\n')
    print('\n[INFO]: Loading agent')

    agent_info = get_agent(agent)

    print(f'\n[ATENTION]: The agente loaded was trained with symbol {agent_info["symbol"]} for turn {agent_info["player_turn"]}')
    print('            Based on this information, choose your arguments for this game!\n')

    symbol = input("Please choose the symbol you want to play with (X or O):  ")
    player_turn = int(input("Please choose player turn? (1/2):  "))
    print(player_turn)
    
    if symbol == "o" or symbol == "O":
        p1 = Human(1)
        p2 = Agent(-1) # 0
    elif symbol == "x" or symbol == "X":
        p1 = Human(-1)
        p2 = Agent(1) # 0


    p2.value_function(agent_info["V"])

    # Loop responsável por manter o jogo entre utilizador e IA a decorrer até instruções em contrário
    game_loop = True

    while game_loop:
        game = Tictactoe()
        play_game(p1,p2,player_turn,game,draw_board=True)

        play_again = input("Do you want to play again (Y/N):  ")
        if play_again =="n" or play_again =="N":
            game_loop = False
    	    
            # Atualização do "cerébro" do agente com base nos jogos realizados
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
    """Função ginásio responsável por criar um ambiente de competição entre dois agentes pré treinados"""

    print('\n[INFO]: Getting the board ready.')

    # Obter a lista dos agentes treinados, para seleção de jogadores
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

    # Loop de jogo entre 2 agentes selecionados
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

    # Resultados de competição: vitórias, derrotas e empates
    print(f'\n[GAME RESULTS]: Agent 1 | Victories: {agent_1_victories} | Losses: {iterations-agent_1_victories-ties} | Ties: {ties} | Agent: {choices[first_agent].strip(".pickle")}')
    print(f'[GAME RESULTS]: Agent 2 | Victories: {agent_2_victories} | Losses: {iterations-agent_2_victories-ties} | Ties: {ties} | Agent: {choices[second_agent].strip(".pickle")}')

    # Escolher o agente vencedor
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

    # Representar graficamente os resultados do vencedor
    plt.bar(data_names, data_values)
    plt.title(f'{winner_agent_name}')
    plt.show()


if __name__ == "__main__":
    main()