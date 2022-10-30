import os
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
# api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://jueeadhvgqftvn:b6fcbd3432d01827ecbe5845c3cfe62275cdd218e46a2f4d786c515fb702d66f@ec2-54-155-110-181.eu-west-1.compute.amazonaws.com:5432/d3phv792lca812"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)
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
            make_data_response(200, message="Success!")
        except:
            db.session.rollback()
            make_data_response(500, message="Database add error!")
       

        return make_data_response(jsonify(new_person), 200)


@app.route('/api/v1/persons/<int:person_id>', methods = ['GET'])
def get_one_person(person_id):
    if request.method == 'GET':

        result = db.session.query(PersonModel).filter(PersonModel.id==person_id).one_or_none()
        if not result:
            abort(404)
        return make_response(jsonify(result), 200)

@app.route('/api/v1/persons/<int:person_id>', methods = ['DELETE', 'PATCH'])
def delete_one_person(person_id):
    if request.method == "DELETE":
        "Удалить человечка"
        if db.session.query(Person).filter(Person.id.like(person_id)).one() is None:
            abort(404, message = "Person with id = {} not found!".format(person_id))
        
        person = db.session.query(Person).filter(Person.id.like(person_id)).one()
        try:
            db.session.delete(person)
        except exc.SQLAlchemyError:
            db.session.rollback()
            return make_data_response(500, message= "Database delete error")

    elif request.method == "PATCH":
        if db.session.query(Person).filter(Person.id.like(person_id)).one() is None:
            abort(404, message = "Person with id = {} not found!".format(person_id))
        
        try:
            args = request.json
        except ValidationError as error:
            return make_data_response(400, message="Bad JSON format")
        
        person = db.session.query(Person).filter(Person.id.like(person_id)).one()

        for key in args:
            if args[key] is not None:
                setattr(person, key, args[key])

    # address=ism&age=22&name=Ayjahan&work=ivi
# @app.route('/api/v1/persons', methods = ['POST'])
# def post_one_person():
#     # if request.method == 'POST':
#     "Создать человечка"
#     try:
#         args = PersonSchema().load(request.json)
#         print("args = ", args)
#     except ValidationError as error:
#         return make_response(400, message="Bad JSON format")
#     person = PersonModel(**args)
#     if(not person):
#         make_data_response(400, message="ty tupoy")
#     print("person = ", person)
#     try:
#         db.session.add(person)
#         # return make_data_response(200, message ="Success!")
#     except:
#         db.session.rollback()
#         make_data_response(500, message="Database add error!")
#     return make_data_response(jsonify(person), 200)
    ##########################################################################
# class Person(Resource):
#     @staticmethod
#     def get():
#         flash("Success!")
#         return redirect('/api/v1')


#     def post():
#         "Создать человечка"
#         try:
#             args = PersonSchema().load(request.json)
#         except ValidationError as error:
#             return make_data_response(400, message = "Bad JSON format")
#         person = Person(**args)
#         try:
#             db.session.add(person)
#             # return make_data_response(200, message ="Success!")
#         except:
#             db.session.rollback()
#             make_data_response(500, message = "Database add error!")
        

#         try:
#             db.session.commit()
#         except exc.SQLAlchemyError:
#             db.session.rollback()
#             return make_data_response(500, message = "Database commit error!")

#         return make_empty(201)


#     def delete(person_id):
#         "Удалить человечка"
#         if db.session.query(Person).filter(Person.id.like(person_id)).one() is None:
#             abort(404, message = "Person with id = {} not found!".format(person_id))
        
#         person = db.session.query(Person).filter(Person.id.like(person_id)).one()
#         try:
#             db.session.delete(person)
#         except exc.SQLAlchemyError:
#             db.session.rollback()
#             return make_data_response(500, message= "Database delete error")


#         try:
#             db.session.commit()
#         except exc.SQLAlchemyError:
#             db.session.rollback()
#             return make_data_response(500, message = "Database commit error!")


#         return make_empty(200)


#     def patch(person_id):
#         "update person"
#         if db.session.query(Person).filter(Person.id.like(person_id)).one() is None:
#             abort(404, message = "Person with id = {} not found!".format(person_id))
        
#         try:
#             args = request.json
#         except ValidationError as error:
#             return make_data_response(400, message="Bad JSON format")
        
#         person = db.session.query(Person).filter(Person.id.like(person_id)).one()

#         for key in args:
#             if args[key] is not None:
#                 setattr(person, key, args[key])
        

#         try:
#             db.session.commit()

#         except exc.SQLAlchemyError:
#             db.session.rollback()
#             return make_data_response(500, message = "Database commit error!")


#         return make_empty(200)

# app.add_resource(Person, '/<int:person_id>')


############################################################################
#     if request.method == 'POST':
#         name = request.form['name']
#         address = request.form['address']
#         work = request.form['work']
#         age = request.form['age']
#         new_person = PersonModel(name=name, address=address, work=work, age=age)
#         db.session.add(new_person)
#         db.session.commit()
#         return f'Finish'


if __name__=="__main__":
    app.run(debug=True)



# resource_fields = {
# 	'id': fields.Integer,
# 	'name': fields.String,
# 	'address': fields.String,
# 	'work': fields.String,
#     'age': fields.Integer
# }

# def abort_if_person_id_doesnt_exist(person_id):
#     if person_id not in persons:
#         abort('Person id is not valid.')
# class Person(Resource):
#     @marshal_with(resource_fields)
#     def get(self, person_id):
#         abort_if_person_id_doesnt_exist(person_id) 
#         result = PersonModel.query.fitler_by(id=person_id).first()
#         if not result:
#             abort(404, message='Could not find person with that id')
#         return result
    
#     @marshal_with(resource_fields)
#     def post(self):
#         result = PersonModel.query



    # def delete(self, person_id):
	# 	abort_if_person_id_doesnt_exist(person_id)
	# 	del persons[person_id]
	# 	return '', 204


# api.add_resource(Person, '/persons/<int: person_id>')

# @app.route("/persons/<id>", methods=['GET'])
# def index(id):
#     content=request.json
#     print (content)
#     # res=make_response('yes', 200)
#     return id

# @app.route("/persons", methods=['GET'])
# def index():
#     res=make_response('yes', 200)
#     return res



# @app.errorhandler(404)
# def idNot(error):
#     return ("id not found", 404)

# api.add_resource(Person, "/persons/<int: person_id>")
