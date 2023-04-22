from . import check_set_on_field, check_set, init_game, send_to_render
from random import randint
from flask_socketio import socketio


def set_main(field, set_indexes, trash_queue):
    if check_set.check_set((field[set_indexes[0]], field[set_indexes[1]], field[set_indexes[2]])):
        for i in range(3):
            trash_queue.append(field[set_indexes[i]])
    newcard1 = {
        'number': randint(0, 2),
        'fill': randint(0, 2),
        'color': randint(0, 2),
        'shape': randint(0, 2)
    }
    newcard2 = {
        'number': randint(0, 2),
        'fill': randint(0, 2),
        'color': randint(0, 2),
        'shape': randint(0, 2)
    }
    newcard3 = {
        'number': randint(0, 2),
        'fill': randint(0, 2),
        'color': randint(0, 2),
        'shape': randint(0, 2)
    }
