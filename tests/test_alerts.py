
import unittest

from src.alerts.alert_manager import check_alert


class TestSecurityAlerts(unittest.TestCase):

    def test_normal_walking(self):

        analysis = {
            "suspicious_activity": False,
            "suspicious_activity_evidence": "",
            "technical_anomalies": []
        }

        result = check_alert(
            "Person walking normally",
            "Main Gate",
            analysis
        )

        self.assertIn("Normal observation", result)
        self.assertNotIn("Security alert", result)

    def test_suspicious_activity(self):

        analysis = {
            "suspicious_activity": True,
            "suspicious_activity_evidence": "Person attempting to climb a restricted fence",
            "technical_anomalies": []
        }

        result = check_alert(
            "Person climbing a fence",
            "Parking Area",
            analysis
        )

        self.assertIn("Security alert", result)
        self.assertIn("Parking Area", result)

    def test_technical_anomaly(self):

        analysis = {
            "suspicious_activity": False,
            "suspicious_activity_evidence": "",
            "technical_anomalies": ["Possible timestamp mismatch"]
        }

        result = check_alert(
            "Person standing near entrance",
            "Main Gate",
            analysis
        )

        self.assertIn("Technical warning", result)
        self.assertIn("timestamp mismatch", result)


if __name__ == "__main__":
    unittest.main()
