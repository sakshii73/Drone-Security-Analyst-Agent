
import os
import json
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import tool
from langchain.agents import create_agent

from src.agent.query_engine import (
    get_all_events,
    search_by_location,
    count_events
)

# Load Gemini API key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Connect Gemini model
llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash",
    google_api_key=api_key,
    temperature=0
)


# Database tools for LangChain
@tool
def get_drone_events():
    """Retrieve all recorded drone security events."""
    return str(get_all_events())


@tool
def get_events_by_location(location: str):
    """Find drone security events at a specified location."""
    return str(search_by_location(location))


@tool
def get_total_events():
    """Get the total number of recorded drone security events."""
    return str(count_events())


tools = [
    get_drone_events,
    get_events_by_location,
    get_total_events
]


agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt=(
        "You are a drone security monitoring assistant. "
        "Use database tools for recorded event information. "
        "Never invent security incidents. "
        "Normal walking is not suspicious activity."
    )
)


# Direct database question handling
def answer_from_database(question):

    q = question.lower()

    events = get_all_events()

    # Location identification
    location = None

    if "main gate" in q:
        location = "Main Gate"

    elif "parking" in q:
        location = "Parking Area"

    if location:
        events = search_by_location(location)

    if not events:
        return "No matching drone events found."

    # Parse structured AI analysis
    analyses = []

    for event in events:
        try:
            data = json.loads(event[9]) if event[9] else {}
        except (IndexError, TypeError, json.JSONDecodeError):
            data = {}

        analyses.append(data)

    # Suspicious activity questions
    if "suspicious" in q:

        suspicious_events = []

        for event, analysis in zip(events, analyses):
            if analysis.get("suspicious_activity") is True:
                suspicious_events.append(event)

        if suspicious_events:
            answer = "Potential suspicious activity detected:\n"

            for event in suspicious_events:
                answer += (
                    f"\nLocation: {event[3]}"
                    f"\nTimestamp: {event[2]}"
                    f"\nDescription: {event[4]}"
                    f"\nAlert: {event[5]}\n"
                )

            return answer

        return (
            f"No suspicious activities were detected "
            f"in the {len(events)} recorded events."
        )

    # People count
    if "people" in q or "person" in q:

        total_people = sum(
            analysis.get("people_count", 0)
            for analysis in analyses
        )

        return f"Total people detected across matching events: {total_people}"

    # Vehicle count
    if "vehicle" in q or "vehicles" in q:

        total_vehicles = sum(
            analysis.get("vehicle_count", 0)
            for analysis in analyses
        )

        return f"Total vehicles detected across matching events: {total_vehicles}"

    # Alert questions
    if "alert" in q or "warning" in q:

        answer = "Recorded security alerts:\n"

        for event in events:
            answer += (
                f"\nLocation: {event[3]}"
                f"\nAlert: {event[5]}\n"
            )

        return answer

    # Location-specific event count
    if location and ("how many" in q or "count" in q):
        return f"Total events at {location}: {len(events)}"

    # Total event count
    if "how many" in q or "count" in q:
        return f"Total drone events recorded: {count_events()}"

    # Show all events
    if (
        "all events" in q
        or "show events" in q
        or "recorded drone security events" in q
    ):

        answer = "All recorded drone events:\n"

        for event in events:
            answer += (
                f"\nTimestamp: {event[2]}"
                f"\nLocation: {event[3]}"
                f"\nDescription: {event[4]}"
                f"\nAlert: {event[5]}\n"
            )

        return answer

    return None


# Run the agent
if __name__ == "__main__":

    print("Drone Security AI Agent is ready!")

    question = input("\nAsk a security question: ")

    response = answer_from_database(question)

    if response is not None:

        print("\nDatabase Response:")
        print(response)

    else:

        try:
            response = agent.invoke({
                "messages": [
                    {"role": "user", "content": question}
                ]
            })

            print("\nAgent Response:")
            print(response["messages"][-1].content)

        except Exception as error:
            print("\nAI Agent Error:")
            print("Gemini API may be temporarily unavailable.")
            print("Database questions can still be answered.")
            print("Error:", error)
