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

"""
import colorama
from colorama import Fore, Back, Style
colorama.init(autoreset=True)
"""


class Board:

    def __init__(self, grid):

        """
        Initializes a Board object.

        Args:
            grid (list): The grid layout representing the board.
        """

        # Grid for the board
        self.grid = grid

        # Board for the board
        self.board = self

        # Grid for positions in the correct orientation
        self.valid_positions = []

        self.validNeighborsMissing = []

        # int to keep up with its heuristic value
        self.heuristic = 0

        # Grid for explored positions
        self.explored = []
        self.unique_rot = 0
        self.node_test = []
        self.connected = []

    def unique_rotations(self, list) -> int:
        """
        Returns the number of unique rotations for the board.
        """
        unique = 0
        for action in list:
            if action[3] == 1:
                unique += 1
        
        return unique


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
        """
        Checks if the position is the upper right corner of the grid.

        Args:
            row (int): The row index of the position.
            col (int): The column index of the position.

        Returns:
            bool: True if the position is the upper right corner, False otherwise.
        """
        return row == 0 and col == len(self.grid[0]) - 1

    def is_connected_left(self, row: int, col: int) -> bool:
            # Sees if a piece is connected to the left
            # If piece has a left neighbor
            piece = self.grid[row][col]
            if col > 0:
                # If the left neighbor is connected to the right neighbor
                left_piece = self.grid[row][col - 1]
                if piece in ('FE', 'BC', 'BB', 'BE', 'VC', 'VE', 'LH'):
                    if left_piece in ('FD', 'BC', 'BB', 'BD', 'VD', 'VB', 'LH'):
                        return True
                else:
                    if left_piece in ('FC', 'FB', 'FD', 'BE', 'VC', 'VE', 'LV'):
                        return True
                return False  
            
            # Then it is a border piece
            # See if it is a corner piece
            if self.is_corner_upper_left(row, col):
                if piece in ('FB', 'FD', 'VB'):
                    return True
                else :
                    return False
                
            # See if it is a border piece
            if self.is_edge_left(row, col):
                if piece in ('FC', 'FB', 'FD', 'BD', 'VB', 'VD', 'LV'):
                    return True
                else:
                    return False
            
            if self.is_corner_lower_left(row, col):
                if piece in ('FC', 'FD', 'VD'):
                    return True 
                else:       
                    return False

    
    def is_connected_right(self, row: int, col: int) -> bool:
        # Sees if a piece is connected to the right
        # If piece has a right neighbor
        piece = self.grid[row][col]
        if col < len(self.grid[0]) - 1:
            # If the right neighbor is connected to the left neighbor
            right_piece = self.grid[row][col + 1]
            if piece in ('FD', 'BC', 'BB', 'BD', 'VD', 'VB', 'LH'):
                if right_piece in ('FE', 'BC', 'BB', 'BE', 'VC', 'VE', 'LH'):
                    return True
            else:
                if right_piece in ('FC', 'FB', 'FD', 'BD', 'VB', 'VD', 'LV'):
                    return True
            return False
        
        # If it is a border piece
        # See if it is a corner piece
        if self.is_corner_upper_right(row, col):
            if piece in ('FE', 'FB', 'VE'):
                return True
            else:
                return False
        
        # See if it is a border piece
        if self.is_edge_right(row, col):
            if piece in ('FC', 'FE', 'FB', 'BE', 'VC', 'VE', 'LV'):
                return True
            else:
                return False
            
        if self.is_corner_lower_right(row, col):
            if piece in ('FC', 'FE', 'VC'):
                return True
            else:
                return False

    def is_connected_upper(self, row: int, col: int) -> bool:
        # Sees if a piece is connected to the upper
        # If piece has a upper neighbor
        piece = self.grid[row][col]
        if row > 0:
            # If the upper neighbor is connected to the lower neighbor
            upper_piece = self.grid[row - 1][col]
            if piece in ('FC', 'BC', 'BE', 'BD', 'VC', 'VD', 'LV'):
                if upper_piece in ('FB', 'BB', 'BE', 'BD', 'VB', 'VE', 'LV'):
                    return True
            else:
                if upper_piece in ('FC', 'FD', 'FE', 'BC', 'VC', 'VD', 'LH'):
                    return True
            return False
        
        # If it is a border piece
        # See if it is a corner piece
        if self.is_corner_upper_left(row, col):
            if piece in ('FB', 'FD', 'VB'):
                return True
            else :
                return False
            
        if self.is_corner_upper_right(row, col):
            if piece in ('FE', 'FB', 'VE'):
                return True
            else:
                return False
            
        # See if it is a border piece
        if self.is_edge_upper(row, col):
            if piece in ('FD', 'FB', 'FE', 'BB', 'VB', 'VE', 'LH'):
                return True
            else:
                return False
                
    def is_connected_lower(self, row: int, col: int) -> bool:
        # Sees if a piece is connected to the lower
        # If piece has a lower neighbor
        piece = self.grid[row][col]
        if row < len(self.grid) - 1:
            # If the lower neighbor is connected to the upper neighbor
            lower_piece = self.grid[row + 1][col]
            if piece in ('FB', 'BB', 'BE', 'BD', 'VB', 'VE', 'LV'):
                if lower_piece in ('FC', 'BC', 'BE', 'BD', 'VC', 'VD', 'LV'):
                    return True
            else:
                if lower_piece in ('FB', 'FD', 'FE', 'BB', 'VB', 'VE', 'LH'):
                    return True
            return False

        # If it is a border piece
        # See if it is a corner piece
        if self.is_corner_lower_right(row, col):
            if piece in ('FC', 'FE', 'VC'):
                return True
            else:
                return False
            
        if self.is_corner_lower_left(row, col):
                if piece in ('FC', 'FD', 'VD'):
                    return True 
                else:       
                    return False
                
        # See if it is a border piece
        if self.is_edge_lower(row, col):
            if piece in ('FC', 'FE', 'FD', 'BC', 'VC', 'VD', 'LH'):
                return True
            else:
                return False
    


    def is_corner_upper_left(self, row: int, col: int) -> bool:
        """
        Checks if the position is the upper left corner of the grid.

        Args:
            row (int): The row index of the position.
            col (int): The column index of the position.

        Returns:
            bool: True if the position is the upper left corner, False otherwise.
        """
        return row == 0 and col == 0
    
    def is_corner_lower_right(self, row: int, col: int) -> bool:
        """
        Checks if the position is the lower right corner of the grid.

        Args:
            row (int): The row index of the position.
            col (int): The column index of the position.

        Returns:
            bool: True if the position is the lower right corner, False otherwise.
        """
        return row == len(self.grid) - 1 and col == len(self.grid[0]) - 1
    
    def is_corner_lower_left(self, row: int, col: int) -> bool:
        """
        Checks if the position is the lower left corner of the grid.

        Args:
            row (int): The row index of the position.
            col (int): The column index of the position.

        Returns:
            bool: True if the position is the lower left corner, False otherwise.
        """
        return row == len(self.grid) - 1 and col == 0
    

    def is_edge_upper(self, row: int, col: int) -> bool:
        """
        Checks if the position is on the upper edge of the grid.

        Args:
            row (int): The row index of the position.
            col (int): The column index of the position.

        Returns:
            bool: True if the position is on the upper edge, False otherwise.
        """
        return row == 0
    
    def is_edge_lower(self, row: int, col: int) -> bool:
        """
        Checks if the position is on the lower edge of the grid.

        Args:
            row (int): The row index of the position.
            col (int): The column index of the position.

        Returns:
            bool: True if the position is on the lower edge, False otherwise.
        """
        return row == len(self.grid) - 1
    
    def is_edge_left(self, row: int, col: int) -> bool:
        """
        Checks if the position is on the left edge of the grid.

        Args:
            row (int): The row index of the position.
            col (int): The column index of the position.

        Returns:
            bool: True if the position is on the left edge, False otherwise.
        """
        return col == 0
    
    def is_edge_right(self, row: int, col: int) -> bool:
        """
        Checks if the position is on the right edge of the grid.

        Args:
            row (int): The row index of the position.
            col (int): The column index of the position.

        Returns:
            bool: True if the position is on the right edge, False otherwise.
        """
        return col == len(self.grid[0]) - 1          

    def get_value(self, row: int, col: int) -> str:
        """
        Gets the value (piece identifier) at the given position in the grid.

        Args:
            row (int): The row index of the position.
            col (int): The column index of the position.

        Returns:
            str: The piece identifier at the specified position.
        """
        return self.grid[row][col]

    """
    def print(self):
        
        for i, row in enumerate(self.grid):
            for j, piece in enumerate(row):
                if (i, j) in self.valid_positions:
                    print(Fore.GREEN + piece, end='\t')
                elif (i, j) in self.explored:
                    print(Fore.YELLOW + piece, end='\t')
                else:
                    print(piece, end='\t')
            print()  # print a newline at the end of each row
    """
    def print(self):
        
        for row in self.grid:
            print('\t'.join(row))

            
    def is_fixed_piece(self, row: int, col: int) -> bool:
        """
        Checks if the piece at the given position is fixed (already in its final position).

        Args:
            row (int): The row index of the piece.
            col (int): The column index of the piece.

        Returns:
            bool: True if the piece is fixed, False otherwise.
        """
        return (row, col) in self.valid_positions

    def validate_pipe(self, row: int, col: int):
        """
        Validates the pipe at the given position.

        Args:
            row (int): The row index of the pipe.
            col (int): The column index of the pipe.
        """
        # Check if the piece is already in the list of valid positions
        if not self.is_fixed_piece(row, col):

            # If not, add it to the list
            self.valid_positions.append((row, col))

    def valid_upper_left_corner_actions(piece: str):

        """
        Determines valid actions for a piece located at the upper left corner of the grid.

        Args:
            piece (str): The piece identifier.

        Returns:
            list: A list of valid actions for the piece at the upper left corner.
        """

        # See if it is a locking pipe
        if piece in ('FC', 'FB', 'FE', 'FD'):
            return ['FB', 'FD']
        
        # See if it a return pipe
        if piece in ('VC', 'VB', 'VE', 'VD'):
            return ['VB']
        
    def valid_upper_right_corner_actions(piece: str):

        """
        Determines valid actions for a piece located at the upper right corner of the grid.

        Args:
            piece (str): The piece identifier.

        Returns:
            list: A list of valid actions for the piece at the upper right corner.
        """

         # See if it is a locking pipe
        if piece in ('FC', 'FB', 'FE', 'FD'):
            return ['FB', 'FE']
        
        # See if it a return pipe
        if piece in ('VC', 'VB', 'VE', 'VD'):
            return ['VE']
        
    def valid_lower_left_corner_actions(piece: str):
        
        """
        Determines valid actions for a piece located at the lower left corner of the grid.

        Args:
            piece (str): The piece identifier.

        Returns:
            list: A list of valid actions for the piece at the lower left corner.
        """

         # See if it is a locking pipe
        if piece in ('FC', 'FB', 'FE', 'FD'):
            return ['FC', 'FD']
        
        # See if it a return pipe
        if piece in ('VC', 'VB', 'VE', 'VD'):
            return ['VD']
         
    def valid_lower_right_corner_actions(piece: str):

        """
        Determines valid actions for a piece located at the lower right corner of the grid.

        Args:
            piece (str): The piece identifier.

        Returns:
            list: A list of valid actions for the piece at the lower right corner.
        """

         # See if it is a locking pipe
        if piece in ('FC', 'FB', 'FE', 'FD'):
            return ['FC', 'FE']
        
        # See if it a return pipe
        if piece in ('VC', 'VB', 'VE', 'VD'):
            return ['VC']
        
    def valid_upper_edge_actions(piece: str):

        """
        Determines valid actions for a piece located at the upper edge of the grid.

        Args:
            piece (str): The piece identifier.

        Returns:
            list: A list of valid actions for the piece at the upper edge.
        """

        # See if it is a locking pipe
        if piece in ('FC', 'FB', 'FE', 'FD'):
            return ['FB', 'FD', 'FE']
        
        # See if it is a fork pipe
        if piece in ('BC', 'BB', 'BE', 'BD'):
            return ['BB']
        
        # See if it a return pipe
        if piece in ('VC', 'VB', 'VE', 'VD'):
            return ['VB', 'VE']
        
        # See if it is a straight pipe
        if piece in ('LH', 'LV'):
            return ['LH']
        
    def valid_lower_edge_actions(piece: str):
            
        """
        Determines valid actions for a piece located at the lower edge of the grid.

        Args:
            piece (str): The piece identifier.

        Returns:
            list: A list of valid actions for the piece at the lower edge.
        """
            
        # See if it is a locking pipe
        if piece in ('FC', 'FB', 'FE', 'FD'):
            return ['FC', 'FD', 'FE']
        
        # See if it is a fork pipe
        if piece in ('BC', 'BB', 'BE', 'BD'):
            return ['BC']
        
        # See if it a return pipe
        if piece in ('VC', 'VB', 'VE', 'VD'):
            return ['VD', 'VC']
        
        # See if piece is a straight pipe
        if piece in ('LH', 'LV'):
            return ['LH']
            
    def valid_left_edge_actions(piece: str):
        
        """
        Determines valid actions for a piece located at the left edge of the grid.

        Args:
            piece (str): The piece identifier.

        Returns:
            list: A list of valid actions for the piece at the left edge.
        """

        # See if it is a locking pipe
        if piece in ('FC', 'FB', 'FE', 'FD'):
            return ['FC', 'FB', 'FD']
        
        # See if it is a fork pipe
        if piece in ('BC', 'BB', 'BE', 'BD'):
            return ['BD']
        
        # See if it a return pipe
        if piece in ('VC', 'VB', 'VE', 'VD'):
            return ['VB', 'VD']
        
        # See if it is a straight pipe
        if piece in ('LH', 'LV'):
            return ['LV']
        
    def valid_right_edge_actions(piece: str):
            
        """
        Determines valid actions for a piece located at the right edge of the grid.

        Args:
            piece (str): The piece identifier.

        Returns:
            list: A list of valid actions for the piece at the right edge.
        """
        
        # See if it is a locking pipe
        if piece in ('FC', 'FB', 'FE', 'FD'):
            return ['FC', 'FB', 'FE']
        
        # See if it is a fork pipe
        if piece in ('BC', 'BB', 'BE', 'BD'):
            return ['BE']
        
        # See if it a return pipe
        if piece in ('VC', 'VB', 'VE', 'VD'):
            return ['VE', 'VC']
        
        # See if it is a straight pipe
        if piece in ('LH', 'LV'):
            return ['LV']

    def valid_actions_with_upper_neighbor(piece: str, upper_neighbor: str):

        """
        Returns valid actions for a piece considering the correct orientation of the upper neighbor.

        Args:
            piece (str): The piece identifier.
            upper_neighbor (str): The identifier of the upper neighbor.

        Returns:
            list: A list of valid actions for the piece.
        """

        # If the piece is a locking pipe
        if piece in ('FC', 'FB', 'FE', 'FD'):

            # If the upper neighbor is connected to the lower neighbor
            if upper_neighbor in ('BB', 'BE', 'BD', 'VB', 'VE', 'LV'):
                return ['FC']
            
            
            # If the upper neighbor is not connected to the lower neighbor
            elif upper_neighbor in ('FC', 'FE', 'FD', 'BC', 'VC', 'VD', 'LH'):
                return ['FB', 'FE', 'FD']
        
        # If piece is a fork pipe
        elif piece in ('BC', 'BB', 'BE', 'BD'):

            # If the upper neighbor is connected to the lower neighbor
            if upper_neighbor in ('FB', 'BB', 'BE', 'BD', 'VB', 'VE', 'LV'):
                return ['BC', 'BE', 'BD']
            
            # If the upper neighbor is not connected to the lower neighbor
            else:
                return ['BB']
        
        # If piece is a return pipe 
        elif piece in ('VC', 'VB', 'VE', 'VD'):

            # If the upper neighbor is connected to the lower neighbor
            if upper_neighbor in ('FB', 'BB', 'BE', 'BD', 'VB', 'VE', 'LV'):
                return ['VC', 'VD']
            
            # If the upper neighbor is not connected to the lower neighbor
            else:
                return ['VB', 'VE']
            
        # If piece is a straight pipe
        elif piece in ('LH', 'LV'):

            # If the upper neighbor is connected to the lower neighbor
            if upper_neighbor in ('FB', 'BB', 'BE', 'BD', 'VB', 'VE', 'LV'):
                return ['LV']
            
            # If the upper neighbor is not connected to the lower neighbor
            else:
                return ['LH']
            
        return []
    
    def valid_actions_with_lower_neighbor(piece: str, lower_neighbor: str):

        """
        Returns valid actions for a piece considering the correct orientation of the lower neighbor.

        Args:
            piece (str): The piece identifier.
            lower_neighbor (str): The identifier of the lower neighbor.

        Returns:
            list: A list of valid actions for the piece.
        """

        # If the piece is a locking pipe
        if piece in ('FC', 'FB', 'FE', 'FD'):

            # If the lower neighbor is not connected to the upper neighbor
            if lower_neighbor in ('FB', 'FE', 'FD', 'BB', 'VB', 'VE', 'LH'):
                return ['FC', 'FE', 'FD']        
            
            # If the lower neighbor is connected to the upper neighbor
            elif lower_neighbor in ('BC', 'BE', 'BD', 'VC', 'VD', 'LV'):
                return ['FB'] 
            
        # If piece is a fork pipe
        if piece in ('BC', 'BB', 'BE', 'BD'):

            # If the lower neighbor is not connected to the upper neighbor
            if lower_neighbor in ('FB', 'FE', 'FD', 'BB', 'VB', 'VE', 'LH'):
                return ['BC'] 
            
            # If the lower neighbor is connected to the upper neighbor
            else:
                return ['BB', 'BE', 'BD'] 
            
        # If piece is a return pipe
        if piece in ('VC', 'VB', 'VE', 'VD'):

            # If the lower neighbor is not connected to the upper neighbor
            if lower_neighbor in ('FB', 'FE', 'FD', 'BB', 'VB', 'VE', 'LH'):
                return ['VC', 'VD'] 
            
            # If the lower neighbor is connected to the upper neighbor
            else:
                return ['VB', 'VE'] 
            
        # If piece is a straight pipe
        if piece in ('LH', 'LV'):

            # If the lower neighbor is not connected to the upper neighbor
            if lower_neighbor in ('FB', 'FE', 'FD', 'BB', 'VB', 'VE', 'LH'):
                return ['LH'] 
            
            # If the lower neighbor is connected to the upper neighbor
            else:
                return ['LV'] 
            
    def valid_actions_with_left_neighbor(piece: str, left_neighbor: str):

        """
        Returns valid actions for a piece considering the correct orientation of the left neighbor.

        Args:
            piece (str): The piece identifier.
            left_neighbor (str): The identifier of the left neighbor.

        Returns:
            list: A list of valid actions for the piece.
        """
        
        # If the piece is a locking pipe
        if piece in ('FC', 'FB', 'FE', 'FD'):

            # If the left neighbor is connected to the right neighbor
            if left_neighbor in ('BB', 'BC', 'BD', 'VD', 'VB', 'LH'):
                return ['FE'] 
            
            # If the left neighbor is not connected to the right neighbor
            elif left_neighbor in ('FC', 'FB', 'FE', 'BE', 'VC', 'VE', 'LV'):
                return ['FB', 'FC', 'FD']
        
        # If piece is a fork pipe
        if piece in ('BC', 'BB', 'BE', 'BD'):

            # If the left neighbor is connected to the right neighbor
            if left_neighbor in ('FD', 'BB', 'BC', 'BD', 'VD', 'VB', 'LH'):
                return ['BC', 'BE', 'BB']
            
            # If the left neighbor is not connected to the right neighbor
            else:
                return ['BD']
        
        # If piece is a return pipe
        if piece in ('VC', 'VB', 'VE', 'VD'):

            # If the left neighbor is connected to the right neighbor
            if left_neighbor in ('FD', 'BB', 'BC', 'BD', 'VD', 'VB', 'LH'):
                return ['VC', 'VE']
            
            # If the left neighbor is not connected to the right neighbor
            else:
                return ['VB', 'VD']
        
        # If piece is a straight pipe
        if piece in ('LH', 'LV'):

            # If the left neighbor is connected to the right neighbor
            if left_neighbor in ('FD', 'BB', 'BC', 'BD', 'VD', 'VB', 'LH'):
                return ['LH']
            
            # If the left neighbor is not connected to the right neighbor
            else:
                return ['LV']

        return []

    def valid_actions_with_right_neighbor(piece: str, right_neighbor: str):

        """
        Returns valid actions for a piece considering the correct orientation of the right neighbor.

        Args:
            piece (str): The piece identifier.
            right_neighbor (str): The identifier of the right neighbor.

        Returns:
            list: A list of valid actions for the piece.
        """

        # If the piece is a locking pipe
        if piece in ('FC', 'FB', 'FE', 'FD'):

            # If the right neighbor is  connected to the left neighbor
            if right_neighbor in ('BC', 'BB', 'BE', 'VC', 'VE', 'LH'):
                return ['FD']
            
            # If the right neighbor is not connected to the left neighbor
            elif right_neighbor in ('FC', 'FD', 'FB', 'BD', 'VD', 'VB', 'LV'):
                return ['FB', 'FE', 'FC'] 
            
        # If piece is a fork pipe
        if piece in ('BC', 'BB', 'BE', 'BD'):

            # If the right neighbor is connected to the left neighbor
            if right_neighbor in ('FE','BC', 'BB', 'BE', 'VC', 'VE', 'LH'):
                return ['BC', 'BB', 'BD']
            
            # If the right neighbor is not connected to the left neighbor
            else:
                return ['BE']
        
        # If piece is a return pipe
        if piece in ('VC', 'VB', 'VE', 'VD'):

            # If the right neighbor is connected to the left neighbor
            if right_neighbor in ('FE','BC', 'BB', 'BE', 'VC', 'VE', 'LH'):
                return ['VB', 'VD']
            
            # If the right neighbor is not connected to the left neighbor
            else:
                return ['VC', 'VE']
        
        # If piece is a straight pipe
        if piece in ('LH', 'LV'):

            # If the right neighbor is connected to the left neighbor
            if right_neighbor in ('FE','BC', 'BB', 'BE', 'VC', 'VE', 'LH'):
                return ['LH']
            
            # If the right neighbor is not connected to the left neighbor
            else:
                return ['LV']

        return []
    
    def get_all_rotations(self,piece: str):

        # If the piece is a locking pipe
        if piece in ('FC', 'FB', 'FE', 'FD'):
            return ['FC', 'FB', 'FE', 'FD']
        
        # If the piece is a fork pipe
        if piece in ('BC', 'BB', 'BE', 'BD'):
            return ['BC', 'BB', 'BE', 'BD']
        
        # If the piece is a return pipe
        if piece in ('VC', 'VB', 'VE', 'VD'):
            return ['VC', 'VB', 'VE', 'VD']
        
        # If the piece is a straight pipe
        if piece in ('LH', 'LV'):
            return ['LH', 'LV']

    def get_valid_rotations_pos(self, piece: str, row: int, col: int) -> list:     
        """
        Returns valid rotations of a piece based on the limits of the grid.

        Args:
            piece (str): The piece identifier.
            row (int): The row index of the piece on the grid.
            col (int): The column index of the piece on the grid.

        Returns:
            list: A list of valid rotations for the piece at the specified position.
        """  
        valid_rotations = []
        # Check if the piece is a upper left corner
        if self.board.is_corner_upper_left(row, col):
            valid_rotations.append(Board.valid_upper_left_corner_actions(piece))

        # Check if the piece is a upper right corner
        elif self.board.is_corner_upper_right(row, col):
            valid_rotations.append(Board.valid_upper_right_corner_actions(piece))

        # Check if the piece is a lower left corner
        elif self.board.is_corner_lower_left(row, col):
            valid_rotations.append(Board.valid_lower_left_corner_actions(piece))

        # Check if the piece is a lower right corner
        elif self.board.is_corner_lower_right(row, col):
            valid_rotations.append(Board.valid_lower_right_corner_actions(piece))

        # Check if the piece is an upper edge
        elif self.board.is_edge_upper(row, col):
            valid_rotations.append(Board.valid_upper_edge_actions(piece))

        # Check if the piece is a lower edge
        elif self.board.is_edge_lower(row, col) and not (self.board.is_corner_lower_left(row, col) or self.board.is_corner_lower_right(row, col)):
            valid_rotations.append(Board.valid_lower_edge_actions(piece))

        # Check if the piece is a upper edge
        elif self.board.is_edge_left(row, col) and not (self.board.is_corner_upper_left(row, col) or self.board.is_corner_upper_right(row, col)):
            valid_rotations.append(Board.valid_left_edge_actions(piece))

        # Check if the piece is a right edge
        elif self.board.is_edge_right(row, col) and not (self.board.is_corner_upper_right(row, col) or self.board.is_corner_lower_right(row, col)):
            valid_rotations.append(Board.valid_right_edge_actions(piece))

        # Check if the piece is a left piece
        elif self.board.is_edge_left(row, col) and not (self.board.is_corner_upper_left(row, col) or self.board.is_corner_lower_left(row, col)):
            valid_rotations.append(Board.valid_left_edge_actions(piece))

        # Join all the valid rotations into single array
        valid_rot = []
        for rot in valid_rotations:
            valid_rot.extend(rot)

        return valid_rot
    
    def get_valid_rotations_neighbors(self, piece: str, row: int, col: int) -> list:
        """
        Returns valid positions based on neighbors that are already in their final position.

        Args:
            piece (str): The piece identifier.
            row (int): The row index of the piece on the grid.
            col (int): The column index of the piece on the grid.

        Returns:
            list: A list of valid rotations based on the neighboring pieces.
        """
        upper = []
        lower = []
        left = []
        right = []
        exists = [False, False, False, False]   
        rotations = [upper, lower, left, right]
        existing_neighbors = []

        # See if upper neighbor is in the correct orientation 
        if row > 0:
            if self.board.is_fixed_piece(row-1, col):  

                # Get the valid rotations based on the upper neighbor
                upper.extend(Board.valid_actions_with_upper_neighbor(piece, self.board.get_value(row-1, col)))
                if len(upper) > 0:
                    exists[0] = True

        # See if lower neighbor is in the correct orientation
        if row < len(self.board.grid) - 1:
            if self.board.is_fixed_piece(row+1, col):

                # Get the valid rotations based on the lower neighbor
                lower.extend(Board.valid_actions_with_lower_neighbor(piece, self.board.get_value(row+1, col)))
                if len(lower) > 0:
                    exists[1] = True
        
        # See if left neighbor is in the correct orientation
        if col > 0:
            if self.board.is_fixed_piece(row, col-1):

                # Get the valid rotations based on the left neighbor
                left.extend(Board.valid_actions_with_left_neighbor(piece, self.board.get_value(row, col-1)))
                if len(left) > 0:  
                    exists[2] = True


        # See if right neighbor is in the correct orientation
        if col < len(self.board.grid[0]) - 1:
            if self.board.is_fixed_piece(row, col+1):

                # Get the valid rotations based on the right neighbor
                right.extend(Board.valid_actions_with_right_neighbor(piece, self.board.get_value(row, col+1)))
                if len(right) > 0:
                    exists[3] = True


        # Check if no neighbors are in the correct orientation
        if exists == [False, False, False, False]:
            return board.get_all_rotations(piece)
        
        
        # check which have valid rotations
        for i in range(4):
            if exists[i]:
                existing_neighbors.append(rotations[i])

        # do the intersection of the lists
        intersect_rotations = []
        if len(existing_neighbors) > 0:
            intersect_rotations = existing_neighbors[0]
            for i in range(1, len(existing_neighbors)):
                intersect_rotations = [value for value in intersect_rotations if value in existing_neighbors[i]]

        return intersect_rotations

    def get_valid_rotations(self, piece: str, row: int, col: int) -> list:

        """
        Returns valid rotations for a piece considering both its position and neighboring pieces.

        Args:
            piece (str): The piece identifier.
            row (int): The row index of the piece on the grid.
            col (int): The column index of the piece on the grid.

        Returns:
            list: A list of valid rotations for the piece at the specified position.
        """

        # Check if the piece is already in the correct position
        if self.is_fixed_piece(row, col):
            # If so, return an empty list
            return []

        # Get the valid rotations based on the limits of the grid
        valid_rotations_pos = self.get_valid_rotations_pos(piece, row, col) 

        # Get the valid rotations based on the neighbors of the piece that are already in the correct position
        valid_rotations_neighbors = self.get_valid_rotations_neighbors(piece, row, col) 

        # do the intersection of the two lists
        valid_rotations = []

        # See if there are limitations on the piece's position (outer border or not)
        if len(valid_rotations_neighbors) != 0 and len(valid_rotations_pos) != 0:

            # If so, the valid rotations are the intersection of the two lists
            valid_rotations = [(value, row, col, len(valid_rotations_neighbors)+len(valid_rotations_pos)) for value in valid_rotations_pos if value in valid_rotations_neighbors]

        # If the piece is not in the outer border
        elif len(valid_rotations_pos) == 0 and len(valid_rotations_neighbors) != 0:

            # If so, the valid rotations are the list of valid rotations based on the neighbors
            valid_rotations = [(value, row, col, len(valid_rotations_neighbors)) for value in valid_rotations_neighbors]
        

        return valid_rotations


    @staticmethod
    def parse_instance():
        """
        Parses an input string representing the problem instance and returns a Board instance.

        Returns:
            Board: An instance of the Board class representing the parsed grid.
        """
        grid = []
        input_str = sys.stdin.read().strip()  # Read the entire input instead of just one line
    
        lines = input_str.split('\n')  # Split by newline characters
        for line in lines:
            pieces = line.split()  # Split by whitespace (spaces)
            grid.append(pieces)

        return Board(grid)


