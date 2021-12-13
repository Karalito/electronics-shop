import json
from django.contrib.auth.models import User
from django.http import response
from django.urls import reverse
from rest_framework import status
import rest_framework
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken


class ProductList(APITestCase):

    def test_get_product_list(self):
        url = reverse('products')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CreateProduct(APITestCase):

    def test_create_product_success(self):
        url = reverse('token_obtain_pair')
        user = User.objects.create_user(
            username="mailer@gmail.com", email="mailer@gmail.com", password="Stronger15!")

        user.is_active = True
        # Setting user as admin
        user.is_staff = True
        user.save()

        # Logging in
        response = self.client.post(url, {
            'username': "mailer@gmail.com", 'email': "mailer@gmail.com", 'password': "Stronger15!"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in response.data)
        token = response.data['token']

        url = reverse('product-create')
        data = {
            'name': "test product",
            'price': 12.50,
            'brand': "test brand",
            'count_in_stock': 10,
            'category': "electronics",
            'description': "test description",
        }

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer " + token)

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_product_fail_not_admin_fail(self):
        url = reverse('token_obtain_pair')
        user = User.objects.create_user(
            username="mailer@gmail.com", email="mailer@gmail.com", password="Stronger15!")

        user.is_active = True
        user.save()

        # Logging in
        response = self.client.post(url, {
            'username': "mailer@gmail.com", 'email': "mailer@gmail.com", 'password': "Stronger15!"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in response.data)
        token = response.data['token']

        url = reverse('product-create')
        data = {
            'name': "test product",
            'price': 12.50,
            'brand': "test brand",
            'count_in_stock': 10,
            'category': "electronics",
            'description': "test description",
        }

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer " + token)

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_item_logged_out_fail(self):
        url = reverse('product-create')
        data = {
            'name': "test product",
            'price': 12.50,
            'brand': "test brand",
            'count_in_stock': 10,
            'category': "electronics",
            'description': "test description",
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class CreateProductReviewTestCase(APITestCase):

    def test_create_product_review_success(self):
        CreateProduct.test_create_product_success(self)
        url = reverse('create-review', args=[1])
        data = {
            'rating': 5,
            'comment': "GREAT product would buy again 10/10"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_product_review_second_time_fail(self):
        CreateProductReviewTestCase.test_create_product_review_success(self)
        url = reverse('create-review', args=[1])
        data = {
            'rating': 5,
            'comment': "GREAT product would buy again 10/10"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_product_review_logged_out_fail(self):
        url = reverse('create-review', args=[1])
        data = {
            'rating': 5,
            'comment': "GREAT product would buy again 10/10"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TopProductsTestCase(APITestCase):

    def test_get_top_products_success(self):
        url = reverse('top-products')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetProductByIdTestCase(APITestCase):

    def test_get_product_by_id_success(self):
        CreateProduct.test_create_product_success(self)
        url = reverse('product', args=[1])

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UpdateProductTestCase(APITestCase):

    def test_update_product_success(self):
        CreateProduct.test_create_product_success(self)
        url = reverse('product-update', args=[1])

        data = {
            'name': "test product (updated)",
            'price': 15.50,
            'brand': "test brand (updated)",
            'count_in_stock': 18,
            'category': "electronics (updated)",
            'description': "test description (updated)",
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_product_not_admin_fail(self):

        CreateProduct.test_create_product_success(self)

        url = reverse('token_obtain_pair')
        user = User.objects.create_user(
            username="mailer5@gmail.com", email="mailer5@gmail.com", password="Stronger15!")

        user.is_staff = False
        user.save()

        response = self.client.post(url, {
            'username': "mailer5@gmail.com", 'email': "mailer5@gmail.com", 'password': "Stronger15!"}, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in response.data)

        token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer " + token)

        url = reverse('product-update', args=[1])
        data = {
            'name': "test product (updated)",
            'price': 15.50,
            'brand': "test brand (updated)",
            'count_in_stock': 18,
            'category': "electronics (updated)",
            'description': "test description (updated)",
        }

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_product_logged_out(self):
        url = reverse('product-update', args=[1])
        data = {
            'name': "test product (updated)",
            'price': 15.50,
            'brand': "test brand (updated)",
            'count_in_stock': 18,
            'category': "electronics (updated)",
            'description': "test description (updated)",
        }

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class DeleteProductByIdTestCase(APITestCase):

    def test_delete_product_success(self):

        CreateProduct.test_create_product_success(self)

        url = reverse('product-delete', args=[1])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_product_not_admin_fail(self):

        CreateProduct.test_create_product_success(self)

        url = reverse('token_obtain_pair')
        user = User.objects.create_user(
            username="mailer5@gmail.com", email="mailer5@gmail.com", password="Stronger15!")

        user.is_staff = False
        user.save()

        response = self.client.post(url, {
            'username': "mailer5@gmail.com", 'email': "mailer5@gmail.com", 'password': "Stronger15!"}, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in response.data)

        token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer " + token)

        url = reverse('product-delete', args=[1])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_product_logged_out(self):
        url = reverse('product-delete', args=[1])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)