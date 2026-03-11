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
    env_assets = decoder.get_environment_constants(job_definition)

    # Assert
    assert len(env_assets) == 1
    assert env_assets[0]["BLOB"] == "42"
