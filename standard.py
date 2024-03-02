import csv
import openai
from enums import Model
from ollama import promptOllama


class StandardPrompt:

    def __init__(self, dataset, answers, choices, input_model):
        self.dataset = dataset
        self.answers = answers
        self.choices = choices
        self.answers = answers
        self.input_model = input_model

    def sample(self, count, offset):
        if count > len(self.dataset):
            count = len(self.dataset)
        for i in range(count):
            if self.choices is None:
                input_prompt = self.dataset[i]
            else:
                input_prompt = f'{self.dataset[i]}\n{self.choices[i]}'
            prompt = f'{input_prompt}'
            print(f'Executing prompt {offset+i}')

            if self.input_model == Model.GPT4 or self.input_model == Model.GPT3point5:
                if self.input_model == Model.GPT4:
                    answer = openai.chat.completions.create(
                        model='gpt-4-0613',
                        messages=[
                            {
                                'role': 'user',
                                'content': prompt
                            }
                        ]
                    )
                    response = answer.choices[0].message.content
                    count = (answer.usage.prompt_tokens + answer.usage.completion_tokens)
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
                    response = answer.choices[0].message.content
                    count = (answer.usage.prompt_tokens + answer.usage.completion_tokens)
            else:
                answer = promptOllama(prompt, self.input_model)
                response = answer["text"]
                count = (answer["input_count"] + answer["output_count"])

            with (open("sp-l27bchat-feb5.csv", 'a')) as csvFile:
                writer = csv.writer(csvFile, delimiter=',')
                writer.writerow(
                    [prompt, response, self.answers[i], count])
