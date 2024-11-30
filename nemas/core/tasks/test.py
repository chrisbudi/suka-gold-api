from celery import shared_task


@shared_task
def create_test_data():
    for i in range(5):
        print(f"Creating test data {i}")

    return "Test data created successfully."
