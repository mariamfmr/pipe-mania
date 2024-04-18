from sys import stdin
from search import Problem, Node


class State:
    state_id = 0
    def __init__(self, board):
        self.board = board
        self.id = State.state_id
        State.state_id += 1

    def __lt__(self, other):
        """ Este método é utilizado em caso de empate na gestão da lista
        de abertos nas procuras informadas. """
        return self.id < other.id


class Board:

    def __init__(self, grid):
        self.grid = grid

    def adjacent_vertical_values(self, row: int, col: int) -> (str, str):
        """ Devolve os valores imediatamente acima e abaixo, respectivamente. """
        above = None if row == 0 else self.grid[row - 1][col]
        below = None if row == len(self.grid) - 1 else self.grid[row + 1][col]
        return above, below

    def adjacent_horizontal_values(self, row: int, col: int) -> (str, str):
        """ Devolve os valores imediatamente à esquerda e à direita, respectivamente. """
        left = None if col == 0 else self.grid[row][col - 1]
        right = None if col == len(self.grid[0]) - 1 else self.grid[row][col + 1]
        return left, right

    def print(self):
        """ Imprime a grelha. """
        for row in self.grid:
            print('\t'.join(row))
    
    
    @staticmethod
    def parse_instance(input_string: str):
        """Lê a instância do problema a partir de uma string no formato especificado
        e retorna uma instância da classe Board.
        """
        grid = []
        lines = input_string.strip().split('\n')
        for line in lines:
            pieces = line.split('\t')
            grid.append(pieces)

        return Board(grid)

class PipeMania(Problem):
    def __init__(self, initial_state: Board, goal_state: Board):
        """ O construtor especifica o estado inicial. """
        # TODO
        pass

    def actions(self, state: State):
        """ Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento. """
        # TODO
        pass

    def result(self, state: State, action):
        """ Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state). """
        # TODO
        pass
    
    """
    def h(self, node: Node):
         Função heuristica utilizada para a procura A*. 
        # TODO
        pass
    """

# Assuming you have the input string
input_string = "FB\tVC\tVD\nBC\tBB\tLV\nFB\tFB\tFE\n"

# Create a Board object by parsing the input string
board = Board.parse_instance(input_string)
board.print()
print(board.adjacent_horizontal_values(1, 1))
