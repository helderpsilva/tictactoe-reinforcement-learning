<br/>
<p align="center">
        <img width="60%" src="/img/logo.png" alt="tictactoe">
    </a>
</p>

<br/>

<p align="center">
  <a href="#Estrutura">Estrutura do Código</a> •
  <a href="#Utilização">Utilização</a> •
  <a href="#Contribuições">Contribuições</a>
</p>

> **Tic Tac Toe** Jogo e/ou passatempo popular.
> A origem deste jogo popular é desconhecida, todavia há indícios que indicam que pode ter começado no antigo Egito, onde foram encontrados tabuleiros esculpidos na rocha, que teriam mais de 3.500 anos.

>Este projeto aborda o jogo Tic-Tac-Toe usando o método de **reinforcement learning**. Num tabuleiro 3 x 3, o número de estados deste jogo pode ser estimado aproximadamente em 3 ^ 9 = 19.683, um número muito bom para um computador desktop normal.


## Estrutura

> O diretório assets contém o código principal para este projeto. Existem 4 arquivos principais:
* game.py
* agent.py
* human.py
* value_function.py


## Utilização

### Treinar um novo agente num ambiente virtual

    python run.py -t 10000        (Treina um agente durante 10000 interações contra um jogador AI)
    python run.py -t 10000 -r     (Treina um agente durante 10000 interações contra um jogador aleatório)

### Jogar contra um agente pré - treinado

    python run.py -p <nome do agente>  (Jogar contra um agente treinado)

### Colocar 2 agentes a competir

    python run.py -g                   (colocar 2 agentes a jogar um contra o outro)
    
#### Bibliotecas utilizadas:
* Numpy
* Matplotlib
* Argparse
* TQDM

## Contribuições
Criado por [Carla M. Lemos](https://github.com/CarlaMLemos) e [Hélder P. Silva ](https://github.com/helderpsilva)



