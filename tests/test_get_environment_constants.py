# Tests for the decoder's get_environment_assets() function.
from typing import Dict

import pytest

pytestmark = pytest.mark.unit

from decoder import decoder


def test_get_environment_constants():
    # Arrange
    job_definition: Dict = {
        "image": {
            "environment": [
                {
                    "name": "BLOB",
                    "value-from": {"constant": {"value": "42"}},
                }
            ],
        },
    }

    # Act
    env_constants = decoder.get_environment_constants(job_definition)

    # Assert
    assert len(env_constants) == 1
    assert "BLOB" in env_constants
    assert env_constants["BLOB"] == "42"
