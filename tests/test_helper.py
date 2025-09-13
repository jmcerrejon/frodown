import datetime
import os
import subprocess
import sys
from unittest.mock import MagicMock, mock_open, patch

import pytest

# Add the src directory to sys.path to import the helper module
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
)

from frodown.helper import Helper


class TestHelper:
    @patch("frodown.helper.tomli.load")
    @patch("builtins.open", new_callable=mock_open)
    def test_get_settings_success(self, mock_file, mock_tomli_load):
        # Arrange
        expected_settings = {"default": {"author": "Test Author"}}
        mock_tomli_load.return_value = expected_settings

        # Act
        result = Helper.get_settings()

        # Assert
        mock_file.assert_called_once_with("settings.toml", mode="rb")
        assert result == expected_settings

    @patch("builtins.open")
    def test_get_settings_file_not_found(self, mock_file):
        # Arrange
        mock_file.side_effect = FileNotFoundError()

        # Act & Assert
        with pytest.raises(SystemExit) as excinfo:
            Helper.get_settings()
        assert "settings.toml not found." in str(excinfo.value)

    @patch("frodown.helper.tomli.load")
    @patch("builtins.open", new_callable=mock_open)
    def test_get_settings_key_error(self, mock_file, mock_tomli_load):
        # Arrange
        mock_tomli_load.side_effect = KeyError()

        # Act
        result = Helper.get_settings()

        # Assert
        assert result == ""

    @patch("frodown.helper.tomli.load")
    @patch("builtins.open", new_callable=mock_open)
    def test_get_settings_exception(self, mock_file, mock_tomli_load):
        # Arrange
        mock_tomli_load.side_effect = Exception()

        # Act & Assert
        with pytest.raises(SystemExit) as excinfo:
            Helper.get_settings()
        assert "settings.toml does not have the correct format." in str(excinfo.value)

    def test_get_cheat_sheet(self):
        # Act
        result = Helper.get_cheat_sheet()

        # Assert
        assert isinstance(result, str)
        assert "::: important Custom important" in result
        assert "::: info Custom info" in result

    @pytest.mark.parametrize(
        "category, expected_icon",
        [
            ("General", "fa-regular fa-newspaper"),
            ("Raspberry Pi", "fa-brands fa-raspberry-pi"),
            ("Developer", "fa-solid fa-code"),
            ("Apple", "fa-brands fa-apple"),
            ("Linux", "fa-brands fa-linux"),
            ("Android", "fa-brands fa-android"),
            ("Arduino", "fa-brands fa-arduino"),
            ("Atomic Pi", "fa-solid fa-microchip"),
            ("Banana Pi", "fa-solid fa-ban"),
            ("ODROID", "fa-solid fa-microchip"),
            ("Orange Pi", "fa-solid fa-microchip"),
            ("Unknown Category", "fa-regular fa-newspaper"),  # Default icon
        ],
    )
    def test_get_icon_by_category(self, category, expected_icon):
        # Act
        result = Helper.get_icon_by_category(category)

        # Assert
        assert result == expected_icon

    @patch("os.listdir")
    @patch("builtins.open", new_callable=mock_open)
    def test_get_draft_file_content_no_draft(self, mock_file, mock_listdir):
        # Arrange
        mock_listdir.return_value = ["file1.txt", "file2.md"]

        # Act
        result = Helper.get_draft_file_content()

        # Assert
        assert result is None

    @patch("os.listdir")
    @patch("builtins.open")
    def test_get_draft_file_content_with_draft(self, mock_open, mock_listdir):
        # Arrange
        mock_listdir.return_value = ["test_article.md.draft"]
        mock_file_content = """---
title: Test Article
icon: fa-solid fa-code
author: Test Author
date: 2023-01-01
category:
  - Developer
tags:
  - python, testing
---
# Test Content
This is a test article.
"""
        mock_open.return_value.__enter__.return_value.readlines.return_value = (
            mock_file_content.split("\n")
        )

        # Act
        result = Helper.get_draft_file_content()

        # Assert
        assert result is not None
        assert result["title"] == "Test Article"
        assert result["author"] == "Test Author"
        assert result["date"] == "2023-01-01"
        assert result["category"] == "Developer"
        assert "python, testing" in result["tags"]
        assert result["filename"] == "test_article.md.draft"

    @patch("os.path.exists")
    @patch("builtins.open", new_callable=mock_open)
    def test_save_file(self, mock_file, mock_exists):
        # Arrange
        mock_exists.return_value = False

        # Create a mock app with the required attributes
        mock_app = MagicMock()
        mock_app._title = MagicMock(value="Test Article")
        mock_app._author = MagicMock(value="Test Author")
        mock_app._date = MagicMock(value="2023-01-01")
        mock_app._category = MagicMock(value="Developer")
        mock_app._tags = MagicMock(value="python,testing")
        mock_app._textarea = MagicMock(text="# Test Content\nThis is a test article.")
        mock_app.format_tags = lambda tags: "\n  -".join(tags.split(","))

        # Act
        result = Helper.save_file(mock_app, output_directory="./", is_draft=False)

        # Assert
        assert result == "./test_article.md"
        mock_file.assert_called_once_with("./test_article.md", "w")
        mock_file().write.assert_any_call("---\n")
        mock_file().write.assert_any_call("# Test Content\nThis is a test article.")

    @patch("subprocess.check_output")
    def test_get_vscode_path_success(self, mock_check_output):
        # Arrange
        mock_check_output.return_value = b"/usr/bin/code\n"

        # Act
        result = Helper.get_vscode_path()

        # Assert
        assert result == "/usr/bin/code\n"

    @patch("subprocess.check_output")
    def test_get_vscode_path_failure(self, mock_check_output):
        # Arrange
        mock_check_output.side_effect = subprocess.CalledProcessError(1, "which code")

        # Act
        result = Helper.get_vscode_path()

        # Assert
        assert result is False

    @patch("subprocess.check_call")
    def test_open_vscode_success(self, mock_check_call):
        # Arrange
        directory = "/test/directory"

        # Act
        with patch("builtins.print") as mock_print:
            Helper.open_vscode(directory)

        # Assert
        mock_check_call.assert_called_once_with(["code", directory])
        mock_print.assert_called_once_with(f"VSCode opened at {directory}")

    @patch("subprocess.check_call")
    def test_open_vscode_failure(self, mock_check_call):
        # Arrange
        directory = "/test/directory"
        mock_check_call.side_effect = subprocess.CalledProcessError(1, "code")

        # Act
        with patch("builtins.print") as mock_print:
            Helper.open_vscode(directory)

        # Assert
        mock_print.assert_called_once_with("Failed to open VSCode")

    @patch("builtins.open", new_callable=mock_open)
    def test_read_markdown_file(self, mock_file):
        # Arrange
        mock_file.return_value.__enter__.return_value.readlines.return_value = [
            "# Line 1\n",
            "Line 2\n",
            "Line 3\n",
            "Line 4\n",
            "Line 5\n",
        ]

        # Act
        result = Helper.read_markdown_file("test.md", 2, 4)

        # Assert
        assert result == "Line 2\nLine 3\nLine 4\n"
