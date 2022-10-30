import os
import psycopg2
from flask import Flask, request
from flask_migrate import Migrate
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from flask import send_from_directory, make_response, jsonify



app = Flask(__name__)
# api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://jueeadhvgqftvn:b6fcbd3432d01827ecbe5845c3cfe62275cdd218e46a2f4d786c515fb702d66f@ec2-54-155-110-181.eu-west-1.compute.amazonaws.com:5432/d3phv792lca812"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)

db = SQLAlchemy(app)

class PersonModel(db.Model):
    __tablename__ = 'persons'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    work = db.Column(db.String(200), nullable=False)
    age = db.Column(db.Integer, nullable = False)

    def __repr__(self):
       return f"Person(name = {self.name}, address = {self.address}, work = {self.work}, age = {self.age})"


@app.route('/favicon.ico') 
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                          'favicon.ico',mimetype='image/vnd.microsoft.icon')


@app.route('/api/v1/persons', methods = ['GET'])
def get_all_persons():
    if request.method == 'GET':
        result=PersonModel.query.all()
        print(result)
        return make_response(jsonify(result), 200)

app.run()

# with app.test_request_context('/persons'):
#     print(PersonModel.query.all())