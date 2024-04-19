from sys import stdin
import numpy as np
from search import Problem, Node


class PipeManiaState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = PipeManiaState.state_id
        PipeManiaState.state_id += 1

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
    
    def get_value(self, row: int, col: int) -> str:
        """ Devolve o valor na posição (row, col). """
        return self.grid[row][col]

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
        self.initial_state = initial_state
        self.goal_state = goal_state

    def rotate(rotation: str, clockwise: bool) -> str:
        """Rotate the given string representing orientation clockwise or counter-clockwise."""
        # Define clockwise and counter-clockwise rotations for each orientation
        clockwise_rotations = {'C': 'D', 'D': 'B', 'B': 'E', 'E': 'C', 'H': 'V', 'V': 'H'}
        counter_clockwise_rotations = {'C': 'E', 'D': 'C', 'B': 'D', 'E': 'B', 'H': 'V', 'V': 'H'}

        # Select the appropriate dictionary based on the direction of rotation
        rotations = clockwise_rotations if clockwise else counter_clockwise_rotations

        # Return the next or previous orientation based on the direction of rotation
        return rotations.get(rotation, rotation)  # Return the current rotation if not found in the dictionary


    def actions(self, state: PipeManiaState):
        """ Returns a 3D array of actions that can be executed from the given state. """
        num_rows, num_cols = len(state.board.grid), len(state.board.grid[0])
        available_actions = np.empty((num_rows, num_cols, 2), dtype=object)

        # Iterate over each position on the board
        for row in range(num_rows):
            for col in range(num_cols):
                piece = state.board.get_value(row, col)
                actions_at_position = [piece[0] + PipeMania.rotate(piece[1], clockwise) for clockwise in [0, 1]]
                available_actions[row, col] = actions_at_position

        return available_actions

                

    def result(self, state: PipeManiaState, action):
        """ Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state). """
        
        piece = Board.get_value(state.board, action[0], action[1])
        rotated_piece = piece[0] + PipeMania.rotate(piece[1], action[2])
        possible_rotations = self.actions(state)[action[0], action[1]]
        if (rotated_piece in possible_rotations):
            state.board.grid[action[0]][action[1]] = rotated_piece
            
        return state
    
    def h(self, node: Node):
        """ Função heuristica utilizada para a procura A*. """
        # TODO
        pass


# Assuming you have the input string
input_string = "FB\tVC\tVD\nBC\tBB\tLV\nFB\tFB\tFE\n"

# Create a Board object by parsing the input string
board = Board.parse_instance(input_string)
board.print()
print(board.adjacent_horizontal_values(0, 0))

# Create insatance of PipeMania
problem = PipeMania(board, board)
# print(problem.actions(PipeManiaState(board)))

# Create the initial state
initial_state = PipeManiaState(board)
print(board.get_value(2, 2))
result_state = problem.result(initial_state, (2, 2, True))
print(result_state.board.get_value(2, 2))

# Cr