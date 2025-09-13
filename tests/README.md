# Tests for Frodown

This directory contains tests for the Frodown application.

## Running Tests

First, make sure you have installed the development dependencies:

```bash
# Using uv (recommended)
uv sync --extra dev
```

To run all tests:

```bash
uv run python -m pytest
```

To run a specific test file:

```bash
uv run python -m pytest tests/test_helper.py
```

To run a specific test function:

```bash
uv run python -m pytest tests/test_helper.py::TestHelper::test_get_settings_success
```

## Test Coverage

To generate a test coverage report:

```bash
uv run python -m pytest --cov=. --cov-report=term-missing
```
