from flask import request, render_template, make_response, flash, redirect
from flask_login import login_required
from flask_restful import Resource, abort, url_for
from marshmallow import ValidationError
from werkzeug.security import generate_password_hash


from models import PersonModel, PersonSchema

from utils import make_empty, make_data_response
from models import db
from sqlalchemy import exc

class Person(Resource):
    @staticmethod
    def get():
        flash("Success!")
        return redirect('/api/v1')


    def post():
        "Создать человечка"
        try:
            args = PersonSchema().load(request.json)
        except ValidationError as error:
            return make_data_response(400, message = "Bad JSON format")
        person = Person(**args)
        try:
            db.session.add(person)
            # return make_data_response(200, message ="Success!")
        except:
            db.session.rollback()
            make_data_response(500, message = "Database add error!")
        

        try:
            db.session.commit()
        except exc.SQLAlchemyError:
            db.session.rollback()
            return make_data_response(500, message = "Database commit error!")

        return make_empty(201)


    def delete(person_id):
        "Удалить человечка"
        if db.session.query(Person).filter(Person.id.like(person_id)).one() is None:
            abort(404, message = "Person with id = {} not found!".format(person_id))
        
        person = db.session.query(Person).filter(Person.id.like(person_id)).one()
        try:
            db.session.delete(person)
        except exc.SQLAlchemyError:
            db.session.rollback()
            return make_data_response(500, message= "Database delete error")


        try:
            db.session.commit()
        except exc.SQLAlchemyError:
            db.session.rollback()
            return make_data_response(500, message = "Database commit error!")


        return make_empty(200)


    def patch(person_id):
        "update person"
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
        

        try:
            db.session.commit()

        except exc.SQLAlchemyError:
            db.session.rollback()
            return make_data_response(500, message = "Database commit error!")


        return make_empty(200)

        
