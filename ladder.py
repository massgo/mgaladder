#! /usr/bin/env python3

import unittest


class Rank:

    def __init__(self, value):
        if int(value) == 0:
            raise ValueError('Rank values must be a nonzero integer')
        self.value = int(value)

    def __add__(self, other):
        # adding ranks is nonsensical
        return NotImplemented

    def __sub__(self, other):
        # note that this returns an nonnegative integer, NOT a rank (intentionally)

        # check whether both values have the same sign
        if abs(self.value + other.value) == abs(self.value) + abs(other.value):
            return abs(self.value - other.value)
        else:
            return abs(self.value) + abs(other.value) - 1

    # there's gotta be a better way to do this
    def __iadd__(self, other):
        if other < 0:
            self -= abs(other)
        elif self.value < 0:
            if abs(self.value) > other:
                self.value += other
            else:
                self.value += other + 1
        else:
            self.value += other
        return self

    def __isub__(self, other):
        if other < 0:
            self += abs(other)
        elif self.value < 0:
            self.value -= other
        else:
            if self.value > other:
                self.value -= other
            else:
                self.value -= other + 1
        return self

    def __int__(self, other):
        return self.value

    def __str__(self):
        rank_str = ''
        if self.value < 0:
            rank_str = '{:d}K'.format(-self.value)
        else:
            rank_str = '{:d}D'.format(self.value)
        return rank_str


class Player:

    def __init__(self, name, rank):
        self.name = name
        self.rank = Rank(rank)

    def __repr__(self):
        return '<{:s}(name={:s}, rank={:d})>'.format(self.__class__.__name__, self.name, self.rank)

    def __str__(self):
        return '{:s} {:s}'.format(self.name, self.rank)


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


class RankTestCase(unittest.TestCase):

    def test_init(self):
        self.assertRaises(ValueError, Rank, 0)

    def test_add(self):
        with self.assertRaises(TypeError):
            value = Rank(1) + Rank(2)
        with self.assertRaises(TypeError):
            value = Rank(1) + 2

    def test_sub(self):
        self.assertEqual(Rank(5) - Rank(1), 4)
        self.assertEqual(Rank(5) - Rank(5), 0)
        self.assertEqual(Rank(5) - Rank(6), 1)
        self.assertEqual(Rank(5) - Rank(-3), 7)
        self.assertEqual(Rank(1) - Rank(-1), 1)

    def test_inc(self):
        rank = Rank(1)
        rank += 1
        self.assertEqual(rank.value, Rank(2).value)
        rank += 5
        self.assertEqual(rank.value, Rank(7).value)
        rank += 0
        self.assertEqual(rank.value, Rank(7).value)
        rank += -1
        self.assertEqual(rank.value, Rank(6).value)
        rank += -6
        self.assertEqual(rank.value, Rank(-1).value)
        rank += -10
        self.assertEqual(rank.value, Rank(-11).value)
        rank += 15
        self.assertEqual(rank.value, Rank(5).value)

    def test_dec(self):
        rank = Rank(-1)
        rank -= 1
        self.assertEqual(rank.value, Rank(-2).value)
        rank -= 5
        self.assertEqual(rank.value, Rank(-7).value)
        rank -= 0
        self.assertEqual(rank.value, Rank(-7).value)
        rank -= -1
        self.assertEqual(rank.value, Rank(-6).value)
        rank -= -6
        self.assertEqual(rank.value, Rank(1).value)
        rank -= -10
        self.assertEqual(rank.value, Rank(11).value)
        rank -= 15
        self.assertEqual(rank.value, Rank(-5).value)

    def test_str(self):
        self.assertEqual(str(Rank(5)), '5D')
        self.assertEqual(str(Rank(1)), '1D')
        self.assertEqual(str(Rank(-5)), '5K')
        self.assertEqual(str(Rank(-1)), '1K')


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
