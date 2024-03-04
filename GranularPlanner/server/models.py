from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

from config import db

class Day(db.Model, SerializerMixin):
    __tablename__ = 'days'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    # Add relationship
    day_routines = db.relationship('DayRoutine', back_populates = 'day')
    # Add serialization rules to prevent recursion
    serialize_rules = ('-day_routines.day', ) #make sure they're tuples


class Routine(db.Model, SerializerMixin):
    __tablename__ = 'routines'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    # Add relationship
    day_routines = db.relationship('DayRoutine', back_populates = 'routine')
    routine_tasks = db.relationship('RoutineTask', back_populates = 'routine')
    # Add serialization rules to prevent recursion
    serialize_rules = ('-day_routines.routine', '-routine_tasks.routine' ) #make sure they're tuples

    # Add validation


class DayRoutine(db.Model, SerializerMixin):
    __tablename__ = 'day_routines'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    day_id = db.Column(db.Integer, db.ForeignKey('days.id'))
    routine_id = db.Column(db.Integer, db.ForeignKey('routines.id'))

    # Add relationships
    day = db.relationship('Day', back_populates = 'day_routines')
    routine = db.relationship('Routine', back_populates = 'day_routines')
    # Add serialization rules to prevent recursion
    serialize_rules = ('-day.day_routines', '-routine.day_routines')

    # Add validation

class Task(db.Model, SerializerMixin):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    # Add relationship
    routine_tasks = db.relationship('RoutineTask', back_populates = 'task')
    # Add serialization rules to prevent recursion
    serialize_rules = ('-droutine_tasks.task', ) #make sure they're tuples

class RoutineTask(db.Model, SerializerMixin):
    __tablename__ = 'routine_tasks'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    routine_id = db.Column(db.Integer, db.ForeignKey('routines.id'))
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'))

    # Add relationships
    routine = db.relationship('Routine', back_populates = 'routine_tasks')
    task = db.relationship('Task', back_populates = 'routine_tasks')
    
    # Add serialization rules to prevent recursion
    serialize_rules = ('-routine.routine_tasks', '-task.routine_tasks')

    # Add validation
# add any models you may need.
