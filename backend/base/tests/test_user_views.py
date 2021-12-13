import json
from django.contrib.auth.models import User
from django.http import response
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken


class RegistrationTestCase(APITestCase):

    def test_registration_success(self):
        data = {'name': "TestCase",
                'surname': "Tester",
                'email': "t3ester@outlook.com",
                'password': "Haha123@",
                }
        response = self.client.post("/api/users/register/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_registration_fail(self):
        data = {'name': "Tast",
                'surname': "Test",
                'email': "t3ester@.com",
                'password': "Weakpass",
                }
        response = self.client.post("/api/users/register/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registration_no_data_fail(self):
        data = {
            'name': "",
            'surname': "",
            'email': "",
            'password': "",
        }
        response = self.client.post("/api/users/register/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registration_email_exists(self):
        data = {'name': "TestCase",
                'surname': "Tester",
                'email': "t3ester@outlook.com",
                'password': "Haha123@",
                }
        response = self.client.post("/api/users/register/", data)
        # Posting same data gain to check if we can register user with same email
        response = self.client.post("/api/users/register/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginUserTestCase(APITestCase):

    def test_login_success(self):
        url = reverse('token_obtain_pair')
        user = User.objects.create_user(
            username="mailer@gmail.com", email="mailer@gmail.com", password="Stronger15!")

        user.is_active = True
        user.save()

        response = self.client.post(url, {
            'username': "mailer@gmail.com", 'email': "mailer@gmail.com", 'password': "Stronger15!"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in response.data)
        #token = response.data['token']
        # print(token)

    def test_login_fail(self):
        url = reverse('token_obtain_pair')
        response = self.client.post(url, {
            'username': "mailer@gmail.com", 'email': "mailer@gmail.com", 'password': "Stronger15!"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_no_data(self):
        url = reverse('token_obtain_pair')
        response = self.client.post(url, {
            'username': "", 'email': "", 'password': ""}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserProfileTestCase(APITestCase):

    def test_get_user_profile_success(self):
        # Login before getting user Profile
        url = reverse('token_obtain_pair')
        user = User.objects.create_user(
            username="mailer@gmail.com", email="mailer@gmail.com", password="Stronger15!")

        user.is_active = True
        user.save()

        response = self.client.post(url, {
            'username': "mailer@gmail.com", 'email': "mailer@gmail.com", 'password': "Stronger15!"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in response.data)
        token = response.data['token']
        # print(token)
        # Now check if we can access user profile using auth token
        url = reverse('users-profile')
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer " + token)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_user_profile_fail(self):
        url = reverse('users-profile')
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer " + 'bad token')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserProfileUpdateTestCase(APITestCase):

    def setUp(self):
        # Login before getting user Profile
        url = reverse('token_obtain_pair')
        user = User.objects.create_user(
            username="mailer@gmail.com", email="mailer@gmail.com", password="Stronger15!")

        user.is_active = True
        user.save()

        response = self.client.post(url, {
            'username': "mailer@gmail.com", 'email': "mailer@gmail.com", 'password': "Stronger15!"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in response.data)
        token = response.data['token']
        # print(token)

        # Now check if we can access user profile using auth token
        url = reverse('users-profile')
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer " + token)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_user_profile_success(self):
        # Since we have an access we can send data to update our user
        url = reverse('user-profile-update')
        data = {'name': "TestCase",
                'surname': "Tester",
                'email': "t3ester@outlook.com",
                'password': "Haha123@",
                }

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_user_profile_fail(self):
        url = reverse('user-profile-update')
        data = {'name': "Test",
                'surname': "Test",
                'email': "testmail@gmail.com",
                }

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserListTestCase(APITestCase):

    def test_get_user_list_success(self):
        url = reverse('token_obtain_pair')
        user = User.objects.create_user(
            username="mailer@gmail.com", email="mailer@gmail.com", password="Stronger15!")

        user.is_active = True
        # Setting user as admin
        user.is_staff = True
        user.save()

        response = self.client.post(url, {
            'username': "mailer@gmail.com", 'email': "mailer@gmail.com", 'password': "Stronger15!"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in response.data)
        token = response.data['token']
        # print(token)

        # Now check if we can access users list as admin
        url = reverse('users')
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer " + token)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_user_list_fail_not_admin(self):
        url = reverse('token_obtain_pair')
        user = User.objects.create_user(
            username="mailer@gmail.com", email="mailer@gmail.com", password="Stronger15!")

        user.is_active = True
        # User is not admin by default
        user.save()

        response = self.client.post(url, {
            'username': "mailer@gmail.com", 'email': "mailer@gmail.com", 'password': "Stronger15!"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in response.data)
        token = response.data['token']
        # print(token)

        # Now check if we can access users list as not admin
        url = reverse('users')
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer " + token)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_user_list_fail_logged_out(self):
        url = reverse('users')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserByIdTestCase(APITestCase):

    def test_get_user_by_id_success(self):
        # Login before getting user Profile
        url = reverse('token_obtain_pair')
        user = User.objects.create_user(
            username="mailer@gmail.com", email="mailer@gmail.com", password="Stronger15!")

        user.is_active = True
        # Setting user as admin
        user.is_staff = True
        user.save()

        response = self.client.post(url, {
            'username': "mailer@gmail.com", 'email': "mailer@gmail.com", 'password': "Stronger15!"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in response.data)
        token = response.data['token']
        # print(token)

        # Creating new user with id = 3
        user = User.objects.create_user(
            id=3, username="mailer3@gmail.com", email="mailer3@gmail.com", password="Stronger15!")

        user.is_active = True
        user.save()
        # Now check if we can access user as admin
        url = reverse('user', args=[3])
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer " + token)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_user_by_id_not_admin_fail(self):
        # Login before getting user Profile
        url = reverse('token_obtain_pair')
        user = User.objects.create_user(
            username="mailer@gmail.com", email="mailer@gmail.com", password="Stronger15!")

        user.is_active = True
        user.save()

        response = self.client.post(url, {
            'username': "mailer@gmail.com", 'email': "mailer@gmail.com", 'password': "Stronger15!"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in response.data)
        token = response.data['token']
        # print(token)

        # Creating new user with id = 3
        user = User.objects.create_user(
            id=3, username="mailer3@gmail.com", email="mailer3@gmail.com", password="Stronger15!")

        user.is_active = True
        user.save()
        # Now check if we can access user as non admin
        url = reverse('user', args=[3])
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer " + token)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class UpdateUserTestCase(APITestCase):
    def test_update_user_success(self):
        url = reverse('token_obtain_pair')
        user = User.objects.create_user(
            username="mailer@gmail.com", email="mailer@gmail.com", password="Stronger15!")

        user.is_active = True
        # Setting user as admin
        user.is_staff = True
        user.save()

        response = self.client.post(url, {
            'username': "mailer@gmail.com", 'email': "mailer@gmail.com", 'password': "Stronger15!"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in response.data)
        token = response.data['token']
        # print(token)

        # Creating new user with id = 3
        user = User.objects.create_user(
            id=3, username="mailer3@gmail.com", email="mailer3@gmail.com", password="Stronger15!")

        user.is_active = True
        user.save()
        # Now check if we can update user as admin
        url = reverse('user-update', args=[3])
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer " + token)

        data = {'name': "TestCase",
                'surname': "Tester",
                'email': "mailer3@gmail.com",
                'password': "",
                'isAdmin': False,
                }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_user_fail_not_admin(self):
        url = reverse('token_obtain_pair')
        user = User.objects.create_user(
            id=1, username="mailer@gmail.com", email="mailer@gmail.com", password="Stronger15!")

        user.is_active = True
        user.save()

        response = self.client.post(url, {
            'username': "mailer@gmail.com", 'email': "mailer@gmail.com", 'password': "Stronger15!"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in response.data)
        token = response.data['token']

        # Creating new user with id = 3
        user = User.objects.create_user(
            id=3, username="mailer3@gmail.com", email="mailer3@gmail.com", password="Stronger15!")

        user.is_active = True
        user.save()
        # Now check if we can update user as admin
        url = reverse('user-update', args=[3])
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer " + token)

        data = {'name': "TestCase",
                'surname': "Tester",
                'email': "mailer3@gmail.com",
                'password': "",
                'isAdmin': False,
                }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class DeleteUserTestCase(APITestCase):
    def test_delete_user_success(self):
        url = reverse('token_obtain_pair')
        user = User.objects.create_user(
            username="mailer@gmail.com", email="mailer@gmail.com", password="Stronger15!")

        user.is_active = True
        # Setting user as admin
        user.is_staff = True
        user.save()

        response = self.client.post(url, {
            'username': "mailer@gmail.com", 'email': "mailer@gmail.com", 'password': "Stronger15!"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in response.data)
        token = response.data['token']
        # print(token)

        # Creating new user with id = 3
        user = User.objects.create_user(
            id=3, username="mailer3@gmail.com", email="mailer3@gmail.com", password="Stronger15!")

        user.is_active = True
        user.save()
        # Now check if we can delete user as admin
        url = reverse('user-delete', args=[3])
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer " + token)

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_user_not_admin_fail(self):
        url = reverse('token_obtain_pair')
        user = User.objects.create_user(
            username="mailer@gmail.com", email="mailer@gmail.com", password="Stronger15!")

        user.is_active = True
        user.save()

        response = self.client.post(url, {
            'username': "mailer@gmail.com", 'email': "mailer@gmail.com", 'password': "Stronger15!"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in response.data)
        token = response.data['token']
        # print(token)

        # Creating new user with id = 3
        user = User.objects.create_user(
            id=3, username="mailer3@gmail.com", email="mailer3@gmail.com", password="Stronger15!")

        user.is_active = True
        user.save()
        # Now check if we can delete user as admin
        url = reverse('user-delete', args=[3])
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer " + token)

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
