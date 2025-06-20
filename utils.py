import os
import json
import time
import yaml
import random
import requests

from typing import Optional
from glob import glob
from local_client import LocalClient
from contextlib import contextmanager

@contextmanager
def no_proxy():
    original_http_proxy = os.environ.pop('http_proxy', None)
    original_https_proxy = os.environ.pop('https_proxy', None)
    try:
        yield
    finally:
        if original_http_proxy is not None:
            os.environ['http_proxy'] = original_http_proxy
        if original_https_proxy is not None:
            os.environ['https_proxy'] = original_https_proxy

def log_message(message):
    if len(message) > 150:
        print(f"{time.time()}: {message[:100]}...{message[-20:]}")
    else:
        print(f"{time.time()}: {message}")

def log_error(e):
    print(f"{time.time()}: {type(e)}: {e}")

# API setting constants
API_MAX_RETRY = 16
API_RETRY_SLEEP = 10
API_ERROR_OUTPUT = "$ERROR$"


OPENAI_MODEL_LIST = (
    "gpt-3.5-turbo",
    "gpt-3.5-turbo-0301",
    "gpt-3.5-turbo-0613",
    "gpt-3.5-turbo-0613-verbose",
    "gpt-3.5-turbo-1106",
    "gpt-3.5-turbo-0125",
    "gpt-4",
    "gpt-4-0314",
    "gpt-4-0613",
    "gpt-4-turbo",
    "gpt-4-1106-preview",
    "gpt-4-0125-preview",
)


temperature_config = {
    "writing": 0.7,
    "roleplay": 0.7,
    "extraction": 0.0,
    "math": 0.0,
    "coding": 0.0,
    "reasoning": 0.0,
    "stem": 0.1,
    "humanities": 0.1,
}


def load_questions(question_file: str):
    """Load questions from a file."""
    questions = []
    with open(question_file, "r") as ques_file:
        for line in ques_file:
            if line:
                questions.append(json.loads(line))
    return questions


def load_model_answers(answer_dir: str):
    """Load model answers.

    The return value is a python dict of type:
    Dict[model_name: str -> Dict[question_id: int -> answer: dict]]
    """
    filenames = glob(os.path.join(answer_dir, "*.jsonl"))
    filenames.sort()
    model_answers = {}

    for filename in filenames:
        model_name = os.path.basename(filename)[:-6]
        answer = {}
        with open(filename) as fin:
            for line in fin:
                line = json.loads(line)
                answer[line["question_id"]] = line
        model_answers[model_name] = answer

    return model_answers


def get_endpoint(endpoint_list):
    if not endpoint_list:
        return None
    assert endpoint_list is not None
    # randomly pick one
    api_dict = random.choices(
        endpoint_list
    )[0]
    return api_dict


# load config args from config yaml files
def make_config(config_file: str) -> dict:
    config_kwargs = {}
    with open(config_file, "r") as f:
        config_kwargs = yaml.load(f, Loader=yaml.SafeLoader)

    return config_kwargs

# load output srtucture in either json or yson format
def load_structure_file(file_path):
    _, file_extension = os.path.splitext(file_path)
    if file_extension.lower() == '.json':
        with open(file_path, 'r') as file:
            return json.load(file)

    if file_extension.lower() == '.yaml':
        with open(file_path, 'rb') as file:
            return yaml.load(file, Loader=yaml.SafeLoader)

    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except json.JSONDecodeError:
        pass
    try:
        with open(file_path, 'rb') as file:
            return yaml.load(file, Loader=yaml.SafeLoader)
    except yaml.YsonError:
        pass
    raise RuntimeError(f"Failed to parse the structure file: {file_path}. Ensure it is valid JSON or YAML.")

def chat_completion_local(model: str, messages, temperature: float, max_tokens: int, api_dict=None):
    client = LocalClient(
        model=model,
        options=api_dict,
    )
    output = API_ERROR_OUTPUT
    for _ in range(API_MAX_RETRY):
        try:
            output = client.run(
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            break
        except client.RateLimitError as e:
            log_error(e)
            time.sleep(API_RETRY_SLEEP)
        except client.BadRequestError as e:
            log_error(e)
        except KeyError:
            log_error(e)
            break

    return output

def chat_completion_openai(model, messages, temperature, max_tokens, api_dict=None, response_format=None):
    import openai
    if api_dict:
        client = openai.OpenAI(
            base_url=api_dict["api_base"],
            api_key=api_dict["api_key"],
        )
    else:
        client = openai.OpenAI()

    chat_completion_args = {
        "model" : model,
        "messages" : messages,
        "temperature" : temperature,
        "max_tokens" : max_tokens
    }

    if response_format is not None:
        chat_completion_args["extra_body"] = {"guided_json": response_format}

    def parse_completion(completion):
        if completion.choices is not None:
            choice = completion.choices[0]
        else:
            if hasattr(completion.response, 'choices'):
                choice = completion.response.choices[0]
            else:
                choice = completion.response["choices"][0]

        if hasattr(choice, 'message'):
            message = choice.message
        elif isinstance(choice, dict) and 'message' in choice:
            message = choice['message']
        else:
            raise TypeError(f"Unexpected choice structure: {choice}")

        if hasattr(message, 'content'):
            content = message.content
        elif isinstance(message, dict) and 'content' in message:
            content = message['content']
        else:
            raise TypeError(f"Unexpected choice structure: {choice}")
        return content

    content = API_ERROR_OUTPUT
    for _ in range(API_MAX_RETRY):
        completion = None
        try:
            completion = client.chat.completions.create(**chat_completion_args)
            content = parse_completion(completion)
            break
        except openai.RateLimitError as e:
            log_error(e)
            time.sleep(API_RETRY_SLEEP)
        except openai.BadRequestError as e:
            log_message(f"Bad request, messages: {messages}")
            log_error(e)
        except KeyError:
            print(type(e), e, completion)
            break
        except Exception as e:
            try:
                models = client.models.list()
                log_message(f"Api Client got available models: {models}, however something went wrong for {model}")
            except:
                log_message(f"Api Client unreachable")
            log_error(e)
            print(f"Received completion: {completion}")
            raise
    return content


def chat_completion_openai_azure(model, messages, temperature, max_tokens, api_dict=None):
    import openai
    from openai import AzureOpenAI

    api_base = api_dict["api_base"]
    client = AzureOpenAI(
        azure_endpoint = api_base,
        api_key= api_dict["api_key"],
        api_version=api_dict["api_version"],
        timeout=240,
        max_retries=2
    )

    output = API_ERROR_OUTPUT
    for _ in range(API_MAX_RETRY):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                n=1,
                temperature=temperature,
                max_tokens=max_tokens,
                seed=42,
            )
            output = response.choices[0].message.content
            break
        except openai.RateLimitError as e:
            log_error(e)
            time.sleep(API_RETRY_SLEEP)
        except openai.BadRequestError as e:
            log_error(e)
            break
        except KeyError:
            log_error(e)
            break

    return output


