import csv
import json
from ollama import promptOllama
import openai
from trace import PromptJsonTrace
from enums import Model
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI")

class SystemOfThought:

    def __init__(self, dataset, answers, choices, count, input_model, output_model, ollama_mode):
        self.dataset = dataset
        self.answers = answers
        self.choices = choices
        self.input_model = input_model
        self.output_model = output_model
        self.ollama_mode = ollama_mode
        self.count = count  # maximum number of prompts provided

    def sample(self, count, offset):
        for i in range(count):
            # Initialize JSON Tracer for data parsing
            trace = PromptJsonTrace()
            trace.add_question_input(self.dataset[i], self.answers[i])
            if self.choices is None:
                input_prompt = self.dataset[i]
            else:
                input_prompt = f'{self.dataset[i]}\n{self.choices[i]}'
            # Create prompt
            prompt = (f'Create very short step-by-step prompts for this problem:'
                      f'{input_prompt}'
                      f'Format as a list.'
                      f'Assume no knowledge of the original question, including any knowledge of variables.'
                      f'Do not solve the problem. Only generate steps to tell another model, in as few words as possible.'
                      f'Pass all important values (numerical, informational, etc) into your prompts.'
                      f'If choices are provided, indicate them in a final step for the user to choose from.'
                      f'Use as few steps as possible.')
            print(f'Executing prompt {offset+i+1}')

            # If we are using a closed source model, indicate that tokens are cost tokens
            if self.input_model == Model.GPT4 or self.input_model == Model.GPT3point5:
                cost = True
            else:
                cost = False
            trace.add_delegation(prompt, cost)

            # Create the list of prompts returned from our target model
            if self.input_model == Model.GPT4 or self.input_model == Model.GPT3point5:
                if self.input_model == Model.GPT4:
                    prompts = openai.chat.completions.create(
                        model='gpt-4-0613',
                        messages=[
                            {
                                'role': 'user',
                                'content': prompt
                            }
                        ]
                    )
                    step_one_result = prompts.choices[0].message.content
                    trace.add_delegate_return(step_one_result, prompts.usage.prompt_tokens, prompts.usage.completion_tokens)
                else:
                    prompts = openai.chat.completions.create(
                        model='gpt-3.5-turbo-0613',
                        messages=[
                            {
                                'role': 'user',
                                'content': prompt
                            }
                        ]
                    )
                    step_one_result = prompts.choices[0].message.content
                    trace.add_delegate_return(step_one_result, prompts.usage.prompt_tokens, prompts.usage.completion_tokens)
            else:
                prompts = promptOllama(prompt, self.input_model)
                step_one_result = prompts["text"]
                trace.add_delegate_return(step_one_result, prompts["input_count"], prompts["output_count"])
           ##  print(f'RESPONSE:\n{step_one_result}\n\n')

            answer_prompt = f'We are given the following problem to solve:\n{input_prompt}\nUse the following steps to solve the problem.\n{step_one_result}'

            # If we are using a closed source model, indicate that tokens are cost tokens
            if self.output_model == Model.GPT4 or self.output_model == Model.GPT3point5:
                cost = True
            else:
                cost = False
            trace.add_answer(answer_prompt, cost)

            if self.output_model == Model.GPT4 or self.output_model == Model.GPT3point5:
                if self.output_model == Model.GPT4:
                    answer = openai.chat.completions.create(
                        model='gpt-4-0613',
                        messages=[
                            {
                                'role': 'user',
                                'content': answer_prompt
                            }
                        ]
                    )
                    step_two_result = answer.choices[0].message.content
                    trace.add_answer_return(step_two_result, answer.usage.prompt_tokens, answer.usage.completion_tokens)
                else:
                    answer = openai.chat.completions.create(
                        model='gpt-3.5-turbo-0613',
                        messages=[
                            {
                                'role': 'user',
                                'content': prompt
                            }
                        ]
                    )
                    step_two_result = answer.choices[0].message.content
                    trace.add_answer_return(step_two_result, answer.usage.prompt_tokens, answer.usage.completion_tokens)
            else:
                answer = promptOllama(answer_prompt, self.output_model)
                step_two_result = answer["text"]
                trace.add_answer_return(step_two_result, answer["input_count"], answer["output_count"])
            ## print(f'ANSWER: {step_two_result}')

            trace.set_tokens()

            ## print(trace.dump_string())
            with open('sot-results-gpt4-llama7bchat-new-feb4-traces.csv', 'a') as csvFile:
                writer = csv.writer(csvFile)
                writer.writerow([trace.dump_string(),prompt, step_one_result, step_two_result, self.answers[i], trace.state["cost_total"]])

            with open(f'traces/sot-trace-gpt4-llama7bchat-new-feb4-iter{i}.json', 'w') as file:
                json.dump(trace.state, file)

