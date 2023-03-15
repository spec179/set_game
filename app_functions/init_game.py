from random import shuffle
import json
from ..data import db_session
from ..data import game as gm


def run():
    all_cards = []
    for a in range(3):
        for b in range(3):
            for c in range(3):
                for d in range(3):
                    card = {
                        "color": a,
                        "shape": b,
                        "number": c,
                        "fill": d
                    }
                    all_cards.append(card)
    shuffle(all_cards)
    game_json = {
        "cards": [all_cards[i] for i in range(12)],
        "trash-queue": [all_cards[i] for i in range(12, 27)]
    }
    game = gm.Game()
    game.game = json.dumps(game_json)
    db_sess = db_session.create_session()
    db_sess.add(game)
    db_sess.commit()
    return 'ABOBA'
   