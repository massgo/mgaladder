#! /usr/bin/env python3

import unittest


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

    def players(self):
        return set(self.standings)

    def match_valid(self, player_one, player_two):
        if not {player_one, player_two} <= self.players():
            return False
        return True


class LadderTestCase(unittest.TestCase):

    def setUp(self):
        self.player_one = Player('Andrew', -1)
        self.player_two = Player('Walther', 5)
        self.player_three = Player('Milan', -6)
        self.ladder = Ladder([self.player_one, self.player_two])

    def test_match_valid(self):
        self.assertTrue(self.ladder.match_valid(self.player_one, self.player_two))
        self.assertFalse(self.ladder.match_valid(self.player_one, self.player_three))
        self.assertFalse(self.ladder.match_valid(self.player_two, self.player_three))


if __name__ == '__main__':
    ladder = Ladder([Player('Andrew', -1), Player('Walther', 5), Player('Milan', -6)])
    print(ladder)
    unittest.main()
