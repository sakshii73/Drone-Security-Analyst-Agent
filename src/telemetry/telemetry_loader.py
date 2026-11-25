import json

def load_telemetry():
    with open("data/drone_telemetry/telemetry.json", "r") as file:
        data = json.load(file)

    return data


if __name__ == "__main__":
    telemetry = load_telemetry()

    for record in telemetry:
        print(record)