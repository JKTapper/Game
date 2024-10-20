import re
import random

class Game:
    
    setup_input = 'Begin game?'
    Help = 'Placeholder'
    options = {'dimensions':(2,3),'players':[('human','X'),('random','O')],'number of players':2} #default options
    advanced_options_explanation = 'Placeholder'

    @classmethod
    def change_options(cls):
        size = int(input('What size of board do you want to play on?'))
        number_of_human_players = int(input('Single player(1) or multiplayer(2)?'))
        players = ['player1','player2']
        if number_of_human_players == 1:
            player_pieces = input('Do you want to play as X or O?')
            player_turn = int(input('Do you want to play first(1) or second(2)?'))
            players[player_turn - 1] = ('human','player_pieces')
            pieces = ['X','O']
            pieces.remove(player_pieces)
            players[2 - player_turn] = ('random',pieces[0])
        elif number_of_human_players == 2:
            players = [('human','X'),('human','O')]
        else:
            players = [('random','X'),('random','O')]
        dimensions = (size,size)
        Game.options = {'dimensions':dimensions,'players':players,'number of players':len(players)}
            

    #def change_options_advanced(cls,advanced_options_string):
        
    
    def __init__(self):
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
        self.turn = 1
        self.active_player = Game.options['players'][self.turn]
        self.next_player = Game.options['players'][~self.turn]

    def __str__(self):
        rows = ['|'.join(['',*[self.cells[(x,y)] for x in range(0,self.width)],''])for y in range(self.height)]
        return ('\n ' + '-'*(2*self.width - 1) + ' \n').join(['',*rows,''])

    def compressed_string(self):
        rows = [''.join([self.cells[(x,y)] for x in range(0,self.width)])for y in range(self.height)]
        return ''.join(rows)
    
    def do_move(self,move):
        self.turn = ~self.turn
        self.active_player = self.next_player
        self.cells[move] = self.active_player[1]
        self.empty_cells.remove(move)
        self.next_player = Game.options['players'][~self.turn]

    def check_if_board_square_is_empty(self,move):
        return move in self.empty_cells

    def validate_player_input_format(self,player_input):
        while True:
            try:
                valid = re.match('([0-9]+).+([0-9]+)',player_input)
                coords = valid.group(1,2)
                move = tuple([int(coord) for coord in coords])
                return(move)
            except:
                player_input = input('Please enter a valid input of the form x,y where x and y are the coordinates of where you want to play.')

    def generate_computer_move(self):
        move = random.choice(list(self.empty_cells))
        return move

    def check_if_move_is_available(self,move):
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
