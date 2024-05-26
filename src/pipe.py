# Grupo 01:
# 105875 Maria Ramos
# 106909 Guiherme Campos

from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
)

import sys
from collections import deque

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

        # Flag to check if the board is invalid
        self.invalid = False

        # Auxiliar flag for the actions method
        self.unique_to_be_explored = True

        # Number of actions taken
        self.action_count = 0

        # Number of pipes in the board
        self.board_size = len(grid) * len(grid)

        # Number of explored pipes
        self.explored_count = 0

        self.num_rows = len(grid)

        self.num_cols = len(grid)
        
        # Grid for the explored positions
        self.explored_grid = [[' ' for _ in range(self.num_rows)] for _ in range(self.num_cols)]

        # Action that led to the current state
        self.last_action = None

    def print(self):
        """
        Prints the grid layout.

        """
        for row in self.grid:
            print('\t'.join(row))

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

    def get_reachable_explored(self, row: int, col: int) -> list:
        """
        Gets the reachable explored positions from the given position.

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
    
    # Auxiliar Functions to Check Position of the a Piece

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
    
    # Rotation Functions
    
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

    def piece_restrictions(self, row: int, col: int) -> list:
        """
        Returns valid rotations based on the types of pieces in the neighbors of the given position.

        Args:
            row (int): The row index of the position.
            col (int): The column index of the position.

        Returns:
            list: A list of valid rotations based on the F pieces in the neighbors.
        """

        piece = self.board.get_value(row, col)
        neighbors_count = 0

        # Neighbors that are F pieces
        upper = False
        lower = False
        left = False
        right = False

        # Returns [upper, lower, left, right] neighbors that are F pieces
        if row > 0:
            # If upper neighbor is starts with F
            if self.board.get_value(row-1, col).startswith('F'):
                upper = True
                neighbors_count += 1
        
        if row < self.board.num_rows - 1:
            # If lower neighbor is starts with F
            if self.board.get_value(row+1, col).startswith('F'):
                lower = True
                neighbors_count += 1

        if col > 0:
            # If left neighbor is starts with F
            if self.board.get_value(row, col-1).startswith('F'):
                left = True
                neighbors_count += 1

        if col < self.board.num_cols - 1:
            # If right neighbor is starts with F
            if self.board.get_value(row, col+1).startswith('F'):
                right = True
                neighbors_count += 1
        
        # If piece starts with F
        if piece.startswith('F'):

            # If there is only one F neighbor
            if neighbors_count == 1:
                if upper == True:
                    return ['FB', 'FE', 'FD']
                if left == True:
                    return ['FC', 'FD', 'FB']
                if lower == True:
                    return ['FC', 'FE', 'FD']
                if right == True:
                    return ['FC', 'FB', 'FE']
            
            # If there are two F neighbors
            if neighbors_count == 2:
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
            
            # If there are three F neighbors
            if neighbors_count == 3:
                if upper == False:
                    return ['FC']
                if lower == False:
                    return ['FB']
                if left == False:
                    return ['FE']
                if right == False:
                    return ['FD']
            
        # If the piece starts with V
        if piece.startswith('V'):

            # If there is only two F neighbor
            if neighbors_count == 2:
                if upper == True and right == True:
                    return ['VC', 'VE', 'VB']
                if upper == True and left == True:
                    return ['VD', 'VE', 'VB']
                if lower == True and right == True:
                    return ['VC', 'VD', 'VE']
                if lower == True and left == True:
                    return ['VC', 'VD', 'VB']
            
            # If there are three F neighbors
            if neighbors_count == 3:
                if upper == False:
                    return ['VC', 'VD']
                if lower == False:
                    return ['VB', 'VE']
                if left == False:
                    return ['VC', 'VE']
                if right == False:
                    return ['VD', 'VB']

        # If the piece starts with L
        if piece.startswith('L'):

            # If there is only two F neighbor
            if neighbors_count == 2:
                if upper == True and lower == True:
                    return ['LH']
                if left == True and right == True:
                    return ['LV']
                
            # If there are three F neighbors
            if neighbors_count == 3:
                if upper == False:
                    return ['LV']
                if lower == False:
                    return ['LV']
                if left == False:
                    return ['LH']
                if right == False:
                    return ['LH']
        
        return self.board.get_all_rotations(piece)

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

        # Initialize lists for the rotations of the neighbors
        upper = []
        lower = []
        left = []
        right = []

        # Initialize a list to check if the neighbors are in the correct orientation
        exists = [False, False, False, False]   
        rotations = [upper, lower, left, right]

        # Initialize a list to store the neighbors that are in the correct orientation
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

        
        
        # Check which have valid rotations
        for i in range(4):
            if exists[i]:
                existing_neighbors.append(rotations[i])

        # Do the intersection of the lists
        intersect_rotations = []
        if len(existing_neighbors) > 0:
            intersect_rotations = existing_neighbors[0]
            for i in range(1, len(existing_neighbors)):
                intersect_rotations = [value for value in intersect_rotations if value in existing_neighbors[i]]

         # Check if no neighbors are in the correct orientation
        if exists == [False, False, False, False]:
            intersect_rotations = board.get_all_rotations(piece)

        # Check if piece (except B pieces) have F pieces in the neighbors
        f_neighbor_restrictions = self.piece_restrictions(row, col)
        
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

        # Do the intersection of the two lists
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
        input_str = sys.stdin.read().strip()  # Read the entire input
    
        lines = input_str.split('\n')  # Split by newline characters
        for line in lines:
            pieces = line.split()  # Split by whitespaces
            grid.append(pieces)

        # Create a Board instance with the parsed grid
        return Board(grid)

class PipeManiaState:
    # Static variable to keep track of the state id
    state_id = 0

    def __init__(self, board: Board):
        """
        Initializes a new PipeManiaState instance.

        Args:
            board (Board): The board
        """

        # Set the board 
        self.board = board
        
        # Set the state id
        self.id = PipeManiaState.state_id

        # Increment the state id
        PipeManiaState.state_id += 1


    def __lt__(self, other):
        """This method is used in case of a tie in managing the open list in informed searches.
        
        Args:
            other (PipeManiaState): The other state to compare with.
        """
        return self.board.action_count > other.board.action_count

class PipeMania(Problem):

    def __init__(self, initial_state: Board):
        """The constructor specifies the initial state."""

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

        # Check if the board is invalid
        if state.board.invalid:
            return []

        # Check if there are still only unique actions to be explored
        if state.board.unique_to_be_explored:
            for row in range(num_rows):
                for col in range(num_cols):
                    piece = state.board.get_value(row, col)
                    valid_rotations = state.board.get_valid_rotations(piece, row, col)

                    # If there is only one valid rotation for a piece
                    if len(valid_rotations) == 1:
                        # Mark the position as explored
                        state.board.explored_grid[row][col] = valid_rotations[0][0]

                        # Accumulate the unique action
                        available_actions.append(valid_rotations[0])
        
            if available_actions:
                return [available_actions]

        # Mark the board as not unique to be explored if there are no unique actions
        state.board.unique_to_be_explored = False

        """
        For a center exploration method, replace iterating logic with:
        center_row, center_col = num_rows // 2, num_cols // 2
        cells = [(row, col) for row in range(num_rows) for col in range(num_cols)]
        cells.sort(key=lambda cell: abs(cell[0] - center_row) + abs(cell[1] - center_col))

        for row, col in cells:
            (...)
        """

        # Iterate the board in a diagonal manner
        for s in range(num_rows + num_cols - 1):
            for row in range(max(0, s - num_cols + 1), min(s + 1, num_rows)):
                col = s - row
                # If the position is not explored
                if state.board.explored_grid[row][col] == ' ':
                    piece = state.board.get_value(row, col)
                    valid_rotations = state.board.get_valid_rotations(piece, row, col)
                    # If there is more than one valid rotation for a piece
                    if len(valid_rotations) > 1:
                        for rotation in valid_rotations:
                            action = unique_actions.copy()
                            action.append(rotation)
                            available_actions.append(action)
                        # Return unique actions along with one of the valid rotations
                        return available_actions

                    # If there is no valid rotation for a piece, mark the board as invalid
                    if not valid_rotations:
                        if not available_actions:
                            if not unique_actions:
                                state.board.invalid = True
                                return []
                            return unique_actions

                    else:
                        state.board.explored_grid[row][col] = valid_rotations[0][0]
                        unique_actions.append(valid_rotations[0])

        # Return the unique actions
        return [unique_actions]
                         
    def goal_test(self, state: PipeManiaState)-> bool:

        """
        Checks if the given state is a goal state.

        Args:
            state (PipeManiaState): The state to be tested.

        Returns:
            bool: True if the state is a goal state, False otherwise.
        """

        # Check if the board is fully explored
        if state.board.explored_count != state.board.board_size:
            return False
        
        # If last action is None
        if len(state.board.last_action) == 0:
            return self.bfs(state, (0,0))
        
        # Check if the last action is list
        if isinstance(state.board.last_action, list):
            return self.bfs(state, (state.board.last_action[-1][1], state.board.last_action[-1][2]))
        elif isinstance(state.board.last_action, tuple):
            return self.bfs(state, (state.board.last_action[1], state.board.last_action[2]))
   
    def bfs(self, state, source):
        """
        Perform a BFS traversal from a given position to check if all positions are connected.
        This BFS ensures that each node is visited exactly once and doesn't form cycles.

        Args:
            state: The current state of the board.
            source: The starting position (row, col) for the BFS traversal.

        Returns:
            bool: True if all explored positions are connected and no cycles are detected, False otherwise.
        """
        num_rows = state.board.num_rows
        num_cols = state.board.num_cols
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
                    return False # Not all positions are connected

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

        # Copy the board attributes
        new_board.unique_to_be_explored = state.board.unique_to_be_explored

        new_board.action_count = len(action)

        new_board.explored_count = state.board.explored_count

        # Copy the action that led to the new state
        new_board.last_action = action

        # Copy explored positions
        new_board.explored_grid = [row[:] for row in state.board.explored_grid]  

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
        """Heuristic function"""

        # Check if the node is invalid
        if node.state.board.invalid:
            # Return a high value to avoid expanding invalid nodes
            return node.state.board.board_size + 1
        return node.state.board.board_size - node.state.board.explored_count

if __name__ == "__main__": 
    board = Board.parse_instance()
    problem = PipeMania(board)
    goal_node = greedy_search(problem)
    goal_node.state.board.print()
    pass