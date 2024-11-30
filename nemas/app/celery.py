# app/celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery, shared_task

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")

app = Celery("app")

# Load task settings from Django settings file
app.config_from_object("django.conf:settings", namespace="CELERY")

# Automatically discover tasks.py files in installed apps
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")


# @shared_task(name="task_harga_emas_process")
# def run_harga_emas_process():
#     print("Task executed successfully!")
#     # process_harga_emas()
