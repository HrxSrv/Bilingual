import os

import pytest
from app.services.clustering.handlers import clustering_async
from app.services.clustering.models.request import ClusteringRequest


@pytest.mark.asyncio
async def test_clustering():
    test_pairs = [
        (
            os.path.dirname(os.path.abspath(__file__)) + "/files/test1.txt",
            2,
        )
    ]
    for input_file, expected_output in test_pairs:
        with open(input_file, "r") as f:
            input = f.read()
            req = ClusteringRequest(
                text=input,
            )
            resp = await clustering_async(req)
            print(resp)
            assert len(resp.clusters) == expected_output
