import copy
import re
import random

class Game:
    
    def __init__(self,cells,available_cells):
        self.cells = cells
        self.available_cells = available_cells

    def __str__(self):
        rows = ['|'.join(['',*[self.cells[(x,y)] for x in range(0,width)],''])for y in range(height)]
        return ('\n ' + '-'*(2*width - 1) + ' \n').join(['',*rows,''])

    def do_move(self,move,player):
        self.cells[move] = player
        self.available_cells.remove(move)

    def is_available(self,move):
        return move in self.available_cells

def print_game():
    rows = ['|'.join(['',*[game.cells[(x,y)] for x in range(0,width)],''])for y in range(height)]

    print(('\n ' + '-'*(2*width - 1) + ' \n').join(['',*rows,'']))

def player_prompt():
    return 'Please enter the coordinates of where you want to play'

def action(player_input):
    valid = re.match('([0-9]+).+([0-9]+)',player_input)
    coords = valid.group(1,2)
    player_action = tuple([int(coord) for coord in coords])
    return(player_action)

def available(move):
    if game.cells[move] != '.':
        if player == human:
            print('That space is taken')
        return False
    if move[0] not in range(0,height) or move[1] not in range(0,width):
            print('That is outside of the game board')
            return False
    return True

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

def player_won(player):
    horizontal = [[(x,y) for x in range(0,width)] for y in range(0,height)]
    veritical = [[(x,y) for y in range(0,height)] for x in range(0,width)]
    lines = horizontal + veritical
    if width == height:
        diagonal = [[(x,x) for x in range(width)],[(x,width - x - 1) for x in range(width)]]
        lines += diagonal
    player_won = any([all([game.cells[cell] == player for cell in line]) for line in lines])
    return player_won

def end_game_value():
    if player_won(player):
        return 1
    board_full = len(game.available_cells) == 0
    if board_full:
        return 0
    return -1

def computer_move():
    while True:
        move = (random.randint(0,2),random.randint(0,2))
        if move in game.available_cells:
            return move

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
            move = action(player_input.strip())
        except:
            print('Please enter a valid input')
            continue
    else:
        move = computer_move()
        print(f'The computer plays in position {move}.')
    if not available(move):
            continue
    game.do_move(move,player)
    turn +=1
