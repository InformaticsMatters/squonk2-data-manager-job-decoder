# Tests for the schema validator.
from typing import Any, Dict
from copy import deepcopy

import pytest

pytestmark = pytest.mark.unit

from decoder import decoder

# A minimal Job Definition.
# Tests can use this and adjust accordingly.
_MINIMAL: Dict[str, Any] = {
    "kind": "DataManagerJobDefinition",
    "kind-version": "2021.1",
    "collection": "test",
    "jobs": {
        "demo": {
            "version": "1.0.0",
            "name": "test",
            "image": {
                "name": "blob",
                "tag": "1.0.0",
                "project-directory": "/data",
                "working-directory": "/data",
                "fix-permissions": True,
            },
            "command": "sys.exit(1)",
        }
    },
}


def test_validate_minimal():
    # Arrange

    # Act
    error = decoder.validate_job_schema(_MINIMAL)

    # Assert
    assert error is None


def test_validate_image_env_from_api_token():
    # Arrange
    text: Dict[str, Any] = deepcopy(_MINIMAL)
    demo_job: Dict[str, Any] = text["jobs"]["demo"]
    demo_job["image"]["environment"] = [
        {"name": "ENV_VAR", "value-from": {"api-token": {"roles": ["abc"]}}}
    ]

    # Act
    error = decoder.validate_job_schema(text)

    # Assert
    assert error is None


def test_validate_image_env_from_constant():
    # Arrange
    text: Dict[str, Any] = deepcopy(_MINIMAL)
    demo_job: Dict[str, Any] = text["jobs"]["demo"]
    demo_job["image"]["environment"] = [
        {"name": "ENV_VAR", "value-from": {"constant": {"value": "123"}}}
    ]

    # Act
    error = decoder.validate_job_schema(text)

    # Assert
    assert error is None


def test_validate_image_env_from_secret():
    # Arrange
    text: Dict[str, Any] = deepcopy(_MINIMAL)
    demo_job: Dict[str, Any] = text["jobs"]["demo"]
    demo_job["image"]["environment"] = [
        {
            "name": "ENV_VAR",
            "value-from": {"secret": {"name": "secret-a", "key": "secret"}},
        }
    ]

    # Act
    error = decoder.validate_job_schema(text)

    # Assert
    assert error is None


def test_validate_image_env_from_account_server_asset():
    # Arrange
    text: Dict[str, Any] = deepcopy(_MINIMAL)
    demo_job: Dict[str, Any] = text["jobs"]["demo"]
    demo_job["image"]["environment"] = [
        {
            "name": "ENV_VAR",
            "value-from": {"account-server-asset": {"name": "asset-a"}},
        }
    ]

    # Act
    error = decoder.validate_job_schema(text)

    # Assert
    assert error is None


def test_validate_image_file_from_account_server_asset():
    # Arrange
    text: Dict[str, Any] = deepcopy(_MINIMAL)
    demo_job: Dict[str, Any] = text["jobs"]["demo"]
    demo_job["image"]["file"] = [
        {
            "name": "/usr/local/licence.txt",
            "content-from": {"account-server-asset": {"name": "asset-a"}},
        }
    ]

    # Act
    error = decoder.validate_job_schema(text)

    # Assert
    assert error is None


def test_validate_image_memory_32gi():
    # Arrange
    text: Dict[str, Any] = deepcopy(_MINIMAL)
    demo_job: Dict[str, Any] = text["jobs"]["demo"]
    demo_job["image"]["memory"] = "32Gi"

    # Act
    error = decoder.validate_job_schema(text)

    # Assert
    assert error is None


def test_validate_image_memory_100mi():
    # Arrange
    text: Dict[str, Any] = deepcopy(_MINIMAL)
    demo_job: Dict[str, Any] = text["jobs"]["demo"]
    demo_job["image"]["memory"] = "100Mi"

    # Act
    error = decoder.validate_job_schema(text)

    # Assert
    assert error is None


def test_validate_image_cores_1():
    # Arrange
    text: Dict[str, Any] = deepcopy(_MINIMAL)
    demo_job: Dict[str, Any] = text["jobs"]["demo"]
    demo_job["image"]["cores"] = 1

    # Act
    error = decoder.validate_job_schema(text)

    # Assert
    assert error is None


def test_validate_image_cores_32():
    # Arrange
    text: Dict[str, Any] = deepcopy(_MINIMAL)
    demo_job: Dict[str, Any] = text["jobs"]["demo"]
    demo_job["image"]["cores"] = 32

    # Act
    error = decoder.validate_job_schema(text)

    # Assert
    assert error is None


def test_validate_two_basic_tests():
    # Arrange
    text: Dict[str, Any] = deepcopy(_MINIMAL)
    demo_job: Dict[str, Any] = text["jobs"]["demo"]
    demo_job["tests"] = {
        "basic-1": {"run-level": 1, "ignore": None},
        "basic-2": {
            "run-level": 100,
            "timeout-minutes": 30,
            "inputs": {"files": ["blob-1.txt", "blob-2.txt"]},
            "options": {"param-1": 32, "param-2": "a"},
            "environment": ["ENV_1", "ENV_2"],
            "checks": {
                "exitCode": 0,
                "outputs": [
                    {
                        "name": "blob.txt",
                        "checks": [{"exists": True}, {"lineCount": 100}],
                    }
                ],
            },
        },
    }

    # Act
    error = decoder.validate_job_schema(text)

    # Assert
    assert error is None
