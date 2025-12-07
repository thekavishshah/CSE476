#!/usr/bin/env python3
"""
Generate a placeholder answer file that matches the expected auto-grader format.

Replace the placeholder logic inside `build_answers()` with your own agent loop
before submitting so the ``output`` fields contain your real predictions.

Reads the input questions from cse_476_final_project_test_data.json and writes
an answers JSON file where each entry contains a string under the "output" key.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List
import os
import requests


INPUT_PATH = Path("cse_476_final_project_test_data.json")
OUTPUT_PATH = Path("cse_476_final_project_answers.json")

API_KEY = os.getenv("OPENAI_API_KEY", "cse476")
API_BASE = os.getenv("API_BASE", "http://10.4.58.53:41701/v1")
MODEL = os.getenv("MODEL_NAME", "bens_model")

def load_questions(path: Path) -> List[Dict[str, Any]]:
    with path.open("r") as fp:
        data = json.load(fp)
    if not isinstance(data, list):
        raise ValueError("Input file must contain a list of question objects.")
    return data

def make_answer_short(x: str) -> str:
    x = x.strip()
    if not x:
        return x
    y = [p.strip() for p in x.splitlines() if p.strip()]
    if y:
        return y[-1]
    return x

def model_call(a: str) -> str:
    b = API_BASE + "/chat/completions"
    c = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    d = {"model": MODEL, "messages": [{"role": "system","content": "You MUST reply with ONLY the final answer for the question. Do NOT include steps, explanations, or plans. Your reply must be a single short answer string only.",},
        {"role": "user", "content": a,},],"temperature": 0.0, "max_tokens": 64,}
    e = requests.post(b, headers=c, json=d, timeout=60)
    if e.status_code != 200:
        return ""
    f = e.json()
    g = f.get("choices", [{}])[0].get("message", {}).get("content", "")
    g = (g or "").strip()
    g = make_answer_short(g)
    return g

def build_answers(questions: List[Dict[str, Any]]) -> List[Dict[str, str]]:
    answers = []
    for idx, question in enumerate(questions, start=1):
        # Example: assume you have an agent loop that produces an answer string.
        # real_answer = agent_loop(question["input"])
        # answers.append({"output": real_answer})
        a=question.get("input","")
        a = str(a)
        placeholder_answer = model_call(a)
        if not placeholder_answer:
            placeholder_answer = "Error"
        answers.append({"output": placeholder_answer})
        print(idx)
    return answers


def validate_results(
    questions: List[Dict[str, Any]], answers: List[Dict[str, Any]]
) -> None:
    if len(questions) != len(answers):
        raise ValueError(
            f"Mismatched lengths: {len(questions)} questions vs {len(answers)} answers."
        )
    for idx, answer in enumerate(answers):
        if "output" not in answer:
            raise ValueError(f"Missing 'output' field for answer index {idx}.")
        if not isinstance(answer["output"], str):
            raise TypeError(
                f"Answer at index {idx} has non-string output: {type(answer['output'])}"
            )
        if len(answer["output"]) >= 5000:
            raise ValueError(
                f"Answer at index {idx} exceeds 5000 characters "
                f"({len(answer['output'])} chars). Please make sure your answer does not include any intermediate results."
            )


def main() -> None:
    questions = load_questions(INPUT_PATH)
    answers = build_answers(questions)

    with OUTPUT_PATH.open("w") as fp:
        json.dump(answers, fp, ensure_ascii=False, indent=2)

    with OUTPUT_PATH.open("r") as fp:
        saved_answers = json.load(fp)
    validate_results(questions, saved_answers)
    print(
        f"Wrote {len(answers)} answers to {OUTPUT_PATH} "
        "and validated format successfully."
    )


if __name__ == "__main__":
    main()