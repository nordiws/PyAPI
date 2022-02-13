from flask import Flask, request
from flask_restful import Resource, Api
from models import People, Activities, Users
from flask_httpauth import HTTPBasicAuth

import models

app = Flask(__name__)
api = Api(app)
auth = HTTPBasicAuth()


@auth.verify_password
def verify(login, password):
    if not (login, password):
        return False
    return Users.query.filter_by(login=login, password=password).first()


class Person(Resource):
    @auth.login_required
    def get(self, name):
        person = People.query.filter_by(name=name).first()
        try:
            response = {
                'id': person.id,
                'name': person.name,
                'age': person.age
            }
        except AttributeError:
            response = {
                'status': 404,
                'message': 'Person not found'
            }

        return response

    @auth.login_required
    def put(self, name):
        person = People.query.filter_by(name=name).first()
        data = request.json
        try:
            if 'name' in data:
                person.name = data['name']
            if 'age' in data:
                person.age = data['age']
            person.save()
            response = {
                'id': person.id,
                'name': person.name,
                'age': person.age
            }
        except AttributeError:
            response = {
                'status': 404,
                'message': 'Person not found'
            }
        return response

    @auth.login_required
    def delete(self, name):
        person = People.query.filter_by(name=name).first()
        person.delete()
        message = 'Person {} deleted'.format(name)
        response = {
            'status': 200,
            'message': message
        }
        return response


class ListPeople(Resource):
    @auth.login_required
    def get(self):
        people = People.query.all()
        response = [
            {
                'id': person.id,
                'name': person.name,
                'age': person.age
            } for person in people
        ]
        return response

    @auth.login_required
    def post(self):
        data = request.json
        person = People(name=data['name'], age=data['age'])
        person.save()
        response = {
            'id': person.id,
            'name': person.name,
            'age': person.age
        }
        return response


class ActivitiesList(Resource):
    @auth.login_required
    def get(self):
        activities = Activities.query.all()
        response = [
            {
                'id': i.id,
                'name': i.name,
                'person': i.person.name
            } for i in activities
        ]
        return response

    @auth.login_required
    def post(self):
        data = request.json
        person = People.query.filter_by(name=data['person']).first()
        activity = Activities(name=data['name'], person=person)
        activity.save()
        response = {
            'person': activity.person.name,
            'name': activity.name,
            'id': activity.id
        }
        return response


api.add_resource(Person, '/person/<string:name>')
api.add_resource(ListPeople, '/person')
api.add_resource(ActivitiesList, '/activity')

if __name__ == '__main__':
    app.run(debug=True)
    models.init_db()
