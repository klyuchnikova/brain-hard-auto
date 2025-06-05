import json
import yaml
import argparse
import os
import re
from tqdm import tqdm

from utils import (
    load_questions,
    chat_completion_openai,
    chat_completion_openai_azure,
    chat_completion_anthropic,
    load_model_answers,
    get_endpoint,
    make_config,
)


def get_score(judgment, pattern):
    matches = pattern.findall(judgment)
    matches = [m for m in matches if m != ""]
    if len(set(matches)) == 0:
        return None, True
    elif len(set(matches)) == 1:
        return int(matches[0])
    else:
        return None, False


def get_answer(model, conv, temperature, max_tokens, endpoint_dict=None):
    api_dict = get_endpoint(endpoint_dict["endpoints"])

    if endpoint_dict["api_type"] == "anthropic":
        output = chat_completion_anthropic(model, conv, temperature, max_tokens)
    elif endpoint_dict["api_type"] == "azure":
        output = chat_completion_openai_azure(model, conv, temperature, max_tokens, api_dict)
    else:
        output = chat_completion_openai(model, conv, temperature, max_tokens, api_dict)
    return output


def judgment(**args):
    question = args["question"]
    answer = args["answer"]
    baseline = args["baseline_answer"] if args["baseline"] else None
    configs = args["configs"]
    output_file = args["output_file"]
    model = configs["judge_model"]
    current_model = args["current_model"]

    output = {
        "question_id": question["question_id"],
        "model": current_model,
        "judge": model,
        "temperature": configs["temperature"],
        "conv": []
    }

    conv = [{"role": "system", "content": configs["system_prompt"]}]

    for template in configs["prompt_template"]:
        prompt_args = {
            "question": "\n".join([turn["content"] for turn in question["turns"]]),
            "answer": "\n".join([turn["content"] for turn in answer["choices"][0]["turns"]]),
            "aspects": ", ".join(question.get("aspects", []))
        }

        if baseline:
            prompt_args["baseline"] = "\n".join([turn["content"] for turn in baseline["choices"][0]["turns"]])

        user_prompt = template.format(**prompt_args)
        conv.append({"role": "user", "content": user_prompt})

    output["conv"] = conv

    with open(output_file, "a") as f:
        f.write(json.dumps(output, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--setting-file", type=str, default="config/judge_config.yaml")
    parser.add_argument("--endpoint-file", type=str, default="config/api_config.yaml")
    args = parser.parse_args()
    print(args)

    configs = make_config(args.setting_file)
    endpoint_list = make_config(args.endpoint_file)

    if configs.get("regex_pattern"):
        pattern = re.compile(configs["regex_pattern"])

    models = [model for model in configs["model_list"]]

    questions = load_questions(configs["question_file"])
    answer_dir = os.path.join("data", configs["bench_name"], "model_answer")
    model_answers = load_model_answers(answer_dir)

    # Create single output file
    output_dir = f"data/{configs['bench_name']}/model_judgment"
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f"{configs['judge_model']}_judgment_questions.jsonl")

    # Clear existing file if it exists
    if os.path.exists(output_file):
        os.remove(output_file)

    endpoint_info = endpoint_list.get(configs["judge_model"])

    for model in tqdm(models, desc="Processing models"):
        for question in tqdm(questions, desc=f"Processing questions for {model}", leave=False):
            question_id = question["question_id"]
            kwargs = {
                "question": question,
                "current_model": model,
                "answer": model_answers[model][question_id],
                "baseline": configs["baseline"],
                "baseline_answer": model_answers[configs["baseline_model"]][question_id] if configs["baseline"] else None,
                "configs": configs,
                "endpoint_dict": endpoint_info,
                "output_file": output_file,
            }
            if configs.get("regex_pattern"):
                kwargs["regex_pattern"] = pattern
            judgment(**kwargs)