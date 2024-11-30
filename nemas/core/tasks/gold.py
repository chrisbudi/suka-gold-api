from celery import shared_task

from core.management.commands.harga_emas import Command as process_harga_emas


@shared_task(name="task_harga_emas_process")
def run_harga_emas_process():
    print("Task executed successfully!")
    process_harga_emas()
