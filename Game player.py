from ocupy_row import Game
from Minmax import evaluate_game_position
import time
while True:
    turn = 0
    while True:
        setup_input = input(Game.setup_input)
        if setup_input == 'help':
            print(Game.help)
        if setup_input == 'options':
            options = Game.change_options()
        if setup_input == 'advanced_options':
            options = Game.change_options()
        break
    game = Game()
    print(game)
    while True:
        if game.active_player[0] == 'human':
            player_input = input(game.get_player_prompt())
            if player_input == 'reset':
                break
            if player_input == 'evaluate':
                start_time = time.time()
                print(evaluate_game_position(game,0),time.time() - start_time) 
                break
            move = game.validate_player_input_format(player_input.strip())
        else:
            move = game.generate_computer_move()
            print(f'The computer plays in position {move}.')
        if not game.check_if_move_is_available(move):
            continue
        game.do_move(move)
        if game.check_if_player_has_won(game.active_player[1]):
            print(f'{game.active_player[1]} won!')
            print(game)
            break   
        elif not game.empty_cells:
            print('It\'s a draw.')
            print(game)
            break
        print(game)
    input('Play again?')
