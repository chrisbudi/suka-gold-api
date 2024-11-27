from celery import shared_task
from core.management.commands.harga_emas import Command as process_harga_emas


@shared_task
def example_task():
    print("Task executed successfully!")
    process_harga_emas()
