import json
import yaml
import argparse
import os
import re
import concurrent.futures

from tqdm import tqdm

from utils import (
    load_questions,
    chat_completion_openai,
    chat_completion_openai_azure,
    chat_completion_anthropic,
    load_questions,
    load_model_answers,
    get_endpoint,
    make_config,
)


def get_score(judgment, pattern, pairwise=True):
    matches = pattern.findall(judgment)
    matches = [m for m in matches if m != ""]
    if len(set(matches)) == 0:
        return None, True
    elif len(set(matches)) == 1:
        if pairwise:
            return matches[0].strip("\n"), False
        return int(matches[0])
    else:
        return None, False


# get answer from model
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
    reference = args["reference"]
    baseline = args["baseline_answer"]
    configs = args["configs"]
    output_file = args["output_file"]
    model = configs["judge_model"]
    model_1 = args["model_1"]
    model_2 = args["model_2"]

    num_games = 2 if configs["pairwise"] else 1

    output = {
        "question_id": question["question_id"],
        "model_1": model_1,
        "model_2": model_2,
        "judge": model,
        "temperature": configs["temperature"],
        "games": []
    }

    for game in range(num_games):
        conv = [{"role": "system", "content": configs["system_prompt"]}]

        for template in configs["prompt_template"]:
            prompt_args = {}

            for i, turn in enumerate(question["turns"]):
                prompt_args[f"question_{i+1}"] = turn["content"]
            base = 1

            if baseline:
                if game % 2 == 1: # swap position
                    answer, baseline = baseline, answer

                for i, turn in enumerate(baseline["choices"][0]["turns"]):
                    prompt_args[f"answer_{i+1}"] = turn["content"]
                    base += 1
            if answer:
                for i, turn in enumerate(answer["choices"][0]["turns"]):
                    prompt_args[f"answer_{i+base}"] = turn["content"]

            if reference:
                prompt_args["ref_answer"] = reference

            user_prompt = template.format(**prompt_args)
            conv.append({"role": "user", "content": user_prompt})

        output["games"].append(conv)

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

    if configs["regex_pattern"]:
        pattern = re.compile(configs["regex_pattern"])

    models = [model for model in configs["model_list"]]

    question_file = os.path.join("data", configs["bench_name"], "question.jsonl")
    answer_dir = os.path.join("data", configs["bench_name"], "model_answer")
    ref_answer_dir = os.path.join("data", configs["bench_name"], "model_answer")

    questions = load_questions(question_file)
    model_answers = load_model_answers(answer_dir)
    # reference_answers = pd.read_json("datasets/final_dataser_filtered-v1.json")

    output_files = {}
    output_dir = f"data/{configs['bench_name']}/model_judgment/{configs['judge_model']}"
    # ---------------------------
    configs["pairwise"] = False
    count = 0
    for model_1 in models:
        for model_2 in models:
            if model_1 == model_2:
                continue

            output_files[f"{model_1}_{model_2}"] = os.path.join(
                output_dir,
                f"{model_1}_{model_2}.jsonl",
            )
            os.makedirs(os.path.dirname(output_files[f"{model_1}_{model_2}"]), exist_ok=True)
            endpoint_info = endpoint_list.get(configs["judge_model"])
            for question in questions:
                question_id = question["question_id"]
                kwargs = {}
                kwargs["question"] = question
                kwargs["model_1"] = model_1
                kwargs["model_2"] = model_2
                kwargs["answer"] = model_answers[model_1][question_id]
                kwargs["reference"] = None # reference_answers["model_answer"][question_id]
                kwargs["baseline_answer"] = model_answers[model_2][question_id]
                kwargs["configs"] = configs
                kwargs["endpoint_dict"] = endpoint_info
                kwargs["output_file"] = output_files[f"{model_1}_{model_2}"]
                kwargs["regex_pattern"] = pattern
                judgment(**kwargs)
