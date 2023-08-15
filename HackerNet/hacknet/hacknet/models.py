import datetime
from peewee import Model, SqliteDatabase, CharField, DateField

db = SqliteDatabase("victims.db")


class Victim(Model):
    date = DateField(default=datetime.datetime.now)
    file_ = CharField()
    signing_key = CharField()

    class Meta:
        database = db


class AuthorizedToken(Model):
    token = CharField()

    class Meta:
        database = db


db.create_tables([Victim, AuthorizedToken])
AuthorizedToken.get_or_create(token="jo7aiXieShaephaevi4Ohvengiey0kah")
