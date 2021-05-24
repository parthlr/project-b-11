from exercise_gamification.models import FriendRequest

"""
Title: How I do render a queryset in a Django base template?
Source: https://stackoverflow.com/questions/57828493/how-i-do-render-a-queryset-in-a-django-base-template
"""
# Add this function to context_processors in settings.py
def add_variables(request):
    if (request.user.is_authenticated):
        incoming_fr = FriendRequest.objects.filter(to_user=request.user)
        outgoing_fr = FriendRequest.objects.filter(from_user=request.user)
        num_fr = FriendRequest.objects.filter(to_user=request.user).count()
        return {
            'incoming_fr': incoming_fr,
            'outgoing_fr': outgoing_fr,
            'num_fr': num_fr
        }
    return {}
