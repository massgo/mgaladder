from peewee import *
import datetime

db = SqliteDatabase('ladder.db')


class Player(Model):
    name = CharField()
    rank = IntegerField()
    aga_id = IntegerField()
    created = DateTimeField(default=datetime.datetime.now)
    position = IntegerField()
    active = BooleanField(default=True)

    class Meta:
        database = db

    def __init__(self, name, rank, aga_id):
        players = Player.select().order_by(Player.position)

        if len(players) > 0:
            last_standing = players[-1].position
        else:
            last_standing = 0

        return super().__init__(name=name, rank=rank, aga_id=aga_id, position=last_standing + 1)

    def delete_instance(self):
        self.drop()
        return super().delete_instance()

    def drop(self):
        removed_position = self.position
        self.active = False
        players = Player.select()
        for player in players:
            if player.position > removed_position:
                player.position -= 1
                player.save()

    def __dict__(self):
        return model_to_dict(self)

    @classmethod
    def players(cls, players):
        return [dict(player) for player in players]

class Result(Model):
    white_player = ForeignKeyField(Player, related_name='white_results')
    black_player = ForeignKeyField(Player, related_name='black_results')
    white_won = BooleanField()
    created = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db

    def __init__(self, white_player_id, black_player_id, white_won):
        white_player = Player.get(id=white_player_id)
        black_player = Player.get(id=black_player_id)

        white_position = white_player.position
        black_position = black_player.position
        white_rank = Rank(white_player.rank)
        black_rank = Rank(black_player.rank)

        self.validate_match(white_rank, black_rank, white_position, black_position)

        if not white_won:
            players = Players.select()

            for player in players:
                if player.position <= white_position and player.position > black_position:
                    player.position += 1
                    player.save()

            black_player.position = white_position
            black_player.save()

        return super().__init__(white_player=white_player, black_player=black_player, white_won=white_won)

    def validate_match(self, white_rank, black_rank, white_position, black_position):
        if black_position < white_position:
            raise ValueError('White standing ({:d}) <= black standing ({:d})'
                             .format(white_position, black_position))
        position_diff = black_position - white_position
        rank_diff = white_rank - black_rank
        if position_diff > 2 and rank_diff > 2:
            raise ValueError('Rank difference: {:d}, position difference: {:d}'.format(rank_diff,
                                                                                       position_diff))


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