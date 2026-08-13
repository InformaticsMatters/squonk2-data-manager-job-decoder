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


def _job_with_output_annotations(
    annotation_properties: Dict[str, Any]
) -> Dict[str, Any]:
    """A copy of the minimal Job Definition whose single output variable
    carries the given annotation properties.
    """
    text: Dict[str, Any] = deepcopy(_MINIMAL)
    demo_job: Dict[str, Any] = text["jobs"]["demo"]
    demo_job["variables"] = {
        "outputs": {
            "type": "object",
            "properties": {
                "outputFile": {
                    "title": "Output file",
                    "creates": "{{ outputFile }}",
                    "type": "file",
                    "annotation-properties": annotation_properties,
                }
            },
        }
    }
    return text


def _job_with_option_items(items: Dict[str, Any]) -> Dict[str, Any]:
    """A copy of the minimal Job Definition whose single (array) option
    variable is built from the given 'items' sub-schema.
    """
    text: Dict[str, Any] = deepcopy(_MINIMAL)
    demo_job: Dict[str, Any] = text["jobs"]["demo"]
    demo_job["variables"] = {
        "options": {
            "type": "object",
            "properties": {
                "properties": {
                    "title": "Properties",
                    "type": "array",
                    "items": items,
                }
            },
        }
    }
    return text


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


def test_validate_image_cores_99():
    # Arrange
    text: Dict[str, Any] = deepcopy(_MINIMAL)
    demo_job: Dict[str, Any] = text["jobs"]["demo"]
    demo_job["image"]["cores"] = 99

    # Act
    error = decoder.validate_job_schema(text)

    # Assert
    assert error is None


def test_validate_image_cores_10m():
    # Arrange
    text: Dict[str, Any] = deepcopy(_MINIMAL)
    demo_job: Dict[str, Any] = text["jobs"]["demo"]
    demo_job["image"]["cores"] = "10m"

    # Act
    error = decoder.validate_job_schema(text)

    # Assert
    assert error is None


def test_validate_image_cores_1500m():
    # Arrange
    text: Dict[str, Any] = deepcopy(_MINIMAL)
    demo_job: Dict[str, Any] = text["jobs"]["demo"]
    demo_job["image"]["cores"] = "1500m"

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


def test_validate_test_option_array():
    # Arrange
    text: Dict[str, Any] = deepcopy(_MINIMAL)
    demo_job: Dict[str, Any] = text["jobs"]["demo"]
    demo_job["tests"] = {
        "option-array": {
            "options": {"param-array": ["a", "b"]},
        },
    }

    # Act
    error = decoder.validate_job_schema(text)

    # Assert
    assert error is None


def test_validate_test_groups():
    # Arrange
    text: Dict[str, Any] = deepcopy(_MINIMAL)
    text["test-groups"] = [{"name": "demo-1"}, {"name": "demo-2"}]

    # Act
    error = decoder.validate_job_schema(text)

    # Assert
    assert error is None


def test_validate_test_groups_with_environment():
    # Arrange
    text: Dict[str, Any] = deepcopy(_MINIMAL)
    text["test-groups"] = [
        {
            "name": "demo-1",
            "environment": [{"ENV_A": "1"}, {"ENV_B": 2}, {"ENV_C": True}],
        }
    ]

    # Act
    error = decoder.validate_job_schema(text)

    # Assert
    assert error is None


def test_validate_test_groups_with_compose():
    # Arrange
    text: Dict[str, Any] = deepcopy(_MINIMAL)
    text["test-groups"] = [
        {"name": "demo-1", "compose": {"file": "docker-compose-abc.yaml"}}
    ]

    # Act
    error = decoder.validate_job_schema(text)

    # Assert
    assert error is None


def test_validate_test_groups_with_compose_delay():
    # Arrange
    text: Dict[str, Any] = deepcopy(_MINIMAL)
    text["test-groups"] = [
        {
            "name": "demo-1",
            "compose": {"file": "docker-compose-abc.yaml", "delay-seconds": 10},
        }
    ]

    # Act
    error = decoder.validate_job_schema(text)

    # Assert
    assert error is None


