from flask import render_template, request, redirect, url_for
from app import app
from app.forms import SiteChekForm
from app.utils import task_add

from app import db
from app.models import Results, Tasks, TaskStatus

import requests

@app.route('/', methods=['GET', 'POST'])
def home_page():
    form = SiteChekForm()
    if form.validate_on_submit():
        site = form.site.data
        task_add(site)
        return redirect(url_for('.result_success_page', site=site))
    return render_template('index.html', title='Home', form=form)


@app.route('/result_success')
def result_success_page():
    site = request.args['site']
    return render_template('result_success.html', title='Task added', site = site)


@app.route('/tasks')
def tasks_page():
    tasks = Tasks.query.all()
    return render_template('tasks.html', title='Tasks', tasks = tasks)

@app.route('/results')
def results_page():
    results = Results.query.all()
    return render_template('results.html', title='Results', results = results)

# @app.route('/dellall')
# def dellall_page():
#     # функция для очистки базы, только для разработки!
#     results = Results.query.all()
#     for r in results:
#         db.session.delete(r)
#     tasks = Tasks.query.all()
#     for t in tasks:
#         db.session.delete(t)
#     db.session.commit()
#     return render_template('dellall.html', title='Удалено')
