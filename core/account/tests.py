from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client
# Create your tests here.


"""creating login with email not with username"""

# create_user(): used to create a new user with the provided username and password. It sets the is_staff and is_superuser flags to False by default

# create() is used to create a new User object with the username "jane", the specified password, and the is_staff flag set to True

class CreateUserName(TestCase):
    def test_create_with_email(self):
        email = "rajan@example.com"
        password = "rajan123"
        user = get_user_model().objects.create_user(
            email = email,
            password = password
        )

        self.assertEqual(user.email , email)
        self.assertTrue(user.check_password(password))

    def withour_email(self):
        """trying to create an account without email address """
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('','rajan13')


    def create_superuser(self):
        user = get_user_model().objects.create_superuser(
            'rajan@gmail.com',
            'rajan123'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)


class AdminSiteTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email = 'admin@example.com',
            password = 'admin123'
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email = 'user@example.com',
            password = 'test123',
            name = 'user1'
        )

