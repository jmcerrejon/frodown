import os
import sys
from unittest.mock import MagicMock, patch

import pytest

# Add the src directory to sys.path
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
)

from frodown.helper import Helper
from frodown.main import Frodown


class TestAIIntegration:
    @patch("frodown.helper.httpx.post")
    def test_predice_ai_tags_success(self, mock_post):
        # Arrange
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "response": "python,testing,markdown\nMore text"
        }
        mock_post.return_value = mock_response

        # Act
        result = Helper.predice_ai_tags("Developer", "Unit Testing with Pytest")

        # Assert
        assert result == "python,testing,markdown"
        mock_post.assert_called_once()

    @patch("frodown.helper.httpx.post")
    def test_predice_ai_tags_error(self, mock_post):
        # Arrange
        mock_post.side_effect = Exception("Connection error")

        # Act
        result = Helper.predice_ai_tags("Developer", "Unit Testing with Pytest")

        # Assert
        assert result is None

    @patch("frodown.helper.Helper.predice_ai_tags")
    def test_on_select_changed_with_ai_tags(self, mock_predice_ai_tags):
        # Arrange
        app = Frodown()
        app._category = MagicMock(value="Developer")
        app._title = MagicMock(value="Unit Testing with Pytest")
        app._tags = MagicMock(value="")
        event = MagicMock()
        mock_predice_ai_tags.return_value = "python,testing,pytest"

        # Act
        app.on_select_changed(event)

        # Assert
        assert app._tags.value == "python,testing,pytest"

    @patch("frodown.helper.Helper.predice_ai_tags")
    def test_on_select_changed_with_existing_tags(self, mock_predice_ai_tags):
        # Arrange
        app = Frodown()
        app._category = MagicMock(value="Developer")
        app._title = MagicMock(value="Unit Testing with Pytest")
        app._tags = MagicMock(value="existing,tags")
        event = MagicMock()

        # Act
        app.on_select_changed(event)

        # Assert
        mock_predice_ai_tags.assert_not_called()
        assert app._tags.value == "existing,tags"

    @patch("frodown.helper.Helper.predice_ai_tags")
    def test_on_select_changed_with_ai_error(self, mock_predice_ai_tags):
        # Arrange
        app = Frodown()
        app._category = MagicMock(value="Developer")
        app._title = MagicMock(value="Unit Testing with Pytest")
        app._tags = MagicMock(value="")
        event = MagicMock()
        mock_predice_ai_tags.return_value = None

        # Act
        app.on_select_changed(event)

        # Assert
        assert app._tags.value == ""
