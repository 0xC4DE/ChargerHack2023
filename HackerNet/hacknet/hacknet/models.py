from peewee import Model, SqliteDatabase, CharField, DateTimeField, ForeignKeyField

db = SqliteDatabase("victims.db")


class Victim(Model):
    date = DateTimeField()
    file_ = CharField()
    signing_key = CharField()

    class Meta:
        database = db


class AuthorizedToken(Model):
    name = CharField()
    token = CharField()

    class Meta:
        database = db


class Credits(Model):
    pwner = ForeignKeyField(AuthorizedToken)
    pwn = ForeignKeyField(Victim)

    class Meta:
        database = db


db.create_tables([Victim, AuthorizedToken, Credits])
AuthorizedToken.get_or_create(
    name="SealedVessel", token="jo7aiXieShaephaevi4Ohvengiey0kah"
)
