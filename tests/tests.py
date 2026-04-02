"""Unit tests for the CaesarAI Blockchain API."""

from __future__ import annotations

import unittest

import requests

BASE_URL: str = "http://proofofresolution:8080"


class BlockchainEndpointTests(unittest.TestCase):
    """Integration tests for the /blockchain routes."""

    def test_mine_block_returns_no_error(self) -> None:
        response = requests.get(f"{BASE_URL}/blockchain/mine", timeout=10)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("index", data)
        self.assertIn("proof", data)
        self.assertIn("previous_hash", data)
        self.assertIn("message", data)

    def test_get_chain_returns_list(self) -> None:
        response = requests.get(f"{BASE_URL}/blockchain/chain", timeout=10)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("chain", data)
        self.assertIn("length", data)
        self.assertIsInstance(data["chain"], list)

    def test_valid_returns_validity(self) -> None:
        response = requests.get(f"{BASE_URL}/blockchain/valid", timeout=10)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("is_valid", data)
        self.assertIn("message", data)


class ResolutionEndpointTests(unittest.TestCase):
    """Integration tests for the /resolutions routes."""

    # Class variable to store the resolution ID created in test_create_resolution
    created_resolution_id: str = ""
    resolution_payload = {
        "title": "Test Resolution",
        "description": "This is a test resolution.",
        "category": "Testing"
    }

    @classmethod
    def setUpClass(cls):
        pass

    def test_1_create_resolution_success(self) -> None:
        """Test successfully creating a new resolution."""
        response = requests.post(f"{BASE_URL}/resolutions/", json=self.resolution_payload, timeout=30)
        self.assertEqual(response.status_code, 201, f"Expected status 201, got {response.status_code}. Response: {response.json()}")
        data = response.json()
        self.assertIn("goal_id", data)
        self.assertIn("resolution", data)
        self.assertIn("title", data["resolution"])
        self.assertEqual(data["resolution"]["title"], self.resolution_payload["title"])
        ResolutionEndpointTests.created_resolution_id = data["goal_id"]

    def test_2_get_all_resolutions(self) -> None:
        """Test retrieving all resolutions and confirming the newly created resolution is present."""
        self.assertTrue(ResolutionEndpointTests.created_resolution_id, "Resolution ID should be set from creation test")
        response = requests.get(f"{BASE_URL}/resolutions/", timeout=10)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("resolutions", data)
        self.assertIsInstance(data["resolutions"], list)

        found = any(
            r.get("goal_id") == ResolutionEndpointTests.created_resolution_id
            for r in data["resolutions"]
        )
        self.assertTrue(found, "Newly created resolution not found in the list of all resolutions.")

    def test_3_get_specific_resolution_by_id(self) -> None:
        """Test retrieving the specific resolution by its ID."""
        self.assertTrue(ResolutionEndpointTests.created_resolution_id, "Resolution ID should be set from creation test")
        response = requests.get(f"{BASE_URL}/resolutions/{ResolutionEndpointTests.created_resolution_id}", timeout=10)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("resolution", data)
        self.assertEqual(data["resolution"]["goal_id"], ResolutionEndpointTests.created_resolution_id)
        self.assertEqual(data["resolution"]["title"], self.resolution_payload["title"])

    def test_4_attempt_delete_resolution_returns_immutable_response(self) -> None:
        """Test attempting to delete the resolution returns the immutable blockchain response."""
        self.assertTrue(ResolutionEndpointTests.created_resolution_id, "Resolution ID should be set from creation test")
        response = requests.delete(f"{BASE_URL}/resolutions/{ResolutionEndpointTests.created_resolution_id}", timeout=10)
        self.assertEqual(response.status_code, 200, f"Expected status 200, got {response.status_code}. Response: {response.json()}")
        data = response.json()
        self.assertIn("message", data)
        self.assertIn("goal_id", data)
        # Router returns: "🔒 Nice try! The blockchain never forgets – and neither do we."
        self.assertIn("blockchain never forgets", data["message"])

    def test_5_attempt_update_resolution_returns_immutable_response(self) -> None:
        """Test attempting to update the resolution returns the immutable blockchain response."""
        self.assertTrue(ResolutionEndpointTests.created_resolution_id, "Resolution ID should be set from creation test")
        updated_payload = {"title": "Updated Test Resolution", "description": "Updated description."}
        response = requests.put(f"{BASE_URL}/resolutions/{ResolutionEndpointTests.created_resolution_id}", json=updated_payload, timeout=10)
        self.assertEqual(response.status_code, 200, f"Expected status 200, got {response.status_code}. Response: {response.json()}")
        data = response.json()
        self.assertIn("message", data)
        self.assertIn("goal_id", data)
        # Router returns: "✋ Nice try! You thought you could change your resolution... but the blockchain gods said NO."
        self.assertIn("blockchain gods said NO", data["message"])


if __name__ == "__main__":
    unittest.main()