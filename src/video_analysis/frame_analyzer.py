
import os
import json
from dotenv import load_dotenv
from google import genai
from PIL import Image

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file")

client = genai.Client(api_key=api_key)


def analyze_frame(frame_path):

    image = Image.open(frame_path)

    prompt = """
    Analyze this security camera image carefully.

    Return ONLY valid JSON with these fields:

    {
        "people_count": 0,
        "vehicle_count": 0,
        "activities": [],
        "suspicious_activity": false,
        "suspicious_activity_evidence": "",
        "environment": "",
        "technical_anomalies": [],
        "security_summary": ""
    }

    Rules:
    1. Count only clearly visible people and vehicles.
    2. Describe only activities supported by visual evidence.
    3. A person walking or standing normally is NOT suspicious by itself.
    4. Set suspicious_activity to true only when clear visual
       evidence supports potentially suspicious behavior.
    5. If there is no suspicious evidence, set it to false.
    6. Mention possible image or timestamp issues under
       technical_anomalies only when supported by available evidence.
    7. Do not invent details.
    """

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=[prompt, image]
    )

    raw_text = response.text.strip()

    # Remove JSON markdown formatting if Gemini includes it
    if raw_text.startswith("```"):
        raw_text = raw_text.split("\n", 1)[1]
        raw_text = raw_text.rsplit("```", 1)[0].strip()

    analysis = json.loads(raw_text)

    result = {
        "frame": os.path.basename(frame_path),
        "description": analysis["security_summary"],
        "structured_analysis": analysis
    }

    return result


if __name__ == "__main__":

    image_path = "data/simulated_frames/frame_001.png"

    result = analyze_frame(image_path)

    print("\nStructured AI Analysis:")
    print(json.dumps(result, indent=4))
