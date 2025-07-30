from django.db import models
from mongoengine import Document, DictField, StringField

class CrossData(Document):
    source = StringField(default="cross")
    data = DictField()
    
class LongData(Document):
    source = StringField(default="long")
    data = DictField()
