def normalize_answer(r: str) -> str:
    return r.lower().strip().replace(".", "")
