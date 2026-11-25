
from src.agent.query_engine import (
    get_all_events,
    search_by_location,
    count_events
)


def answer_question(question):

    question = question.lower()

    # Count total events
    if "how many" in question or "count" in question:
        total = count_events()
        return f"Total drone events recorded: {total}"

    # Search by location
    elif "main gate" in question:
        events = search_by_location("Main Gate")

    elif "parking" in question:
        events = search_by_location("Parking Area")

    # Show all events
    elif "all events" in question or "show events" in question:
        events = get_all_events()

    else:
        return "Sorry, I could not understand your question."

    if not events:
        return "No matching events found."

    answer = ""

    for event in events:
        answer += f"\nTimestamp: {event[2]}\n"
        answer += f"Location: {event[3]}\n"
        answer += f"Description: {event[4]}\n"
        answer += f"Alert: {event[5]}\n"

    return answer


if __name__ == "__main__":

    question = input("Ask a security question: ")

    response = answer_question(question)

    print("\nAgent Response:")
    print(response)
