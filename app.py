import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from bson.objectid import ObjectId

app = Flask(__name__)


app.config["MONGO_DBNAME"] = 'task-manager'
app.config[ "MONGO_URI"] = 'mongodb+srv://root:London20@myfirstcluster-ay9fk.mongodb.net/task_manager?retryWrites=true&w=majority'

mongo= PyMongo(app)

@app.route('/')
@app.route('/get_tasks')
def get_tasks():
    return render_template("tasks.html", tasks=mongo.db.tasks.find())

@app.route('/add_task')
def add_task():
    return render_template("addtask.html",
    categories=mongo.db.categories.find())

@app.route('/insert_task', methods=['POST'])
def insert_task():
    tasks= mongo.db.tasks
    tasks.insert_one(request.form.to_dict())
    return redirect(url_for('get_tasks'))

@app.route('/edit_task/<task_id>')
def edit_task(task_id):
    _task = mongo.db.tasks.find_one({"_id": ObjectId(task_id)})
    _categories = mongo.db.categories.find()
    category_list = [category for category in _categories]
    return render_template('edittask.html', task =_task, categories= category_list)

@app.route('/update_task/<task_id>', methods=["POST"])
def update_task(task_id):
    tasks = mongo.db.tasks
    tasks.update(  {'_id': ObjectId(task_id)},
    {
        'task_name': request.form.get('task_name'),
        'category_name': request.form.get('category_name'),
        'task_description': request.form.get('task_descrpition'),
        'due_date':  request.form.get('due_date'),
        'is_urgent': request.form.get('is_urgent')
    })
    return redirect(url_for('get_tasks'))

@app.route('/delete_task/<task_id>')
def delete_task(task_id):
    mongo.db.tasks.remove({'_id':ObjectId(task_id)})
    return redirect(url_for('get_tasks'))

@app.route('/get_categories')
def get_categories():
    return render_template('categories.html',
    categories=mongo.db.categories.find())

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
        port=int(os.environ.get('PORT')),
        debug=True)

