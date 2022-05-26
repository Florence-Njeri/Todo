from crypt import methods
from urllib import request
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
import sys

app = Flask(__name__)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI']= 'postgresql://florencenjeri:mypassword@127.0.0.1:5432/todoapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f'<Todo {self.id} {self.description}>'

db.create_all()
@app.route('/')
def index():
    return render_template('index.html', data = Todo.query.all())

@app.route('/todos/create', methods=['POST'])
def create_todo():
    error = False
    body = {}
    try:
        description = request.get_json()['description']
        todo_item = Todo(description=description )
        db.session.add(todo_item )
        db.session.commit()
        body['id'] = todo_item.id
        body['description'] = todo_item.description
    except:
        error = True
        db.session.rollback();
        print(sys.exc_info())
    finally:
        db.session.close()
        if error:
            abort(400)
        else:
            return jsonify(body)



