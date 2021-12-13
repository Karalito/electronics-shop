import datetime
from django.db.models.fields import DateTimeField
from django.test import TestCase
from base.models import *
# Create your tests here.

class ProductTestCase(TestCase):

    def test__str__(self):
        product = Product.objects.create(
            user=User.objects.create_user(
                username="mailer@gmail.com", email="mailer@gmail.com", password="Stronger15!"),
            name="test",
            image="/placeholder.png",
            brand="test",
            category="",
            description="",
            price="30.80",
            is_promoted=True,
            count_in_stock=1,
            created_at="2021-11-15T09:44:46.162397Z",
            rating="4.44",
            numReviews=1
        )

        nametest = "test"
        self.assertEquals(product.name, nametest)


class OderTestCase(TestCase):
    def test__str__(self):
        d1 = datetime.datetime(2021, 11, 15)
        order = Order.objects.create(
            user=User.objects.create_user(
                username="mailer@gmail.com", email="mailer@gmail.com", password="Stronger15!"),
            paymentMethod=1,
            shippingPrice=1,
            totalPrice=1,
            isPaid=False,
            paidAt='2021-11-15T11:45:08Z',
            isDelivered=False,
            deliveredAt='2021-11-15T11:45:08Z',
            createdAt=''
        )

        self.assertNotEqual(order.createdAt, '')


class OrderItemTestCase(TestCase):
    def test__str__(self):
        userInfo=User.objects.create_user(
                    username="mailer@gmail.com", email="mailer@gmail.com", password="Stronger15!")

        orderitem = OrderItem.objects.create(
            product=Product.objects.create(
                user=userInfo,
                name="test",
                image="/placeholder.png",
                brand="test",
                category="",
                description="",
                price="30.80",
                is_promoted=True,
                count_in_stock=1,
                created_at="2021-11-15T09:44:46.162397Z",
                rating="4.44",
                numReviews=1),
            order=Order.objects.create(
                user=userInfo,
                paymentMethod="PayPal",
                shippingPrice=1,
                totalPrice=1,
                isPaid=False,
                paidAt='2021-11-15T09:44:46.162397Z',
                isDelivered=False,
                deliveredAt='2021-11-15T09:44:46.162397Z',
                createdAt='2021-11-15T09:44:46.162397Z'),
            name='test',
            qty=1,
            price=1,
            image=''
        )

        self.assertEquals(orderitem.name, 'test')


class ShippingAddressTestCase(TestCase):
    def test__str__(self):
        self.shipingaddress = ShippingAddress.objects.create(
            order=Order.objects.create(
                user=User.objects.create_user(
                    username="mailer@gmail.com", email="mailer@gmail.com", password="Stronger15!"),
                paymentMethod=1,
                shippingPrice=1,
                totalPrice=1,
                isPaid=False,
                paidAt='2021-11-15T09:44:46.162397Z',
                isDelivered=False,
                deliveredAt='2021-11-15T09:44:46.162397Z',
                createdAt='2021-11-15T09:44:46.162397Z'),
            country='',
            city='',
            address='',
            postalCode=''
        )

        self.assertEquals(self.shipingaddress.address, '')


class ReviewTestCase(TestCase):
    def test__str__(self):
        userInfo=User.objects.create_user(
                    username="mailer@gmail.com", email="mailer@gmail.com", password="Stronger15!")

        self.review = Review.objects.create(
            product=Product.objects.create(
                user=userInfo,
                name="test",
                image="/placeholder.png",
                brand="test",
                category="",
                description="",
                price="30.80",
                is_promoted=True,
                count_in_stock=1,
                created_at="2021-11-15T09:44:46.162397Z",
                rating="4.44",
                numReviews=1),
            user=userInfo,
            name='',
            rating=1,
            comment='',
            created_at='2021-11-15T09:44:46.162397Z'
        )

        self.assertEquals(self.review.rating, 1)
