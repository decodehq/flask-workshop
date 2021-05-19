from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI') or 'sqlite:///workshop.db'
db = SQLAlchemy(app)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    assignee = db.Column(db.Text)
    description = db.Column(db.Text)
    priority = db.Column(db.Integer)


@app.route("/")
def index():
    return 'Hello world!'


@app.route("/hello")
def hello():
    return '<h1>We can change Hello world routes!</h1>'


@app.route("/assignee/<assignee>")
def assignee(name):
    return 'Hi, my name is {}'.format(name)


@app.route("/assignee/<name>/priority/<priority>")
def assignee_priority(assignee, priority):
    return 'Hi, my name is {} and I have some task with priority {}'.format(assignee, priority)


@app.route("/tasks/create", methods=["GET"])
def tasks_create():
    return render_template('task-create.html')


@app.route("/tasks_basic", methods=["GET", "POST"])
def tasks_basic():
    if request.method == 'GET':
        tasks_list = [
            {'assignee': 'joe', 'description': 'pay taxes', 'priority': 7},
            {'assignee': 'karen', 'description': 'buy mask', 'priority': 2},
            {'assignee': 'donald', 'description': 'learn flask', 'priority': 1},
            {'assignee': 'anna', 'description': 'drive bike', 'priority': 8}
        ]

        return render_template('tasks-list.html', tasks_list=tasks_list)
    else:
        task = request.form.to_dict()

        return render_template('task.html', task=task)


@app.route("/tasks", methods=["GET", "POST"])
def tasks_list():
    if request.method == 'GET':
        tasks_list = Task.query.filter().all()

        return render_template('tasks-list.html', tasks_list=tasks_list)
    else:
        task_data = request.form.to_dict()

        task = Task(
            assignee=task_data.get('assignee'),
            description=task_data.get('description'),
            priority=int(task_data.get('priority')),
        )

        db.session.add(task)
        db.session.commit()

        return render_template('task.html', task=task)


@app.route("/tasks/<int:task_id>", methods=['GET', 'DELETE'])
def task_by_id(task_id):
    task = Task.query.filter(Task.id == task_id).first_or_404()

    if request.method == 'GET':
        return render_template('task.html', task=task)
    else:
        db.session.delete(task)
        db.session.commit()

        return 'Task {} deleted!'.format(task_id)
