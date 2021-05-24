from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from .models import *
from .views import *

class RecommenderTests(TestCase):

    def test_recommender_form(self):
        response = self.client.get('/workout_recommender/', secure=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Workout Recommender")

    def test_selector_form(self):
        self.factory = RequestFactory()
        request = self.factory.post('/workout_recommender/', secure=True)
        request.user = User.objects.create()
        response = selector_form(request)
        self.assertEqual(response.status_code, 200)

    def test_view_recommends(self):
        self.factory = RequestFactory()
        request = self.factory.post('/workout_recommender/view', secure=True, data={'muscle-group':'Abs'})
        request.user = User.objects.create()
        response = redirect_form(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Crunches")
        self.assertNotContains(response, "Bench Press")
        request = self.factory.post('/workout_recommender/view', secure=True, data={'muscle-group':'Chest'})
        request.user = User.objects.get()
        response = redirect_form(request)
        self.assertContains(response, "Bench Press")
        self.assertNotContains(response, "Crunches")
        request = self.factory.post('/workout_recommender/view', secure=True, data={'muscle-group':'Any/All'})
        request.user = User.objects.get()
        response = redirect_form(request)
        self.assertContains(response, "Bench Press")
        self.assertContains(response, "Crunches")