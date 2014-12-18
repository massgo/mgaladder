#! /usr/bin/env python3


class Player:

    def __init__(self, name, rank):
        self.name = name
        self.rank = rank

    def __repr__(self):
        return '<{:s}(name={:s}, rank={:d})>'.format(self.__class__.__name__, self.name, self.rank)


    def __str__(self):
        rank_str = ''
        if self.rank < 0:
            rank_str = '{:d}K'.format(-self.rank)
        else:
            rank_str = '{:d}D'.format(self.rank)

        return '{:s} {:s}'.format(self.name, rank_str)


class Ladder:

    def __init__(self, standings):
        self.standings = standings

    def __str__(self):
        the_string = 'Ladder standings:'
        position = 1
        for player in self.standings:
            the_string += '\n    {:d}. {:s}'.format(position, str(player))
            position += 1
        return the_string


if __name__ == '__main__':
    ladder = Ladder([Player('Andrew', -1), Player('Walther', 5), Player('Milan', -6)])
    print(ladder)
