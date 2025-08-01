import json

import pytest

from app.core.llm import get_llm_info
from app.core.models.gen_ai import (
    ChatCompletionsRequest,
    FunctionToolRequest,
    MessageRequest,
    WebSearchToolRequest,
)
from app.services.completions.completion import stream


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "model",
    ["gpt-4o-mini", "o3-mini", "claude-3-7-sonnet-20250219"],
)
@pytest.mark.parametrize(
    "llm_type",
    ["openai", "azure"],
)
async def test_stream(model, llm_type) -> None:
    """streamメソッドのテスト"""
    # == arrange ==
    messages = [MessageRequest(role="user", content="こんにちは")]
    request = ChatCompletionsRequest(messages=messages, model=model, llm_type=llm_type)

    # == act ==
    response_generator = stream(request)
    responses: list[str] = []
    async for chunk in response_generator:
        responses.append(chunk)

    # == assert ==
    # レスポンスが1つ以上あることを確認
    assert len(responses) > 0

    content = ""
    for i, response in enumerate(responses):
        # 各レスポンスがSSE形式であることを確認
        assert response.startswith("event: message\ndata: ")

        # JSONデータを抽出して解析
        json_data = response.split("data: ")[1].strip()
        data = json.loads(json_data)

        # 出力を確認
        print(data)

        if data.get("content"):
            content += data["content"]

        # 最後のレスポンスには使用量情報が含まれている
        if i == len(responses) - 1:
            # usage
            assert "usage" in data
            assert "input_tokens" in data["usage"]
            assert "output_tokens" in data["usage"]
            assert "cache_read_input_tokens" in data["usage"]
            assert "cost" in data["usage"]

            # deprecated fields.
            assert "cost" in data
            assert "prompt_tokens" in data
            assert "completion_tokens" in data
            assert "model_name" in data

    # レスポンスの内容が空でないことを確認
    assert content != ""


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "model",
    ["gpt-4o-mini", "o3-mini", "claude-3-7-sonnet-20250219"],
)
@pytest.mark.parametrize(
    "llm_type",
    ["openai", "azure"],
)
async def test_stream_with_tools(model, llm_type) -> None:
    """toolsを指定した場合のstreamメソッドのテスト"""
    # == arrange ==
    messages = [MessageRequest(role="user", content="東京の天気を℃で教えて")]
    tools = [
        FunctionToolRequest(
            name="get_weather",
            description="現在の天気情報を取得する",
            arguments={
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "都市名または地域名",
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "description": "温度の単位",
                    },
                },
                "required": ["location"],
            },
        )
    ]
    request = ChatCompletionsRequest(
        messages=messages, model=model, llm_type=llm_type, tools=tools
    )

    # == act ==
    response_generator = stream(request)
    responses: list[str] = []
    async for chunk in response_generator:
        responses.append(chunk)

    # == assert ==
    # レスポンスが1つ以上あることを確認
    assert len(responses) > 0

    tool_calls_found = False
    name = ""
    argument = ""
    for response in responses:
        # 各レスポンスがSSE形式であることを確認
        assert response.startswith("event: message\ndata: ")

        # JSONデータを抽出して解析
        json_data = response.split("data: ")[1].strip()
        data = json.loads(json_data)

        # 出力を確認
        print(data)

        # tool_callsが含まれているかチェック
        if "tool_calls" in data and data["tool_calls"]:
            tool_calls_found = True
            # tool_callsの形式を確認
            tool_call = data["tool_calls"][0]
            if tool_call["name"]:
                name += tool_call["name"]
            if tool_call["arguments"]:
                argument += tool_call["arguments"]

    # tool_callsが正しく取得できていること
    assert tool_calls_found
    assert name == "get_weather"
    assert json.loads(argument) == json.loads('{"location":"東京","unit":"celsius"}')

    # 最後のレスポンスには使用量情報が含まれていること
    last_response = responses[-1]
    last_data = json.loads(last_response.split("data: ")[1].strip())
    # usage
    assert "usage" in last_data
    assert "input_tokens" in last_data["usage"]
    assert "output_tokens" in last_data["usage"]
    assert "cache_read_input_tokens" in last_data["usage"]
    assert "cost" in last_data["usage"]
    # deprecated fields.
    assert "cost" in last_data
    assert "prompt_tokens" in last_data
    assert "completion_tokens" in last_data
    assert "model_name" in last_data


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "model",
    ["gpt-4o-mini", "o3-mini"],
)
@pytest.mark.parametrize(
    "llm_type",
    ["openai"],
)
async def test_stream_with_web_search(model, llm_type) -> None:
    """streamメソッドのテスト"""
    # == arrange ==
    messages = [
        MessageRequest(
            role="user",
            content="東京の今日の天気を調べて",
        )
    ]
    request = ChatCompletionsRequest(
        messages=messages,
        model=model,
        llm_type=llm_type,
        web_search=WebSearchToolRequest(
            enabled=True,
            type="web_search_preview",
            user_location=None,
            search_context_size="medium",
        ),
    )

    # == act ==
    response_generator = stream(request)
    responses: list[str] = []
    async for chunk in response_generator:
        responses.append(chunk)

    # == assert ==
    # レスポンスが1つ以上あることを確認
    assert len(responses) > 0

    content = ""
    web_search_found = False
    for i, response in enumerate(responses):
        # 各レスポンスがSSE形式であることを確認
        assert response.startswith("event: message\ndata: ")

        # JSONデータを抽出して解析
        json_data = response.split("data: ")[1].strip()
        data = json.loads(json_data)

        # 出力を確認
        print(data)

        if data.get("content"):
            content += data["content"]

        if data.get("web_search"):
            web_search_found = True

        # 最後のレスポンスには使用量情報が含まれている
        if i == len(responses) - 1:
            # usage
            assert "usage" in data
            assert "input_tokens" in data["usage"]
            assert "output_tokens" in data["usage"]
            assert "cache_read_input_tokens" in data["usage"]
            assert "cost" in data["usage"]

            # deprecated fields.
            assert "cost" in data
            assert "prompt_tokens" in data
            assert "completion_tokens" in data
            assert "model_name" in data

    # レスポンスの内容が空でないことを確認
    assert content != ""

    model_info = get_llm_info(model)
    assert model_info is not None
    if model_info.web_search_enabled:
        # web_searchが正しく取得できていること
        assert web_search_found
