from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from django.contrib import messages

from .models import Profile, FriendRequest, Workout, Cardio_Workout, Strength_Workout, Other_Workout

import logging

# Create your views here.

def show_profile(request):
    if (request.user.is_authenticated):
        # Create new profile if the profile doesn't exist
        if (Profile.objects.filter(user=request.user).count() == 0):
            full_name = 'User' + str(request.user.id)
            Profile.objects.create(user=request.user, name=full_name, username=request.user.username, email=request.user.email, bio='', level=0, xp=0)
        # Calculate the "progress" of the user's XP bar to the next level on the profile page
        progress_width = "width: "+ str(int((request.user.profile.xp - request.user.profile.level*10000)/100)) +"%"
        return render(request, 'exercise_gamification/profile.html', {'profile': request.user.profile, 'friends': request.user.profile.friends.all(), 'workouts': request.user.profile.workouts.all()[:5], 'width': progress_width})
    return HttpResponseRedirect('/accounts/google/login/')

def show_other_user_profile(request, username):
    profile = get_object_or_404(Profile, username=username)
    workouts = profile.workouts.all()[:5] # Get only the first 5 most recent workouts
    progress_width = "width: "+ str(int((profile.xp - profile.level*10000)/100)) +"%"  #Calculate the "progress" of the other profile's XP bar to the next level on the profile page
    if (request.user.is_authenticated):
        if (username == request.user.profile.username):
            return HttpResponseRedirect(reverse('exercise_gamification:profile'))
        # Passes the profile's friend status to the user
        # 'yes' - The profile and the user are friends
        # 'out request' - The user has sent this profile a friend request
        # 'in request' - The user is receiving a friend request from the profile
        # 'no' - The profile and the user are not friends at all (no friends requests)
        if (request.user.profile.friends.filter(username=username).count() > 0):
            friends = 'yes'
        else:
            if (FriendRequest.objects.filter(to_user=profile.user, from_user=request.user).count() > 0):
                friends = 'out request'
            elif (FriendRequest.objects.filter(to_user=request.user, from_user=profile.user).count() > 0):
                friends = 'in request'
            else:
                friends = 'no'
        return render(request, 'exercise_gamification/profile.html', {'profile': profile, 'is_friend': friends, 'workouts': workouts, 'width': progress_width})
    return render(request, 'exercise_gamification/profile.html', {'profile': profile, 'workouts': workouts, 'width': progress_width})

def save_profile(request):
    if (request.user.is_authenticated):
        # Get POST profile data from form
        user_full_name = request.POST['name']
        profile_user = request.POST['username']
        user_email = request.POST['email']
        user_bio = request.POST['bio']

        # Update the User object username so it matches the profile
        request.user.username = profile_user
        request.user.save()
        # Create new profile if the profile doesn't exist
        if (Profile.objects.filter(user=request.user).count() == 0):
            Profile.objects.create(user=request.user, name=user_full_name, username=profile_user, email=user_email, bio=user_bio, level=0, xp=0)
        else:
            Profile.objects.filter(user=request.user).update(name=user_full_name, username=profile_user, email=user_email, bio=user_bio)
        return HttpResponseRedirect(reverse('exercise_gamification:profile'))
    return HttpResponseRedirect('/accounts/google/login/')

"""
Title: How to delete a record in Django models?
Source: https://stackoverflow.com/questions/3805958/how-to-delete-a-record-in-django-models
"""
def accept_friend_request(request, username):
    if (request.user.is_authenticated):
        profile = get_object_or_404(Profile, username=username)
        request.user.profile.friends.add(profile) # Add the user to their friends list
        fr = FriendRequest.objects.filter(to_user=request.user, from_user=profile.user).delete() # Delete the friend request since it has been accepted and is no longer needed
        return HttpResponseRedirect(reverse('exercise_gamification:user_profile', args=(username,)))
    return HttpResponseRedirect('/accounts/google/login/')

