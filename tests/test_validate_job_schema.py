# Tests for the schema validator.
from typing import Any, Dict

import pytest
pytestmark = pytest.mark.unit

from decoder import decoder


def test_validate_minimal():
    # Arrange
    text: Dict[str, Any] = {
        'kind': 'DataManagerJobDefinition',
        'kind-version': '2021.1',
        'collection': 'test',
        'repository-url': 'https://example.com',
        'repository-tag': '1.0.0',
        'jobs': {'demo': {'version': '1.0.0',
                          'name': 'test',
                          'image': {'name': 'blob',
                                    'tag': '1.0.0',
                                    'project-directory': '/data'},
                          'command': 'sys.exit(1)'}}}

    # Act
    error = decoder.validate_job_schema(text)

    # Assert
    assert error is None
