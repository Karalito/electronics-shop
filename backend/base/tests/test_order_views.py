import json
from django.contrib.auth.models import User
from django.http import response
from django.urls import reverse
from rest_framework import status
import rest_framework
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient


class AddOrderItemsTestCase(APITestCase):

    def test_add_order_items_success(self):
        url = reverse('token_obtain_pair')
        user = User.objects.create_user(
            username="karl.pigaga@gmail.com", email="karl.pigaga@gmail.com", password="Stronger15!")

        user.is_active = True
        user.is_staff = True
        user.save()

        # Logging in
        response = self.client.post(url, {
            'username': "karl.pigaga@gmail.com", 'email': "karl.pigaga@gmail.com", 'password': "Stronger15!"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in response.data)
        token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer " + token)

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
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = {'id': 1,
                'orderItems': [
                    {'id': 1,
                     'name': "test product",
                     'qty': 2,
                     'price': 12.50,
                     'image': "imagelink",
                     'product': 1,
                     'order': 1,
                     },
                ],
                'shippingAddress': {
                    '_id': 1,
                    'country': "Lithuania",
                    'city': "Vilnius",
                    'address': "Vilniaus Gatve 24",
                    'postalCode': "LT65200",
                    'order': 1,
                },
                'user': {
                    'id': 1,
                    '_id': 1,
                    'username': "karl.pigaga@gmail.com",
                    'email': "karl.pigaga@gmail.com",
                    'name': "Karolisu",
                    'surname': "Pigaga",
                    'isAdmin': True
                },
                'paymentMethod': "PayPal",
                'shippingPrice': "0.00",
                'totalPrice': "698.98",
                'isPaid': False,
                'paidAt': "2021-11-15T11:45:08Z",
                'isDelivered': False,
                'deliveredAt': "2021-11-17T09:47:13Z",
                'createdAt': "2021-11-15T09:44:46.162397Z"
                }

        url = reverse('orders-add')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_order_items_logged_out_fail(self):

        data = {'id': 1,
                'orderItems': [
                    {'id': 1,
                     'name': "test product",
                     'qty': 2,
                     'price': 12.50,
                     'image': "imagelink",
                     'product': 1,
                     'order': 1,
                     },
                ],
                'shippingAddress': {
                    '_id': 1,
                    'country': "Lithuania",
                    'city': "Vilnius",
                    'address': "Vilniaus Gatve 24",
                    'postalCode': "LT65200",
                    'order': 1,
                },
                'user': {
                    'id': 1,
                    '_id': 1,
                    'username': "karl.pigaga@gmail.com",
                    'email': "karl.pigaga@gmail.com",
                    'name': "Karolisu",
                    'surname': "Pigaga",
                    'isAdmin': True
                },
                'paymentMethod': "PayPal",
                'shippingPrice': "0.00",
                'totalPrice': "698.98",
                'isPaid': False,
                'paidAt': "2021-11-15T11:45:08Z",
                'isDelivered': False,
                'deliveredAt': "2021-11-17T09:47:13Z",
                'createdAt': "2021-11-15T09:44:46.162397Z"
                }

        url = reverse('orders-add')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class OrderListTestCase(APITestCase):

    def test_get_orders_success(self):
        AddOrderItemsTestCase.test_add_order_items_success(self)
        url = reverse('orders')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_orders_not_admin_fail(self):
        AddOrderItemsTestCase.test_add_order_items_success(self)
        url = reverse('token_obtain_pair')
        user = User.objects.create_user(
            username="pigaga@gmail.com", email="pigaga@gmail.com", password="Stronger15!")

        user.is_active = True
        user.save()

        # Logging in with another user who has no admin rights
        response = self.client.post(url, {
            'username': "pigaga@gmail.com", 'email': "pigaga@gmail.com", 'password': "Stronger15!"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in response.data)
        token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer " + token)

        url = reverse('orders')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_orders_list_logged_out_fail(self):
        url = reverse('orders')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class GetMyOrdersTestCase(APITestCase):
    
    def test_get_my_orders_success(self):
        AddOrderItemsTestCase.test_add_order_items_success(self)
        url = reverse('my-orders')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_my_orders_logged_out_fail(self):
        url = reverse('my-orders')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class UpdateOrderToDeliveredTestCase(APITestCase):
    
    def test_update_order_to_delivered_success(self):
        AddOrderItemsTestCase.test_add_order_items_success(self)
        url = reverse('order-delivered', args=[1])
        response = self.client.put(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_update_order_to_delivered_not_admin_fail(self):
        AddOrderItemsTestCase.test_add_order_items_success(self)
        url = reverse('token_obtain_pair')
        user = User.objects.create_user(
            username="pigaga@gmail.com", email="pigaga@gmail.com", password="Stronger15!")

        user.is_active = True
        user.save()

        # Logging in with another user who has no admin rights
        response = self.client.post(url, {
            'username': "pigaga@gmail.com", 'email': "pigaga@gmail.com", 'password': "Stronger15!"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in response.data)
        token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer " + token)

        url = reverse('order-delivered', args=[1])
        response = self.client.put(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_order_to_delivered_logged_out_fail(self):
        url = reverse('order-delivered', args=[1])
        response = self.client.put(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class GetOrderByIdTestCase(APITestCase):

    def test_get_order_by_id_success(self):
        AddOrderItemsTestCase.test_add_order_items_success(self)
        url = reverse('user-order', args=[1])
        response =self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_order_by_id_logged_out_fail(self):
        url = reverse('user-order', args=[1])
        response =self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class UpdateOrderToPaidTestCase(APITestCase):

    def test_update_order_to_paid_success(self):
        AddOrderItemsTestCase.test_add_order_items_success(self)
        url = reverse('pay', args=[1])
        response = self.client.put(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_order_to_paid_fail(self):
        url = reverse('pay', args=[1])
        response = self.client.put(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)