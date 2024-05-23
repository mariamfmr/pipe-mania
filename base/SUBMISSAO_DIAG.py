# pipe.py: Template para implementação do projeto de Inteligência Artificial 2023/2024.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes sugeridas, podem acrescentar outras que considerem pertinentes.

# Grupo 01:
# 105875 Maria Ramos
# 106909 Guiherme Campos

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

import time
import psutil

import colorama
from colorama import Fore, Back, Style
colorama.init(autoreset=True)

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

        self.invalid = False

        self.unique_to_be_explored = True

        self.action_count = 0

        self.board_size = len(grid) * len(grid[0])

        self.explored_count = 0

        self.num_rows = len(grid)

        self.num_cols = len(grid[0])
        
        # Grid for the explored board with the same dimensions as the original grid
        self.explored_grid = [[' ' for _ in range(len(grid[0]))] for _ in range(len(grid))]

        self.unique_grid = [[' ' for _ in range(len(grid[0]))] for _ in range(len(grid))]   

        

        self.last_action = None

    def is_loop(self, row: int, col: int) -> bool:
        """
        Checks if the position changed to a loop. Tries to find an unexplored position from the current position. 
        If it finds one, then it is not a loop. If it goes through all reachable positions and finds no unexplored position,
        then it is a loop.

        Args:
            row (int): The row index of the position.
            col (int): The column index of the position.

        Returns:
            bool: True if the position is a loop, False otherwise.
        """
        visited = set()
        queue = [(row, col)]

        while queue:
            current = queue.pop(0)
            visited.add(current)

            for neighbor in self.get_reachable(current[0], current[1]):
                if self.explored_grid[neighbor[0]][neighbor[1]] == ' ':
                    return False
                if neighbor not in visited:
                    queue.append(neighbor)

        return True
        
        
    
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

    def print(self):
        
        for i, row in enumerate(self.grid):
            for j, piece in enumerate(row):
                if self.unique_grid[i][j] != ' ':
                    print(Fore.GREEN + piece + "g", end='\t')
                else:
                    print(piece, end='\t')
            print()  # print a newline at the end of each row

    # Goal Test Handling Functions
    def get_reachable_explored(self, row: int, col: int) -> list:
        """
        Gets the reachable positions from the given position.

        Args:
            row (int): The row index of the position.
            col (int): The column index of the position.

        Returns:
            list: A list of reachable positions from the given position.
        """
        reachable = []
        piece = self.get_value(row, col)
        if piece in ('FC', 'BC', 'BE', 'BD', 'VC', 'VD', 'LV'):
            if row > 0:
                if self.explored_grid[row - 1][col] != ' ':
                        reachable.append((row - 1, col))
        if piece in ('FB', 'BB', 'BE', 'BD', 'VB', 'VE', 'LV'):
            if row < self.num_rows - 1:
                if self.explored_grid[row + 1][col] != ' ':
                    reachable.append((row + 1, col))
        if piece in ('FD', 'BC', 'BB', 'BD', 'VD', 'VB', 'LH'):
            if col < self.num_cols - 1:
                if self.explored_grid[row][col + 1] != ' ':
                    reachable.append((row, col + 1))
        if piece in ('FE', 'BC', 'BB', 'BE', 'VC', 'VE', 'LH'):
            if col > 0:
                if self.explored_grid[row][col - 1] != ' ':
                    reachable.append((row, col - 1))

        # Make sure the reachable positions are within the grid
        reachable = [(r, c) for r, c in reachable if 0 <= r < self.num_rows and 0 <= c < self.num_cols]

        return reachable

    def get_reachable(self, row: int, col: int) -> list:
        """
        Gets the reachable positions from the given position.

        Args:
            row (int): The row index of the position.
            col (int): The column index of the position.

        Returns:
            list: A list of reachable positions from the given position.
        """
        reachable = []
        piece = self.get_value(row, col)
        if piece in ('FC', 'BC', 'BE', 'BD', 'VC', 'VD', 'LV'):
           reachable.append((row - 1, col))
        if piece in ('FB', 'BB', 'BE', 'BD', 'VB', 'VE', 'LV'):
            reachable.append((row + 1, col))
        if piece in ('FD', 'BC', 'BB', 'BD', 'VD', 'VB', 'LH'):
            reachable.append((row, col + 1))
        if piece in ('FE', 'BC', 'BB', 'BE', 'VC', 'VE', 'LH'):
            reachable.append((row, col - 1))

        # Make sure the reachable positions are within the grid
        reachable = [(r, c) for r, c in reachable if 0 <= r < self.num_rows and 0 <= c < self.num_cols]

        return reachable

    def is_connected_left(self, piece: str, row: int, col: int) -> bool:
        """
        Checks if the piece is connected to the left.

        Args:
            piece (str): The piece identifier.
            row (int): The row index of the piece.
            col (int): The column index of the piece.
        
        Returns:
            bool: True if the piece is connected to the left, False otherwise.
        """
        
        # If piece has a left neighbor
        if col > 0:
            left_piece = self.get_value(row, col - 1)
            return left_piece in allowed_left_neighbors.get(piece, [])
        
        # Then it is a border piece
        # See if it is a corner piece
        if self.is_corner_upper_left(row, col):
            return piece in ('FB', 'FD', 'VB')
            
        # See if it is a border piece
        if self.is_edge_left(row, col):
            return piece in ('FC', 'FB', 'FD', 'BD', 'VB', 'VD', 'LV')
        
        if self.is_corner_lower_left(row, col):
            return piece in ('FC', 'FD', 'VD')

        return True
    
    def is_connected_right(self, piece: str, row: int, col: int) -> bool:
        """
        Checks if the piece is connected to the right.

        Args:
            piece (str): The piece identifier.
            row (int): The row index of the piece.
            col (int): The column index of the piece.

        Returns:
            bool: True if the piece is connected to the right, False otherwise.
        """

        # If piece has a right neighbor
        if col < self.num_cols - 1:
            right_piece = self.get_value(row, col + 1)
            return right_piece in allowed_right_neighbors.get(piece, [])
        
        # If it is a border piece
        # See if it is a corner piece
        if self.is_corner_upper_right(row, col):
            return piece in ('FE', 'FB', 'VE')
        
        # See if it is a border piece
        if self.is_edge_right(row, col):
            return piece in ('FC', 'FE', 'FB', 'BE', 'VC', 'VE', 'LV')
  
        if self.is_corner_lower_right(row, col):
            return piece in ('FC', 'FE', 'VC')

        return True
    

    def is_connected_upper(self, piece: str, row: int, col: int) -> bool:
        """
        Checks if the piece is connected to the upper.

        Args:
            piece (str): The piece identifier.
            row (int): The row index of the piece.
            col (int): The column index of the piece.
        
        Returns:
            bool: True if the piece is connected to the upper, False otherwise.
        """
        
        # If piece has an upper neighbor
        if row > 0:
            upper_piece = self.get_value(row - 1, col)
            return upper_piece in allowed_upper_neighbors.get(piece, [])
        
        # If it is a border piece
        if self.is_corner_upper_left(row, col):
            return piece in ('FB', 'FD', 'VB')
        
        if self.is_corner_upper_right(row, col):
            return piece in ('FE', 'FB', 'VE')
        
        if self.is_edge_upper(row, col):
            return piece in ('FD', 'FB', 'FE', 'BB', 'VB', 'VE', 'LH')
        
        return True

                
    def is_connected_lower(self, piece:str, row: int, col: int) -> bool:
        """
        Checks if the piece is connected to the lower.  

        Args:
            piece (str): The piece identifier.
            row (int): The row index of the piece.
            col (int): The column index of the piece.
        
        Returns:
            bool: True if the piece is connected to the lower, False otherwise.
        """
        
        # If piece has a lower neighbor
        if row < self.num_rows - 1:
            lower_piece = self.get_value(row + 1, col)
            if lower_piece in allowed_lower_neighbors.get(piece, []):
                return True
            return False

        # If it is a border piece
        # See if it is a corner piece
        if self.is_corner_lower_right(row, col):
            return piece in ('FC', 'FE', 'VC')

        if self.is_corner_lower_left(row, col):
            return piece in ('FC', 'FD', 'VD')
                
        # See if it is a border piece
        if self.is_edge_lower(row, col):
            return piece in ('FC', 'FE', 'FD', 'BC', 'VC', 'VD', 'LH')

        return True

    # Board Edge and Corner Detection Functions

    def is_corner_upper_right(self, row: int, col: int) -> bool:
        """
        Checks if the position is the upper right corner of the grid.

        Args:
            row (int): The row index of the position.
            col (int): The column index of the position.

        Returns:
            bool: True if the position is the upper right corner, False otherwise.
        """
        return row == 0 and col == self.num_cols - 1
    
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
        return row == self.num_rows - 1 and col == self.num_cols - 1
    
    def is_corner_lower_left(self, row: int, col: int) -> bool:
        """
        Checks if the position is the lower left corner of the grid.

        Args:
            row (int): The row index of the position.
            col (int): The column index of the position.

        Returns:
            bool: True if the position is the lower left corner, False otherwise.
        """
        return row == self.num_rows - 1 and col == 0
    
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
        return row == self.num_rows - 1
    
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
        return col == self.num_cols - 1          

    # Valid Actions Determination Functions Based on Position

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

    # Valid Actions Determination Functions Based on Neighbors

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
    
    def get_all_rotations(self, piece: str):
        """
        Returns all possible rotations for a piece.

        Args:
            piece (str): The piece identifier.

        Returns:
            list: A list of all possible rotations for the piece.
        """
        # Define possible rotations for each piece
        rotations = {
            'FC': ['FC', 'FB', 'FE', 'FD'],
            'FB': ['FC', 'FB', 'FE', 'FD'],
            'FE': ['FC', 'FB', 'FE', 'FD'],
            'FD': ['FC', 'FB', 'FE', 'FD'],
            'BC': ['BC', 'BB', 'BE', 'BD'],
            'BB': ['BC', 'BB', 'BE', 'BD'],
            'BE': ['BC', 'BB', 'BE', 'BD'],
            'BD': ['BC', 'BB', 'BE', 'BD'],
            'VC': ['VC', 'VB', 'VE', 'VD'],
            'VB': ['VC', 'VB', 'VE', 'VD'],
            'VE': ['VC', 'VB', 'VE', 'VD'],
            'VD': ['VC', 'VB', 'VE', 'VD'],
            'LH': ['LH', 'LV'],
            'LV': ['LH', 'LV']
        }
        
        # Return possible rotations for the given piece
        return rotations.get(piece, [])

    def f_piece_restrictions(self, row: int, col: int) -> list:
        piece = self.board.get_value(row, col)
        f_neighbors_count = 0
        upper = False
        lower = False
        left = False
        right = False
        # Returns [upper, lower, left, right] neighbors that are F pieces
        if row > 0:
            # If upper neighbor is starts with F
            if self.board.get_value(row-1, col).startswith('F'):
                upper = True
                f_neighbors_count += 1
        
        if row < self.board.num_rows - 1:
            # If lower neighbor is starts with F
            if self.board.get_value(row+1, col).startswith('F'):
                lower = True
                f_neighbors_count += 1

        if col > 0:
            # If left neighbor is starts with F
            if self.board.get_value(row, col-1).startswith('F'):
                left = True
                f_neighbors_count += 1

        if col < self.board.num_cols - 1:
            # If right neighbor is starts with F
            if self.board.get_value(row, col+1).startswith('F'):
                right = True
                f_neighbors_count += 1
        
        # If piece starts with F and has at least 1 F neighbor
        if piece.startswith('F'):
            if f_neighbors_count == 1:
                if upper == True:
                    return ['FB', 'FE', 'FD']
                if left == True:
                    return ['FC', 'FD', 'FB']
                if lower == True:
                    return ['FC', 'FE', 'FD']
                if right == True:
                    return ['FC', 'FB', 'FE']
            
            if f_neighbors_count == 2:
                if upper == True and lower == True:
                    return ['FE', 'FD']
                if left == True and right == True:
                    return ['FC', 'FB']
                if upper == True and right == True:
                    return ['FE', 'FB']
                if upper == True and left == True:
                    return ['FD', 'FB']
                if lower == True and right == True:
                    return ['FE', 'FC']
                if lower == True and left == True:
                    return ['FD', 'FC']
                
            if f_neighbors_count == 3:
                if upper == False:
                    return ['FC']
                if lower == False:
                    return ['FB']
                if left == False:
                    return ['FE']
                if right == False:
                    return ['FD']
                

    # Board Rotation Functions

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
        elif self.board.is_edge_upper(row, col) and not (self.board.is_corner_upper_left(row, col) or self.board.is_corner_upper_right(row, col)):
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
            if self.explored_grid[row-1][col] != ' ':
                
                # Get the valid rotations based on the upper neighbor
                upper.extend(Board.valid_actions_with_upper_neighbor(piece, self.board.explored_grid[row-1][col]))
                if len(upper) > 0:
                    exists[0] = True

        # See if lower neighbor is in the correct orientation
        if row < self.board.num_rows - 1:
            if self.explored_grid[row+1][col] != ' ':

                # Get the valid rotations based on the lower neighbor
                lower.extend(Board.valid_actions_with_lower_neighbor(piece, self.board.explored_grid[row+1][col]))
                if len(lower) > 0:
                    exists[1] = True
        
        # See if left neighbor is in the correct orientation
        if col > 0:
            if self.explored_grid[row][col-1] != ' ':

                # Get the valid rotations based on the left neighbor
                left.extend(Board.valid_actions_with_left_neighbor(piece, self.board.explored_grid[row][col-1]))
                if len(left) > 0:  
                    exists[2] = True


        # See if right neighbor is in the correct orientation
        if col < self.board.num_cols - 1:
            if self.explored_grid[row][col+1] != ' ':

                # Get the valid rotations based on the right neighbor
                right.extend(Board.valid_actions_with_right_neighbor(piece, self.board.explored_grid[row][col+1]))
                if len(right) > 0:
                    exists[3] = True

        
        
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

         # Check if no neighbors are in the correct orientation
        if exists == [False, False, False, False]:
            intersect_rotations = board.get_all_rotations(piece)

        # Check if piece (except B pieces) have F pieces in the neighbors
        f_neighbor_restrictions = self.f_piece_restrictions(row, col)
        
        # Intersect the valid rotations with the F piece restrictions
        if f_neighbor_restrictions != None:
            intersect_rotations = [value for value in intersect_rotations if value in f_neighbor_restrictions]
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
        if self.explored_grid[row][col] != ' ':
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
            valid_rotations = [(value, row, col) for value in valid_rotations_pos if value in valid_rotations_neighbors]

        # If the piece is not in the outer border
        elif len(valid_rotations_pos) == 0 and len(valid_rotations_neighbors) != 0:

            # If so, the valid rotations are the list of valid rotations based on the neighbors
            valid_rotations = [(value, row, col) for value in valid_rotations_neighbors]
    
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
    

