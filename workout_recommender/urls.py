from django.urls import path

from . import views

app_name = 'workout_recommender'
urlpatterns = [
    path('', views.selector_form, name='selector_form'),
    path('view', views.redirect_form, name='redirect_form'),
]
