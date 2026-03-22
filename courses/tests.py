from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import Course


class CourseTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='ali', password='1234')

        response = self.client.post('/api/token/', {
            'username': 'ali',
            'password': '1234'
        })
        self.token = response.data['token']

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        self.course1 = Course.objects.create(name='Python', teacher='Ali', price=500)
        self.course2 = Course.objects.create(name='Django', teacher='Vali', price=700)
        self.course3 = Course.objects.create(name='Java', teacher='Ali', price=600)

    def test_get_all_courses(self):
        url = reverse('course-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_filter_courses_by_teacher(self):
        url = reverse('course-list') + '?teacher=Ali'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_search_course(self):
        url = reverse('course-list') + '?search=Python'
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_order_by_price(self):
        url = reverse('course-list') + '?ordering=price'
        response = self.client.get(url)

        prices = [item['price'] for item in response.data]
        self.assertEqual(prices, sorted(prices))

    def test_create_course(self):
        url = reverse('course-list')

        data = {
            "name": "C++",
            "teacher": "Ali",
            "price": 800
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_course(self):
        url = reverse('course-detail', args=[self.course1.id])

        data = {
            "name": "Updated Course",
            "teacher": "Ali",
            "price": 999
        }

        response = self.client.put(url, data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], "Updated Course")

    def test_partial_update_course(self):
        url = reverse('course-detail', args=[self.course1.id])

        response = self.client.patch(url, {"price": 1000})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['price'], 1000)

    def test_delete_course(self):
        url = reverse('course-detail', args=[self.course1.id])

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_token_auth(self):
        response = self.client.post('/api/token/', {
            'username': 'ali',
            'password': '1234'
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.data)