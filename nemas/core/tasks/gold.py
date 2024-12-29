from celery import shared_task

from core.management.commands.harga_emas import Command as process_harga_emas
import subprocess


@shared_task(name="task_harga_emas_process")
def run_harga_emas_process():
    subprocess.run(["python", "manage.py", "harga_emas"], check=True)
    # update price web socket
    print("Task executed successfully!")

    return "Execute process harga emas success"
