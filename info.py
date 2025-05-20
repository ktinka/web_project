import json


def get_dicts(dict_name):
    with open('info.json') as file:
        f = file.read()
        data = json.loads(f)
        info = data[dict_name]
    return info


classes_info = get_dicts("classes_info")
races_info = get_dicts("races_info")
