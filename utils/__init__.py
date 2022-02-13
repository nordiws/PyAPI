from models import People, Users


def insert_people():
    person = People(name='Juliano', age=33)
    person.save()


def query_people():
    people = People.query.all()
    for person in people:
        print(person.name)
        print(person.age)


def update_person():
    person = People.query.filter_by(name='Pablo').first()
    person.age = 21
    person.save()


def delete_person():
    person = People.query.filter_by(name='Pedro').first()
    person.delete()


def insert_user(login, password):
    user = Users(login=login, password=password)
    user.save()


def query_users():
    users = Users.query.all()
    print(users)


if __name__ == '__main__':
    # insert_people()
    # update_person()
    # delete_person()
    query_people()
    insert_user('admin', 'admin')
    insert_user('nordiws', '123')
    query_users()
