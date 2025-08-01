from langchain.prompts import PromptTemplate

# Template for the prompt to ask whether two sentences have the same meaning
_about_same_meaning_template = """## Sentence A
```{sentence_a}```

## Sentence B
```{sentence_b}```

## Instruction
Please answer with 'yes' or 'no' whether Sentence A and Sentence B have kind of similar meanings.
if 'no' please write the reason why they are different.
Output only 'yes' or 'no'.

## Answer
"""

about_same_meaning_prompt = PromptTemplate(
    template=_about_same_meaning_template,
    input_variables=["sentence_a", "sentence_b"],
)