def test_validate_test_run_groups():
    # Arrange
    text: Dict[str, Any] = deepcopy(_MINIMAL)
    demo_job: Dict[str, Any] = text["jobs"]["demo"]
    demo_job["tests"] = {
        "basic-1": {
            "run-groups": [
                {"name": "demo-1", "ordinal": 1},
                {"name": "demo-2", "ordinal": 1},
            ],
        },
    }

    # Act
    error = decoder.validate_job_schema(text)

    # Assert
    assert error is None


def test_validate_test_run_groups_without_ordinal():
    # Arrange
    text: Dict[str, Any] = deepcopy(_MINIMAL)
    demo_job: Dict[str, Any] = text["jobs"]["demo"]
    demo_job["tests"] = {
        "basic-1": {
            "run-groups": [{"name": "demo-1"}, {"name": "demo-2"}],
        },
    }

    # Act
    error = decoder.validate_job_schema(text)

    # Assert
    assert error == "'ordinal' is a required property"


def test_validate_replaces():
    text: Dict[str, Any] = deepcopy(_MINIMAL)
    demo_job: Dict[str, Any] = text["jobs"]["demo"]
    demo_job["replaces"] = [{"collection": "test-collection", "job": "test-job"}]

    # Act
    error = decoder.validate_job_schema(text)

    # Assert
    assert error is None


# Output variable annotation properties.
#
# Only three annotations are recognised: 'fields-descriptor', 'derived-from'
# and 'service-execution'. The tests below record every combination, and every
# field shape, found in the Job Definitions we publish.


def test_validate_annotation_properties_fields_descriptor():
    # Arrange
    text: Dict[str, Any] = _job_with_output_annotations(
        {
            "fields-descriptor": {
                "origin": "squonk2-job",
                "description": "Something",
                "fields": {
                    "smiles": {"type": "string", "description": "Molecule"},
                },
            }
        }
    )

    # Act
    error = decoder.validate_job_schema(text)

    # Assert
    assert error is None


def test_validate_annotation_properties_derived_from():
    # Arrange
    text: Dict[str, Any] = _job_with_output_annotations({"derived-from": "inputFile"})

    # Act
    error = decoder.validate_job_schema(text)

    # Assert
    assert error is None


def test_validate_annotation_properties_derived_from_and_fields_descriptor():
    # Arrange
    text: Dict[str, Any] = _job_with_output_annotations(
        {
            "derived-from": "inputFile",
            "fields-descriptor": {
                "origin": "squonk2-job",
                "description": "Something",
                "fields": {
                    "smiles": {"type": "string", "description": "Molecule"},
                },
            },
        }
    )

    # Act
    error = decoder.validate_job_schema(text)

    # Assert
    assert error is None


def test_validate_annotation_properties_with_service_execution():
    # Arrange
    text: Dict[str, Any] = _job_with_output_annotations(
        {
            "derived-from": "inputFile",
            "fields-descriptor": {
                "origin": "squonk2-job",
                "description": "Something",
                "fields": {
                    "smiles": {"type": "string", "description": "Molecule"},
                },
            },
            "service-execution": {"service_ref": "https://example.com/service"},
        }
    )

    # Act
    error = decoder.validate_job_schema(text)

    # Assert
    assert error is None


def test_validate_annotation_properties_fields_descriptor_without_fields():
    # Arrange
    text: Dict[str, Any] = _job_with_output_annotations(
        {"fields-descriptor": {"origin": "squonk2-job", "description": "Something"}}
    )

    # Act
    error = decoder.validate_job_schema(text)

    # Assert
    assert error is None


def test_validate_annotation_properties_all_observed_field_shapes():
    # Arrange
    text: Dict[str, Any] = _job_with_output_annotations(
        {
            "fields-descriptor": {
                "origin": "squonk2-job",
                "description": "Something",
                "fields": {
                    "a": {"type": "string", "description": "A"},
                    "b": {"type": "string", "description": "B", "required": True},
                    "c": {
                        "type": "string",
                        "description": "C",
                        "required": True,
                        "active": True,
                    },
                    "d": {
                        "type": "number",
                        "description": "D",
                        "expression": "1 + 1",
                    },
                    "e": {
                        "type": "number",
                        "description": "E",
                        "required": False,
                        "expression": "1 + 1",
                    },
                    "f": {
                        "type": "number",
                        "description": "F",
                        "required": False,
                        "active": False,
                        "expression": "1 + 1",
                    },
                },
            }
        }
    )

    # Act
    error = decoder.validate_job_schema(text)

    # Assert
    assert error is None


