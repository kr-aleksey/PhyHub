from celery import shared_task

from PhyHub.celery import app


@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(10.0,
                             periodic_task.s(),
                             name='Add sensor reading')


@app.task
def periodic_task():
    print('Периодическая задача выполнена')
