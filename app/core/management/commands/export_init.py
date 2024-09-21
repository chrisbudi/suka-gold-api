import os
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Auto-generates __init__.py files for models, views, or serializers in an app.'

    def add_arguments(self, parser):
        parser.add_argument('app_name', type=str, help='The Django app for which you want to generate __init__.py')
        parser.add_argument('module', type=str, help='The module to scan (e.g., models, views, serializers)')

    def handle(self, *args, **options):
        app_name = options['app_name']
        module = options['module']
        
        # Define the path to the app's module directory (e.g., models, views, serializers)
        app_dir = os.path.join(os.getcwd(), app_name, module)

        # Check if the directory exists
        if not os.path.exists(app_dir):
            self.stdout.write(self.style.ERROR(f"Directory '{app_dir}' does not exist."))
            return

        # Get all .py files in the directory except __init__.py
        files = [f[:-3] for f in os.listdir(app_dir) if f.endswith('.py') and f != '__init__.py']

        if not files:
            self.stdout.write(self.style.WARNING(f"No Python files found in '{app_dir}'."))
            return

        # Create or overwrite the __init__.py file with import statements
        init_file = os.path.join(app_dir, '__init__.py')
        with open(init_file, 'w') as f:
            for file in files:
                f.write(f"from .{file} import *\n")

        self.stdout.write(self.style.SUCCESS(f"__init__.py file generated in '{app_dir}' with imports: {', '.join(files)}"))