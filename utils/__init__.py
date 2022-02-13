from models import People

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

if __name__ == '__main__':
    #insert_people()
    #update_person()
    delete_person()
    query_people()