def chat_completion_anthropic(model, messages, temperature, max_tokens, api_dict=None):
    import anthropic

    if api_dict:
        api_key = api_dict["api_key"]
    else:
        api_key = os.environ["ANTHROPIC_API_KEY"]

    sys_msg = ""
    if messages[0]["role"] == "system":
        sys_msg = messages[0]["content"]
        messages = messages[1:]

    output = API_ERROR_OUTPUT
    for _ in range(API_MAX_RETRY):
        try:
            c = anthropic.Anthropic(api_key=api_key)
            response = c.messages.create(
                model=model,
                messages=messages,
                stop_sequences=[anthropic.HUMAN_PROMPT],
                max_tokens=max_tokens,
                temperature=temperature,
                system=sys_msg
            )
            output = response.content[0].text
            break
        except anthropic.APIError as e:
            log_error(e)
            time.sleep(API_RETRY_SLEEP)
    return output


def chat_completion_mistral(model, messages, temperature, max_tokens):
    from mistralai.client import MistralClient
    from mistralai.models.chat_completion import ChatMessage
    from mistralai.exceptions import MistralException

    api_key = os.environ["MISTRAL_API_KEY"]
    client = MistralClient(api_key=api_key)

    prompts = [ChatMessage(role=message["role"], content=message["content"]) for message in messages]
    
    output = API_ERROR_OUTPUT
    for _ in range(API_MAX_RETRY):
        try:
            chat_response = client.chat(
                model=model,
                messages=prompts,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            output = chat_response.choices[0].message.content
            break
        except MistralException as e:
            log_error(e)
            break

    return output


def http_completion_gemini(model, message, temperature, max_tokens):
    api_key = os.environ["GEMINI_API_KEY"]
    
    safety_settings = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_NONE"
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_NONE"
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_NONE"
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_NONE"
        },
    ]

    output = API_ERROR_OUTPUT
    try:
        response = requests.post(
            f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}",
            json={
                "contents": [{
                    "parts":[
                        {"text": message}
                    ]
                }],
                "safetySettings": safety_settings,
                "generationConfig":{
                    "temperature": temperature,
                    "maxOutputTokens": max_tokens,
                }
            },
        )
    except Exception as e:
        print(f"**API REQUEST ERROR** Reason: {e}.")

    if response.status_code != 200:
        print(f"**API REQUEST ERROR** Reason: status code {response.status_code}.")

    output = response.json()["candidates"][0]["content"]["parts"][0]["text"]

    return output


def chat_completion_cohere(model, messages, temperature, max_tokens):
    import cohere

    co = cohere.Client(os.environ["COHERE_API_KEY"])
    assert len(messages) > 0

    template_map = {"system":"SYSTEM",
                    "assistant":"CHATBOT",
                    "user":"USER"}

    assert messages[-1]["role"] == "user"
    prompt = messages[-1]["content"]

    if len(messages) > 1:
        history = []
        for message in messages[:-1]:
            history.append({"role":template_map[message["role"]], "message":message["content"]})
    else:
        history = None

    output = API_ERROR_OUTPUT
    for _ in range(API_MAX_RETRY):
        try:
            response = co.chat(
                message=prompt,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
                chat_history=history,
            )
            output = response.text
            break
        except cohere.core.api_error.ApiError as e:
            log_error(e)
            raise
        except Exception as e:
            log_error(e)
            break
    
    return output


def reorg_answer_file(answer_file):
    """Sort by question id and de-duplication"""
    answers = {}
    with open(answer_file, "r") as fin:
        for l in fin:
            qid = json.loads(l)["question_id"]
            answers[qid] = l

    qids = sorted(list(answers.keys()))
    with open(answer_file, "w") as fout:
        for qid in qids:
            fout.write(answers[qid])
