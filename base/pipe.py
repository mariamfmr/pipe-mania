# pipe.py: Template para implementação do projeto de Inteligência Artificial 2023/2024.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes sugeridas, podem acrescentar outras que considerem pertinentes.

# Grupo 00:
# 00000 Nome1
# 00000 Nome2

import sys
import numpy as np
from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
)

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
    
    def is_corner_upper_right(self, row: int, col: int) -> bool:
        """ Verifica se a posição é um canto superior direito. """
        return row == 0 and col == len(self.grid[0]) - 1
    
    def is_corner_upper_left(self, row: int, col: int) -> bool:
        """ Verifica se a posição é um canto superior esquerdo. """
        return row == 0 and col == 0
    
    def is_corner_lower_right(self, row: int, col: int) -> bool:
        """ Verifica se a posição é um canto inferior direito. """
        return row == len(self.grid) - 1 and col == len(self.grid[0]) - 1
    
    def is_corner_lower_left(self, row: int, col: int) -> bool:
        """ Verifica se a posição é um canto inferior esquerdo. """
        return row == len(self.grid) - 1 and col == 0
    
    def is_edge_upper(self, row: int, col: int) -> bool:
        """ Verifica se a posição é uma aresta superior. """
        return row == 0
    
    def is_edge_lower(self, row: int, col: int) -> bool:
        """ Verifica se a posição é uma aresta inferior. """
        return row == len(self.grid) - 1
    
    def is_edge_left(self, row: int, col: int) -> bool:
        """ Verifica se a posição é uma aresta esquerda. """
        return col == 0
    
    def is_edge_right(self, row: int, col: int) -> bool:
        """ Verifica se a posição é uma aresta direita. """
        return col == len(self.grid[0]) - 1
    
    def is_connected_horizontal(self, row: int, col: int, isLeft: bool) -> bool:
        """ Verifica se a peça na posição (row, col) está ligada à direita. """
        horizontal_pairs = [['FD', 'BC'], ['FD', 'BB'], ['FD', 'BE'], ['FD', 'VC'], ['FD', 'VE'], ['FD', 'LH'], 
                            ['BC','BC'] ,['BC', 'BB'], ['BC', 'BE'], ['BC', 'FE'],['BC', 'VC'], ['BC', 'VE'], ['BC', 'LH'],
                            ['BB','BB'], ['BB', 'FE'], ['BC', 'BC'], ['BB', 'BE'], ['BB', 'VC'], ['BB', 'VE'], ['BB', 'LH'],
                            ['BD', 'FE'], ['BD', 'BC'], ['BD', 'BB'] , ['BD', 'VC'], ['BD', 'VE'], ['BD', 'LH'], ['BD', 'BE'],
                            ['VB', 'FE'], ['VB', 'BC'], ['VB', 'BB'], ['VB', 'BE'], ['VB', 'VC'], ['VB', 'VE'], ['VB', 'LH'],
                            ['LH', 'FE'], ['LH', 'BC'], ['LH', 'BB'], ['LH', 'BE'], ['LH', 'VC'], ['LH', 'VE'], ['LH', 'LH'],
                            ['VD', 'FE'], ['VD', 'BC'], ['VD', 'BB'], ['VD', 'BE'], ['VD', 'VC'],['VD', 'LH']]
        horizontal = self.adjacent_horizontal_values(row, col) # left, right

        if isLeft:
            return ([self.grid[row][col], horizontal[1]] in horizontal_pairs)
        else:
            return ([horizontal[0], self.grid[row][col]] in horizontal_pairs)
                

    def is_connected_vertical(self, row: int, col: int, isUpper: bool) -> bool:
        """ Verifica se a peça na posição (row, col) está ligada acima. """
        vertical_pairs = [['FC', 'BB'], ['FC', 'BE'], ['FC', 'BD'], ['FC', 'VB'], ['FC', 'VE'], ['FC', 'LV'],
                          ['BC', 'FB'], ['BC', 'BB'], ['BC', 'BE'], ['BC', 'BD'], ['BC', 'VB'], ['BC', 'VE'], ['BC', 'LV'], 
                          ['BE', 'BD'], ['BE', 'VB'], ['BE', 'VE'], ['BE', 'LV'], ['BD', 'FB'], ['BD', 'VB'], ['BD', 'VE'], ['BD', 'LV'], ['VC', 'FB'], ['VC', 'BB'], ['VC', 'BD'], ['VC', 'VB'], ['VC', 'VE'], ['VC', 'LV'], ['VD', 'FB'], ['VD', 'BB'], ['VD', 'BE'], ['VD', 'BD'], ['VD', 'VB'], ['VD', 'VE'], ['VD', 'LV'], ['LV', 'FB'], ['LV', 'BB'], ['LV', 'BE'], ['LV', 'BD'], ['LV', 'VB'], ['LV', 'VE'], ['LV', 'LV']]
        vertical = self.adjacent_vertical_values(row, col) # above, below
        if not isUpper:
            return ([self.grid[row][col], vertical[0] ] in vertical_pairs) 
        else:
            return ([vertical[1], self.grid[row][col]] in vertical_pairs)

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

