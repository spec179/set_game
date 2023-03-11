def check_set(set_cards):
    color, form, number, fill = set(), set(), set(), set()
    
    for i in range(3):
        color.add(set_cards[i][0])
        form.add(set_cards[i][1])
        number.add(set_cards[i][2])
        fill.add(set_cards[i][3])

    return len(color) != 2 and len(form) != 2 and len(number) != 2 and len(fill) != 2