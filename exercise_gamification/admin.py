from django.contrib import admin
from .models import Profile, FriendRequest, Workout, Cardio_Workout, Strength_Workout, Other_Workout

# Register your models here.
admin.site.register(Profile)
admin.site.register(Workout)
admin.site.register(Cardio_Workout)
admin.site.register(Strength_Workout)
admin.site.register(Other_Workout)
admin.site.register(FriendRequest)
