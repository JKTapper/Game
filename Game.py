import copy
import re
import random

class Game:
    
    setup_input = 'Begin game?'
    Help = 'Placeholder'
    options = {'dimensions':(3,3),'players':[('human','X'),('random','O')],'number of players':2} #default options
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

    def __str__(self):
        rows = ['|'.join(['',*[self.cells[(x,y)] for x in range(0,self.width)],''])for y in range(self.height)]
        return ('\n ' + '-'*(2*self.width - 1) + ' \n').join(['',*rows,''])

    def do_move(self,move,player):
        self.cells[move] = player
        self.empty_cells.remove(move)

    def check_if_board_square_is_empty(self,move):
        return move in self.empty_cells

    def validate_player_input_format(self,player_input):
        if player_input == 'reset':
            return 'reset'
        while True:
            try:
                valid = re.match('([0-9]+).+([0-9]+)',player_input)
                coords = valid.group(1,2)
                move = tuple([int(coord) for coord in coords])
                return(move)
            except:
                print('Please enter a valid input of the form x,y where x and y are the coordinates of where you want to play.')

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

while True:
    turn = 0
    while True:
        setup_input = input(Game.setup_input)
        if setup_input == 'help':
            print(Game.help)
        if setup_input == 'options':
            options = Game.change_options()
        if setup_input == 'advanced_options':
            options = game.change_options()
        break
    game = Game()
    print(Game.options)
    player = Game.options['players'][turn % Game.options['number of players']]
    while True:
        print(game)
        if game.check_if_player_has_won(player[1]):
            print(f'{player[1]} won!')
            break   
        elif game.empty_cells == {}:
            print('It\'s a draw.')
            break
        if player[0] == 'human':
            player_input = input(game.get_player_prompt())
            move = game.validate_player_input_format(player_input.strip())
            if move == 'reset':
                break
        else:
            move = game.generate_computer_move()
            print(f'The computer plays in position {move}.')
        if not game.check_if_move_is_available(move):
                continue
        game.do_move(move,player[1])
        turn +=1
        player = Game.options['players'][turn % Game.options['number of players']]
    input('Play again?')
