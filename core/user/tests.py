"""test for the user API"""


from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status



"""

what is get_user_model():
when we doesnot customize our user model then while accessing the data we use User.objects.get()
but when we customize our User model then we cannot write User.object.... for that we need to use get_user_model 
that is  currently active in your Django project's authentication system. 
"""


"""

Request Payload: In an HTTP request, the payload refers to the data sent from the client to the server in the request body. 
It contains the information or parameters needed to perform the desired action on the server. 
For example, in a POST request to create a new user, the payload may include data such as the username, email, and password.

Response Payload: In an HTTP response, the payload refers to the data sent from the server to the client in the response body. 
It contains the data or content requested by the client. 
For example, when fetching a list of user profiles, the server may respond with a payload that includes the user details in JSON format.

"""

CREATE_USER_URL = reverse("user:create")
TOKEN_URL = reverse('user:token')

def create_user(**params):
    """create and return a new user """
    return get_user_model().objects.create_user(**params)



class PublicApiTests(TestCase):
    """things that we need inside of this class """
    def setUp(self):
        """person who request to perform """
        self.client = APIClient

    def test_create_user_success(self):
        """is user sucessfully created """
        payload = {
            'email':'test1@example.com',
            'password':'test1example',
            'name':'test name'
        }
        res = self.client.post(CREATE_USER_URL,payload)
        
        self.assertEqual(res.status_code,status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        """this is not a part of request that is send from server to client"""
        self.assertNotIn('password',res.data)


    def test_user_with_email_exist_error(self):
        """see wether email exist or not """
        payload = {
            'email':'test1@example.com',
            'password':'test1example',
            'name':'test name'
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL,payload)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """password too short  """
        payload = {
            'email':'test1@example.com',
            'password':'password',
            'name':'test name'
        }
        res = self.client.post(CREATE_USER_URL,payload)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)
        user_exists =get_user_model().objects.filter(email = payload['email']).exists()
        self.assertFalse(user_exists)


    def test_create_token_for_user(self):
        """test generates token for valid credentials"""
        user_details = {
            'email':'test1@example.com',
            'password':'password',
            'name':'test name'         
        }
        create_user(**user_details)
        payload = {
            'email':user_details['email'],
            'password':user_details['password']
        }
        res = self.client.post(TOKEN_URL,payload)
        self.assertIn('token',res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)


