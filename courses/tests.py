from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Course


class CourseTest(APITestCase):
    def setUp(self):
        Course.objects.create(name='Python', teacher='Ali', price=500)
        Course.objects.create(name='Django', teacher='Vali', price=700)
        Course.objects.create(name='Java', teacher='Ali', price=600)

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