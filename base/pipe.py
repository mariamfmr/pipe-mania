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

        # Grid for the board
        self.grid = grid

        # Board for the board
        self.board = self

        # Grid for positions in the correct orientation
        self.valid_positions = []

        self.validNeighborsMissing = []



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
        
    def get_connected_pieces(self) -> list:
        """ Retorna uma lista de peças conectadas à peça na posição (row, col). """
        connected_pieces = []
        # check for each piece if it is connected
        for row in range(len(self.grid)):
            for col in range(len(self.grid[0])):
                piece = self.get_value(row, col)
                if Piece(piece).isConnected(self, row, col):
                    connected_pieces.append([row, col])
        return connected_pieces

    def get_value(self, row: int, col: int) -> str:
        """ Devolve o valor na posição (row, col). """
        return self.grid[row][col]

    def print(self):
        """ Imprime a grelha. """
        for row in self.grid:
            print('\t'.join(row))

    def is_fixed_piece(self, row: int, col: int) -> bool:
        """ Verifica se a posição está correta. """
        return (row, col) in self.valid_positions

    def validatePipe(self, row: int, col: int):
        # Validate piece at the given position
        if not self.is_fixed_piece(row, col):
            self.valid_positions.append((row, col))

    def validateBorders(self):
        """
        Validates the pipes at the borders of the grid to ensure correct orientation and position.

        Iterates over the upper and bottom rows, and left and right columns, excluding corners,
        looking for straight pipes and adjusts them to horizontal or vertical orientation accordingly,
        while validating their positions.

        Iterates over the corner pipes, adjusting them to the correct orientation and validating their positions.
        """

        # Iterate over upper and bottom rows except corners
        for col in range(1, len(self.grid[0])-1):

            # Check if the piece is a straight pipe in the upper row
            if self.grid[0][col] in ('LH', 'LV'):

                # Change the piece to horizontal
                self.grid[0][col] = 'LH'

                # Validate the position of the piece
                self.validatePipe(0, col)
            
            # Check if the piece is a straight pipe in the bottom row
            if self.grid[len(self.grid)-1][col] in ('LH', 'LV'):

                # Change the piece to horizontal
                self.grid[len(self.grid)-1][col] = 'LH'

                # Validate the position of the piece
                self.validatePipe(len(self.grid)-1, col)

        # Iterate over left and right columns except corners
        for row in range(1, len(self.grid)-1):

            # Check if the piece is a straight pipe in the left column
            if self.grid[row][0] in ('LH', 'LV'):

                # Change the piece to vertical
                self.grid[row][0] = 'LV'

                # Validate the position of the piece
                self.validatePipe(row, 0)

            # Check if the piece is a straight pipe in the right column
            if self.grid[row][len(self.grid[0])-1] in ('LH', 'LV'):

                # Change the piece to vertical
                self.grid[row][len(self.grid[0])-1] = 'LV'

                # Validate the position of the piece
                self.validatePipe(row, len(self.grid[0])-1)

        # See if the upper left corner is a return pipe
        if self.grid[0][0] in ('VC', 'VB', 'VE', 'VD'):

            # Change the piece to correct orientation
            self.grid[0][0] = 'VB'

            # Validate the position of the piece
            self.validatePipe(0, 0)

        # See if the upper right corner is a return pipe
        if self.grid[0][len(self.grid[0])-1] in ('VC', 'VB', 'VE', 'VD'):

            # Change the piece to correct orientation
            self.grid[0][len(self.grid[0])-1] = 'VE'

            # Validate the position of the piece
            self.validatePipe(0, len(self.grid[0])-1)

        # See if the lower left corner is a return pipe
        if self.grid[len(self.grid)-1][0] in ('VC', 'VB', 'VE', 'VD'):

            # Change the piece to correct orientation
            self.grid[len(self.grid)-1][0] = 'VD'

            # Validate the position of the piece
            self.validatePipe(len(self.grid)-1, 0)

        # See if the lower right corner is a return pipe
        if self.grid[len(self.grid)-1][len(self.grid[0])-1] in ('VC', 'VB', 'VE', 'VD'):

            # Change the piece to correct orientation
            self.grid[len(self.grid)-1][len(self.grid[0])-1] = 'VC'

            # Validate the position of the piece
            self.validatePipe(len(self.grid)-1, len(self.grid[0])-1)

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
            if left_neighbor in ('BB', 'BC', 'BD', 'VD' 'VB', 'LH'):
                return ['FE']
            
            # If the left neighbor is not connected to the right neighbor
            elif left_neighbor in ('FC', 'FB', 'FE', 'BE', 'VC', 'VE', 'LV'):
                return ['FB', 'FC', 'FD']
        
        # If piece is a fork pipe
        if piece in ('BC', 'BB', 'BE', 'BD'):

            # If the left neighbor is connected to the right neighbor
            if left_neighbor in ('FD', 'BB', 'BC', 'BD', 'VD' 'VB', 'LH'):
                return ['BC', 'BE', 'BB']
            
            # If the left neighbor is not connected to the right neighbor
            else:
                return ['BD']
        
        # If piece is a return pipe
        if piece in ('VC', 'VB', 'VE', 'VD'):

            # If the left neighbor is connected to the right neighbor
            if left_neighbor in ('FD', 'BB', 'BC', 'BD', 'VD' 'VB', 'LH'):
                return ['VC', 'VE']
            
            # If the left neighbor is not connected to the right neighbor
            else:
                return ['VB', 'VD']
        
        # If piece is a straight pipe
        if piece in ('LH', 'LV'):

            # If the left neighbor is connected to the right neighbor
            if left_neighbor in ('FD', 'BB', 'BC', 'BD', 'VD' 'VB', 'LH'):
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
            elif right_neighbor in ('FC', 'BE', 'VD', 'VB', 'BC', 'LH'):
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
    
    # returns valid positions based on neighbors that are already in their final position
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
        valid_rotations = []

        # See if upper neighbor is in the correct orientation 
        if row > 0:
            if self.board.is_fixed_piece(row-1, col):  

                # Get the valid rotations based on the upper neighbor
                valid_rotations.append(Board.valid_actions_with_upper_neighbor(piece, self.board.get_value(row-1, col)))

        # See if lower neighbor is in the correct orientation
        if row < len(self.board.grid) - 1:
            if self.board.is_fixed_piece(row+1, col):

                # Get the valid rotations based on the lower neighbor
                valid_rotations.append(Board.valid_actions_with_lower_neighbor(piece, self.board.get_value(row+1, col)))
        
        # See if left neighbor is in the correct orientation
        if col > 0:
            if self.board.is_fixed_piece(row, col-1):

                # Get the valid rotations based on the left neighbor
                valid_rotations.append(Board.valid_actions_with_left_neighbor(piece, self.board.get_value(row, col-1)))

        # See if right neighbor is in the correct orientation
        if col < len(self.board.grid[0]) - 1:
            if self.board.is_fixed_piece(row, col+1):

                # Get the valid rotations based on the right neighbor
                valid_rotations.append(Board.valid_actions_with_right_neighbor(piece, self.board.get_value(row, col+1)))


        # Intersection of the valid rotations
        intersect_rotations = []    
        size = len(valid_rotations)
        if size > 0:
            for rot in valid_rotations[0]:
                for i in range(0, size):
                    if rot in valid_rotations[i] and rot != piece:
                        intersect_rotations.append(rot)

        return intersect_rotations

    # valid rotations for one position
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

        # if there is only one valid rotation, we can conclude that the piece is in the correct position
        if len(valid_rotations) == 1:
            
        return valid_rotations

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
        self.goal = goal_state
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
        if (piece == 'FC' and board.is_edge_upper(row, col) or (piece == 'FC' and board.get_value(row-1, col) == 'FB')):
            return False
        elif (piece == 'FB' and board.is_edge_lower(row, col) or (piece == 'FB' and board.get_value(row+1, col) == 'FC')):
            return False
        elif (piece == 'FE' and board.is_edge_left(row, col) or (piece == 'FE' and board.get_value(row, col-1) == 'FD')):
            return False
        elif (piece == 'FD' and board.is_edge_right(row, col) or (piece == 'FD' and board.get_value(row, col+1) == 'FE')):
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

    def actions(self, state: PipeManiaState):
        """ Returns a 3D array of actions that can be executed from the given state. """
        num_rows, num_cols = len(state.board.grid), len(state.board.grid[0])
        available_actions = []

        # Iterate over each position on the board
        for row in range(num_rows):
            for col in range(num_cols):
                if not state.board.is_fixed_piece(row, col):
                    piece = state.board.get_value(row, col)
                    actions_at_position = state.board.get_valid_rotations(piece, row, col)
                    available_actions.extend(actions_at_position)
        return available_actions
        
        
    def goal_test(self, state: PipeManiaState)-> bool:
        if (state.board.grid == self.goal.grid) and (state.board.valid_positions == len(self.goal.grid) * len(self.goal.grid[0])):
            print("Goal reached")
            return True
        return False
    
    def result(self, state: PipeManiaState, action): # action = (new_rot, row, col)
        """ Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state). """
        # Create a copy of the board to modify
        new_grid = [row[:] for row in state.board.grid]
        new_board = Board(new_grid)
        new_board.valid_positions = state.board.valid_positions.copy()
        new_board.grid[action[1]][action[2]] = action[0]
        new_board.validatePipe(action[1], action[2])
        
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
                
        
if __name__ == "__main__":
    # TODO:
    # Ler o ficheiro do standard input,
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    # Assuming you have the input string
    input_string = "FB\tVC\tVD\nBC\tBB\tLV\nFB\tFB\tFE\n"

    board = Board.parse_instance(input_string)
    board.print()
    board.validateBorders() 
    print("\n")
    board.print()
    
    s1 = PipeManiaState(board)
    
    goal = "FB\tVB\tVE\nBD\tBE\tLV\nFC\tFC\tFC\n"
    goal_board = Board.parse_instance(goal)
    s2 = PipeManiaState(goal_board)
    
    
    problem = PipeMania(board, goal_board)
    print(board.valid_positions)

    root = Node(PipeManiaState(board), None, None, 0)
    #print(problem.actions(root.state))
    #expand_tree(problem, root)
    
    goal_node = depth_first_tree_search(problem)
    #goal_node.state.board.print()
    #goal_node2 = breadth_first_tree_search(problem)



    #goal = breadth_first_tree_search(problem)

    #print("Is goal?", Problem.goal_test(problem, s2))
    #print("Solution:\n", goal_node.solution(), sep="")
    pass