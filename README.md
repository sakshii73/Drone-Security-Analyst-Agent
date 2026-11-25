
# 🚁 Drone Security Analyst Agent

## Project Overview

The Drone Security Analyst Agent is an AI-powered security monitoring system designed to analyze drone surveillance images, identify objects and activities, generate security alerts, and answer questions about recorded security events.

The system uses a Vision-Language Model (VLM) to analyze simulated drone images and combines the results with drone telemetry data such as timestamps, GPS coordinates, altitude, and location.

The analyzed information is stored in an SQLite database, allowing users to retrieve and monitor security events through an AI-assisted query system and an interactive Streamlit dashboard.

## Problem Statement

Traditional surveillance monitoring requires security personnel to continuously observe camera footage and manually identify unusual activities.

This project aims to simplify surveillance analysis by automating image descriptions, object counting, event storage, security alert generation, and natural-language querying.



---

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Google Gemini | Vision-language model for image analysis |
| Google GenAI SDK | Connects the application to Gemini |
| LangChain | AI agent and tool integration |
| SQLite | Stores drone security events |
| Streamlit | Interactive monitoring dashboard |
| Pandas | Data processing and analysis |
| Plotly | Interactive charts and visualizations |
| Pillow | Image loading and processing |
| python-dotenv | Secure API key configuration |

## Key Features

- **Drone Image Analysis:** Analyzes simulated drone frames using Gemini.
- **Object Detection and Counting:** Extracts estimated people and vehicle counts.
- **Activity Description:** Generates descriptions of visible activities.
- **Telemetry Integration:** Associates image analysis with timestamps, GPS coordinates, altitude, and location.
- **Security Alerts:** Identifies potentially suspicious activities and technical anomalies.
- **Database Storage:** Stores analyzed events in SQLite.
- **AI Agent:** Supports natural-language questions about recorded security events.
- **Interactive Dashboard:** Displays event statistics, charts, alerts, and drone images.
- **Automated Testing:** Includes unit tests for database operations and alert generation.



---

## System Architecture

The project follows a modular architecture in which each component performs a specific task.

```text
             Drone Images
                  |
                  v
          Gemini Image Analysis
                  |
                  v
          Structured Frame Data
                  |
                  v
          Telemetry Integration
                  |
                  v
          Security Alert Manager
                  |
                  v
             SQLite Database
                  |
          +-------+--------+
          |                |
          v                v
    LangChain Agent   Streamlit Dashboard
          |                |
          v                v
    User Questions    Visual Monitoring
```

### Main Project Modules

| Module | Responsibility |
|---|---|
| `telemetry` | Loads drone telemetry records |
| `video_analysis` | Analyzes drone images using Gemini |
| `indexing` | Saves frame analysis in JSON |
| `alerts` | Generates security alerts |
| `database` | Creates and manages SQLite records |
| `agent` | Answers questions about recorded events |
| `app` | Provides the Streamlit dashboard |
| `tests` | Contains automated unit tests |




---

## Installation and Setup

### 1. Clone the Repository

```bash
git clone YOUR_PRIVATE_GITHUB_REPOSITORY_URL
cd Drone_Security_Analyst_Agent
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

### 3. Activate the Virtual Environment

**Windows PowerShell:**

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure Gemini API Key

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key
```

Replace the placeholder with your own Gemini API key.

**Important:** Never upload your `.env` file or expose your API key publicly.

### 6. Run the Drone Analysis Pipeline

```bash
python -m src.main
```

### 7. Launch the Dashboard

```bash
python -m streamlit run app/dashboard.py
```

Open the local URL displayed in the terminal, usually:

```text
http://localhost:8501
```

### 8. Run Automated Tests

```bash
python -m unittest discover -s tests -v
```



---

## Project Structure

```text
Drone_Security_Analyst_Agent/
│
├── app/
│   └── dashboard.py
│
├── data/
│   ├── simulated_frames/
│   ├── drone_telemetry/
│   │   └── telemetry.json
│   └── frame_analysis/
│       └── frames.json
│
├── database/
│   └── drone_security.db
│
├── src/
│   ├── telemetry/
│   ├── video_analysis/
│   ├── indexing/
│   ├── alerts/
│   ├── database/
│   ├── agent/
│   └── main.py
│
├── tests/
│   ├── test_database.py
│   └── test_alerts.py
│
├── docs/
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

## Testing

The project includes automated unit tests using Python's `unittest` framework.

Current test coverage includes:

- Retrieving recorded drone events.
- Counting database events.
- Searching events by location.
- Ensuring normal walking does not trigger suspicious activity alerts.
- Detecting explicitly flagged suspicious activity.
- Generating technical anomaly warnings.

Run all tests using:

```bash
python -m unittest discover -s tests -v
```

**Current test result:** 6 tests passed successfully.



---

## Limitations

- The current implementation uses simulated drone images rather than live drone footage.
- Image descriptions and object counts are generated by an AI model and may not always be accurate.
- Security alerts depend on the visual analysis results and predefined rules.
- Real-time drone integration has not yet been implemented.
- Gemini API usage may be subject to rate limits and quotas.

## Future Improvements

- Integrate live drone video feeds.
- Implement continuous video and multi-frame analysis.
- Improve suspicious activity detection and alert accuracy.
- Add real-time security notifications.
- Introduce advanced event search and filtering.
- Improve scalability for multiple drones and surveillance locations.
- Add authentication and role-based dashboard access.

## Project Status

The project currently provides a working prototype with simulated drone image analysis, telemetry integration, SQLite event storage, security alerts, a LangChain-based agent, and an interactive Streamlit dashboard.

Automated database and alert tests are included.
