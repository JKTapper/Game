"""
This file defines the Game class for the other python scripts to use. The game
defined here 'ocupy row' is a generalised noughts & crosses that can be played
on a board with arbitrary dimensions and with an abritrary number of players.
These values can be changed not just by editing the code but also by the user
while the code is running using the inbuilt settings.
"""
import re
import random

class Game:
    """
    The class variables and methods handle the game setup parameters, which
    the user can change in settings and also a couple other things that do
    not depend on the specific state of the game.
    """
    
    setup_input = 'Begin game?'
    Help = 'Placeholder'
    players = [['human','X'],['random','O']]
    options = {'dimensions':(3,3),'players':players,'number of players':len(players)} #default options
    advanced_options_explanation = 'Placeholder'

    @classmethod
    def change_options(cls):
        """
        This class method allows the use to change the fundamental
        parameters of the game like the sixe of the board and the
        number of players.
        """
        size = int(input('What size of board do you want to play on?'))
        number_of_human_players = int(input('Single player(1) or multiplayer(2)?'))
        players = [['player1','X'],['player2','O']]
        if number_of_human_players == 1:
            player_turn = int(input('Do you want to go first(type 0) or second(type 1)?'))
            players[player_turn][0] = 'human'
            players[1-player_turn][0] = 'random'
        elif number_of_human_players == 2:
            players = [('human','X'),('human','O')]
        else:
            players = [('random','X'),('random','O')]
        dimensions = (size,size)
        Game.options = {'dimensions':dimensions,'players':players,'number of players':len(players)}

    @classmethod
    def game_type_string(cls):
        """
        This class method returns a string representing the game's
        fundamental parameters. It's used to name SQL tables of
        game positions.
        """
        return 'ocupy_row' + ''.join([str(dimension) for dimension in Game.options['dimensions']]) + str(Game.options['number of players'])

    #def change_options_advanced(cls,advanced_options_string):
        
    
    def __init__(self):
        """
        This method create a new game with all blanks cells.
        """
        dimensions = Game.options['dimensions']
        players = Game.options['players']
        self.width = dimensions[0]
        self.height = dimensions[1]
        cells = {}
        empty_cells = set({})
        for x in range(self.width):
            for y in range(self.height):
                cells[(x,y)] = '.'
                empty_cells.add((x,y))
        self.cells = cells
        self.empty_cells = empty_cells
        horizontal = [[(x,y) for x in range(0,self.width)] for y in range(0,self.height)]
        vertical = [[(x,y) for y in range(0,self.height)] for x in range(0,self.width)]
        lines = horizontal + vertical
        if self.width == self.height:
            diagonal = [[(x,x) for x in range(self.width)],[(x,self.width - x - 1) for x in range(self.width)]]
            lines += diagonal
        self.winning_lines = lines
        self.turn = 0
        self.active_player = Game.options['players'][self.turn]
        self.next_turn = 1
        self.next_player = Game.options['players'][self.next_turn]

    def __str__(self):
        """This method defines how a board state can be
        transformed into a string that can then be displayed
        as an ASCII representation of the game.
        """
        rows = ['|'.join(['',*[self.cells[(x,y)] for x in range(0,self.width)],''])for y in range(self.height)]
        return ('\n ' + '-'*(2*self.width - 1) + ' \n').join(['',*rows,''])

    def compressed_string(self):
        """This method defines an alternative way to represent
        a game state with a string. This time it's optimised
        for length rather than legibility so it can be entered
        into a database.
        """
        rows = [''.join([self.cells[(x,y)] for x in range(0,self.width)])for y in range(self.height)]
        return ''.join(rows)

    def flip_compressed_string_horizontal(self,string):
        return ''.join([string[i*self.width:(i+1)*self.width][::-1] for i in range(self.height)])
    

    def flip_compressed_string_vertical(self,string):
        return ''.join([string[i*self.width:(i+1)*self.width] for i in range(self.height)][::-1])
    

    def flip_compressed_string_diagonal(self,string):
        return ''.join(string[i + j * self.width] for i in range(self.width) for j in range(self.width))

    def return_symmetrical_compressed_strings(self,string):
        """
        This method uses the previous three methods to identify
        other game states that are equiviliant to a given one.
        Note that it only identifys the associated compressed
        string representations rather than the games themselves.
        """
        strings = {string}
        return strings
        if self.width != self.height:
            string = self.flip_compressed_string_horizontal(string)
            strings.add(string)
            string = self.flip_compressed_string_vertical(string)
            strings.add(string)
            string = self.flip_compressed_string_horizontal(string)
            strings.add(string)
            return strings
        string = self.flip_compressed_string_diagonal(string)
        strings.add(string)
        string = self.flip_compressed_string_horizontal(string)
        strings.add(string)
        string = self.flip_compressed_string_diagonal(string)
        strings.add(string)
        string = self.flip_compressed_string_horizontal(string)
        strings.add(string)
        string = self.flip_compressed_string_diagonal(string)
        strings.add(string)
        string = self.flip_compressed_string_horizontal(string)
        strings.add(string)
        string = self.flip_compressed_string_diagonal(string)
        strings.add(string)
        return strings
    
    def do_move(self,move):
        """
        This method performs a move by a player. Note that
        it does not take the player as an input, instead relying
        on the object variable active_player.
        """
        self.cells[move] = self.active_player[1]
        self.empty_cells.remove(move)
        self.turn = self.next_turn
        self.active_player = self.next_player
        self.next_turn = (self.turn + 1) % Game.options['number of players']
        self.next_player = Game.options['players'][self.next_turn]

    def check_if_board_square_is_empty(self,move):
        return move in self.empty_cells

    def validate_player_input_format(self,player_input):
        """
        This method checks if a player has inputted a move in
        the correct format.
        """
        while True:
            try:
                valid = re.match('([0-9]+).+([0-9]+)',player_input)
                coords = valid.group(1,2)
                move = tuple([int(coord) for coord in coords])
                return(move)
            except:
                player_input = input('Please enter a valid input of the form x,y where x and y are the coordinates of where you want to play.')

    def generate_computer_move(self):
        """
        This method is a placeholder that generates a
        random move for an automated opponent to make.
        """
        move = random.choice(list(self.empty_cells))
        return move

    def check_if_move_is_available(self,move):
        """
        Once a player's move has been verified as being
        written in the right format, it must then still
        be checked to ensure it is actually available
        in the current board state. That is what this
        method is for.
        """
        if move not in self.cells.keys():
            print('That is outside of the game board.')
            return False
        if move not in self.empty_cells:
            print('That space is taken.')
            return False
        return True

    def check_if_player_has_won(self,player):
        player_won = any([all([self.cells[cell] == player for cell in line]) for line in self.winning_lines])
        return player_won
        
    def get_player_prompt(self):
        return 'Please enter the coordinates of where you want to play in the form x,y where x and y are the coordinates of where you want to play.'

    def evaluate_end_game(self):
        """
        This method defines the value any end game state
        has to each player. It is used by another script
        to perform the minimax algorthmn on the game.
        """
        players = [player[1] for player in Game.options['players']]
        end_game_value = {player:-100 for player in players}
        for player in players:
            if self.check_if_player_has_won(player):
                end_game_value[player] = 100
                return end_game_value
        if not self.empty_cells:
            end_game_value = end_game_value.fromkeys(end_game_value,0)
            return end_game_value
        return None

    def return_available_moves(self):
        return self.empty_cells
