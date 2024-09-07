import copy
import re
import random

class Game:
    
    def __init__(self,cells,empty_cells):
        self.cells = cells
        self.available_cells = empty_cells

    def __str__(self):
        rows = ['|'.join(['',*[self.cells[(x,y)] for x in range(0,width)],''])for y in range(height)]
        return ('\n ' + '-'*(2*width - 1) + ' \n').join(['',*rows,''])

    def do_move(self,move,player):
        self.cells[move] = player
        self.available_cells.remove(move)

    def check_if_board_square_is_empty(self,move):
        return move in self.empty_cells

    def validate_player_input_format(self,player_input):
            valid = re.match('([0-9]+).+([0-9]+)',player_input)
            coords = valid.group(1,2)
            player_action = tuple([int(coord) for coord in coords])
            return(player_action)

    def generate_computer_move():
        move = random.choice(list(empty_cells))
        return move

    def check_if_move_is_available(move):
        if move not in cells.keys():
            print('That is outside of the game board.')
            return False
        if move not in empty_cells:
            print('That space is taken.')
            return False
        return True

    def check_if_player_has_won(player):
        horizontal = [[(x,y) for x in range(0,width)] for y in range(0,height)]
        veritical = [[(x,y) for y in range(0,height)] for x in range(0,width)]
        lines = horizontal + veritical
        if width == height:
            diagonal = [[(x,x) for x in range(width)],[(x,width - x - 1) for x in range(width)]]
            lines += diagonal
        player_won = any([all([cells[cell] == player for cell in line]) for line in lines])
        return player_won
        

def player_prompt():
    return 'Please enter the coordinates of where you want to play X,Y, where X=0-n, Y=0-n'

def reset():
    global game
    global turn
    global human
    game = copy.deepcopy(begin)
    turn = 0
    human = input('Do you want to play first(X) or second(O)')

def game_over():
        input('Play again?')
        reset()

def end_game_value():
    if check_if_player_has_won(player):
        return 1
    board_full = len(game.available_cells) == 0
    if board_full:
        return 0
    return -1

def evaluate(move):
    pass

width = 4
height = 4
one_row = ['.']*width
begining_game_state = {}
all_cells = set({})
for x in range(width):
    for y in range(height):
        begining_game_state[(x,y)] = '.'
        all_cells.add((x,y))
begin = Game(begining_game_state,all_cells)
game = copy.deepcopy(begin)
players = {0:'X',1:'O'}
player = 'X'
turn = 0
human = input('Do you want to play first(X) or second(O)')
    
while True:
    print(game)
    end_game = end_game_value()
    if end_game == 1:
        print(f'{player} won!')
        game_over()
        continue
    elif end_game == 0:
        print('It\'s a draw.')
        game_over()
        continue
    player = players[turn % 2]
    if player == human:
        player_input = input(player_prompt())
        if player_input == 'reset':
            reset()
            continue
        try:
            move = validate_player_input_format(game,player_input.strip())
        except:
            print('Please enter a valid input')
            continue
    else:
        move = computer_move()
        print(f'The computer plays in position {move}.')
    if not check_if_move_is_available(move):
            continue
    game.do_move(move,player)
    turn +=1
