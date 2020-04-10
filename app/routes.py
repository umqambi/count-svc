from flask import render_template, request, redirect, url_for
from app import app
from app.forms import SiteChekForm
from app.utils import task_add

from app import db
from app.models import Results, Tasks, TaskStatus
from config import Config

import requests

@app.route('/', methods=['GET', 'POST'])
def home_page():
    # Главная траница, по гет возращает форму, по пост ее обрабатывает
    form = SiteChekForm()
    if form.validate_on_submit():
        site = form.site.data
        task_add(site)
        return redirect(url_for('.result_success_page', site=site))
    return render_template('index.html', title='Home', form=form)


@app.route('/result_success')
def result_success_page():
    # Страница информатор о постановке задачи
    site = request.args['site']
    return render_template('result_success.html', title='Task added', site = site)


@app.route('/tasks')
def tasks_page():
    # Страница просмотра задач
    tasks = Tasks.query.all()
    return render_template('tasks.html', title='Tasks', tasks = tasks)

@app.route('/results')
def results_page():
    # Страница просмотра результатов
    results = Results.query.all()
    return render_template('results.html', title='Results', results = results)

@app.route('/configvam')
def configvam_page():
    # функция для просмотра конфига, только для ОТЛАДКИ!
    c = Config
    return render_template('configvam.html', title='configvam', c = c)

# @app.route('/dellall')
# def dellall_page():
#     # функция для очистки базы, только для ОТЛАДКИ!
#     results = Results.query.all()
#     for r in results:
#         db.session.delete(r)
#     tasks = Tasks.query.all()
#     for t in tasks:
#         db.session.delete(t)
#     db.session.commit()
#     return render_template('dellall.html', title='Удалено')
