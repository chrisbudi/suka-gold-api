# Register your models here.
from django.contrib import admin
from django.http import HttpResponse
from app.celery import app


from django.db import models


class CeleryTasks(models.Model):
    class Meta:
        managed = False
        verbose_name = "Celery Task"
        verbose_name_plural = "Celery Tasks"


@admin.register(CeleryTasks)
class CeleryTasksAdmin(admin.ModelAdmin):
    def changelist_view(self, request, extra_context=None):
        all_tasks = app.tasks.keys()
        tasks_html = "<h1>Available Tasks</h1><ul>"
        for task in all_tasks:
            tasks_html += f"<li>{task}</li>"
        tasks_html += "</ul>"
        return HttpResponse(tasks_html)
