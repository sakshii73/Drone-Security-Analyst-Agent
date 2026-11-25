
def check_alert(description, location, structured_analysis=None):

    alerts = []

    # Use structured AI analysis when available
    if structured_analysis:

        if structured_analysis.get("suspicious_activity") is True:

            evidence = structured_analysis.get(
                "suspicious_activity_evidence",
                "Visual evidence requires review."
            )

            alerts.append(
                f"Security alert: Potential suspicious activity at "
                f"{location}. Evidence: {evidence}"
            )

        technical_anomalies = structured_analysis.get(
            "technical_anomalies", []
        )

        for anomaly in technical_anomalies:
            alerts.append(
                f"Technical warning at {location}: {anomaly}"
            )

        if alerts:
            return " | ".join(alerts)

        return f"Normal observation: No suspicious activity detected at {location}."

    # Fallback for older records without structured analysis
    description = description.lower()

    if "climbing" in description:
        alerts.append("Possible unauthorized climbing")

    if "running" in description:
        alerts.append("Unusual running activity detected")

    if alerts:
        return " | ".join(alerts)

    return f"Normal observation at {location}."


if __name__ == "__main__":

    sample_analysis = {
        "people_count": 1,
        "vehicle_count": 3,
        "activities": ["Person walking near entrance"],
        "suspicious_activity": False,
        "suspicious_activity_evidence": "",
        "technical_anomalies": ["Possible timestamp mismatch"]
    }

    result = check_alert(
        "Person walking near entrance",
        "Main Gate",
        sample_analysis
    )

    print("\nSecurity Alert Result:")
    print(result)
