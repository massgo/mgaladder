from peewee import *

db = SqliteDatabase('ladder.db')


class Player(Model):
    name = CharField()
    rank = FloatField()
    aga_id = IntegerField()

    class Meta:
        database = db


class Result(Model):
    white_player = ForeignKeyField(Player, related_name='results')
    black_player = ForeignKeyField(Player, related_name='results')
    white_won = BooleanField()
    time = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db # this model uses the "people.db" database
