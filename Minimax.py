"""
This code determines which, if either, player has a winning strategy
from a given position in a game using the minimax algorithmn. It is
written to be able to interface with any game that's code is
structured similarly to ocupy_row.py.
"""
import copy
import ocupy_row
import mysql.connector

def check_for_listed_value(position):
    """
    This function is called to check if the position being evaluated
    already has a known value stored in the associated database.
    """
    game_position_values = mysql.connector.connect(user='root',
                                password='password@2024',
                                database='gamepositionvalues')
    cursor = game_position_values.cursor(dictionary = True)
    query = f"""SELECT * FROM {name}
                WHERE position = '{position}'"""
    cursor.execute(query)
    result = cursor.fetchone()
    if result:
      result.pop('position')
      print('retrieving')
      return (True,result)
    return(False,False)

def save_value(game,position,value):
    """
    This function is called once a position has been evaluated
    to store the position's value in the relevant database.
    """
    values = ','.join([str(value[player]) for player in players])
    #positions = list(game.return_symmetrical_compressed_strings(position))
    positions = [position]
    data_rows = ','.join([f"('{position}',{values})" for position in positions])
    command = f"""INSERT INTO {name} (position,{','.join(players)})
                VALUES {data_rows}"""
    game_position_values = mysql.connector.connect(user='root',
                                password='password@2024',
                                database='gamepositionvalues')
    cursor = game_position_values.cursor(dictionary = True)
    cursor.execute(command)
    game_position_values.commit()

def evaluate_game_position(game,depth):
    """
    The functions initiates the evaluation process before handing off
    to the recursive function. In particular, it creates a MySQL
    database to store evaluated positions for the game in question if
    one does not already exist.
    """
    global name
    name = game.game_type_string()
    players_INT = ', '.join([player[1] + ' INT' for player in game.options['players']])
    global players
    players = [player[1] for player in game.options['players']]
    command = f"""
    CREATE TABLE IF NOT EXISTS {name} (
        position VARCHAR(255),
        {players_INT}
    );
    """
    game_position_values = mysql.connector.connect(user='root',
                                password='password@2024',
                                database='gamepositionvalues')
    cursor = game_position_values.cursor(dictionary = True)
    cursor.execute(command)
    return evaluate_game_position_recursion(game,depth)

def evaluate_game_position_recursion(game,depth):
    """
    This functions implements the minimax game solving
    algorithmn recursively. Given a game position, it first
    checks if the position already has a stored value in the
    database. Then, it checks if the position is an endgame.
    If neither condiiton holds then it evaluates all the
    possible future game states and then evaluates the given
    position by assuming the active player makes the best
    move available to them.
    """
    depth += 1
    print('loading')
    position = game.compressed_string() 
    listed_value = check_for_listed_value(position)
    if listed_value[0]:
        return listed_value[1]
    end_game_value = game.evaluate_end_game()
    if end_game_value is not None:
        save_value(game,position,end_game_value)
        return end_game_value
    current_best_value = -100
    first_option = True
    for move in game.return_available_moves():
        game_after_move = copy.deepcopy(game)
        game_after_move.do_move(move)
        game_position_value_after_move = evaluate_game_position_recursion(game_after_move,depth)
        if game_position_value_after_move[game.next_player[1]] > current_best_value:
            current_best_value = game_position_value_after_move[game.next_player[1]]
            game_position_value_after_optimal_move = game_position_value_after_move
            if game_position_value_after_move[game.next_player[1]] == 100:
                save_value(game,position,game_position_value_after_optimal_move)
                return game_position_value_after_optimal_move
            first_option = False
        if first_option:
            game_position_value_after_optimal_move = game_position_value_after_move
            first_option = False
    save_value(game,position,game_position_value_after_optimal_move)
    return game_position_value_after_optimal_move
