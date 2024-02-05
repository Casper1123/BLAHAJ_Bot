import json


# JSON funnies
def load_json(filename: str) -> dict:
    with open(f"{filename}", "r") as cj:
        return json.load(cj)


def write_json(filename: str, cj_dict: dict):
    with open(f"{filename}", "w") as cj:
        json.dump(cj_dict, cj, indent=4)