from collections import deque

class PipeManiaState:
    state_id = 0

    state_possible_actions = []

    def __init__(self, board: Board):
        self.board = board
        self.id = PipeManiaState.state_id
        PipeManiaState.state_id += 1


    def __lt__(self, other):
        """ Este método é utilizado em caso de empate na gestão da lista
        de abertos nas procuras informadas. """
        return self.board.action_count > other.board.action_count
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
        num_rows, num_cols = state.board.num_rows, state.board.num_cols
        unique_actions = [] 
        available_actions = []

        if state.board.invalid:
            return []

        if state.board.unique_to_be_explored:
            for row in range(num_rows):
                for col in range(num_cols):
                    piece = state.board.get_value(row, col)
                    valid_rotations = state.board.get_valid_rotations(piece, row, col)
                    if len(valid_rotations) == 1:
                        state.board.explored_grid[row][col] = valid_rotations[0][0]
                        available_actions.append(valid_rotations[0])
                        state.board.unique_grid[row][col] = valid_rotations[0][0]
            if available_actions:
                #Add positions to rotated list
                
                return [available_actions]

        print("Explored Count: ", state.board.explored_count)
        state.board.unique_to_be_explored = False
            
        for s in range(num_rows + num_cols - 1):
            for row in range(max(0, s - num_cols + 1), min(s + 1, num_rows)):
                col = s - row
                if state.board.explored_grid[row][col] == ' ':
                    piece = state.board.get_value(row, col)
                    valid_rotations = state.board.get_valid_rotations(piece, row, col)
                    if len(valid_rotations) > 1:
                        for rotation in valid_rotations:
                            action = unique_actions.copy()
                            action.append(rotation)
                            available_actions.append(action)
                            state.board.unique_grid[row][col] = rotation[0]
                        return available_actions

                    if not valid_rotations:
                        if not available_actions:
                            if not unique_actions:
                                state.board.invalid = True
                                if state.board.explored_count < 190 and state.board.explored_count > 175:
                                    state.board.print()
                                    print("Piece: ", piece, "Row: ", row, "Col: ", col)
                                    print("Invalid")
                                    print()
                                return []
                            return unique_actions

                    else:
                        state.board.explored_grid[row][col] = valid_rotations[0][0]
                        unique_actions.append(valid_rotations[0])
                        state.board.unique_grid[row][col] = valid_rotations[0][0]

        return [unique_actions]
            
            
    def goal_test(self, state: PipeManiaState)-> bool:

        """
        Checks if the given state is a goal state.

        Args:
            state (PipeManiaState): The state to be tested.

        Returns:
            bool: True if the state is a goal state, False otherwise.
        """

        if state.board.explored_count != state.board.board_size:
            return False
        
        if len(state.board.last_action) == 0:
            return self.bfs(state, (0,0))
        
        # Check if the last action is list
        if isinstance(state.board.last_action, list):
            return self.bfs(state, (state.board.last_action[-1][1], state.board.last_action[-1][2]))
        elif isinstance(state.board.last_action, tuple):
            return self.bfs(state, (state.board.last_action[1], state.board.last_action[2]))

    

   
    def bfs(self, state, source):
        """
        Perform a BFS traversal from the source position to check if all explored positions are connected.
        This BFS ensures that each node is visited exactly once and doesn't form cycles.

        Args:
            state: The current state of the board.
            source: The starting position (row, col) for the BFS traversal.

        Returns:
            bool: True if all explored positions are connected and no cycles are detected, False otherwise.
        """
        num_rows = len(state.board.grid)
        num_cols = len(state.board.grid[0])
        visited = [[False for _ in range(num_cols)] for _ in range(num_rows)]
        queue = deque([(source, None)])  # Store (current_node, previous_node)

        while queue:
            (row, col), prev = queue.popleft()
            
            if visited[row][col]:
                continue
            
            visited[row][col] = True

            reachable_positions = state.board.get_reachable_explored(row, col)
            for next_row, next_col in reachable_positions:
                if (next_row, next_col) != prev:
                    if visited[next_row][next_col]:
                        state.board.invalid = True
                        return False  # Found a cycle
                    queue.append(((next_row, next_col), (row, col)))

        # Check if all explored positions have been visited
        for r in range(num_rows):
            for c in range(num_cols):
                if state.board.explored_grid[r][c] != ' ' and not visited[r][c]:
                    state.board.invalid = True
                    return False

        state.board.invalid = True
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
        
        # Mark parent as invalid since it has been explored
        state.board.invalid = True

        # Create a copy of the board to modify
        new_grid = [row[:] for row in state.board.grid]
        new_board = Board(new_grid)


        new_board.unique_to_be_explored = state.board.unique_to_be_explored

        new_board.action_count = len(action)

        new_board.explored_count = state.board.explored_count

        new_board.last_action = action

        # Copy explored positions
        new_board.explored_grid = [row[:] for row in state.board.explored_grid]  
        new_board.unique_grid = [row[:] for row in state.board.unique_grid]

        if len(action) == 3 and isinstance(action[0], str):
            new_board.grid[action[1]][action[2]] = action[0]

            # Add them to the explored grid
            new_board.explored_grid[action[1]][action[2]] = action[0]
            new_board.explored_count += 1

        else:
            for rotation in action:   
                new_board.grid[rotation[1]][rotation[2]] = rotation[0]

                # Add them to the explored grid
                new_board.explored_grid[rotation[1]][rotation[2]] = rotation[0]
                new_board.explored_count += 1

        return PipeManiaState(new_board)

    def h(self, node: Node):
        if node.state.board.invalid:
            return node.state.board.board_size + 1

        return node.state.board.action_count
    

if __name__ == "__main__":
    start_time = time.time()

    # Track initial memory usage
    initial_memory = psutil.Process().memory_info().rss
    
    board = Board.parse_instance()
    problem = PipeMania(board)
    goal_node = greedy_search(problem)
    goal_node.state.board.print()
    
    # Calculate execution time
    end_time = time.time()
    execution_time = end_time - start_time
    print("Execution time:", execution_time, "seconds")

    
    
    # Calculate memory usage
    final_memory = psutil.Process().memory_info().rss
    memory_usage = final_memory - initial_memory
    memory_usage_MB = memory_usage / (1024 * 1024)
    print("Memory usage:", memory_usage_MB, "MB")
    print("Size:", len(board.grid[0] * len(board.grid)))
    pass