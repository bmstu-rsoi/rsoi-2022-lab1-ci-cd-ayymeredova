import os
import psycopg2
from flask import Flask, request
from flask_migrate import Migrate
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from models import PersonModel, db


app = Flask(__name__)
# api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:1148@localhost:5432/persons"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app)

def get_db_connection():
    conn = psycopg2.connect(host='localhost',
                            database='persons',
                            user=os.environ['DB_USERNAME'],
                            password=os.environ['DB_PASSWORD'])
    return conn


@app.route('/persons', methods = ['GET'])
def get_all_persons():
    if request.method == 'GET':
        result=PersonModel.query.all()
        return result
@app.route('/persons/<int: person_id>', methods = ['GET', 'POST'])
def get_post_one_person(person_id):
    if request.method == 'GET':
        result = PersonModel.query.fitler_by(id=person_id).first()
        return result

    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        work = request.form['work']
        age = request.form['age']
        new_person = PersonModel(name=name, address=address, work=work, age=age)
        db.session.add(new_person)
        db.session.commit()
        return f'Finish'


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
