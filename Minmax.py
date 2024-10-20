import copy
import ocupy_row
import mysql.connector

def check_for_listed_value(position):
    game_position_values = mysql.connector.connect(user='root',
                                password='password@2024',
                                database='gamepositionvalues')
    cursor = game_position_values.cursor(dictionary = True)
    query = f"""SELECT * FROM ocupyrow33
                WHERE position = '{position}'"""
    cursor.execute(query)
    result = cursor.fetchone()
    if result:
      result.pop('position')
      print('retrieving')
      return (True,result)
    return(False,False)

def save_value(position,value):
    command = f"""INSERT INTO ocupyrow33 (position,X,O)
                VALUES ('{position}',{value['X']},{value['O']})"""
    game_position_values = mysql.connector.connect(user='root',
                                password='password@2024',
                                database='gamepositionvalues')
    cursor = game_position_values.cursor(dictionary = True)
    cursor.execute(command)
    game_position_values.commit()

def evaluate_game_position(game,depth):
    return evaluate_game_position_recursion(game,depth)

def evaluate_game_position_recursion(game,depth):
    depth += 1
    print('loading')
    position = game.compressed_string() 
    listed_value = check_for_listed_value(position)
    if listed_value[0]:
        return listed_value[1]
    end_game_value = game.evaluate_end_game()
    if end_game_value is not None:
        save_value(position,end_game_value)
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
                save_value(position,game_position_value_after_optimal_move)
                return game_position_value_after_optimal_move
            first_option = False
        if first_option:
            game_position_value_after_optimal_move = game_position_value_after_move
            first_option = False
    save_value(position,game_position_value_after_optimal_move)
    return game_position_value_after_optimal_move
