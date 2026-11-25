
import sqlite3


def get_all_events():

    connection = sqlite3.connect("database/drone_security.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM events")
    records = cursor.fetchall()

    connection.close()

    return records


def search_by_location(location):

    connection = sqlite3.connect("database/drone_security.db")
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM events WHERE location LIKE ?",
        ('%' + location + '%',)
    )

    records = cursor.fetchall()

    connection.close()

    return records


def count_events():

    connection = sqlite3.connect("database/drone_security.db")
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM events")
    result = cursor.fetchone()

    connection.close()

    return result[0]


if __name__ == "__main__":

    print("\nTotal Drone Events:")
    print(count_events())

    print("\nEvents at Main Gate:")

    events = search_by_location("Main Gate")

    for event in events:
        print(event)
