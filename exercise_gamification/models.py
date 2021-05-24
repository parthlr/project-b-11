from django.db import models
from django.contrib.auth.models import User
import datetime

"""
Profile hold additional data about a user and is connected to the account that
is setup upon google authentication

Fields:
    user - This is the account that a profile is connected to (user is created when using google sig-in)
    username - Unique identifier of profile (will be useful to find friends)
    email - the email address for a profile
    bio - (OPTIONAL) the personal bio of the user
    level - current level of the profile
    xp - current xp of the profile
    friends (OPTIONAL) - the set of all profiles that this profile is friends with
    workouts - the set of all workouts that this profile has recorded
"""
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    username = models.CharField(max_length=15, primary_key=True)
    email = models.EmailField()
    bio = models.TextField()
    level = models.IntegerField()
    xp = models.IntegerField()
    friends = models.ManyToManyField('self', blank=True)
    workouts = models.ManyToManyField('Workout', blank=True)

"""
FriendRequest class holds data about friend requests sent between two users

Fields:
    to_user - The user who is being send the friend request
    from_user - The user who sent the friend request

Friend Requests System
Source: https://medium.com/analytics-vidhya/add-friends-with-689a2fa4e41d
The idea of creating a FriendRequest model came from this source. We figured the rest out
on our own.
"""
class FriendRequest(models.Model):
    to_user = models.ForeignKey(User, related_name='to_user', on_delete=models.CASCADE)
    from_user = models.ForeignKey(User, related_name='from_user', on_delete=models.CASCADE)

"""
Workout class is ment to be a Parent object to hold common fields, but is implimented
with more specific subclasses

Fields:
    base_profile - Any workout can only have 1 profile that it is related to
    date - The date that the workout occurred (Should not allow for future dates)
    name - Name of the workout (i.e. "Pushups")
    estimated_calories - Number of calories burnt during the exercise.
        This number will be provided by API when possible
    notes (OPTIONAL) - place for notes about a given workout
"""
class Workout(models.Model):
    base_profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    date = models.DateField(default=datetime.date.today)
    name = models.CharField(max_length=30)
    estimated_calories = models.DecimalField(max_digits=7, decimal_places=2)
    notes = models.CharField(max_length=400, blank=True)

"""
Cardio_Workout is a child implimentation of Workout for activities like running, walking, swimming, etc.

Fields:
    workout - any Cardio_Workout can belong to only 1 parent Workout model
    duration - time (in MINUTES) of workout
    distance - length (in METERS) of workout [Use API in form validation to record ft/yard/miles in meters]
"""
class Cardio_Workout(models.Model):
    workout = models.OneToOneField(Workout, on_delete=models.CASCADE)
    duration = models.DecimalField(max_digits=7, decimal_places=2)
    distance = models.DecimalField(max_digits=7, decimal_places=2)

"""
Strength_Workout is a child implimentation of Workout for activities like push-ups, bench-press, squats, etc.

Fields:
    workout - Strength_Workout can belong to only 1 parent Workout model
    bodyweight - boolean field to indicate wether workout used resistance training or bodyweight training
    repetitions - how many times was this workout activity repeated
    weight - how much weight was used (IF BODYWEIGHT=TRUE THEN WEIGHT === 0)
"""
class Strength_Workout(models.Model):
    workout = models.OneToOneField(Workout, on_delete=models.CASCADE)
    bodyweight = models.BooleanField()
    repetitions = models.IntegerField()
    weight = models.DecimalField(max_digits=5, decimal_places=2)

"""
Other_Workout is a child implimentation of Workout for activities like Sports, Yoga, etc.

Fields:
    workout - Other_Workout can belong to only 1 parent Workout model
    description (OPTIONAL) - Text that describes what this activity is
"""
class Other_Workout(models.Model):
    workout = models.OneToOneField(Workout, on_delete=models.CASCADE)
    description = models.CharField(max_length=100, blank=True)
