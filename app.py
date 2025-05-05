from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

# definindo o modelo do banco de dados
class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    description = db.Column (db.String(100), unique=True, nullable=False)

#READ
@app.route('/')
def index():
    tasks = Tasks.query.all()
    return render_template('index.html', tasks=tasks)

#Create
@app.route('/create', methods=["POST"])
def create_task():
    description = request.form['description']

    #validar se existe tarefa
    existind_task = Tasks.query.filter_by(description = description).first()
    if existind_task:
        return 'Tarefa já adicionada!', 400

    new_task = Tasks(description = description)
    db.session.add(new_task)
    db.session.commit()
    return redirect('/')

#Delete
@app.route('/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    task = Tasks.query.get(task_id)

    if task:
        db.session.delete(task)
        db.session.commit()
        return redirect('/')
    
#Update
@app.route('/update/<int:task_id>', methods=['POST'])
def update_task(task_id):
    task = Tasks.query.get(task_id)

    if task:
        task.description = request.form['description']
        db.session.commit()
        return redirect('/')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True, port=5153)
