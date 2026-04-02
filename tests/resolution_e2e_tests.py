"""End-to-end tests for the Resolution API."""

import unittest
import requests
import time

BASE_URL: str = "http://proofofresolution:8080"


class ResolutionE2ETests(unittest.TestCase):
    """End-to-end tests for the /resolutions routes."""

    created_resolution_id: str = ""
    resolution_payload = {
        "title": f"Test Resolution {int(time.time())}",  # Unique title per run
        "description": "This is an end-to-end test resolution.",
        "category": "E2E Testing"
    }

    @classmethod
    def setUpClass(cls):
        pass

    def test_1_create_resolution_success(self) -> None:
        """Test successfully creating a new resolution."""
        print("--- Running test_1_create_resolution_success ---")
        response = requests.post(f"{BASE_URL}/resolutions/", json=self.resolution_payload, timeout=30)
        self.assertEqual(response.status_code, 201, f"Expected status 201, got {response.status_code}. Response: {response.json()}")
        data = response.json()
        self.assertIn("goal_id", data)
        self.assertIn("resolution", data)
        self.assertIn("title", data["resolution"])
        self.assertEqual(data["resolution"]["title"], self.resolution_payload["title"])
        ResolutionE2ETests.created_resolution_id = data["goal_id"]
        print(f"Created Resolution ID: {ResolutionE2ETests.created_resolution_id}")

    def test_2_get_all_resolutions(self) -> None:
        """Test retrieving all resolutions and confirming the newly created resolution is present."""
        print("--- Running test_2_get_all_resolutions ---")
        self.assertTrue(ResolutionE2ETests.created_resolution_id, "Resolution ID should be set from creation test")
        response = requests.get(f"{BASE_URL}/resolutions/", timeout=10)
        self.assertEqual(response.status_code, 200, f"Expected status 200, got {response.status_code}. Response: {response.json()}")
        data = response.json()
        self.assertIn("resolutions", data)
        self.assertIsInstance(data["resolutions"], list)

        found = any(
            r.get("goal_id") == ResolutionE2ETests.created_resolution_id
            for r in data["resolutions"]
        )
        self.assertTrue(found, f"Newly created resolution (ID: {ResolutionE2ETests.created_resolution_id}) not found in the list.")
        print("Found created resolution in all resolutions list.")

    def test_3_get_specific_resolution_by_id(self) -> None:
        """Test retrieving the specific resolution by its ID."""
        print("--- Running test_3_get_specific_resolution_by_id ---")
        self.assertTrue(ResolutionE2ETests.created_resolution_id, "Resolution ID should be set from creation test")
        response = requests.get(f"{BASE_URL}/resolutions/{ResolutionE2ETests.created_resolution_id}", timeout=10)
        self.assertEqual(response.status_code, 200, f"Expected status 200, got {response.status_code}. Response: {response.json()}")
        data = response.json()
        self.assertIn("resolution", data)
        self.assertEqual(data["resolution"]["goal_id"], ResolutionE2ETests.created_resolution_id)
        self.assertEqual(data["resolution"]["title"], self.resolution_payload["title"])
        print(f"Successfully retrieved specific resolution by ID: {ResolutionE2ETests.created_resolution_id}")

    def test_4_attempt_delete_resolution_returns_immutable_response(self) -> None:
        """Test attempting to delete returns the immutable blockchain response."""
        print("--- Running test_4_attempt_delete_resolution_returns_immutable_response ---")
        self.assertTrue(ResolutionE2ETests.created_resolution_id, "Resolution ID should be set from creation test")
        response = requests.delete(f"{BASE_URL}/resolutions/{ResolutionE2ETests.created_resolution_id}", timeout=10)
        self.assertEqual(response.status_code, 200, f"Expected status 200, got {response.status_code}. Response: {response.json()}")
        data = response.json()
        self.assertIn("message", data)
        self.assertIn("goal_id", data)
        # Router returns: "🔒 Nice try! The blockchain never forgets – and neither do we."
        self.assertIn("blockchain never forgets", data["message"])
        print(f"Received immutable delete response: {data['message']}")

    def test_5_attempt_update_resolution_returns_immutable_response(self) -> None:
        """Test attempting to update returns the immutable blockchain response."""
        print("--- Running test_5_attempt_update_resolution_returns_immutable_response ---")
        self.assertTrue(ResolutionE2ETests.created_resolution_id, "Resolution ID should be set from creation test")
        updated_payload = {"title": "Updated Test Resolution", "description": "Updated description."}
        response = requests.put(f"{BASE_URL}/resolutions/{ResolutionE2ETests.created_resolution_id}", json=updated_payload, timeout=10)
        self.assertEqual(response.status_code, 200, f"Expected status 200, got {response.status_code}. Response: {response.json()}")
        data = response.json()
        self.assertIn("message", data)
        self.assertIn("goal_id", data)
        # Router returns: "✋ Nice try! You thought you could change your resolution... but the blockchain gods said NO."
        self.assertIn("blockchain gods said NO", data["message"])
        print(f"Received immutable update response: {data['message']}")


if __name__ == "__main__":
    unittest.main()