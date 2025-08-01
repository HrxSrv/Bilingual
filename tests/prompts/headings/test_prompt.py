import os

from app.core.chains import ChainManager
from app.initializers.env import load_env
from app.services.clustering.templates import header_stream_prompt
from tests.utils import normalize_answer
from tests.utils.template import about_same_meaning_prompt

load_env()


def test_headings_prompt():
    cm = ChainManager(llm_type="openai", output_language="japanese")
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
        "n": 1,
        "top_p": 1,
        # "frequency_penalty": 0.8,
        # "presence_penalty": 0.8,
    }
    retry = 2
    for input_file, expected_outputs in test_pairs:
        valid = False
        for _ in range(retry):
            with open(input_file, "r") as f:
                inputs = {
                    "transcript": f.read(),
                    "part": "",
                    "output_language": "japanese",
                }
                output = cm.run(inputs=inputs, pt=header_stream_prompt, params=params)

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
        assert valid, f"Assertion failed: {output} not in {expected_output}, {answer}"