def test_validate_annotation_properties_rejects_unknown_annotation():
    # Arrange
    text: Dict[str, Any] = _job_with_output_annotations({"derived-form": "inputFile"})

    # Act
    error = decoder.validate_job_schema(text)

    # Assert
    assert error is not None


def test_validate_annotation_properties_rejects_misplaced_derived_from():
    # Arrange
    # 'derived-from' belongs beside 'fields-descriptor', not inside it.
    text: Dict[str, Any] = _job_with_output_annotations(
        {
            "fields-descriptor": {
                "origin": "squonk2-job",
                "description": "Something",
                "derived-from": "inputFile",
                "fields": {
                    "smiles": {"type": "string", "description": "Molecule"},
                },
            }
        }
    )

    # Act
    error = decoder.validate_job_schema(text)

    # Assert
    assert error is not None


def test_validate_annotation_properties_rejects_unknown_field_property():
    # Arrange
    text: Dict[str, Any] = _job_with_output_annotations(
        {
            "fields-descriptor": {
                "origin": "squonk2-job",
                "description": "Something",
                "fields": {
                    "smiles": {
                        "type": "string",
                        "description": "Molecule",
                        "requried": True,
                    },
                },
            }
        }
    )

    # Act
    error = decoder.validate_job_schema(text)

    # Assert
    assert error is not None


def test_validate_annotation_properties_rejects_non_string_derived_from():
    # Arrange
    text: Dict[str, Any] = _job_with_output_annotations({"derived-from": ["inputFile"]})

    # Act
    error = decoder.validate_job_schema(text)

    # Assert
    assert error is not None


def test_validate_annotation_properties_rejects_fields_descriptor_without_origin():
    # Arrange
    text: Dict[str, Any] = _job_with_output_annotations(
        {"fields-descriptor": {"description": "Something"}}
    )

    # Act
    error = decoder.validate_job_schema(text)

    # Assert
    assert error is not None


# Option variable 'items'.
#
# 'items' is the JSON-Schema sub-schema for an array-typed option,
# not a free-form object.


def test_validate_option_items_type_only():
    # Arrange
    text: Dict[str, Any] = _job_with_option_items({"type": "string"})

    # Act
    error = decoder.validate_job_schema(text)

    # Assert
    assert error is None


def test_validate_option_items_one_of():
    # Arrange
    text: Dict[str, Any] = _job_with_option_items(
        {
            "type": "string",
            "oneOf": [
                {"const": "atom-count", "title": "Atom count"},
                {"const": "ring-count", "title": "Ring count"},
            ],
        }
    )

    # Act
    error = decoder.validate_job_schema(text)

    # Assert
    assert error is None


def test_validate_option_items_any_of():
    # Arrange
    text: Dict[str, Any] = _job_with_option_items(
        {
            "title": "Model ID",
            "type": "string",
            "anyOf": [
                {"type": "string", "enum": ["herg"], "title": "hERG model"},
                {"type": "string", "enum": ["AMES"], "title": "AMES model"},
            ],
        }
    )

    # Act
    error = decoder.validate_job_schema(text)

    # Assert
    assert error is None


def test_validate_option_items_rejects_unknown_property():
    # Arrange
    text: Dict[str, Any] = _job_with_option_items(
        {"type": "string", "one-of": [{"const": "atom-count"}]}
    )

    # Act
    error = decoder.validate_job_schema(text)

    # Assert
    assert error is not None


def test_validate_option_items_rejects_unknown_choice_property():
    # Arrange
    text: Dict[str, Any] = _job_with_option_items(
        {"type": "string", "oneOf": [{"const": "atom-count", "titel": "Atom count"}]}
    )

    # Act
    error = decoder.validate_job_schema(text)

    # Assert
    assert error is not None
