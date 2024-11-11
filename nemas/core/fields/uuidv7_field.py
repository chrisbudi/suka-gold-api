from django.db import models
from uuid6 import uuid7 


class UUIDv7Field(models.UUIDField):
    def __init__(self, *args, **kwargs):
        # Set the default to use uuid7()
        kwargs['default'] = kwargs.get('default', uuid7)
        super().__init__(*args, **kwargs)