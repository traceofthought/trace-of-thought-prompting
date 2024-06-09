from enum import Enum

class Dataset(Enum):
    GSM8K = 1
    MATH = 2
    CSQA = 3
    NeQA = 4

class Model(Enum):
    GPT4 = 1
    GPT3point5 = 2
    WizardMath7B = 3
    WizardMath13B = 4
    Phi2 = 5
    WizardMath70B = 6
    LlamaPro = 7
    Llama27BText = 8
    Zephyr = 9
    Llama27BChat = 10
    Llama38B = 11

class OllamaMode(Enum):
    Local = 1
    Remote = 2

class Prompt(Enum):
    ChainOfThought = 1
    TraceOfThought = 2
    StandardPrompt = 3
    PlanAndSolve = 4
