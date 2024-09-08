import copy
import re
import random

class Game:
    
    def __init__(self,width,height):
        cells = {}
        empty_cells = set({})
        for x in range(width):
            for y in range(height):
                cells[(x,y)] = '.'
                empty_cells.add((x,y))
        self.cells = cells
        self.empty_cells = empty_cells
        horizontal = [[(x,y) for x in range(0,width)] for y in range(0,height)]
        vertical = [[(x,y) for y in range(0,height)] for x in range(0,width)]
        lines = horizontal + vertical
        if width == height:
            diagonal = [[(x,x) for x in range(width)],[(x,width - x - 1) for x in range(width)]]
            lines += diagonal
        self.winning_lines = lines

    def __str__(self):
        rows = ['|'.join(['',*[self.cells[(x,y)] for x in range(0,width)],''])for y in range(height)]
        return ('\n ' + '-'*(2*width - 1) + ' \n').join(['',*rows,''])

    def do_move(self,move,player):
        self.cells[move] = player
        self.empty_cells.remove(move)

    def check_if_board_square_is_empty(self,move):
        return move in self.empty_cells

    def validate_player_input_format(self,player_input):
            valid = re.match('([0-9]+).+([0-9]+)',player_input)
            coords = valid.group(1,2)
            player_action = tuple([int(coord) for coord in coords])
            return(player_action)

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
        return 'Please enter the coordinates of where you want to play X,Y, where X=0-n, Y=0-n'

width = 4
height = 4
begin = Game(width,height)
players = {0:'X',1:'O'}
player = 'X'
while True:
    game = copy.deepcopy(begin)
    turn = 0
    human = input('Do you want to play first(X) or second(O)')
    while True:
        print(game)
        if game.check_if_player_has_won(player):
            print(f'{player} won!')
            break   
        elif game.empty_cells == {}:
            print('It\'s a draw.')
            break
        player = players[turn % 2]
        if player == human:
            player_input = input(game.get_player_prompt())
            if player_input == 'reset':
                break
            try:
                move = game.validate_player_input_format(player_input.strip())
            except:
                print('Please enter a valid input')
                continue
        else:
            move = game.generate_computer_move()
            print(f'The computer plays in position {move}.')
        if not game.check_if_move_is_available(move):
                continue
        game.do_move(move,player)
        turn +=1
    input('Play again?')
