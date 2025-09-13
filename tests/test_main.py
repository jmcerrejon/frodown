import datetime
import os
import sys
from unittest.mock import MagicMock, PropertyMock, patch

import pytest

# Add the src directory to sys.path to import the main module
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
)

from frodown.main import ExtendedTextArea, Frodown, Message, OptionGroup, Sidebar, Title


class TestExtendedTextArea:
    def test_change_text(self):
        # Arrange
        textarea = ExtendedTextArea()
        event = MagicMock()
        event.character = "("

        # Mock the insert and move_cursor_relative methods
        textarea.insert = MagicMock()
        textarea.move_cursor_relative = MagicMock()

        # Act
        textarea._change_text(
            event, text="(", insert_text="()", move_cursor_relative=-1
        )

        # Assert
        textarea.insert.assert_called_once_with("()")
        textarea.move_cursor_relative.assert_called_once_with(columns=-1)
        event.prevent_default.assert_called_once()

    def test_on_blur(self):
        # Arrange
        textarea = ExtendedTextArea()
        event = MagicMock()

        # Act
        textarea._on_blur(event)

        # Assert
        assert textarea.tab_behavior == "indent"

    def test_on_key_parenthesis(self):
        # Arrange
        textarea = ExtendedTextArea()
        event = MagicMock()
        event.character = "("

        # Mock the methods
        textarea.insert = MagicMock()
        textarea.move_cursor_relative = MagicMock()

        # Act
        textarea._on_key(event)

        # Assert
        textarea.insert.assert_called_once_with("()")
        textarea.move_cursor_relative.assert_called_once_with(columns=-1)
        event.prevent_default.assert_called_once()

    def test_on_key_exclamation_at_start_of_line(self):
        # Arrange
        textarea = ExtendedTextArea()
        event = MagicMock()
        event.character = "!"

        # Mock properties and methods
        with patch.object(
            type(textarea), "cursor_at_start_of_line", new_callable=PropertyMock
        ) as mock_cursor:
            mock_cursor.return_value = True
            with patch.object(textarea, "insert") as mock_insert:
                with patch.object(textarea, "move_cursor_relative") as mock_move:
                    # Act
                    textarea._on_key(event)

                    # Assert
                    mock_insert.assert_called_once_with('![alt]("alt")')
                    mock_move.assert_called_once_with(columns=-6)
                    event.prevent_default.assert_called_once()

    def test_on_key_tab_at_last_line(self):
        # Arrange
        textarea = ExtendedTextArea()
        event = MagicMock()
        event.key = "tab"

        # Mock properties
        with patch.object(
            type(textarea), "cursor_at_last_line", new_callable=PropertyMock
        ) as mock_cursor:
            mock_cursor.return_value = True
            # Act
            textarea._on_key(event)

            # Assert
            assert textarea.tab_behavior == "focus"


class TestFrodown:
    @patch("frodown.main.Helper.get_settings")
    @patch("frodown.main.Helper.get_draft_file_content")
    def test_get_field_values_with_draft(self, mock_get_draft, mock_get_settings):
        # Arrange
        app = Frodown()
        mock_get_settings.return_value = {"default": {"author": "Default Author"}}
        mock_draft = {
            "title": "Draft Title",
            "author": "Draft Author",
            "date": "2023-01-01",
            "category": "Draft Category",
            "tags": "draft,tags",
            "content": "Draft Content",
            "filename": "draft.md.draft",
        }
        mock_get_draft.return_value = mock_draft

        # Act
        result = app.get_field_values()

        # Assert
        assert result["title"] == "Draft Title"
        assert result["author"] == "Draft Author"
        assert result["date"] == "2023-01-01"
        assert result["category"] == "Draft Category"
        assert result["tags"] == "draft,tags"
        assert result["content"] == "Draft Content"
        assert result["is_default_values"] is False
        assert result["filename"] == "draft.md.draft"

    @patch("frodown.main.Helper.get_settings")
    @patch("frodown.main.Helper.get_draft_file_content")
    def test_get_field_values_no_draft(self, mock_get_draft, mock_get_settings):
        # Arrange
        app = Frodown()
        mock_get_settings.return_value = {
            "default": {
                "author": "Default Author",
                "textarea_default_content": "Default Content",
            }
        }
        mock_get_draft.return_value = None

        # Act
        with patch("frodown.main.datetime") as mock_datetime:
            mock_datetime.date.today.return_value = datetime.date(2023, 1, 1)
            result = app.get_field_values()

        # Assert
        assert result["title"] == ""
        assert result["author"] == "Default Author"
        assert result["date"] == "2023-01-01"
        assert result["category"] == "General"
        assert result["tags"] == ""
        assert result["content"] == "Default Content"
        assert result["is_default_values"] is True
        assert result["filename"] is None

    def test_form_has_change_with_changes(self):
        # Arrange
        app = Frodown()
        app.get_field_values = MagicMock(
            return_value={
                "title": "Original Title",
                "author": "Original Author",
                "date": "2023-01-01",
                "category": "Original Category",
                "tags": "original,tags",
                "content": "Original Content",
            }
        )
        app._title = MagicMock(value="Changed Title")
        app._author = MagicMock(value="Original Author")
        app._date = MagicMock(value="2023-01-01")
        app._category = MagicMock(value="Original Category")
        app._tags = MagicMock(value="original,tags")
        app._textarea = MagicMock(text="Original Content")

        # Act
        result = app.form_has_change()

        # Assert
        assert result is True

    def test_form_has_change_no_changes(self):
        # Arrange
        app = Frodown()
        app.get_field_values = MagicMock(
            return_value={
                "title": "Original Title",
                "author": "Original Author",
                "date": "2023-01-01",
                "category": "Original Category",
                "tags": "original,tags",
                "content": "Original Content",
            }
        )
        app._title = MagicMock(value="Original Title")
        app._author = MagicMock(value="Original Author")
        app._date = MagicMock(value="2023-01-01")
        app._category = MagicMock(value="Original Category")
        app._tags = MagicMock(value="original,tags")
        app._textarea = MagicMock(text="Original Content")

        # Act
        result = app.form_has_change()

        # Assert
        assert result is False

    def test_format_tags(self):
        # Arrange
        app = Frodown()
        tags = "python,testing,markdown"

        # Act
        result = app.format_tags(tags)

        # Assert
        assert result == "python\n  -testing\n  -markdown"


class TestSidebar:
    @patch("frodown.main.Helper.get_cheat_sheet")
    def test_sidebar_compose(self, mock_get_cheat_sheet):
        # Arrange
        sidebar = Sidebar()
        mock_get_cheat_sheet.return_value = "Cheat Sheet Content"

        # Act
        result = list(sidebar.compose())

        # Assert
        assert len(result) == 2
        assert isinstance(result[0], Title)
        assert isinstance(result[1], OptionGroup)
