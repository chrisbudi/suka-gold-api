from celery import shared_task


@shared_task
def example_task():
    print("Task executed successfully!")
