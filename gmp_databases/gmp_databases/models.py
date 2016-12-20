from enum import Enum

from django.db.models import Model, CharField, ForeignKey, ManyToManyField, DateTimeField, IntegerField, TextField, \
    TimeField
from django.db.models import OneToOneField
from django.db.models.fields import DecimalField


DEFAULT_CHAR_FIELD_MAX_LENGTH = 256
LOCATION_TYPE = Enum("location_type", "user place")


class OpeningHours(Model):
    day = IntegerField()
    open = TimeField()
    close = TimeField()


class Type(Model):
    name = CharField(max_length=DEFAULT_CHAR_FIELD_MAX_LENGTH)


class Country(Model):
    name = CharField(max_length=DEFAULT_CHAR_FIELD_MAX_LENGTH)


class Street(Model):
    name = CharField(max_length=DEFAULT_CHAR_FIELD_MAX_LENGTH)


class City(Model):
    name = CharField(max_length=DEFAULT_CHAR_FIELD_MAX_LENGTH)


class Location(Model):
    type = IntegerField(choices=[(t.name, t.value) for t in LOCATION_TYPE])
    lat = DecimalField(max_digits=16, decimal_places=12)
    lng = DecimalField(max_digits=16, decimal_places=12)
    formatted_address = CharField(max_length=DEFAULT_CHAR_FIELD_MAX_LENGTH)
    country = ForeignKey(Country)
    city = ForeignKey(City)
    #street = ForeignKey(Street, null=True)


class Place(Model):
    name = CharField(max_length=DEFAULT_CHAR_FIELD_MAX_LENGTH)
    location = ForeignKey(Location)
    types = ManyToManyField(Type)
    opening_hours = ManyToManyField(OpeningHours)
    phone_number = CharField(max_length=DEFAULT_CHAR_FIELD_MAX_LENGTH)
    rating = DecimalField(max_digits=2, decimal_places=1)
    website = CharField(max_length=DEFAULT_CHAR_FIELD_MAX_LENGTH)


class Review(Model):
    author_name = CharField(max_length=DEFAULT_CHAR_FIELD_MAX_LENGTH)
    rating = DecimalField(max_digits=2, decimal_places=1)
    text = TextField()
    place = ForeignKey(Place)


class Image(Model):
    place = ForeignKey(Place)
    url = CharField(max_length=512)


class HistoryParams(Model):
    opening_hours = ForeignKey(OpeningHours)
    place_type = ForeignKey(Type)
    rating = DecimalField(max_digits=2, decimal_places=1)


class User(Model):
    first_name = CharField(max_length=DEFAULT_CHAR_FIELD_MAX_LENGTH)
    last_name = CharField(max_length=DEFAULT_CHAR_FIELD_MAX_LENGTH)
    age = IntegerField()
    password = CharField(max_length=DEFAULT_CHAR_FIELD_MAX_LENGTH)
    username = CharField(max_length=DEFAULT_CHAR_FIELD_MAX_LENGTH)
    location = ForeignKey(Location)
    last_login = DateTimeField()
    history_params = ManyToManyField(HistoryParams)