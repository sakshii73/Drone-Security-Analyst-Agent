import json
import os

def save_frame_analysis(result):
    os.makedirs("data/frame_analysis", exist_ok=True)

    file_path = "data/frame_analysis/frames.json"

    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            records = json.load(file)
    else:
        records = []

    records.append(result)

    with open(file_path, "w") as file:
        json.dump(records, file, indent=4)

    print("Frame analysis saved successfully!")


if __name__ == "__main__":
    sample = {
        "frame": "frame_001.jpg",
        "description": "A person is standing near the main gate."
    }

    save_frame_analysis(sample)