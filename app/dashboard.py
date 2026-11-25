
import streamlit as st
import sqlite3
import pandas as pd
import json
import os
import plotly.express as px


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Drone Security Dashboard",
    page_icon="🚁",
    layout="wide"
)


# --------------------------------------------------
# DATABASE CONNECTION
# --------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DB_PATH = os.path.join(
    BASE_DIR,
    "database",
    "drone_security.db"
)


def load_events():

    if not os.path.exists(DB_PATH):
        return pd.DataFrame()

    connection = sqlite3.connect(DB_PATH)

    query = "SELECT * FROM events ORDER BY timestamp DESC"

    df = pd.read_sql_query(query, connection)

    connection.close()

    return df


# --------------------------------------------------
# DASHBOARD HEADER
# --------------------------------------------------

st.title("🚁 Drone Security Monitoring Dashboard")

st.markdown(
    "AI-powered surveillance monitoring using drone imagery, "
    "telemetry data, and security event analysis."
)

st.divider()


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

if st.button("🔄 Refresh Dashboard"):

    st.rerun()

df = load_events()



# --------------------------------------------------
# STRUCTURED ANALYSIS
# --------------------------------------------------

def parse_analysis(value):

    try:
        if value:
            return json.loads(value)

    except (json.JSONDecodeError, TypeError):
        pass

    return {}


if "structured_analysis" in df.columns:

    df["analysis"] = df["structured_analysis"].apply(parse_analysis)

else:

    df["analysis"] = [{} for _ in range(len(df))]


df["people_count"] = df["analysis"].apply(
    lambda x: x.get("people_count", 0)
)

df["vehicle_count"] = df["analysis"].apply(
    lambda x: x.get("vehicle_count", 0)
)

df["suspicious_activity"] = df["analysis"].apply(
    lambda x: x.get("suspicious_activity", False)
)


# --------------------------------------------------
# SIDEBAR FILTERS
# --------------------------------------------------

st.sidebar.header("Dashboard Filters")

locations = ["All Locations"] + sorted(
    df["location"].dropna().unique().tolist()
)

selected_location = st.sidebar.selectbox(
    "Select Location",
    locations
)

if selected_location != "All Locations":

    filtered_df = df[
        df["location"] == selected_location
    ].copy()

else:

    filtered_df = df.copy()


# --------------------------------------------------
# KEY PERFORMANCE INDICATORS
# --------------------------------------------------

st.subheader("Security Overview")

total_events = len(filtered_df)

total_people = int(filtered_df["people_count"].sum())

total_vehicles = int(filtered_df["vehicle_count"].sum())

suspicious_events = int(
    filtered_df["suspicious_activity"].astype(bool).sum()
)

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Events", total_events)

col2.metric("People Detected", total_people)

col3.metric("Vehicles Detected", total_vehicles)

col4.metric("Suspicious Events", suspicious_events)


st.divider()


# --------------------------------------------------
# CHARTS
# --------------------------------------------------

st.subheader("Event Analytics")

chart_col1, chart_col2 = st.columns(2)


with chart_col1:

    location_counts = (
        filtered_df["location"]
        .value_counts()
        .reset_index()
    )

    location_counts.columns = [
        "Location",
        "Events"
    ]

    fig_location = px.bar(
        location_counts,
        x="Location",
        y="Events",
        title="Events by Location",
        color="Location",
        text="Events"
    )

    st.plotly_chart(
        fig_location,
        use_container_width=True
    )


with chart_col2:

    object_data = pd.DataFrame({
        "Object": ["People", "Vehicles"],
        "Count": [total_people, total_vehicles]
    })

    fig_objects = px.pie(
        object_data,
        names="Object",
        values="Count",
        title="People vs Vehicles Detected",
        hole=0.45
    )

    st.plotly_chart(
        fig_objects,
        use_container_width=True
    )


st.divider()


# --------------------------------------------------
# SECURITY ALERTS
# --------------------------------------------------

st.subheader("🚨 Security Alerts")

alert_df = filtered_df[
    filtered_df["alert"].fillna("").str.contains(
        "alert|warning",
        case=False,
        regex=True
    )
]

if not alert_df.empty:

    for _, row in alert_df.iterrows():

        st.warning(
            f"Location: {row['location']}\n\n"
            f"Timestamp: {row['timestamp']}\n\n"
            f"{row['alert']}"
        )

