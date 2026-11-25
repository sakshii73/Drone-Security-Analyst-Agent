
import unittest

from src.agent.query_engine import (
    get_all_events,
    search_by_location,
    count_events
)


class TestDroneDatabase(unittest.TestCase):

    def test_get_all_events(self):

        events = get_all_events()

        self.assertIsInstance(events, list)

    def test_count_events(self):

        total = count_events()

        self.assertIsInstance(total, int)
        self.assertGreaterEqual(total, 0)

    def test_search_by_location(self):

        events = search_by_location("Main Gate")

        self.assertIsInstance(events, list)

        for event in events:
            self.assertIn("Main Gate", event[3])


if __name__ == "__main__":
    unittest.main()
