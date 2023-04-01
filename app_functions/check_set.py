def check_set(set_cards):
    color, shape, number, fill = set(), set(), set(), set()
    
    for i in range(3):
        color.add(set_cards[i]['color'])
        shape.add(set_cards[i]['shape'])
        number.add(set_cards[i]['number'])
        fill.add(set_cards[i]['fill'])

    return len(color) != 2 and len(shape) != 2 and len(number) != 2 and len(fill) != 2