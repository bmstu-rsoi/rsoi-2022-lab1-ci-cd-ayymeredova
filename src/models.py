from flask_sqlalchemy import SQLAlchemy
 
db = SQLAlchemy()

class PersonModel(db.Model):
    __tablename__ = 'persons'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    work = db.Column(db.String(200), nullable=False)
    age = db.Column(db.Integer, nullable = False)

    def __init__(self, name, address, work, age):
        self.name = name
        self.address = address
        self.work = work
        self.age = age


    def __repr__(self):
        return f"Person(name = {name}, address = {address}, work = {work}, age = {age})"
