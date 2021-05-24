from django.shortcuts import render
from django.db.models import Q

from exercise_gamification.models import Profile

"""
Title: Get the index of an element in a queryset
Source: https://stackoverflow.com/questions/1042596/get-the-index-of-an-element-in-a-queryset

Title: Django excluding specific instances from queryset without using field lookup
Source: https://stackoverflow.com/questions/3032104/django-excluding-specific-instances-from-queryset-without-using-field-lookup
"""
def index(request):
    top_users = Profile.objects.order_by('-xp').exclude(username='admin') # Exclude admin account since it isn't a valid user
    if (request.user.is_authenticated):
        # Create new profile if the profile doesn't exist
        if (Profile.objects.filter(user=request.user).count() == 0):
            full_name = 'User' + str(request.user.id)
            p = Profile.objects.create(user=request.user, name=full_name, username=request.user.username, email=request.user.email, bio='', level=0, xp=0)
        else:
            p = Profile.objects.get(user=request.user)
        # Finds the user's rank out of all users
        for index, item in enumerate(top_users): # Loop through elements in top_users query set
            if (item == p): # If the logged-in user profile is found, break and the index + 1 is the user's rank
                break
        return render(request, 'exercise_gamification/index.html', {'profile': p, 'top_users': top_users[:10], 'rank': index + 1})
    return render(request, 'exercise_gamification/index.html', {'top_users': top_users[:10]})

"""
Title: Django Search Tutorial
Source: https://learndjango.com/tutorials/django-search-tutorial
"""
def search(request):
    search_term = request.GET['search'] # Use GET to get the term that was searched for
    # Get the search results from the search term
    # Q allows you to perform an "OR" when filtering
    # Exclude the admin account since it's not a valid user
    search_results = Profile.objects.filter(Q(name__icontains=search_term) | Q(username__icontains=search_term)).exclude(username='admin')
    return render(request, 'exercise_gamification/search.html', {'search_results': search_results})