"""
Title: How to delete a record in Django models?
Source: https://stackoverflow.com/questions/3805958/how-to-delete-a-record-in-django-models
"""
def reject_friend_request(request, username):
    if (request.user.is_authenticated):
        profile = get_object_or_404(Profile, username=username)
        fr = FriendRequest.objects.filter(to_user=request.user, from_user=profile.user).delete() # Delete the friend request since it has been rejected and is no longer needed
        return HttpResponseRedirect(reverse('exercise_gamification:user_profile', args=(username,)))
    return HttpResponseRedirect('/accounts/google/login/')

def send_friend_request(request, username):
    if (request.user.is_authenticated):
        profile = get_object_or_404(Profile, username=username)
        # Only send a friend request if the user already hasn't sent one (safety check)
        if (FriendRequest.objects.filter(to_user=profile.user, from_user=request.user).count() == 0):
            fr = FriendRequest(to_user=profile.user, from_user=request.user)
            fr.save()
        return HttpResponseRedirect(reverse('exercise_gamification:user_profile', args=(username,)))
    return HttpResponseRedirect('/accounts/google/login/')

"""
Title: How to delete a record in Django models?
Source: https://stackoverflow.com/questions/3805958/how-to-delete-a-record-in-django-models
"""
def remove_friend_request(request, username):
    if (request.user.is_authenticated):
        profile = get_object_or_404(Profile, username=username)
        fr = FriendRequest.objects.filter(to_user=profile.user, from_user=request.user).delete() # Delete the friend request since it has been cancelled and is no longer needed
        return HttpResponseRedirect(reverse('exercise_gamification:user_profile', args=(username,)))
    return HttpResponseRedirect('/accounts/google/login/')


def remove_friend(request, username):
    if (request.user.is_authenticated):
        profile = get_object_or_404(Profile, username=username)
        request.user.profile.friends.remove(profile) # Removes friend from both profiles/users
        return HttpResponseRedirect(reverse('exercise_gamification:user_profile', args=(username,)))
    return HttpResponseRedirect('/accounts/google/login/')

"""
Title: Good ways to sort a queryset? - Django
Source: https://stackoverflow.com/questions/2412770/good-ways-to-sort-a-queryset-django
"""
def display_workouts(request):
    if (request.user.is_authenticated):
        # Create new profile if the profile doesn't exist
        if (Profile.objects.filter(user=request.user).count() == 0):
            full_name = 'User' + str(request.user.id)
            p = Profile.objects.create(user=request.user, name=full_name, username=request.user.username, email=request.user.email, bio='', level=0, xp=0)
        else:
            p = Profile.objects.get(user=request.user)
        workouts = p.workouts.all()
        top_friends = request.user.profile.friends.order_by('-xp')[:3] # Sort user's friends into queryset by xp in descending order (gets the top 3 friends)
        return render(request, 'exercise_gamification/workouts.html', {'workouts': workouts, 'top_friends': top_friends})
    return HttpResponseRedirect('/accounts/google/login/')

def load_cardio_subimssion(request):
    if (request.user.is_authenticated):
        return render(request, 'exercise_gamification/cardio_form.html')
    return HttpResponseRedirect('/accounts/google/login/')

def load_strength_submission(request):
    if (request.user.is_authenticated):
        return render(request, 'exercise_gamification/strength_form.html')
    return HttpResponseRedirect('/accounts/google/login/')

def load_other_submission(request):
    if (request.user.is_authenticated):
        return render(request, 'exercise_gamification/other_workout_form.html')
    return HttpResponseRedirect('/accounts/google/login/')

"""
Title: Accessing Radio/Checkbox button selection in Django form post reques
Source: https://stackoverflow.com/questions/51238341/accessing-radio-checkbox-button-selection-in-django-form-post-request
"""
def redirect_workout(request):
    if (request.user.is_authenticated):
        # Post data returns the name of the radio button in a list
        workout_type = request.POST.getlist('workout_type')
        # Checks the list for the appropriate workout type radio button and redirects
        if ('cardio' in workout_type):
            return HttpResponseRedirect(reverse('exercise_gamification:cardio_workout'))
        elif ('strength' in workout_type):
            return HttpResponseRedirect(reverse('exercise_gamification:strength_workout'))
        elif ('other' in workout_type):
            return HttpResponseRedirect(reverse('exercise_gamification:other_workout'))
        return HttpResponseRedirect(reverse('exercise_gamification:choose_workout'))
    return HttpResponseRedirect('/accounts/google/login/')

