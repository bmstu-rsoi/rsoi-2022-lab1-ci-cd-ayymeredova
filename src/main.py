from email import message
import os 
import sys
from marshmallow import ValidationError
import psycopg2
from flask import Flask, request, flash, redirect
from flask_migrate import Migrate
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with, url_for
from flask_sqlalchemy import SQLAlchemy
from models import PersonModel, PersonSchema, db
from utils import make_data_response, make_empty
from flask import send_from_directory, jsonify, make_response
from sqlalchemy import exc



app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://jueeadhvgqftvn:b6fcbd3432d01827ecbe5845c3cfe62275cdd218e46a2f4d786c515fb702d66f@ec2-54-155-110-181.eu-west-1.compute.amazonaws.com:5432/d3phv792lca812"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app)

def get_db_connection():
    conn = psycopg2.connect(host="ec2-54-155-110-181.eu-west-1.compute.amazonaws.com",
                            database="d3phv792lca812",
                            user='jueeadhvgqftvn',
                            password='b6fcbd3432d01827ecbe5845c3cfe62275cdd218e46a2f4d786c515fb702d66f')
    return conn

@app.route('/favicon.ico') 
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                          'favicon.ico',mimetype='image/vnd.microsoft.icon')

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found the information'}), 404)


@app.route('/api/v1/persons', methods = ['GET', 'POST'])
def get_all_persons():
    if request.method == 'GET':
        result=PersonModel.query.all()
        if not result:
            abort(404)
        return make_response(jsonify(result), 200)
    
    elif request.method == "POST":
        try:
            if request.is_json:
                data = request.get_json()
                new_person = PersonModel(
                    name = data["name"],
                    address = data["address"],
                    work = data["work"],
                    age = data["age"],
                )
            
        except ValidationError as error:
            return make_response(400, message="Bad JSON format")
    
        try:
            db.session.add(new_person)
            db.session.commit()
            return make_data_response(200, message="Successfully added new person: name: {}, address: {}, work: {}, age: {} ".format(new_person.name, 
            new_person.address, new_person.work, new_person.age))
        except:
            db.session.rollback()
            make_data_response(500, message="Database add error!")
       
    return make_empty(201)
        


@app.route('/api/v1/persons/<int:person_id>', methods = ['GET'])
def get_one_person(person_id):
    if request.method == 'GET':

        result = db.session.query(PersonModel).filter(PersonModel.id==person_id).one_or_none()
        if not result:
            abort(404)
        return make_response(jsonify(result), 200)
    return make_empty(200)

@app.route('/api/v1/persons/<int:person_id>', methods = ['DELETE', 'PATCH'])
def delete_one_person(person_id):
    if request.method == "DELETE":
        "Удалить человечка"
        if db.session.query(PersonModel).filter(PersonModel.id==person_id).one_or_none() is None:
            abort(404, message = "Person with id = {} not found!".format(person_id))
        
        person = db.session.query(PersonModel).filter(PersonModel.id==person_id).one_or_none()
        try:
            db.session.delete(person)
            db.session.commit()
            return make_data_response(200, message= "Successfully deleted person with id = {}".format(person_id))
        except exc.SQLAlchemyError:
            db.session.rollback()
            return make_data_response(500, message= "Database delete error")

    elif request.method == "PATCH":
        if db.session.query(PersonModel).filter(PersonModel.id==person_id).one_or_none() is None:
            abort(404, message = "Person with id = {} not found!".format(person_id))
        
        try:
            args = request.json
        except ValidationError as error:
            return make_data_response(400, message="Bad JSON format")
        
        person = db.session.query(PersonModel).filter(PersonModel.id==person_id).one_or_none()

        for key in args:
            if args[key] is not None:
                setattr(person, key, args[key])

        try:
            db.session.commit()
            return make_data_response(200, message="Successfulle updated person with id = {}".format(person_id))
        except exc.SQLAlchemyError:
            db.session.rollback()
            return make_data_response(500, message = "Database commit error!")


    return make_empty(201)

port = 8080
herokuPort = os.environ.get('PORT')
if herokuPort != None:
    port = herokuPort
if len(sys.argv) > 1:
    port = int(sys.argv[1])

if __name__=="__main__":
    app.run(host="0.0.0.0", port=port)






