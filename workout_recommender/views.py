from django.shortcuts import render
from . import api_interactions
# Create your views here.

def selector_form(request):
    return render(request, 'workout_recommender/selector_form.html')

def redirect_form(request):
    form_input = request.POST.getlist('muscle-group')
    selection = ""
    if ("Any/All" in form_input):
        selection = "Any/All"
    elif ('Abs' in form_input):
        selection = "Abs"
    elif ('Arms' in form_input):
        selection = "Arms"
    elif ('Back' in form_input):
        selection = "Back"
    elif ('Calves' in form_input):
        selection = "Calves"
    elif ('Chest' in form_input):
        selection = "Chest"
    elif ('Legs' in form_input):
        selection = "Legs"
    elif ('Shoulders' in form_input):
        selection = "Shoulders"
    
    relevent_workouts = api_interactions.get_workouts(selection)
    return render(request, 'workout_recommender/workouts.html', 
        {"workouts": relevent_workouts})

"""
def selector_form(request):
    context={}
    context['form'] = SelectorForm(request.POST)
    if context['form'].is_valid():
        num_workouts = context['form'].cleaned_data['num_workouts']
        selection = context['form'].cleaned_data['selection']

        relevent_workouts = api_interactions.get_select_workouts(num_workouts, selection)
        return render(request, 'workout_recommender/workouts.html', 
        {"workouts": relevent_workouts})

    return render(request, 'workout_recommender/selector_form.html', context)
    """
        
"""
        return render(request, 'workout_recommender/workouts.html',
            {"workouts": 
                api_interactions.get_select_workouts(num_workouts, selection)})
    """
"""
def all_workouts(request):
    return render(request, 'workout_recommender/workouts.html', 
        {"workouts": api_interactions.get_all_workouts(500)})
"""