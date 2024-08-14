"""
django test for command
"""

from unittest.mock import patch

from psycopg2 import OperationalError as psycopg2Error

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase


@patch('core.management.command.wait_for_db.Command.check')
class CommandTest(SimpleTestCase):
    """Test command"""
    
    
    def test_wait_for_db_ready(self, patch_check):
        """Test waiting for db when db is available"""
        patch_check.return_value = True
        
        call_command('wait_for_db')
        
        patch_check.assert_called_once_with(database='default')
        
        