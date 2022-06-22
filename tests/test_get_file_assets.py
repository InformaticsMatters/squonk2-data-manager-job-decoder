# Tests for the decoder's get_job_doc_url() function.
from typing import Dict

import pytest

pytestmark = pytest.mark.unit

from decoder import decoder


def test_get_file_assets():
    # Arrange
    job_definition: Dict = {
        "image": {
            "environment": [
                {
                    "name": "BLOB",
                    "value-from": {"account-server-asset": {"name": "asset-a"}},
                }
            ],
            "file": [
                {
                    "name": "/tmp/blob-1.txt",
                    "content-from": {"account-server-asset": {"name": "asset-a"}},
                },
                {
                    "name": "/tmp/blob-2.txt",
                    "content-from": {"account-server-asset": {"name": "asset-b"}},
                },
            ],
        },
    }

    # Act
    file_assets = decoder.get_file_assets(job_definition)

    # Assert
    assert len(file_assets) == 2
    print(file_assets)
    for file_asset in file_assets:
        if file_asset["image-file"] == "/tmp/blob-1.txt":
            assert file_asset["asset"] == "asset-a"
        elif file_asset["image-file"] == "/tmp/blob-2.txt":
            assert file_asset["asset"] == "asset-b"
        else:
            # How did we get here?
            assert False
