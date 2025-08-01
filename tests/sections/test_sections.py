import json
import os

import pytest
from app.initializers.env import load_env

load_env()


@pytest.mark.asyncio
async def test_json_format():
    test_file = os.path.dirname(os.path.abspath(__file__)) + "/files/section.json"

    with open(test_file, "r", encoding="utf-8") as f:
        response_json = json.load(f)

    assert isinstance(response_json, dict), "Output is not a JSON object"
    assert "topics" in response_json, "Missing 'topics' field"

    for section in response_json["topics"]:
        assert "title" in section, "Missing 'title' in section"
        assert "content" in section, "Missing 'content' in section"
        assert "startTime" in section, "Missing 'startTime' in section"
        assert "subTopics" in section, "Missing 'subTopics' field in section"

        assert isinstance(section["title"], str), "Title should be a string"
        assert isinstance(section["content"], str), "Content should be a string"
        assert isinstance(section["startTime"], int), "startTime should be an integer"
        assert isinstance(section["subTopics"], list), "subTopics should be a list"

        for subtopic in section["subTopics"]:
            assert "subTitle" in subtopic, "Missing 'subTitle' in subtopic"
            assert "content" in subtopic, "Missing 'content' in subtopic"

            assert isinstance(subtopic["subTitle"], str), "subTitle should be a string"
            assert isinstance(
                subtopic["content"], str
            ), "Content in subtopic should be a string"

    print("JSON format and data types are correct.")
