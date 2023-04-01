def check_set_on_field(field):
    """ field=[card, card, card...] """
    for i in range(len(field)):
        for j in range(i + 1, len(field)):
            c1, c2 = field[i], field[j]
            c3 = {
                'color': 3 - c1['color'] - c2['color'] if c1['color'] != c2['color'] else c1['color'],
                'shape': 3 - c1['shape'] - c2['shape'] if c1['shape'] != c2['shape'] else c1['shape'],
                'number': 3 - c1['number'] - c2['number'] if c1['number'] != c2['number'] else c1['number'],
                'fill': 3 - c1['fill'] - c2['fill'] if c1['fill'] != c2['fill'] else c1['fill'],
            }
            if c3 in field:
                # print(c1, c2, c3)
                return True
    return False

# field = [{"color": 0, "shape": 2, "number": 0, "fill": 0}, {"color": 2, "shape": 1, "number": 1, "fill": 2}, {"color": 2, "shape": 1, "number": 1, "fill": 1}, {"color": 0, "shape": 1, "number": 0, "fill": 0}, {"color": 0, "shape": 2, "number": 0, "fill": 1}, {"color": 2, "shape": 2, "number": 2, "fill": 2}, {"color": 1, "shape": 1, "number": 0, "fill": 2}, {"color": 0, "shape": 2, "number": 2, "fill": 2}, {"color": 2, "shape": 1, "number": 2, "fill": 0}, {"color": 0, "shape": 2, "number": 2, "fill": 1}, {"color": 0, "shape": 2, "number": 2, "fill": 0}, {"color": 0, "shape": 2, "number": 1, "fill": 0}]
# print(check_set_on_field(field))
