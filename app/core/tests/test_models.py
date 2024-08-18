"""
django test for model
"""
from django.contrib.auth import get_user_model
from django.test import TestCase


class CommandTest(TestCase):
    """Test command"""

    def test_create_user_with_email_successful(self):
        """Test waiting for db when db is available"""
        email = 'test@test.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        sample_emails = [
            ["test1@EXAMPLE.COM", "test1@example.com"],
            ["Test2@Example.COM", "Test2@example.com"],
            ["TEST3@EXAMPLE.COM", "TEST3@example.com"],
            ["test4@example.COM", "test4@example.com"]
        ]

        for email, excpected, in sample_emails:
            user = get_user_model().objects.create_user(email, 'test123')
            self.assertEqual(user.email, excpected)

    def test_new_user_without_email(self):
        """Test creating user without email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', "test123")

    def test_create_new_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
