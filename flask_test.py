from flask import Flask, request, redirect, render_template, url_for, jsonify
import simplejson
from flask.ext.mongoengine import MongoEngine
import time
from types import ModuleType
from itertools import groupby
from mongoengine import Document, ObjectIdField, queryset, StringField, ListField, IntField, FloatField, DateTimeField, EmbeddedDocumentField

app = Flask(__name__)
app.config["MONGODB_DB"] = "tasks"
app.config["SECRET_KEY"] = "KeepThisS3cr3t"

db = MongoEngine(app)

def querySetToMongo(queryset):
    a = list()
    for i in queryset:
        a.append(i.to_mongo())
    for i in a:
        del i['_id']
    return a

class Task(Document):
    created_at = db.FloatField(default=time.time(), required=True)
    title = db.StringField(max_length=255, required=True)
    body = db.StringField(required=True)
    status = db.StringField(required=True)
    task_id = db.SequenceField(required=True)

    def __unicode__(self):
        return self.body

    meta = {
        'allow_inheritance': False,
        'indexes': ['-created_at', 'title'],
        'ordering': ['-created_at']
    }


@app.route('/')
def index():
    tasks_query = Task.objects.all()
    tasks = querySetToMongo(tasks_query)
    return jsonify(tasnks = tasks)
#    return render_template('list.html', tasks=tasks)

@app.route('/add/')
def add():
    post = Task(title ='test', slug = 'test', body = 'testbody', status = '1')
    post.save()
    tasks = Task.objects.all()
    return render_template('list.html', tasks=tasks)

@app.route('/delete/<id>')
def delete(id):
    tasks = Task.objects.get(task_id=id)
    tasks.delete()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
