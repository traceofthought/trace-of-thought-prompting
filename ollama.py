import json
from enums import Model
import requests


def promptOllama(prompt, model):
    match model:
        case Model.WizardMath7B:
            model_param = "wizard-math"
        case Model.WizardMath13B:
            model_param = "wizard-math:13b"
        case Model.Phi2:
            model_param = "phi"
        case Model.WizardMath70B:
            model_param = "wizard-math:70b"
        case Model.LlamaPro:
            model_param = "llama-pro"
        case Model.Llama27BText:
            model_param = "llama2:7b-text" ## no chat fine-tuning
        case Model.Llama27BChat:
            model_param = "llama2:7b-chat" ## chat fine-tuning
        case Model.Zephyr:
            model_param = "zephyr"
        case _:
            print("Ollama model not supported.")
            exit(1)

    response = requests.post('http://localhost:11434/api/generate', json={
        "model": model_param, ## replace with phi or whatever model you're using
        "prompt": prompt
    })

    response_text = response.text

    # Convert each line to json
    response_lines = response_text.splitlines()
    response_json = [json.loads(line) for line in response_lines]
    out = ""
    token_count_in = 0
    token_count_out = 0
    for line in response_json:
        # Print the response. No line break
        out += line["response"]
        if "prompt_eval_count" in line: token_count_in = line["prompt_eval_count"]
        if "eval_count" in line: token_count_out = line["eval_count"]

    return {
        "response": response,
        "text": out,
        "input_count": token_count_in,
        "output_count": token_count_out
    }