class PipeManiaState:
    state_id = 0

    def __init__(self, board: Board):
        self.board = board
        self.id = PipeManiaState.state_id
        PipeManiaState.state_id += 1
        self.actions = []


    def __lt__(self, other):
        """ Este método é utilizado em caso de empate na gestão da lista
        de abertos nas procuras informadas. """
        return self.id < other.id
    
    def get_value(self, row: int, col: int) -> str:
        """ Devolve o valor na posição (row, col). """
        return self.board.grid[row][col]

class PipeMania(Problem):

    def __init__(self, initial_state: Board):
        """ O construtor especifica o estado inicial. """
        self.initial = initial_state

    def actions(self, state: PipeManiaState):
        """
        Returns a list of actions that can be executed from the given state.

        Args:
            state (PipeManiaState): The current state of the Pipe Mania puzzle.

        Returns:
            list: A list of actions that can be executed from the given state.
        """
        num_rows, num_cols = len(state.board.grid), len(state.board.grid[0])
        available_actions = []


        # Iterate over each position on the board
        for row in range(num_rows):
            for col in range(num_cols):
                if not state.board.is_fixed_piece(row, col):
                    piece = state.board.get_value(row, col)
                    actions_at_position = state.board.get_valid_rotations(piece, row, col)

                    # Check if position was not explored
                    if (row, col) not in state.board.explored:
                        # If not explored, check if there is a unique valid action
                        if len(actions_at_position) == 1:
                            # Validate the pipe
                            state.board.validate_pipe(row, col)
                            
                            return actions_at_position
                        
                        else:
                            # Remove its own position from the list of valid positions
                            filtered_actions_at_position = [action for action in actions_at_position if action[0] != piece]

                            # Convert the numpy arrays to lists
                            available_actions = [list(action) for action in available_actions]

                            # Convert the numpy arrays to lists
                            available_actions = [list(action) for action in available_actions]

                            # Randomly shuffle the list of valid actions with numpy
                            np.random.shuffle(filtered_actions_at_position)
                            
                            # Now, available_actions is a list of lists, and there is no dtype information
                            available_actions.extend(filtered_actions_at_position)

        # Sort the available actions by the piece identifier
        available_actions = sorted(available_actions, key=lambda x: x[0])

        # No unique action was found, lets explore one action and validate it
        if len(board.node_test) == 0:
            # No unique action was found, lets explore one action and validate it
            if len(available_actions) > 0:
                state.board.validate_pipe(available_actions[0][1], available_actions[0][2])
                test_state = state 
                board.node_test.append(test_state)
                actions_of_node = [action for action in actions_at_position if action[0] != piece and action[1] == available_actions[0][1] and action[2] == available_actions[0][2]]
                test_state.actions = actions_of_node 
        else:
            # If there is a node being tested andd there are no more possibilities, we have to revert back to the test node and explore another action
            if len(available_actions) == 0:
                last_node = board.node_test.pop()
                state.board = last_node.board
                available_actions = last_node.actions


        #print("P validas", len(state.board.valid_positions))
        # If no unique action is found, return all available actions
        #print("Available actions: ", available_actions)
        #print("\n")
        #print("Current board: ")

        return available_actions
        
        
    def goal_test(self, state: PipeManiaState)-> bool:

        """
        Checks if the given state is a goal state.

        Args:
            state (PipeManiaState): The state to be tested.

        Returns:
            bool: True if the state is a goal state, False otherwise.
        """
        
        # Try to validate new nodes
        
        if len(state.board.valid_positions) == len(state.board.grid) * len(state.board.grid[0]):
            #print("Goal reached")
            return True
        else:
            # See if pieces not validated are connected with each other
            for row in range(len(state.board.grid)):
                for col in range(len(state.board.grid[0])):
                    piece = state.board.get_value(row, col)
                    if not state.board.is_fixed_piece(row, col):
                        if not Piece(piece).isConnected(state.board, row, col):
                            
                            #print("Failed to validate piece at position: ", row, col,)
                            return False

        return True
                            

            
    def result(self, state: PipeManiaState, action):

        """
        Returns the resulting state after executing the given action on the given state.

        Args:
            state (PipeManiaState): The current state of the Pipe Mania puzzle.
            action (tuple): The action to be executed, consisting of new rotation, row, and column.

        Returns:
            PipeManiaState: The resulting state after executing the action.
        """
        
        # Create a copy of the board to modify
        new_grid = [row[:] for row in state.board.grid]
        new_board = Board(new_grid)

        # Copy the valid positions from the current state
        new_board.valid_positions = state.board.valid_positions.copy()

        # Copy the explored positions from the current state
        new_board.explored = state.board.explored.copy()

        # Update the board with the action
        new_board.grid[action[1]][action[2]] = action[0]

        # Update heuristics
        new_board.heuristic = action[3]

        # Add the actions' position to the explored list
        new_board.explored.append((action[1], action[2]))
        
        if len(state.board.node_test) != 0:
            new_board.node_test = state.board.node_test.copy()
            # copy the actions of the node being tested
            for i in range(len(state.board.node_test)):
                new_board.node_test[i].actions = state.board.node_test[i].actions.copy()

        # Create and return a new state with the modified board
        return PipeManiaState(new_board)

    def h(self, node: Node):
        """ Função heuristica utilizada para a procura A*. """
        # TODO
        # The heuristic: number of valid actions of the actions of the state
        return board.heuristic
        pass

class Piece():
    def __init__(self, piece_type: str):
        self.piece_type = piece_type

    def isConnected(self, board: Board, row: int, col: int)->bool:
        if board.is_connected_left(row, col) and board.is_connected_right(row, col) and board.is_connected_upper(row, col) and board.is_connected_lower(row, col):
            return True
        else:
            return False
        
    

if __name__ == "__main__":
    board = Board.parse_instance()
    problem = PipeMania(board)
    goal_node = depth_first_tree_search(problem)
    goal_node.state.board.print()
    pass