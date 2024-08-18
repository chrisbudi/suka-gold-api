'''
Django wait for db avail
'''

import time

from django.db.utils import OperationalError
from psycopg2 import OperationalError as Psycopg2Error

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    Django command to pause execution until database is available
    """

    def handle(self, *args, **options):
        self.stdout.write("waiting for db")
        db_up = False
        while db_up is False:
            try:
                self.check(databases=['default'])
                db_up = True
            except (OperationalError, Psycopg2Error):
                self.stdout.write("Database unavailable, waiting 1 second...")
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS("Database available!"))
        pass