else:

    st.success("No security alerts recorded.")


st.divider()


# --------------------------------------------------
# EVENT HISTORY
# --------------------------------------------------

st.subheader("📋 Drone Event History")

display_columns = [
    "timestamp",
    "location",
    "description",
    "alert"
]

st.dataframe(
    filtered_df[display_columns],
    use_container_width=True,
    hide_index=True
)


st.divider()


# --------------------------------------------------
# DETAILED EVENT ANALYSIS
# --------------------------------------------------


# --------------------------------------------------
# DETAILED EVENT ANALYSIS WITH DRONE IMAGES
# --------------------------------------------------

st.subheader("🔍 Detailed Event Analysis")

for _, row in filtered_df.iterrows():

    with st.expander(
        f"{row['location']} | {row['timestamp']}"
    ):

        st.write("### Drone Frame")

        image_path = os.path.join(
            BASE_DIR,
            "data",
            "simulated_frames",
            str(row["frame"])
        )

        if os.path.exists(image_path):

            st.image(
                image_path,
                caption=f"Drone Frame: {row['frame']}",
                use_container_width=True
            )

        else:

            st.warning(
                f"Image not found: {row['frame']}"
            )

        st.divider()

        st.write("### Event Information")

        st.write("**Frame:**", row["frame"])

        st.write("**Timestamp:**", row["timestamp"])

        st.write("**Location:**", row["location"])

        st.write("**Description:**", row["description"])

        st.write("### Detection Results")

        st.write("**People detected:**", row["people_count"])

        st.write("**Vehicles detected:**", row["vehicle_count"])

        st.write(
            "**Suspicious activity:**",
            "Yes" if row["suspicious_activity"] else "No"
        )

        st.write("### Drone Telemetry")

        st.write("**Latitude:**", row["latitude"])

        st.write("**Longitude:**", row["longitude"])

        st.write("**Altitude:**", row["altitude"], "meters")

        st.write("### Security Alert")

        st.info(row["alert"])


# --------------------------------------------------
# SECURITY QUESTION AND ANSWER
# --------------------------------------------------

st.divider()

st.subheader("💬 Ask the Security Analyst")

st.write(
    "Ask questions about recorded drone events, "
    "people, vehicles, locations, and security alerts."
)

question = st.text_input(
    "Enter your security question:",
    placeholder="Example: What happened at Main Gate?"
)

if st.button("Get Answer", type="primary"):

    if not question.strip():

        st.warning("Please enter a question.")

    else:

        q = question.lower()

        answer_df = df.copy()

        # Filter by location if mentioned
        if "main gate" in q:
            answer_df = answer_df[
                answer_df["location"] == "Main Gate"
            ]

        elif "parking" in q:
            answer_df = answer_df[
                answer_df["location"] == "Parking Area"
            ]

        if answer_df.empty:

            st.info("No matching events found.")

        elif "suspicious" in q:

            suspicious = answer_df[
                answer_df["suspicious_activity"].astype(bool)
            ]

            if suspicious.empty:
                st.success(
                    "No suspicious activities were detected "
                    "in the matching recorded events."
                )
            else:
                st.warning(
                    f"{len(suspicious)} potentially suspicious "
                    "event(s) found."
                )
                st.dataframe(
                    suspicious[
                        ["timestamp", "location", "description", "alert"]
                    ],
                    use_container_width=True
                )

        elif "people" in q or "person" in q:

            total = int(answer_df["people_count"].sum())

            st.success(
                f"Total people detected: {total}"
            )

        elif "vehicle" in q:

            total = int(answer_df["vehicle_count"].sum())

            st.success(
                f"Total vehicles detected: {total}"
            )

        elif "alert" in q or "warning" in q:

            st.write("### Recorded Security Alerts")

            for _, row in answer_df.iterrows():

                st.warning(
                    f"{row['location']}: {row['alert']}"
                )

        elif "how many" in q or "count" in q:

            st.success(
                f"Total recorded drone events: {len(answer_df)}"
            )

        elif (
            "what happened" in q
            or "show events" in q
            or "all events" in q
        ):

            st.dataframe(
                answer_df[
                    ["timestamp", "location", "description", "alert"]
                ],
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info(
                "I could not identify this question. "
                "Try asking about events, people, vehicles, "
                "suspicious activities, or alerts."
            )

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "Drone Security Analyst Agent | "
    "AI-based surveillance event monitoring"
)
