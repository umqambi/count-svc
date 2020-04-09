import requests, time
from datetime import datetime
from app.models import Results, Tasks, TaskStatus

from app import db, celery
from app.models import Results, Tasks, TaskStatus

checked_word = 'python'

def word_counter_for_url(url, word):
    site_data = requests.get(url)
    wcfu = site_data.text.lower().count(word)
    return wcfu


@celery.task()
def task_do(id, cword):
    task = Tasks.query.get(id)
    print('!!!!!!!!СТАТУС ЗАДАЧИ {} - {}'.format(id,task.task_status))
    task.task_status = TaskStatus.PENDING
    db.session.add(task)
    db.session.commit()
    time.sleep(20) #пауза 20 секунд для теста
    status = False
    try:
        status = requests.get(task.address, timeout = 10).status_code
    except:
        pass 
    if status:
        if status == 200:
            counter = word_counter_for_url(task.address, cword)
            task_result = Results(
                address = task.address,
                words_count = counter,
                http_status_code = status
            )
        else:
            task_result = Results(
                address = task.address,
                http_status_code = status
            )
    else:
        task_result = Results(
            address = task.address,
            http_status_code = 0
        )
    task.task_status = TaskStatus.FINISHED
    db.session.add(task)
    db.session.add(task_result)
    db.session.commit()


def task_add(site):
    status = False
    try:
        status = requests.get(site, timeout = 10).status_code
    except:
        pass
    if status:
        t = Tasks(
            address = site, 
            timestamp = datetime.now(), 
            task_status = TaskStatus.NOT_STARTED,
            http_status = status
        )
    else:
        t = Tasks(
            address = site, 
            timestamp = datetime.now(), 
            task_status = TaskStatus.NOT_STARTED,
            http_status = 0
        )
    db.session.add(t)
    db.session.commit()
    task_do.delay(t.id, checked_word)





if __name__ == "__main__":
    site_list = ['https://v0land13.github.io/e8check/index.html', 'https://v0land13.github.io/e8check/page0.html', 'https://v0land13.github.io/e8check/page5.html', 'https://v0land13.github.io/e8check/page10.html', 'https://v0land13.github.io/e8check/page15.html', 'https://v0land13.github.io/e8check/page25.html', 'https://v0land13.github.io/e8check/page50.html']
    for site in site_list:
        print('На странице {} "python встречается {} раз'.format(site, word_counter_for_url(site, checked_word)))
