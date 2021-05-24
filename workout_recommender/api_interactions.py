import requests
import json
import html2text

def get_all_muscle_groups():
    raw_responce = requests.get('https://wger.de/api/v2/exercisecategory/?format=json')
    as_text = json.dumps(raw_responce.json(), indent=4)
    parseable = json.loads(as_text)["results"]
    muscle_groups = []
    for muscle_group in parseable:
        new_muscle_group = {
            "id": muscle_group["id"],
            "name": muscle_group["name"].strip()
        }
        muscle_groups.append(new_muscle_group)
    return muscle_groups

def get_select_workouts(limit=30, muscle_group="Any/All"):
    if muscle_group == "Any/All":
        return get_all_workouts(limit=limit)
    else:
        raw_responce = requests.get(f'https://wger.de/api/v2/exerciseinfo/?format=json&limit={limit}&language=2')
        as_text = json.dumps(raw_responce.json(), indent=4)
        parseable = json.loads(as_text)["results"]
        workouts = []
        for workout in parseable:
            if workout["category"]["name"] == muscle_group:
                new_workout = {
                    "name": html2text.html2text(workout["name"]).strip(),
                    "description": html2text.html2text(workout["description"]).strip()
                }

                workouts.append(new_workout)

        return workouts

def get_workouts(muscle_group="Any/All"):
    if muscle_group == "Any/All":
        return get_all_workouts(limit=999)
    else:
        raw_responce = requests.get(f'https://wger.de/api/v2/exerciseinfo/?format=json&limit={999}&language=2')
        as_text = json.dumps(raw_responce.json(), indent=4)
        parseable = json.loads(as_text)["results"]
        workouts = []
        for workout in parseable:
            if workout["category"]["name"] == muscle_group:
                new_workout = {
                    "name": html2text.html2text(workout["name"]).strip(),
                    "description": html2text.html2text(workout["description"]).strip()
                }

                workouts.append(new_workout)

        return workouts


def get_all_workouts(limit=30):
    raw_responce = requests.get(f'https://wger.de/api/v2/exerciseinfo/?format=json&limit={limit}&language=2')
    as_text = json.dumps(raw_responce.json(), indent=4)
    parseable = json.loads(as_text)["results"]
    all_workouts = []
    counter = 0
    for workout in parseable:
        new_workout = {
            "name": html2text.html2text(workout["name"]).strip(),
            "description": html2text.html2text(workout["description"]).strip()
        }
        all_workouts.append(new_workout)

    return all_workouts
