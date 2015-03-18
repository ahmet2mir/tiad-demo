from __future__ import absolute_import

from celery import Celery

from kombu.common import Broadcast
from kombu import Exchange, Queue

app = Celery('rex',
             broker='amqp://myuser:mypassword@172.17.42.1/myvhost',
             backend='amqp',
             include=['rex.tasks'])

app.conf.update(
    CELERY_TASK_TIME_LIMIT=1200,
    CELERY_TASK_RESULT_EXPIRES=3600,
    CELERY_TASK_SERIALIZER='json',
    CELERY_RESULT_SERIALIZER='json',
    CELERY_ACCEPT_CONTENT=['json'],
    CELERY_TIMEZONE='Europe/Paris',
    CELERY_ENABLE_UTC=True,
    CELERY_QUEUES = (
        Broadcast('broadcast_tasks'),
        Queue('run_tasks', Exchange('run_tasks'), routing_key='rex.tasks.run'),
    ),
    CELERY_ROUTES = {'rex.tasks.broadcast': {'queue': 'broadcast_tasks'}, 'rex.tasks.run': {'queue': 'run_tasks'}}
)

if __name__ == '__main__':
    app.start()