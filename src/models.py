# from multiprocessing.reduction import steal_handle
from re import S
import string
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from dataclasses import dataclass

# from main import app
db = SQLAlchemy()

@dataclass
class PersonModel(db.Model):
    id: int
    name: str
    address: str
    work: str
    age: int

    __tablename__ = 'persons'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    work = db.Column(db.String(200), nullable=False)
    age = db.Column(db.Integer, nullable = False)

    # def __init__(self, name, address, work, age):
    #     self.name = name
    #     self.address = address
    #     self.work = work
    #     self.age = age

    def __repr__(self):
       return f"Person(name = {self.name}, address = {self.address}, work = {self.work}, age = {self.age})"


ma = Marshmallow()


# schema
class PersonSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'address', 'work', 'age')

# init schema
# person_schema = PersonSchema(strict=True)
# persons_schema = PersonSchema(many=True, strict=True)