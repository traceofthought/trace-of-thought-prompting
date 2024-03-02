import json


class PromptJsonTrace:

    def __init__(self):
        self.state = {
            "dataset_question": "",
            "dataset_answer": "",
            "delegation": {
                "input_text": "",
                "output_text": "",
                "input_count": "",
                "output_count": "",
                "cost_tokens": 0
            },
            "answer": {
                "input_text": "",
                "output_text": "",
                "input_count": "",
                "output_count": "",
                "cost_tokens": 0
            },
            "annotations": {
                "delegation": "",
                "answer": ""
            },
            "total_count": 0,
            "cost_total": 0
        }

    def add_question_input(self, question: str, answer: str):
        self.state["dataset_question"] += question
        self.state["dataset_answer"] += answer
        return self

    def add_delegation(self, prompt: str, cost: bool):
        self.state["delegation"]["input_text"] += prompt
        self.state["delegation"]["cost_tokens"] = cost
        return self

    def add_delegate_return(self, output_text: str, input_count: int, output_count: int):
        self.state["delegation"]["output_text"] = output_text
        self.state["delegation"]["input_count"] = input_count
        self.state["delegation"]["output_count"] = output_count
        cost_state = self.state["delegation"]["cost_tokens"]
        cost = 0
        if cost_state is True:
            cost = (input_count + output_count)
        self.state["delegation"]["cost_tokens"] = cost
        return self

    def add_answer(self, prompt: str, cost: bool):
        self.state["answer"]["input_text"] += prompt
        self.state["answer"]["cost_tokens"] = cost
        return self

    def add_answer_return(self, output_text: str, input_count: int, output_count: int):
        self.state["answer"]["output_text"] += output_text
        self.state["answer"]["input_count"] = input_count
        self.state["answer"]["output_count"] = output_count
        cost_state = self.state["answer"]["cost_tokens"]
        cost = 0
        if cost_state is True:
            cost = (input_count + output_count)
        self.state["answer"]["cost_tokens"] = cost
        return self

    def add_custom_annotation(self, category: str, annotation: str):
        if not (annotation == "delegation" or annotation == "answer"):
            print("Invalid annotation category - not logged in trace.")
            return

        self.state["annotations"][category] += annotation
        return self

    def __set_total_tokens(self):
        count = 0
        count += self.state["delegation"]["input_count"]
        count += self.state["delegation"]["output_count"]
        count += self.state["answer"]["input_count"]
        count += self.state["answer"]["output_count"]
        self.state["total_count"] = count
        return self

    def __set_cost_tokens(self):
        count = 0
        count += self.state["delegation"]["cost_tokens"]
        count += self.state["answer"]["cost_tokens"]
        self.state["cost_total"] = count
        return self

    def set_tokens(self):
        self.__set_cost_tokens()
        self.__set_total_tokens()
        return self

    def dump_string(self):
        return json.dumps(self.state)
