#!/usr/bin/env python3

# Standard library imports

# Remote library imports
from flask import Flask, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource
import os

# Local imports
from config import app, db, api
# Add your model imports
from models import Day, DayRoutine, Routine, RoutineTask, Task


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)


# Views go here!

@app.route('/')
def index():
    return '<h1>Project Server</h1>'


######## DAYS #########

@app.route('/days', methods = ['GET', 'POST'])
def days():
    if request.method == 'GET':
        days = Day.query.all()
        days_dict = [day.to_dict() for day in days]
        response = make_response(days_dict, 200)
    elif request.method == 'POST':
        try:
            form_data = request.get_json()
            new_day = Day(
                name = form_data['name']
            )

            db.session.add(new_day)
            db.session.commit()
            response = make_response(new_day.to_dict(), 201)
        except ValueError:
            response = make_response({"errors": ["validation errors"]}, 400)
    return response

@app.route('/days/<int:id>', methods = ['GET', 'PATCH', 'DELETE'])
def day_by_id(id):
    day = Day.query.filter(Day.id == id).first()

    if day:
        if request.method == 'GET':
            day_dict = day.to_dict()
            response = make_response(day_dict, 200)
        elif request.method == 'PATCH':
            try:
                form_data = request.get_json()

                for attr in form_data:
                    setattr(day, attr, form_data[attr])

                db.session.commit()

                response = make_response(day.to_dict(), 202)
            except ValueError:
                response = make_response({"errors": ["validation errors"]}, 400)
        #cascade deletes for day_routines
        elif request.method == 'DELETE':
            assoc_day_routines = DayRoutine.query.filter(DayRoutine.day_id == id).all()
            for assoc_day_routine in assoc_day_routines:
                db.session.delete(assoc_day_routine)
        
            db.session.delete(day)
            db.session.commit()

            response = make_response({}, 204)

    else:
        response = make_response(
            {"error": "Day not found"}, 404
        )
    return response

######## DAY_ROUTINES #########


########## ROUTINES ##########

@app.route('/routines', methods = ['GET', 'POST'])
def routines():
    if request.method == 'GET':
        routines = Routine.query.all()
        routines_dict = [routine.to_dict() for routine in routines]
        response = make_response(tasks_dict, 200)
    elif request.method == 'POST':
        try:
            form_data = request.get_json()
            new_routine = Routine(
                name = form_data['name']
            )

            db.session.add(new_routine)
            db.session.commit()
            response = make_response(new_routine.to_dict(), 201)
        except ValueError:
            response = make_response({"errors": ["validation errors"]}, 400)
    return response

@app.route('/routines/<int:id>', methods = ['GET', 'PATCH', 'DELETE'])
def task_by_id(id):
    routine = Routine.query.filter(Routine.id == id).first()

    if routine:
        if request.method == 'GET':
            routine_dict = routine.to_dict()
            response = make_response(task_dict, 200)
        elif request.method == 'PATCH':
            try:
                form_data = request.get_json()

                for attr in form_data:
                    setattr(routine, attr, form_data[attr])

                db.session.commit()

                response = make_response(routine.to_dict(), 202)
            except ValueError:
                response = make_response({"errors": ["validation errors"]}, 400)
        
        elif request.method == 'DELETE':
            #cascade deletes for routine_tasks
            assoc_routine_tasks = RoutineTask.query.filter(RoutineTask.routine_id == id).all()
            for assoc_routine_task in assoc_routine_tasks:
                db.session.delete(assoc_routine_task)
        
            #cascade deletes for day_routines
            assoc_day_routines = DayRoutine.query.filter(DayRoutine.routine_id == id).all()
            for assoc_day_routine in assoc_day_routines:
                db.session.delete(assoc_day_routine)

            db.session.delete(routine)
            db.session.commit()

            response = make_response({}, 204)

    else:
        response = make_response(
            {"error": "Routine not found"}, 404
        )
    return response

######## ROUTINE_TASKS #########



###### TASKS #######

@app.route('/tasks', methods = ['GET', 'POST'])
def tasks():
    if request.method == 'GET':
        tasks = Task.query.all()
        tasks_dict = [task.to_dict() for task in tasks]
        response = make_response(tasks_dict, 200)
    elif request.method == 'POST':
        try:
            form_data = request.get_json()
            new_task = Task(
                name = form_data['name']
            )

            db.session.add(new_task)
            db.session.commit()
            response = make_response(new_task.to_dict(), 201)
        except ValueError:
            response = make_response({"errors": ["validation errors"]}, 400)
    return response

@app.route('/tasks/<int:id>', methods = ['GET', 'PATCH', 'DELETE'])
def task_by_id(id):
    task = Task.query.filter(Task.id == id).first()

    if task:
        if request.method == 'GET':
            task_dict = task.to_dict()
            response = make_response(task_dict, 200)
        elif request.method == 'PATCH':
            try:
                form_data = request.get_json()

                for attr in form_data:
                    setattr(task, attr, form_data[attr])

                db.session.commit()

                response = make_response(task.to_dict(), 202)
            except ValueError:
                response = make_response({"errors": ["validation errors"]}, 400)
        #cascade deletes for routine_tasks
        elif request.method == 'DELETE':
            assoc_routine_tasks = RoutineTask.query.filter(RoutineTask.task_id == id).all()
            for assoc_routine_task in assoc_routine_tasks:
                db.session.delete(assoc_routine_task)
        
            db.session.delete(task)
            db.session.commit()

            response = make_response({}, 204)

    else:
        response = make_response(
            {"error": "Task not found"}, 404
        )
    return response




if __name__ == '__main__':
    app.run(port=5555, debug=True)

