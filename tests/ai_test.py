import sys
from unittest.mock import patch

import pytest

sys.path.insert(0, "../")

from frodown.helper import predice_ai_tags

# Constants used in the tests
TAG_TEMPLATE = "Some template string with {topic} and {title}"
OLLAMA_ENDPOINT = "http://fakeapi.com/endpoint"
OLLAMA_CONFIG = {"key": "value"}


# Mock response for the happy path
class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data

    def raise_for_status(self):
        pass  # To mimic the actual response behavior


# Test cases
@pytest.mark.parametrize(
    "test_id, category, title, expected, status_code, response_data",
    [
        # Happy path tests with various realistic test values
        (
            "happy-1",
            "Science",
            "The Quantum Mechanics",
            "Quantum,Physics",
            200,
            {"response": "Quantum,Physics\nMore text"},
        ),
        (
            "happy-2",
            "Technology",
            "Advances in AI",
            "AI,Machine Learning",
            200,
            {"response": "AI,Machine Learning\nAdditional info"},
        ),
        # Edge cases
        ("edge-1", "", "", "", 200, {"response": "\n"}),  # Empty strings as input
        (
            "edge-2",
            "Science",
            "A" * 1000,
            "LongTitle",
            200,
            {"response": "LongTitle\n"},
        ),  # Very long title
        # Error cases
        (
            "error-1",
            "Science",
            "The Quantum Mechanics",
            None,
            404,
            {"error": "Not Found"},
        ),  # Non-200 status code
        (
            "error-2",
            "Science",
            "The Quantum Mechanics",
            None,
            500,
            {"error": "Server Error"},
        ),  # Server error
    ],
)
def test_predice_ai_tags(
    test_id, category, title, expected, status_code, response_data
):
    with patch("helper.httpx.post") as mock_post:
        # Arrange
        mock_post.return_value = MockResponse(response_data, status_code)

        # Act
        result = predice_ai_tags(category, title)

        # Assert
        if status_code == 200:
            assert result == expected, (
                f"Test {test_id} failed: Expected {expected}, got {result}"
            )
        else:
            assert result is None, f"Test {test_id} failed: Expected None, got {result}"