class PipeManiaState:
    state_id = 0

    def __init__(self, board: Board):
        self.board = board
        self.id = PipeManiaState.state_id
        PipeManiaState.state_id += 1

    def __lt__(self, other):
        """ Este método é utilizado em caso de empate na gestão da lista
        de abertos nas procuras informadas. """
        return self.id < other.id
    
    def get_value(self, row: int, col: int) -> str:
        """ Devolve o valor na posição (row, col). """
        return self.board.grid[row][col]


class PipeMania(Problem):

    def __init__(self, initial_state: Board, goal_state: Board):
        """ O construtor especifica o estado inicial. """
        self.initial = initial_state
        self.goal_state = goal_state
        self.root = Node(PipeManiaState(initial_state), None, None, 0)

    def rotate(rotation: str, clockwise: bool) -> str:
        """Rotate the given string representing orientation clockwise or counter-clockwise."""
        # Define clockwise and counter-clockwise rotations for each orientation
        clockwise_rotations = {'C': 'D', 'D': 'B', 'B': 'E', 'E': 'C', 'H': 'V', 'V': 'H'}
        counter_clockwise_rotations = {'C': 'E', 'D': 'C', 'B': 'D', 'E': 'B', 'H': 'V', 'V': 'H'}
        full_rotations = {'V': 'V', 'H': 'H', 'C': 'B', 'B': 'C', 'D': 'E', 'E': 'D'}

        # Select the appropriate dictionary based on the direction of rotation
        if clockwise == 1:
            rotations = clockwise_rotations
        elif clockwise == 0:
            rotations = counter_clockwise_rotations
        elif clockwise == 2:
            rotations = full_rotations


        # Return the next or previous orientation based on the direction of rotation
        return rotations.get(rotation, rotation)  # Return the current rotation if not found in the dictionary

    def isValidPiece(self, piece: str, row, col) -> bool:
        if (piece == 'FC' and board.is_edge_upper(row, col)):
            return False
        elif (piece == 'FB' and board.is_edge_lower(row, col)):
            return False
        elif (piece == 'FE' and board.is_edge_left(row, col)):
            return False
        elif (piece == 'FD' and board.is_edge_right(row, col)):
            return False
        elif (piece == 'BC' and (board.is_edge_upper(row, col) or board.is_corner_upper_left(row, col) or board.is_corner_upper_right(row, col) or board.is_corner_lower_left(row, col) or board.is_corner_lower_right(row, col))):
            return False
        elif (piece == 'BB' and (board.is_edge_lower(row, col) or board.is_corner_upper_left(row, col) or board.is_corner_upper_right(row, col) or board.is_corner_lower_left(row, col) or board.is_corner_lower_right(row, col))):
            return False
        elif (piece == 'BE' and (board.is_edge_left(row, col) or board.is_corner_upper_left(row, col) or board.is_corner_lower_left(row, col) or board.is_corner_upper_right(row, col) or board.is_corner_lower_right(row, col))):
            return False
        elif (piece == 'BD' and (board.is_edge_right(row, col) or board.is_corner_upper_right(row, col) or board.is_corner_lower_right(row, col) or board.is_corner_upper_left(row, col) or board.is_corner_lower_left(row, col))):
            return False
        elif (piece == 'VC' and (board.is_edge_upper(row, col) or board.is_edge_left(row, col) or board.is_corner_upper_right(row, col) or board.is_corner_lower_left(row, col) or board.is_corner_upper_left(row, col))):
            return False
        elif (piece == 'VB' and (board.is_edge_lower(row, col) or board.is_edge_right(row, col) or board.is_corner_upper_right(row, col) or board.is_corner_lower_left(row, col) or board.is_corner_lower_right(row, col))):
            return False
        elif (piece == 'VE' and (board.is_edge_lower(row, col) or board.is_edge_left(row, col) or board.is_corner_upper_left(row, col) or board.is_corner_lower_left(row, col) or board.is_corner_lower_right(row, col))):
            return False
        elif (piece == 'VD' and (board.is_edge_upper(row, col) or board.is_edge_right(row, col) or board.is_corner_upper_left(row, col) or board.is_corner_upper_right(row, col) or board.is_corner_lower_right(row, col))):
            return False
        elif (piece == 'LH' and (board.is_edge_right(row, col) or board.is_edge_left(row, col) or board.is_corner_upper_left(row, col) or board.is_corner_upper_right(row, col) or board.is_corner_lower_right(row, col) or board.is_corner_lower_left(row, col))):
            return False
        elif (piece == 'LV' and (board.is_edge_upper(row, col) or board.is_edge_lower(row, col) or board.is_corner_upper_left(row, col) or board.is_corner_upper_right(row, col) or board.is_corner_lower_right(row, col) or board.is_corner_lower_left(row, col))):
            return False
        else:
            return True

    def get_valid_rotations(self, piece: str, row: int, col: int) -> list:
        """ Returns a list of valid rotations for the given piece. """
        valid_rotations = [None, None, None]
        if self.isValidPiece(piece[0] + PipeMania.rotate(piece[1], 0),  row, col): # check if the anti-clockwise rotation is valid
            valid_rotations[0] = 1 # flag to indicate that the anti-clockwise rotation is valid
        if self.isValidPiece(piece[0] + PipeMania.rotate(piece[1], 1),  row, col): # check if the clockwise rotation is valid
            valid_rotations[1] = 1 # flag to indicate that the clockwise rotation is valid
        
        # check 180 degree rotation
        clockwise_rotated_piece = piece[0] + PipeMania.rotate(piece[1], 0)
        full_rotated_piece = clockwise_rotated_piece[0] + PipeMania.rotate(clockwise_rotated_piece[1], 0)
        if self.isValidPiece(full_rotated_piece, row, col):
            valid_rotations[2] = 1 # flag to indicate that the 180 degree rotation is valid
        

        return valid_rotations

    def actions(self, state: PipeManiaState):
        """ Returns a 3D array of actions that can be executed from the given state. """
        num_rows, num_cols = len(state.board.grid), len(state.board.grid[0])
        available_actions = []

        # Iterate over each position on the board
        for row in range(num_rows):
            for col in range(num_cols):
                piece = state.board.get_value(row, col)
                actions_at_position = self.get_valid_rotations(piece, row, col)
                if actions_at_position[0] == 1: 
                    available_actions.append((row, col, False)) # anti-clockwise rotation
                if actions_at_position[1] == 1:
                    available_actions.append((row, col, True)) # clockwise rotation
                if actions_at_position[2] == 1:
                    available_actions.append((row, col, 2))

        return available_actions

    def goal_test(self, state: PipeManiaState)-> bool:
        """ Retorna True se 'state' é um estado objetivo. """
        # check for each piece if it is connected
        for row in range(len(state.board.grid)):
            for col in range(len(state.board.grid[0])):
                piece = state.board.get_value(row, col)
                if not Piece(piece).isConnected(state.board, row, col):
                    return False
        return True
    
    def result(self, state: PipeManiaState, action): # action = (row, col, clockwise)
        """ Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state). """
        # Create a copy of the board to modify
        new_board = Board([row[:] for row in state.board.grid])
        piece = new_board.get_value(action[0], action[1])   # get the piece at the given position
        rotated_piece = piece[0] + PipeMania.rotate(piece[1], action[2]) # rotate the piece at the given position clockwise or anti-clockwise
        new_board.grid[action[0]][action[1]] = rotated_piece
        
        # Create and return a new state with the modified board
        return PipeManiaState(new_board)
        
    def h(self, node: Node):
        """ Função heuristica utilizada para a procura A*. """
        # TODO
        pass

