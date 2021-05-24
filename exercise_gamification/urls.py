from django.urls import path

from . import views

app_name = 'exercise_gamification'
urlpatterns = [
    path('friend_requests/send/<str:username>/', views.send_friend_request, name='send_fr'),
    path('friend_requests/remove/<str:username>/', views.remove_friend_request, name='remove_fr'),
    path('friend_requests/accept/<str:username>/', views.accept_friend_request, name='accept_fr'),
    path('friend_requests/reject/<str:username>/', views.reject_friend_request, name='reject_fr'),
    path('workouts/', views.display_workouts, name='workouts'),
    path('workouts/redirect_workout/', views.redirect_workout, name='redirect_workout'),
    path('workouts/cardio_workout/', views.load_cardio_subimssion, name='cardio_workout'),
    path('workouts/submit_cardio/', views.submit_cardio_workout, name='submit_cardio'),
    path('workouts/strength_workout/', views.load_strength_submission, name='strength_workout'),
    path('workouts/submit_strength/', views.submit_strength_workout, name='submit_strength'),
    path('workouts/other_workout/', views.load_other_submission, name='other_workout'),
    path('workouts/submit_other/', views.submit_other_workout, name='submit_other'),
    path('profile/', views.show_profile, name='profile'),
    path('profile/save_profile/', views.save_profile, name='save_profile'),
    path('profile/<str:username>/', views.show_other_user_profile, name='user_profile'),
    path('profile/<str:username>/remove_friend', views.remove_friend, name='remove_friend'),
]