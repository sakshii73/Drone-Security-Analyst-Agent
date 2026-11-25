
import sqlite3
import os
import json


DB_PATH = "database/drone_security.db"


# 1. Create database and upgrade table if required
def create_database():

    os.makedirs("database", exist_ok=True)

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            frame TEXT,
            timestamp TEXT,
            location TEXT,
            description TEXT,
            alert TEXT,
            latitude REAL,
            longitude REAL,
            altitude REAL,
            structured_analysis TEXT
        )
    """)

    # Add structured_analysis to older databases
    cursor.execute("PRAGMA table_info(events)")
    columns = [column[1] for column in cursor.fetchall()]

    if "structured_analysis" not in columns:
        cursor.execute("""
            ALTER TABLE events
            ADD COLUMN structured_analysis TEXT
        """)

    connection.commit()
    connection.close()

    print("Database and events table created successfully!")


# 2. Insert or update drone event
def insert_event(result, alert):

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    structured_analysis = json.dumps(
        result.get("structured_analysis", {})
    )

    # Check whether this frame and timestamp already exist
    cursor.execute("""
        SELECT id FROM events
        WHERE frame = ? AND timestamp = ?
    """, (
        result["frame"],
        result["timestamp"]
    ))

    existing_record = cursor.fetchone()

    if existing_record:

        cursor.execute("""
            UPDATE events
            SET location = ?,
                description = ?,
                alert = ?,
                latitude = ?,
                longitude = ?,
                altitude = ?,
                structured_analysis = ?
            WHERE id = ?
        """, (
            result["location"],
            result["description"],
            alert,
            result["latitude"],
            result["longitude"],
            result["altitude"],
            structured_analysis,
            existing_record[0]
        ))

        print("Existing drone event updated successfully!")

    else:

        cursor.execute("""
            INSERT INTO events (
                frame,
                timestamp,
                location,
                description,
                alert,
                latitude,
                longitude,
                altitude,
                structured_analysis
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            result["frame"],
            result["timestamp"],
            result["location"],
            result["description"],
            alert,
            result["latitude"],
            result["longitude"],
            result["altitude"],
            structured_analysis
        ))

        print("Drone event inserted into SQLite successfully!")

    connection.commit()
    connection.close()


# 3. View all saved drone events
def view_events():

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM events")
    records = cursor.fetchall()

    print("\nSaved Drone Events:")

    if records:
        for record in records:

            print("\n-------------------------")
            print("ID:", record[0])
            print("Frame:", record[1])
            print("Timestamp:", record[2])
            print("Location:", record[3])
            print("Description:", record[4])
            print("Alert:", record[5])
            print("Latitude:", record[6])
            print("Longitude:", record[7])
            print("Altitude:", record[8])

            if len(record) > 9 and record[9]:
                print("Structured Analysis:", record[9])

    else:
        print("No events found.")

    connection.close()


if __name__ == "__main__":
    create_database()
    view_events()