def submit_cardio_workout(request):
    if (request.user.is_authenticated):
        p = Profile.objects.get(user=request.user)
        # Get POST workout data from form
        workout_name = request.POST['workout_name']
        calories = 0 # Dummy value for now
        workout_notes = request.POST['notes']

        cardio_duration = request.POST['duration']
        cardio_distance = request.POST['distance']

        # Save the workout using POST data and add the workout to the profile
        w = Workout(base_profile=p, date=timezone.now(), name=workout_name, estimated_calories=calories, notes=workout_notes)
        w.save()
        c = Cardio_Workout(workout=w, duration=cardio_duration, distance=cardio_distance)
        c.save()

        p.workouts.add(w)
        old_xp = p.xp
        p.xp = int(p.xp + 1000 + float(cardio_duration)*10 + float(cardio_distance)*100)
        old_level = p.level
        p.level = p.xp // 10000
        p.save()
        messages.success(request, "Nice work, " + p.name+". " + str(p.xp-old_xp) + " xp earned!")

        if p.level > old_level:
            messages.success(request, "Amazing " + p.name +", you're now a level " + str(p.level) +"! Keep up the great work!")

        return HttpResponseRedirect(reverse('exercise_gamification:workouts'))
    return HttpResponseRedirect('/accounts/google/login/')

"""
Title: Accessing Radio/Checkbox button selection in Django form post reques
Source: https://stackoverflow.com/questions/51238341/accessing-radio-checkbox-button-selection-in-django-form-post-request
"""
def submit_strength_workout(request):
    if (request.user.is_authenticated):
        p = Profile.objects.get(user=request.user)
        # Get POST workout data from form
        workout_name = request.POST['workout_name']
        calories = 0 # Dummy value for now
        workout_notes = request.POST['notes']

        strength_bodyweight = request.POST.getlist('bodyweight') # List should contain 'on' if t he checkbox is checked
        strength_repitions = request.POST['repetitions']
        strength_weight = request.POST['weight']

        is_bodyweight = False

        if ('on' in strength_bodyweight):
            strength_weight = 0
            is_bodyweight = True

        # Save the workout using POST data and add the workout to the profile
        w = Workout(base_profile=p, date=timezone.now(), name=workout_name, estimated_calories=calories, notes=workout_notes)
        w.save()

        s = Strength_Workout(workout=w, bodyweight=is_bodyweight, repetitions=strength_repitions, weight=strength_weight)
        s.save()

        p.workouts.add(w)

        old_xp = p.xp
        p.xp = int(p.xp + 1000 + float(strength_repitions)*100)
        old_level = p.level
        p.level = p.xp // 10000
        p.save()
        messages.success(request, "Nice work, " + p.name+". " + str(p.xp-old_xp) + " xp earned!")
        if p.level > old_level:
            messages.success(request, "Amazing " + p.name +", you're now a level " + str(p.level) +"! Keep up the great work!")

        return HttpResponseRedirect(reverse('exercise_gamification:workouts'))
    return HttpResponseRedirect('/accounts/google/login/')

def submit_other_workout(request):
    if (request.user.is_authenticated):
        p = Profile.objects.get(user=request.user)
        # Get POST workout data from form
        workout_name = request.POST['workout_name']
        calories = 0 # Dummy value for now
        workout_notes = request.POST['notes']

        workout_description = request.POST['description']

        # Save the workout using POST data and add the workout to the profile
        w = Workout(base_profile=p, date=timezone.now(), name=workout_name, estimated_calories=calories, notes=workout_notes)
        w.save()

        o = Other_Workout(workout=w, description=workout_description)
        o.save()

        p.workouts.add(w)

        p.xp = p.xp + 1000
        old_level = p.level
        p.level = p.xp // 10000
        p.save()
        messages.success(request, "Nice work, " + p.name+". " + str(1000) + " xp earned!")

        if p.level > old_level:
            messages.success(request, "Amazing " + p.name +", you're now a level " + str(p.level) +"! Keep up the great work!")

        return HttpResponseRedirect(reverse('exercise_gamification:workouts'))
    return HttpResponseRedirect('/accounts/google/login/')
