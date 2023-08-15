import datetime
from peewee import Model, SqliteDatabase, CharField, DateField

db = SqliteDatabase("victims.db")


class Victim(Model):
    date = DateField(default=datetime.datetime.now)
    file_ = CharField()

    class Meta:
        database = db


if __name__ == "__main__":
    db.create_tabes([Victim])
