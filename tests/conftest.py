import os
import sys
from unittest.mock import patch

import pytest

# Add the src directory to sys.path
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
)


@pytest.fixture
def mock_settings():
    """Fixture to provide mock settings"""
    return {
        "default": {
            "author": "Test Author",
            "theme": "monokai",
            "categories": ["General", "Developer", "Raspberry Pi"],
            "output_dir": "./output",
            "textarea_default_content": "# Default Content",
        }
    }


@pytest.fixture
def patch_settings(mock_settings):
    """Fixture to patch the Helper.get_settings method"""
    with patch("helper.Helper.get_settings", return_value=mock_settings):
        yield


@pytest.fixture
def mock_draft_content():
    """Fixture to provide mock draft content"""
    return {
        "title": "Test Draft",
        "author": "Draft Author",
        "date": "2023-01-01",
        "category": "Developer",
        "tags": "python,testing",
        "content": "# Draft Content\nThis is a draft article.",
        "filename": "test_draft.md.draft",
    }


@pytest.fixture
def patch_draft_content(mock_draft_content):
    """Fixture to patch the Helper.get_draft_file_content method"""
    with patch("helper.Helper.get_draft_file_content", return_value=mock_draft_content):
        yield


@pytest.fixture
def patch_no_draft_content():
    """Fixture to patch the Helper.get_draft_file_content method to return None"""
    with patch("helper.Helper.get_draft_file_content", return_value=None):
        yield
