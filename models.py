from peewee import *
import datetime
from ladder import Rank

db = SqliteDatabase('ladder.db')


class Player(Model):
    name = CharField()
    rank = IntegerField()
    aga_id = IntegerField()

    class Meta:
        database = db

class Result(Model):
    white_player = ForeignKeyField(Player, related_name='white_results')
    black_player = ForeignKeyField(Player, related_name='black_results')
    ladder = ForeignKeyField(Ladder, related_name='results')
    created = DateTimeField(default=datetime.datetime.now)
    white_won = BooleanField()

    class Meta:
        database = db

class Ladder(Model):
    name = CharField()
    created = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db

    def add_player(self, player_id):
        standings = Standing.select().order_by(Standing.position)

        if len(standings) > 0:
            last_standing = standings[-1].position
        else:
            last_standing = 0

        standing = Standing(player=player_id, ladder=self.id, position=last_standing + 1)
        standing.save()

    def remove_player(self, player_id):
        standing = Standing.get(player=player_id)
        removed_position = standing.position
        standing.delete_instance()
        standings = Standing.select()

        for standing in standings:
            if standing.position > removed_position:
                standing.position = standing.position - 1
                standing.save()

    def add_result(self, white_player_id, black_player_id, white_won):
        white_standing = Standing.get(player=white_player_id)
        black_standing = Standing.get(player=black_player_id)

        white_position = white_standing.position
        black_position = black_standing.position
        white_rank = Rank(black_sanding.player.rank)
        black_rank = Rank(white_standing.player.rank)

        validate_match(white_rank, black_rank, white_position, black_position)

        result = Result(white_player=white_player_id, black_player=black_player_id, white_won=white_won)
        result.save()

        if not white_won:
            standings = Standings.select()

            for standing in standings:
                if standing.position <= white_position and standing.position > black_position:
                    standing.position += 1
                    standing.save()

            black_standing.position = white_position
            black_standing.save()

    def validate_match(self, white_rank, black_rank, white_position, black_position):
        if black_position < white_position:
            raise ValueError('White standing ({:d}) <= black standing ({:d})'
                             .format(white_position, black_position))
        position_diff = black_position - white_position
        rank_diff = white_rank - black_rank
        if position_diff > 2 and rank_diff > 2:
            raise ValueError('Rank difference: {:d}, position difference: {:d}'.format(rank_diff,
                                                                                       position_diff))


class Standing(Model)
    player = ForeignKeyField(Player, related_name='standing')
    ladder = ForeignKeyField(Player, related_name='standings')
    position = IntegerField()

    class Meta:
        database = db


class Rank(object):

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

    def __int__(self):
        return self.value

    def __str__(self):
        rank_str = ''
        if self.value < 0:
            rank_str = '{:d}K'.format(-self.value)
        else:
            rank_str = '{:d}D'.format(self.value)
        return rank_str

    def __eq__(self, other):
        return self.value == other.value

    def __hash__(self):
        return self.value