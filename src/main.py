
import os

from src.telemetry.telemetry_loader import load_telemetry
from src.video_analysis.frame_analyzer import analyze_frame
from src.indexing.frame_indexer import save_frame_analysis
from src.alerts.alert_manager import check_alert
from src.database.db_manager import create_database, insert_event


def main():

    # Create SQLite database
    create_database()

    # Load telemetry records
    telemetry_records = load_telemetry()

    # Process each frame with its matching telemetry
    for record in telemetry_records:

        image_path = os.path.join(
            "data",
            "simulated_frames",
            record["frame"]
        )

        if not os.path.exists(image_path):
            print(f"\nImage not found: {image_path}")
            continue

        print("\n" + "=" * 50)
        print("Analyzing drone footage...")
        print("Frame:", record["frame"])
        print("Timestamp:", record["timestamp"])
        print("Location:", record["location"])

        # Analyze image using Gemini VLM
        result = analyze_frame(image_path)

        # Attach matching telemetry information
        result["timestamp"] = record["timestamp"]
        result["location"] = record["location"]
        result["latitude"] = record["latitude"]
        result["longitude"] = record["longitude"]
        result["altitude"] = record["altitude"]

        # Generate security alert
        alert = check_alert(
            result["description"],
            record["location"],
            result["structured_analysis"]
        )

        print("\nStructured Analysis:")
        print(result["structured_analysis"])

        print("\nSecurity Alert:")
        print(alert)

        # Save analysis in JSON
        save_frame_analysis(result)

        # Save event in SQLite
        insert_event(result, alert)

    print("\nAll available frames have been processed!")


if __name__ == "__main__":
    main()
