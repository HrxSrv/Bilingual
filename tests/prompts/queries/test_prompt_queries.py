import json
import os

import pytest

from app.core.chains import ChainManager
from app.initializers.env import load_env
from app.services.prompt_executor import prompt_execute_async
from app.services.prompt_executor.models import PromptRequest
from tests.utils import normalize_answer
from tests.utils.template import about_same_meaning_prompt

load_env()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "model",
    ["gpt-4o-mini", "claude-3-7-sonnet-20250219"],
)
@pytest.mark.parametrize(
    "llm_type",
    ["openai", "azure"],
)
async def test_prompt_queries(model: str, llm_type: str):
    cm = ChainManager(model_name=model, llm_type=llm_type, output_language="japanese")
    test_pairs = [
        (
            os.path.dirname(os.path.abspath(__file__)) + "/files/test1.txt",
            [
                "社員旅行のブレスト会議",
                "副業組織の社員旅行のブレスト会議",
                "社員旅行の候補地についてのブレスト会議",
                "副業組織の社員旅行に関するブレインストーミング会議記録",
            ],
        )
    ]
    params = {
        "temperature": 0,
        "top_p": 1,
        "n": 1,
        # "frequency_penalty": 0.8,
        # "presence_penalty": 0.8,
    }
    retry = 2
    for input_file, expected_outputs in test_pairs:
        valid = False
        for _ in range(retry):
            with open(input_file, "r") as f:
                req = PromptRequest(
                    input_text=f.read(),
                    prompt_query_type="instructAI",
                    user_prompt="この文字起こし結果に表題をつけてください",
                )
                output = ""
                async for v in prompt_execute_async(req):
                    message = json.loads(v)
                    output += message.get("content", "")

            for expected_output in expected_outputs:
                evaluation_inputs = {
                    "sentence_a": output,
                    "sentence_b": expected_output,
                }
                answer = cm.run(
                    inputs=evaluation_inputs,
                    pt=about_same_meaning_prompt,
                    params=params,
                )
                valid = normalize_answer(answer) == "yes" or output == expected_output
                if valid:
                    break
                print("output not expected", output, expected_output, answer)
            if valid:
                break
            print("retrying...")
        assert valid, f"Assertion failed: {output} not in {expected_outputs}, {answer}"
