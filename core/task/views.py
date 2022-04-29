from flask import render_template, redirect, url_for, request
from .models import Category
from ..models import Todo
from . import task
from .forms import TaskForm
from .. import db
from datetime import datetime

@task.route('/create-task', methods=['GET', 'POST'])
def tasks():
    check= None
    todo= Todo.query.all()
    date= datetime.now()
    now= date.strftime("%Y-%m-%d")

    form= TaskForm()
    form.category.choices =[(category.id, category.name) for category in Category.query.all()]

    return render_template('task/tasks.html', title='Create Tasks', form=form, todo=todo, DateNow=now, check=check)
