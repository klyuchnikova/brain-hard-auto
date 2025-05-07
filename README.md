# Brain-Hard-Auto

This work is a version of Arena-Hard-Auto-v0.1 ([See Paper](https://arxiv.org/abs/2406.11939)) which is an automatic evaluation tool for instruction-tuned LLMs. It contains 500 challenging user queries sourced from Chatbot Arena. They promptrf GPT-4-Turbo as judge to compare the models' responses against a baseline model (default: GPT-4-0314). Notably, Arena-Hard-Auto has the highest correlation and separability to Chatbot Arena among popular open-ended LLM benchmarks ([See Paper](https://arxiv.org/abs/2406.11939)).

## Content
- [Style Control Leaderboard](#style-control-leaderboard)
- [Leaderboard](#leaderboard)
- [Install](#install-dependencies)
- [Evaluation](#evaluate)
- [Style Control: how to mitigate biases](#style-control)
- [Evaluate Benchmarks: how to evaluate benchmarks](#evaluate-benchmarks)
- [Citation](#citation)

## Style Control Leaderboard
Following the newly introduced Style Control on Chatbot Arena, we release Style Control on Arena Hard Auto! We employ the same Style Control methods as proposed in the [blogpost](https://lmsys.org/blog/2024-08-28-style-control/). Please refer to the blogpost for methodology and technical background. 

(Updated: 11/14)
```console
Llama-3.3-Nemotron-Super-49B-v1-Feedback-Edit-ITS | score: 88.7  | 95% CI: (-2.3, 2.2)  | average #tokens: 1217
claude-3-5-sonnet-20241022                        | score: 86.4  | 95% CI: (-1.3, 1.3)  | average #tokens: 691
claude-3-5-sonnet-20240620                        | score: 82.2  | 95% CI: (-1.9, 1.6)  | average #tokens: 567
o1-preview-2024-09-12                             | score: 81.7  | 95% CI: (-2.2, 2.1)  | average #tokens: 1193
o1-mini-2024-09-12                                | score: 79.3  | 95% CI: (-2.8, 2.3)  | average #tokens: 1399
gpt-4-turbo-2024-04-09                            | score: 74.3  | 95% CI: (-2.4, 2.4)  | average #tokens: 662
gpt-4-0125-preview                                | score: 73.6  | 95% CI: (-2.0, 2.0)  | average #tokens: 619
athene-v2-chat                                    | score: 72.1  | 95% CI: (-2.5, 2.5)  | average #tokens: 884
gpt-4o-2024-08-06                                 | score: 71.1  | 95% CI: (-2.5, 2.0)  | average #tokens: 594
llama-3.1-nemotron-70b-instruct                   | score: 71.0  | 95% CI: (-2.8, 3.1)  | average #tokens: 869
gpt-4o-2024-05-13                                 | score: 69.9  | 95% CI: (-2.5, 2.0)  | average #tokens: 696
athene-70b-0725                                   | score: 68.3  | 95% CI: (-2.6, 2.4)  | average #tokens: 683
llama-3.1-405b-instruct-fp8                       | score: 67.1  | 95% CI: (-2.2, 2.8)  | average #tokens: 658
yi-lightning                                      | score: 66.9  | 95% CI: (-3.3, 2.7)  | average #tokens: 875
claude-3-opus-20240229                            | score: 65.5  | 95% CI: (-2.3, 2.2)  | average #tokens: 541
yi-large-preview                                  | score: 65.1  | 95% CI: (-2.5, 2.5)  | average #tokens: 720
gpt-4o-mini-2024-07-18                            | score: 64.0  | 95% CI: (-3.5, 2.9)  | average #tokens: 668
qwen2.5-72b-instruct                              | score: 63.3  | 95% CI: (-2.5, 2.3)  | average #tokens: 821
mistral-large-2407                                | score: 63.1  | 95% CI: (-3.0, 2.6)  | average #tokens: 623
gemini-1.5-pro-api-0514                           | score: 62.7  | 95% CI: (-3.2, 3.0)  | average #tokens: 676
glm-4-0520                                        | score: 61.4  | 95% CI: (-2.6, 2.4)  | average #tokens: 636
yi-large                                          | score: 59.4  | 95% CI: (-2.8, 2.5)  | average #tokens: 626
deepseek-coder-v2                                 | score: 58.3  | 95% CI: (-2.8, 2.6)  | average #tokens: 578
glm-4-0116                                        | score: 54.2  | 95% CI: (-2.2, 2.2)  | average #tokens: 622
llama-3.1-70b-instruct                            | score: 51.8  | 95% CI: (-3.4, 2.1)  | average #tokens: 628
glm-4-air                                         | score: 50.6  | 95% CI: (-2.6, 2.4)  | average #tokens: 619
gpt-4-0314                                        | score: 50.0  | 95% CI:  (0.0, 0.0)  | average #tokens: 423                   
claude-3-sonnet-20240229                          | score: 49.9  | 95% CI: (-2.7, 2.4)  | average #tokens: 552                   
gpt-4-0613                                        | score: 49.7  | 95% CI: (-2.3, 2.5)  | average #tokens: 354
qwen2-72b-instruct                                | score: 49.6  | 95% CI: (-2.1, 2.2)  | average #tokens: 515
gemma-2-27b-it                                    | score: 47.5  | 95% CI: (-2.5, 2.7)  | average #tokens: 577
gemini-1.5-pro-api-0409-preview                   | score: 46.7  | 95% CI: (-2.6, 3.1)  | average #tokens: 478
mistral-large-2402                                | score: 45.6  | 95% CI: (-2.1, 2.3)  | average #tokens: 400
claude-3-haiku-20240307                           | score: 45.4  | 95% CI: (-2.5, 2.7)  | average #tokens: 505
llama-3-70b-instruct                              | score: 44.5  | 95% CI: (-2.4, 2.0)  | average #tokens: 591
mixtral-8x22b-instruct-v0.1                       | score: 44.2  | 95% CI: (-2.7, 3.1)  | average #tokens: 430
gemini-1.5-flash-api-0514                         | score: 39.9  | 95% CI: (-2.5, 2.1)  | average #tokens: 642
llama-3.1-nemotron-51b-instruct                   | score: 39.9  | 95% CI: (-2.9, 2.7)  | average #tokens: 747
qwen1.5-72b-chat                                  | score: 39.9  | 95% CI: (-2.1, 2.4)  | average #tokens: 474
mistral-next                                      | score: 39.6  | 95% CI: (-2.4, 2.7)  | average #tokens: 297
mistral-medium                                    | score: 39.1  | 95% CI: (-2.4, 2.8)  | average #tokens: 485
phi-3-medium-4k-instruct                          | score: 38.8  | 95% CI: (-2.5, 2.7)  | average #tokens: 517
command-r-plus                                    | score: 37.5  | 95% CI: (-2.4, 2.3)  | average #tokens: 541
claude-2.0                                        | score: 36.6  | 95% CI: (-3.0, 3.0)  | average #tokens: 295
claude-2.1                                        | score: 35.0  | 95% CI: (-2.6, 2.3)  | average #tokens: 290
gpt-3.5-turbo-0613                                | score: 34.9  | 95% CI: (-2.4, 2.9)  | average #tokens: 401
gpt-3.5-turbo-0125                                | score: 34.6  | 95% CI: (-2.3, 2.6)  | average #tokens: 329
phi-3-small-8k-instruct                           | score: 33.8  | 95% CI: (-2.4, 1.9)  | average #tokens: 568
gemma-2-9b-it                                     | score: 33.6  | 95% CI: (-2.3, 2.2)  | average #tokens: 541
gpt-3.5-turbo-1106                                | score: 32.9  | 95% CI: (-3.7, 2.4)  | average #tokens: 285
dbrx-instruct-preview                             | score: 32.0  | 95% CI: (-2.5, 2.4)  | average #tokens: 415
internlm2-20b-5-chat                              | score: 30.4  | 95% CI: (-2.2, 2.6)  | average #tokens: 576
mixtral-8x7b-instruct-v0.1                        | score: 29.8  | 95% CI: (-2.3, 2.2)  | average #tokens: 457
gpt-3.5-turbo-0314                                | score: 29.4  | 95% CI: (-2.5, 3.0)  | average #tokens: 334
starling-lm-7b-beta                               | score: 26.1  | 95% CI: (-2.6, 2.0)  | average #tokens: 530
snowflake-arctic-instruct                         | score: 25.8  | 95% CI: (-2.3, 2.1)  | average #tokens: 365
gemini-pro                                        | score: 24.9  | 95% CI: (-1.8, 2.5)  | average #tokens: 322
command-r                                         | score: 23.3  | 95% CI: (-1.9, 2.0)  | average #tokens: 432
snorkel-mistral-pairrm-dpo                        | score: 21.9  | 95% CI: (-1.6, 1.9)  | average #tokens: 564
yi-34b-chat                                       | score: 21.9  | 95% CI: (-1.5, 2.2)  | average #tokens: 611
internlm2-20b-chat                                | score: 21.3  | 95% CI: (-2.1, 1.8)  | average #tokens: 667
llama-3-8b-instruct                               | score: 19.8  | 95% CI: (-1.6, 1.9)  | average #tokens: 585
llama-3.1-8b-instruct                             | score: 18.3  | 95% CI: (-1.6, 1.6)  | average #tokens: 861
tulu-2-dpo-70b                                    | score: 18.0  | 95% CI: (-1.9, 2.4)  | average #tokens: 550
starling-lm-7b-alpha                              | score: 16.4  | 95% CI: (-1.4, 1.5)  | average #tokens: 483
phi-3-mini-128k-instruct                          | score: 16.1  | 95% CI: (-1.5, 1.6)  | average #tokens: 609
mistral-7b-instruct                               | score: 15.2  | 95% CI: (-1.6, 2.0)  | average #tokens: 541
llama-2-70b-chat                                  | score: 13.4  | 95% CI: (-1.5, 1.8)  | average #tokens: 595
vicuna-33b                                        | score: 11.8  | 95% CI: (-1.8, 1.3)  | average #tokens: 451
gemma-1.1-7b-it                                   | score: 11.5  | 95% CI: (-1.5, 1.3)  | average #tokens: 341
gemma-7b-it                                       | score:  7.1  | 95% CI: (-1.3, 1.2)  | average #tokens: 378
gemma-1.1-2b-it                                   | score:  3.5  | 95% CI: (-0.5, 0.8)  | average #tokens: 316
gemma-2b-it                                       | score:  2.9  | 95% CI: (-0.6, 0.7)  | average #tokens: 369
```

# Leaderboard
The following leaderboard has no style control.

(Updated: 11/14)
```console
Llama-3.3-Nemotron-Super-49B-v1-Feedback-Edit-ITS | score: 93.4  | 95% CI: (-1.1, 1.0)  | average #tokens: 1217
o1-mini-2024-09-12                                | score: 92.0  | 95% CI: (-1.2, 1.0)  | average #tokens: 1399
o1-preview-2024-09-12                             | score: 90.4  | 95% CI: (-1.1, 1.3)  | average #tokens: 1193
claude-3-5-sonnet-20241022                        | score: 85.2  | 95% CI: (-1.4, 1.6)  | average #tokens: 691
athene-v2-chat                                    | score: 85.0  | 95% CI: (-1.4, 1.7)  | average #tokens: 884
llama-3.1-nemotron-70b-instruct                   | score: 84.9  | 95% CI: (-1.7, 1.8)  | average #tokens: 869
gpt-4-turbo-2024-04-09                            | score: 82.6  | 95% CI: (-1.8, 1.5)  | average #tokens: 662
yi-lightning                                      | score: 81.5  | 95% CI: (-1.6, 1.6)  | average #tokens: 875
claude-3-5-sonnet-20240620                        | score: 79.3  | 95% CI: (-2.1, 2.0)  | average #tokens: 567
gpt-4o-2024-05-13                                 | score: 79.2  | 95% CI: (-1.9, 1.7)  | average #tokens: 696
gpt-4-0125-preview                                | score: 78.0  | 95% CI: (-2.1, 2.4)  | average #tokens: 619
qwen2.5-72b-instruct                              | score: 78.0  | 95% CI: (-1.8, 1.8)  | average #tokens: 821
gpt-4o-2024-08-06                                 | score: 77.9  | 95% CI: (-2.0, 2.1)  | average #tokens: 594
athene-70b                                        | score: 77.6  | 95% CI: (-2.7, 2.2)  | average #tokens: 684
gpt-4o-mini                                       | score: 74.9  | 95% CI: (-2.5, 1.9)  | average #tokens: 668
gemini-1.5-pro-api-preview                        | score: 72.0  | 95% CI: (-2.1, 2.5)  | average #tokens: 676
mistral-large-2407                                | score: 70.4  | 95% CI: (-1.6, 2.1)  | average #tokens: 623
llama-3.1-405b-instruct-fp8                       | score: 69.3  | 95% CI: (-2.4, 2.2)  | average #tokens: 658
glm-4-0520                                        | score: 63.8  | 95% CI: (-2.9, 2.8)  | average #tokens: 636
yi-large                                          | score: 63.7  | 95% CI: (-2.6, 2.4)  | average #tokens: 626
deepseek-coder-v2                                 | score: 62.3  | 95% CI: (-2.1, 1.8)  | average #tokens: 578
claude-3-opus-20240229                            | score: 60.4  | 95% CI: (-2.5, 2.5)  | average #tokens: 541
gemma-2-27b-it                                    | score: 57.5  | 95% CI: (-2.1, 2.4)  | average #tokens: 577
llama-3.1-70b-instruct                            | score: 55.7  | 95% CI: (-2.9, 2.7)  | average #tokens: 628
glm-4-0116                                        | score: 55.7  | 95% CI: (-2.4, 2.3)  | average #tokens: 622
glm-4-air                                         | score: 50.9  | 95% CI: (-2.9, 2.7)  | average #tokens: 619
gpt-4-0314                                        | score: 50.0  | 95% CI:  (0.0, 0.0)  | average #tokens: 423
gemini-1.5-flash-api-preview                      | score: 49.6  | 95% CI: (-2.2, 2.8)  | average #tokens: 642
qwen2-72b-instruct                                | score: 46.9  | 95% CI: (-2.5, 2.7)  | average #tokens: 515
claude-3-sonnet-20240229                          | score: 46.8  | 95% CI: (-2.3, 2.7)  | average #tokens: 552
llama-3-70b-instruct                              | score: 46.6  | 95% CI: (-2.3, 2.6)  | average #tokens: 591
claude-3-haiku-20240307                           | score: 41.5  | 95% CI: (-2.5, 2.5)  | average #tokens: 505
gpt-4-0613                                        | score: 37.9  | 95% CI: (-2.8, 2.4)  | average #tokens: 354
mistral-large-2402                                | score: 37.7  | 95% CI: (-2.1, 2.6)  | average #tokens: 400
mixtral-8x22b-instruct-v0.1                       | score: 36.4  | 95% CI: (-2.4, 2.6)  | average #tokens: 430
Qwen1.5-72B-Chat                                  | score: 36.1  | 95% CI: (-2.0, 2.7)  | average #tokens: 474
phi-3-medium-4k-instruct                          | score: 33.4  | 95% CI: (-2.6, 2.1)  | average #tokens: 517
command-r-plus                                    | score: 33.1  | 95% CI: (-2.8, 2.4)  | average #tokens: 541
mistral-medium                                    | score: 31.9  | 95% CI: (-1.9, 2.2)  | average #tokens: 485
internlm2.5-20b-chat                              | score: 31.2  | 95% CI: (-2.4, 2.8)  | average #tokens: 576
phi-3-small-8k-instruct                           | score: 29.8  | 95% CI: (-1.8, 1.9)  | average #tokens: 568
mistral-next                                      | score: 27.4  | 95% CI: (-2.4, 2.4)  | average #tokens: 297
gpt-3.5-turbo-0613                                | score: 24.8  | 95% CI: (-1.9, 2.3)  | average #tokens: 401
dbrx-instruct-preview                             | score: 24.6  | 95% CI: (-2.0, 2.6)  | average #tokens: 415
internlm2-20b-chat                                | score: 24.4  | 95% CI: (-2.0, 2.2)  | average #tokens: 667
claude-2.0                                        | score: 24.0  | 95% CI: (-1.8, 1.8)  | average #tokens: 295
Mixtral-8x7B-Instruct-v0.1                        | score: 23.4  | 95% CI: (-2.0, 1.9)  | average #tokens: 457
gpt-3.5-turbo-0125                                | score: 23.3  | 95% CI: (-2.2, 1.9)  | average #tokens: 329
Yi-34B-Chat                                       | score: 23.1  | 95% CI: (-1.6, 1.8)  | average #tokens: 611
Starling-LM-7B-beta                               | score: 23.0  | 95% CI: (-1.8, 1.8)  | average #tokens: 530
claude-2.1                                        | score: 22.8  | 95% CI: (-2.3, 1.8)  | average #tokens: 290
llama-3.1-8b-instruct                             | score: 21.3  | 95% CI: (-1.9, 2.2)  | average #tokens: 861
Snorkel-Mistral-PairRM-DPO                        | score: 20.7  | 95% CI: (-1.8, 2.2)  | average #tokens: 564
llama-3-8b-instruct                               | score: 20.6  | 95% CI: (-2.0, 1.9)  | average #tokens: 585                       
gpt-3.5-turbo-1106                                | score: 18.9  | 95% CI: (-1.8, 1.6)  | average #tokens: 285
gpt-3.5-turbo-0301                                | score: 18.1  | 95% CI: (-1.9, 2.1)  | average #tokens: 334
gemini-1.0-pro                                    | score: 17.8  | 95% CI: (-1.2, 2.2)  | average #tokens: 322
snowflake-arctic-instruct                         | score: 17.6  | 95% CI: (-1.8, 1.5)  | average #tokens: 365
command-r                                         | score: 17.0  | 95% CI: (-1.7, 1.8)  | average #tokens: 432
phi-3-mini-128k-instruct                          | score: 15.4  | 95% CI: (-1.4, 1.4)  | average #tokens: 609
tulu-2-dpo-70b                                    | score: 15.0  | 95% CI: (-1.6, 1.3)  | average #tokens: 550
Starling-LM-7B-alpha                              | score: 12.8  | 95% CI: (-1.6, 1.4)  | average #tokens: 483
mistral-7b-instruct                               | score: 12.6  | 95% CI: (-1.7, 1.4)  | average #tokens: 541
gemma-1.1-7b-it                                   | score: 12.1  | 95% CI: (-1.3, 1.3)  | average #tokens: 341
Llama-2-70b-chat-hf                               | score: 11.6  | 95% CI: (-1.5, 1.2)  | average #tokens: 595
vicuna-33b-v1.3                                   | score:  8.6  | 95% CI: (-1.1, 1.1)  | average #tokens: 451
gemma-7b-it                                       | score:  7.5  | 95% CI: (-1.2, 1.3)  | average #tokens: 378
Llama-2-7b-chat-hf                                | score:  4.6  | 95% CI: (-0.8, 0.8)  | average #tokens: 561
gemma-1.1-2b-it                                   | score:  3.4  | 95% CI: (-0.6, 0.8)  | average #tokens: 316
gemma-2b-it                                       | score:  3.0  | 95% CI: (-0.6, 0.6)  | average #tokens: 369
```

## Install Dependencies
```
git clone https://github.com/lm-sys/arena-hard.git
cd arena-hard
pip install -r requirements.txt
pip install -r requirements-optional.txt  # Optional dependencies (e.g., anthropic sdk)
```

## Download dataset
We have pre-generated many popular models answers and judgments. Check out the `/datasets` folder to figure out the way you want to compose the dataset. There is a ready set of 400 examples in the `data/arena-hard-v0.1/sampled_questions.jsonl`

## Chosen models for the evaluation

| Model Name                                  | Maintainer       | Size | Score | VRAM (GB) | License         | Context Len | Likes | Downloads | Modified    | Languages                          | Architectures        |
|---------------------------------------------|------------------|------|-------|-----------|-----------------|-------------|-------|-----------|-------------|------------------------------------|----------------------|
| Bitnet B1.58 2B 4T                         | microsoft        | 2B   | 0.56  | 1.2       | mit             | 4K          | 399   | 4623      | 2025-04-17  | en                                 | BitnetForCausalLM    |
| Phi 4 Mini Instruct                         | microsoft        | 4B   | 0.55  | 7.7       | mit             | 128K        | 440   | 308905    | 2025-03-10  | •                                  | Phi3ForCausalLM      |
| DeepSeek R1 Distill Qwen 1.5B               | deepseek-ai      | 2B   | 0.53  | 3.5       | mit             | 128K        | 1163  | 1696894   | 2025-02-24  | •                                  | Qwen2ForCausalLM     |
| Phi 3 Mini 4K Instruct                      | microsoft        | 4B   | 0.52  | 7.7       | mit             | 4K          | 1172  | 835997    | 2024-09-20  | en, fr                             | Phi3ForCausalLM      |
| Llama 3.2 3B Instruct                       | meta-llama       | 3B   | 0.5   | 6.5       | llama3.2        | 128K        | 1363  | 1367670   | 2024-10-24  | en, de, fr, it, pt, hi, es, th     | LlamaForCausalLM     |
| Gemma 3 1B It                               | google           | 1B   | 0.5   | 2         | gemma           | 32K         | 321   | 1627903   | 2025-04-04  | •                                  | Gemma3ForCausalLM    |
| SmolLM2 1.7B Instruct                       | HuggingFaceTB    | 2B   | 0.48  | 3.4       | apache-2.0      | 8K          | 595   | 78510     | 2025-03-06  | en                                 | LlamaForCausalLM     |
| Llama 3.2 1B                                | meta-llama       | 1B   | 0.46  | 2.5       | llama3.2        | 128K        | 1840  | 2024482   | 2024-10-24  | en, de, fr, it, pt, hi, es, th     | LlamaForCausalLM     |
| Llama 3.2 1B Instruct                       | meta-llama       | 1B   | 0.46  | 2.5       | llama3.2        | 128K        | 886   | 2299850   | 2024-10-24  | en, de, fr, it, pt, hi, es, th     | LlamaForCausalLM     |
| Granite 3.1 2B Instruct                     | ibm-granite      | 2B   | 0.46  | 5.1       | apache-2.0      | 128K        | 48    | 30744     | 2025-04-16  | •                                  | GraniteForCausalLM   |
| Phi 3.5 Mini Instruct                       | microsoft        | 4B   | 0.45  | 7.7       | mit             | 128K        | 851   | 295670    | 2025-03-02  | •                                  | Phi3ForCausalLM      |
| Phi 3 Mini 128K Instruct                    | microsoft        | 4B   | 0.44  | 7.7       | mit             | 128K        | 1638  | 443733    | 2025-03-02  | en                                 | Phi3ForCausalLM      |
| Qwen2.5 3B Instruct                         | Qwen             | 3B   | 0.44  | 6.2       | other           | 32K         | 237   | 1041285   | 2024-09-25  | en                                 | Qwen2ForCausalLM     |
| SmallThinker 3B Preview                     | PowerInfer       | 3B   | 0.44  | 6.8       | •               | 32K         | 394   | 55459     | 2025-01-16  | en                                 | Qwen2ForCausalLM     |
| Qwen2.5 1.5B Instruct                       | Qwen             | 2B   | 0.43  | 3.1       | apache-2.0      | 32K         | 408   | 925377    | 2024-09-25  | en                                 | Qwen2ForCausalLM     |
| DeepScaleR 1.5B Preview                     | agentica-org     | 2B   | 0.43  | 7.1       | mit             | 128K        | 547   | 56394     | 2025-04-09  | en                                 | Qwen2ForCausalLM     |
| EXAONE 3.5 2.4B Instruct                    | LGAI-EXAONE      | 2B   | 0.42  | 9.7       | other           | 32K         | 154   | 55174     | 2024-12-11  | en, ko                             | ExaoneForCausalLM    |
| ReaderLM V2                                 | jinaai           | 2B   | 0.42  | 3.1       | cc-by-nc-4.0    | 500K        | 607   | 71720     | 2025-03-04  | •                                  | Qwen2ForCausalLM     |
| Phi 2                                       | microsoft        | 3B   | 0.41  | 5.6       | mit             | 2K          | 3310  | 714731    | 2024-04-29  | en                                 | PhiForCausalLM       |
| Gemma 2 2B It                               | google           | 2B   | 0.41  | 5.2       | gemma           | 8K          | 908   | 421819    | 2024-08-27  | •                                  | Gemma2ForCausalLM    |
| Llama 3.2 3B                                | meta-llama       | 3B   | 0.41  | 6.5       | llama3.2        | 128K        | 548   | 744931    | 2024-10-24  | en, de, fr, it, pt, hi, es, th     | LlamaForCausalLM     |
| Granite 3.0 2B Instruct                     | ibm-granite      | 2B   | 0.41  | 5.3       | apache-2.0      | 4K          |       |           |             |                                    |                      |
| Granite 3.2 2B Instruct                     | ibm-granite      | 2B   | 0.41  | 5.1       | apache-2.0      | 128K        | 45    | 25368     | 2025-04-17  | •                                  | GraniteForCausalLM   |
| Cogito V1 Preview Llama 3B                  | deepcogito       | 3B   | 0.41  | 7.2       | llama3.2        | 128K        | 90    | 6274      | 2025-04-08  | •                                  | LlamaForCausalLM     |
| Gemma 3 1B Pt                               | google           | 1B   | 0.4   | 2         | gemma           | 32K         | 106   | 145045    | 2025-03-21  | •                                  | Gemma3ForCausalLM    |
| Mxbai Rerank Large V2                       | mixedbread-ai    | 2B   | 0.4   | 3.1       | apache-2.0      | 32K         | 79    | 115271    | 2025-04-02  | en, zh, de, ja, ko, es, fr, ar, bn, ru, id, sw, te, th | Qwen2ForCausalLM     |
| EXAONE Deep 2.4B                            | LGAI-EXAONE      | 2B   | 0.4   | 4.8       | other           | 32K         | 89    | 48060     | 2025-03-22  | en, ko                             | ExaoneForCausalLM    |
| DeepCoder 1.5B Preview                      | agentica-org     | 2B   | 0.4   | 7.1       | mit             | 128K        | 61    | 1915      | 2025-04-09  | en                                 | Qwen2ForCausalLM     |
| Granite 3.3 2B Instruct                     | ibm-granite      | 2B   | 0.4   | 5.1       | apache-2.0      | 128K        | 16    | 21099     | 2025-04-16  | •                                  | GraniteForCausalLM   |
| Falcon3 3B Instruct                         | tiiuae           | 3B   | 0.39  | 6.5       | other           | 32K         | 26    | 31727     | 2025-01-10  | en, fr, es, pt                     | LlamaForCausalLM     |
| ZR1 1.5B                                    | Zyphra           | 2B   | 0.39  | 7.1       | mit             | 128K        | 56    | 1151      | 2025-04-09  | en                                 | Qwen2ForCausalLM     |
| Qwen2.5 3B                                  | Qwen             | 3B   | 0.38  | 6.2       | other           | 32K         | 107   | 367056    | 2024-09-20  | en                                 | Qwen2ForCausalLM     |
| Qwen2.5 1.5B                                | Qwen             | 2B   | 0.38  | 3.1       | apache-2.0      | 128K        | 97    | 729705    | 2024-10-08  | en                                 | Qwen2ForCausalLM     |
| TinyLlama 1.1B Chat V1.0                    | TinyLlama        | 1B   | 0.37  | 2.2       | apache-2.0      | 2K          | 1227  | 1068970   | 2024-03-17  | en                                 | LlamaForCausalLM     |
| OLMoE 1B 7B 0125 Instruct                   | allenai          | 1B   | 0.37  | 13.8      | apache-2.0      | 4K          | 45    | 11286     | 2025-02-04  | en                                 | OlmoeForCausalLM     |
| Gemma 2 2B                                  | google           | 2B   | 0.36  | 10.5      | gemma           | 8K          | 487   | 182986    | 2024-08-07  | •                                  | Gemma2ForCausalLM    |
| Hermes 3 Llama 3.2 3B                       | NousResearch     | 3B   | 0.36  | 6.5       | llama3          | 128K        | 151   | 12976     | 2024-12-18  | en                                 | LlamaForCausalLM     |
| Falcon3 1B Instruct                         | tiiuae           | 1B   | 0.36  | 3.3       | other           | 8K          | 34    | 36207     | 2025-01-10  | en, fr, es, pt                     | LlamaForCausalLM     |
| Tiny Qwen2ForCausalLM 2.5                   | trl-internal-testing | 2M | 0.36 | •         | •               | 32K         | •     | 2060477   | 2024-11-25  | •                                  | Qwen2ForCausalLM     |
| Bitnet B1.58 2B 4T Bf16                     | microsoft        | 2B   | 0.36  | 4.8       | mit             | 4K          | 10    | 385       | 2025-04-17  | en                                 | BitnetForCausalLM    |
| Kimina Prover Preview Distill 1.5B          | AI-MO            | 2B   | 0.36  | 3.5       | apache-2.0      | 16K         | 8     | 3576      | 2025-04-16  | en                                 | Qwen2ForCausalLM     |
| Llama 3.2 1B Instruct                       | unsloth          | 1B   | 0.35  | 2.5       | llama3.2        | 128K        | 70    | 145670    | 2025-02-25  | en                                 | LlamaForCausalLM     |
| DeepSeek R1 Distill Llama 3B                | suayptalha       | 3B   | 0.35  | 6.5       | mit             | 128K        | 11    | 761       | 2025-02-26  | en                                 | LlamaForCausalLM     |
| Phi 4 Mini Instruct                         | unsloth          | 4B   | 0.35  | 7.7       | mit             | 128K        |       |           |             |                                    |                      |

## Quantized Models for Phi 3.5 Mini Instruct

1. [BNB 4-bit] [unsloth/Phi-3.5-mini-instruct-bnb-4bit](https://huggingface.co/unsloth/Phi-3.5-mini-instruct-bnb-4bit)
2. [AWQ] [flowaicom/Flow-Judge-v0.1-AWQ](https://huggingface.co/flowaicom/Flow-Judge-v0.1-AWQ)
3. [FP8 KV] [RedHatAI/Phi-3.5-mini-instruct-FP8-KV](https://huggingface.co/RedHatAI/Phi-3.5-mini-instruct-FP8-KV)
4. [ONNX INT4] [nvidia/Phi-3.5-mini-Instruct-ONNX-INT4](https://huggingface.co/nvidia/Phi-3.5-mini-Instruct-ONNX-INT4)

## Quantized Models for Llama-3.2-1B-Instruct

1. [Base Model] [onnx-community/Llama-3.2-1B-Instruct](https://huggingface.co/onnx-community/Llama-3.2-1B-Instruct)
2. [AWQ] [llama-3.2-1B-Instruct-AWQ](https://huggingface.co/ciCic/llama-3.2-1B-Instruct-AWQ)
3. [GPTQ INT4] [Almheiri/Llama-3.2-1B-Instruct-GPTQ-INT4](https://huggingface.co/Almheiri/Llama-3.2-1B-Instruct-GPTQ-INT4)
4. [FP8 KV] [amd/Llama-3.2-1B-Instruct-FP8-KV](https://huggingface.co/amd/Llama-3.2-1B-Instruct-FP8-KV)

## Quantized Models for Llama-3.2-3B-Instruct

1. [Base Model] 

## Quantized Models for Llama-3.2-7B-Instruct

1. [Base Model] 

## Quantized Models for Qwen2.5-7B-Instruct

1. [Base Model] [Qwen/Qwen2.5-7B-Instruct](https://huggingface.co/Qwen/Qwen2.5-7B-Instruct)
2. [AWQ] [Qwen/Qwen2.5-7B-Instruct-AWQ](https://huggingface.co/Qwen/Qwen2.5-7B-Instruct-AWQ)
3. [GPTQ Int4] [Qwen/Qwen2.5-7B-Instruct-GPTQ-Int4](https://huggingface.co/Qwen/Qwen2.5-7B-Instruct-GPTQ-Int4)
4. [GPTQ Int8] [Qwen/Qwen2.5-7B-Instruct-GPTQ-Int8](https://huggingface.co/Qwen/Qwen2.5-7B-Instruct-GPTQ-Int8)
5. [Q4F16_1 MLC] [mlc-ai/Qwen2.5-7B-Instruct-q4f16_1-MLC](https://huggingface.co/mlc-ai/Qwen2.5-7B-Instruct-q4f16_1-MLC)
6. [BNB 4-bit] [unsloth/Qwen2.5-7B-Instruct-bnb-4bit](https://huggingface.co/unsloth/Qwen2.5-7B-Instruct-bnb-4bit)

## Quantized Models for Falcon3-7B-Instruct

1. [Base Model] [tiiuae/Falcon3-7B-Instruct](https://huggingface.co/tiiuae/Falcon3-7B-Instruct)
2. [GPTQ Int4] [tiiuae/Falcon3-7B-Instruct-GPTQ-Int4](https://huggingface.co/tiiuae/Falcon3-7B-Instruct-GPTQ-Int4)
3. [GPTQ Int8] [tiiuae/Falcon3-7B-Instruct-GPTQ-Int8](https://huggingface.co/tiiuae/Falcon3-7B-Instruct-GPTQ-Int8)
4. [AWQ] [tiiuae/Falcon3-7B-Instruct-AWQ](https://huggingface.co/tiiuae/Falcon3-7B-Instruct-AWQ)



### Step 1. Set up the endpoint config to your model

Fill in your API endpoint in `config/api_config.yaml`. We support OpenAI compatible API server. You can specify `parallel` to indicate the number of concurrent API requests (default: 1).
```yaml
# example
gpt-3.5-turbo-0125:
    model_name: gpt-3.5-turbo-0125
    endpoints: null
    api_type: openai
    parallel: 8

[YOUR-MODEL-NAME]:
    model_name: [YOUR-MODEL-NAME]
    endpoints:
        - api_base: [YOUR-ENDPOINT-URL]
          api_key: [YOUR-API-KEY]
    api_type: openai
    parallel: 8
```
You may use inference engine such as [Latest TGI version](https://huggingface.co/docs/text-generation-inference/en/messages_api) or [vLLM](https://docs.vllm.ai/en/latest/serving/openai_compatible_server.html) or [SGLang](https://github.com/sgl-project/sglang?tab=readme-ov-file#using-local-models) to host your model with an OpenAI compatible API server.

TGI Quick start
```
hf_pat=
model=
volume=/path/to/cache
port=1996

huggingface-cli download $model
sudo docker run --gpus 8 -e HUGGING_FACE_HUB_TOKEN=$hf_pat --shm-size 2000g -p $port:80 -v $volume:/data ghcr.io/huggingface/text-generation-inference:2.0.4 --model-id $model --max-input-length 8192 --max-batch-total-tokens 8193 --max-batch-prefill-tokens 8193 --max-total-tokens 8193
```

### Step 2. Generate Model Answers

In `config/gen_answer_config.yaml`, add your model name in `model_list`.
```yaml
bench_name: arena-hard-v0.1
temperature: 0.0
max_tokens: 4096
num_choices: 1


model_list:
  - [YOUR-MODEL-NAME]
```
Run the command to generate answers:
```console
python gen_answer.py
```
Caching feature is implemented. The code will skip generating an answer when there is already an existing answer/judgment to the same prompt. 

### Step 3. Generate Judgments

In `config/judge_config.yaml`, add your model name in `model_list`.
```yaml
...
# Add your model below for evaluation
model_list:
  - gpt-3.5-turbo-0125
  - [YOUR-MODEL-NAME]
```

Run the command to generate judgments:
```console
python gen_judgment.py
```
Judgment caching is also implemented. It will skip generating judgments that has already been generated or lacks one of the model answers.  

### Step 4. Show result
Output model win rates.  Optionally, use `--full-stats` for detailed results. To save a csv file of the model rankings, use `--output`
```console
> python show_result.py
```

### Step 5. Arena Hard UI
You can review individual judgment results using our UI code.
```console
> python qa_browser.py --share
```

## Style Control
Following the newly introduced Style Control on Chatbot Arena, we release Style Control on Arena Hard Auto! We employ the same Style Control methods as proposed in the [blogpost](https://lmsys.org/blog/2024-08-28-style-control/). Please refer to the blogpost for methodology and technical background.

Before applying style control, make sure your model answers has proper style attribute generated. Either pull the latest data from [huggingface repo](https://huggingface.co/spaces/lmsys/arena-hard-browser), or run the following script!

To add style attribute to your model answers, use `add_markdown_info.py`. The following command takes model answers from `--dir`, append style attributes (token length, number of headers, etc), and save the new answers in `--output-dir`.

```console
> python add_markdown_info.py --dir data/arena-hard-v0.1/model_answer --output-dir data/arena-hard-v0.1/model_answer
```

To control for style (token length and markdown elements), use `--style-control` when running `show_result.py`.

```console
> python show_result.py --style-control
```

To control for length and markdown separately, use `--length-control-only` and `--markdown-control-only`.

## Evaluate Benchmarks
We outline two key properties that the benchmark aiming to approximate human preference should possess to provide meaningful comparisons between models:
1. Separability: the benchmark should separate models with high confidence.
2. Alignment with Human Preference: the benchmark should agree with human preference.

While previous works have focused on alignment, separability is also a crucial consideration when comparing models of similar quality (e.g., different checkpoints from the same training run). However, achieving high-confidence separability is challenging due to limitations in prompt design and inherent variances in LLM evaluations. Overly simplistic prompts fail to distinguish between models, while the randomness in human and LLM judgments leads to inconsistent predictions. As a result, it is often difficult to confidently determine if a model’s apparent performance reflects a genuine difference in capability or merely noisy observations, highlighting a need for methods to verify whether a benchmark can reliably separate similar models.

Statistical measures like Pearson (Pearson, 1895) and Spearman Correlations (Spearman, 1961), commonly used in benchmarks such as AlpacaEval (Li et al., 2023) to measure correlation to human preference ranking, may fail to adequately address model separability and ranking instability. In addition, these measures only provide a coarse signal of ranking correlation without quantifying the magnitude of performance differences between model pairs. To address these shortcomings, we develop three novel metrics: **Separability with Confidence**, **Agreement with Confidence**, and **Pair Rank Brier Score**.

**Separability with Confidence** quantifies the benchmark’s confidence by measuring its consistency in predicting the winner of a model pair across random seeds through bootstrapping. This is done by calculating the percentage of model pairs that have non-overlapping confidence intervals of their benchmark scores. A higher percentage indicates that the benchmark is more confident in distinguishing between the performance of different models, as the confidence intervals of their scores do not overlap.

For **Agreement with Confidence**, and **Pair Rank Brier Score**, please refer to section 3 of our [paper](https://arxiv.org/abs/2406.11939). The code for calculating these metrics can be found in this [colab notebook](https://colab.research.google.com/drive/1ar6XLWREN_dXEh404WNOxroFVUe_4njp). 

## Citation
The code in this repository is developed from the papers below. Please cite it if you find the repository helpful.
```
@article{li2024crowdsourced,
  title={From Crowdsourced Data to High-Quality Benchmarks: Arena-Hard and BenchBuilder Pipeline},
  author={Li, Tianle and Chiang, Wei-Lin and Frick, Evan and Dunlap, Lisa and Wu, Tianhao and Zhu, Banghua and Gonzalez, Joseph E and Stoica, Ion},
  journal={arXiv preprint arXiv:2406.11939},
  year={2024}
}
@misc{arenahard2024,
    title = {From Live Data to High-Quality Benchmarks: The Arena-Hard Pipeline},
    url = {https://lmsys.org/blog/2024-04-19-arena-hard/},
    author = {Tianle Li*, Wei-Lin Chiang*, Evan Frick, Lisa Dunlap, Banghua Zhu, Joseph E. Gonzalez, Ion Stoica},
    month = {April},
    year = {2024}
}
```
