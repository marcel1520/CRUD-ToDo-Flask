from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///todo.db'
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return '<Task %r>' % self.id


@app.route("/", methods=["GET", "POST"])
@app.route("/home", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        task_name = request.form["content"]
        new_task = Todo(content=task_name)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            print("There was an issue adding the task")
    else:
        tasks = Todo.query.order_by(Todo.id).all()
        return render_template("index.html", items=tasks)


@app.route("/update/<int:id>", methods=["GET" ,"POST"])
def update_todo(id):
    task = Todo.query.get_or_404(id)
    if request.method == "POST":
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "There was a problem updating the task"
    else:
        return render_template("update.html", task=task)


@app.route("/delete/<int:id>", methods=["POST"])
def delete_todo(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect("/")
    except:
        return "There was a problem deleting the task"


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5006, debug=True)