class Piece():
    def __init__(self, piece_type: str):
        self.piece_type = piece_type

    def isConnected(self, board: Board, row: int, col: int)->bool:
        if self.piece_type == 'FC':
            return board.is_connected_vertical(row, col, False)
        elif self.piece_type == 'FB':
            return board.is_connected_vertical(row, col, True)
        elif self.piece_type == 'FE':
            return board.is_connected_horizontal(row, col, False)
        elif self.piece_type == 'FD':
            return board.is_connected_horizontal(row, col, True)
        elif self.piece_type == 'BC':
            return board.is_connected_horizontal(row, col, True) and board.is_connected_horizontal(row, col, False) and board.is_connected_vertical(row, col, False)
        elif self.piece_type == 'BB':
            return board.is_connected_horizontal(row, col, True) and board.is_connected_horizontal(row, col, False) and board.is_connected_vertical(row, col, True)
        elif self.piece_type == 'BE':
            return board.is_connected_horizontal(row, col, False) and board.is_connected_vertical(row, col, False) and board.is_connected_vertical(row, col, True)
        elif self.piece_type == 'BD':
            return board.is_connected_horizontal(row, col, True) and board.is_connected_vertical(row, col, True) and board.is_connected_vertical(row, col, False)
        elif self.piece_type == 'VC':
            return board.is_connected_horizontal(row, col, False) and board.is_connected_vertical(row, col, False)
        elif self.piece_type == 'VB':
            return board.is_connected_horizontal(row, col, True) and board.is_connected_vertical(row, col, True)
        elif self.piece_type == 'VE':
            return board.is_connected_horizontal(row, col, False) and board.is_connected_vertical(row, col, True)
        elif self.piece_type == 'VD':
            return board.is_connected_horizontal(row, col, True) and board.is_connected_vertical(row, col, False)
        elif self.piece_type == 'LH':
            return board.is_connected_horizontal(row, col, True) and board.is_connected_horizontal(row, col, False)
        elif self.piece_type == 'LV':
            return board.is_connected_vertical(row, col, True) and board.is_connected_vertical(row, col, False)
        else:
            return False
        

