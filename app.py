from crypt import methods
from urllib import request
from flask import Flask, render_template, request, redirect, url_for 
from flask_sqlalchemy import SQLAlchemy


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
    description=request.form.get('description', '')
    todo_item=Todo(description=description )
    db.session.add(todo_item )
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
   app.run(host="0.0.0.0", port=3000)