def expand_tree(root: Node, problem: PipeMania):
    frontier = [root]

    while frontier:
        node = frontier.pop()
        children = node.expand(problem)  # Get the children of the current node
        
        # Explore all siblings of the children
        for child in children:
            siblings = child.expand(problem)
            
            # Explore each sibling
            for sibling in siblings:
                print(sibling.state.board.print())
                print("Action:", sibling.action)
                print("Cost:", sibling.path_cost)
                print("\n")
                if problem.goal_test(sibling.state):
                    break
                frontier.append(sibling)
        
        # Break the loop if a goal state is found
        if problem.goal_test(node.state):
            break

if __name__ == "__main__":
    # TODO:
    # Ler o ficheiro do standard input,
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    # Assuming you have the input string
    input_string = "FB\tVC\tVD\nBC\tBB\tLV\nFB\tFB\tFE\n"

    """
    # Create a Board object by parsing the input string
    board = Board.parse_instance(input_string)
    board.print()


    print(board.adjacent_horizontal_values(0, 0))

    # Create insatance of PipeMania
    problem = PipeMania(board, board)
    # print(problem.actions(PipeManiaState(board)))

    # Create the initial state
    initial_state = PipeManiaState(board)
    result_state = problem.result(initial_state, (2, 2, True)) ## Rotate the piece at position (2, 2) clockwise

    result_state.board.print()
    print(result_state.board.is_connected_vertical(1, 0, False))

    """

    """
    board = Board.parse_instance(input_string)
    # Criar uma instância de PipeMania:
    problem = PipeMania(board, board)
    #print board
    board.print() 
    print("\n")

    # Criar um estado com a configuração inicial:
    s0 = PipeManiaState(board)
    # Aplicar as ações que resolvem a instância
    s1 = problem.result(s0, (0, 1, True))
    s2 = problem.result(s1, (0, 1, True))
    s3 = problem.result(s2, (0, 2, True))
    s4 = problem.result(s3, (0, 2, True))
    s5 = problem.result(s4, (1, 0, True))

    s6 = problem.result(s5, (1, 1, True))
    s7 = problem.result(s6, (2, 0, False)) # anti-clockwise (exemplo de uso)
    s8 = problem.result(s7, (2, 0, False)) # anti-clockwise (exemplo de uso)
    s9 = problem.result(s8, (2, 1, True))
    s10 = problem.result(s9, (2, 1, True))
    s11 = problem.result(s10, (2, 2, True))
    # Verificar se foi atingida a solução

    print("S5: Is goal?", problem.goal_test(s5))
    s5.board.print()
    print("S11: Is goal?", problem.goal_test(s11))
    s11.board.print()
    #print("Is goal?", problem.goal_test(s11))
    #print("Solution:\n", s11.board.print(), sep="")
    """

    input_string = "FB\tVC\tVD\nBC\tBB\tLV\nFB\tFB\tFE\n"
    goal = "FB\tVB\tVE\nBD\tBE\tLV\nFC\tFC\tFC\n"
    goal_board = Board.parse_instance(goal)
    
    board = Board.parse_instance(input_string)
    problem = PipeMania(board, goal_board)

    root = Node(PipeManiaState(board), None, None, 0)
    expand_tree(root, problem)



    #goal = breadth_first_tree_search(problem)

    #print("Is goal?", problem.goal_test(goal_node.state))
    #print("Solution:\n", goal_node.solution(), sep="")
    pass
