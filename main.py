from datasets import load_dataset
from dotenv import load_dotenv
from enums import Dataset, Model, OllamaMode, Prompt
from utils import restructureCSQAChoices
import cot
import sot
import standard

load_dotenv()

### STEP 1
### Change your target dataset (all possible values provided through the Dataset Enum):
dataset = Dataset.GSM8K

### STEP 2
### Select your sample size. For experimentation, we recommend 200 for a more holistic approach:
size = 200
offset = 0

### STEP 3
### Select your input and output models, through the Model Enum:
input_model = Model.Llama27BChat
output_model = Model.Llama27BChat

### STEP 4
### Select your Ollama polling mode using the OllamaMode Enum - only applicable if either input or output is Ollama-dependent.
ollama_mode = OllamaMode.Local

### STEP 5
### Select your target prompting method through the Prompt Enum:
prompting = Prompt.ChainOfThought

##### EVERYTHING PAST THIS POINT SHOULD NOT BE ALTERED #####

# Start by initializing the appropriate dataset, and trimming to the desired size.

match dataset:
    case Dataset.GSM8K:
        print("Dataset initialized as GSM8K.")
        target_dataset = load_dataset("gsm8k", "main", split="test")
        question_split = target_dataset["question"]
        choices_split = None
        answer_split = target_dataset["answer"]
        length = len(question_split)
    case Dataset.MATH:
        print("Dataset initialized as MATH.")
        target_dataset = load_dataset("camel-ai/math", split="train")  # Exception to the split rule, as there is no test split.
        question_split = target_dataset["message_1"]
        choices_split = None
        answer_split = target_dataset["message_2"]
        length = len(question_split)
    case Dataset.CSQA:
        print("Dataset initialized as CSQA.")
        target_dataset = load_dataset("tau/commonsense_qa", split="test")
        question_split = target_dataset["question"]
        choices_split = restructureCSQAChoices(target_dataset["choices"])
        answer_split = target_dataset["answerKey"]
        length = len(question_split)
    case Dataset.NeQA:
        print("Dataset initialized as NeQA.")
        target_dataset = load_dataset("inverse-scaling/NeQA", split="train")  # See above
        question_split = target_dataset["prompt"]
        choices_split = target_dataset["classes"]
        answer_split = target_dataset["answer_index"]
        length = len(question_split)
    case _:
        print("Invalid dataset selected, please change & retry.")
        exit(1)

# Now that we have initialized the datasets, "trim" them to max(requested, provided).
if length < size: size = length
print(f'Sample size set to {size}.')

print(f"Input model selected as {input_model}.")
print(f"Output model selected as {output_model}.")

if ollama_mode == OllamaMode.Local:
    ollama_addr = 'http://localhost:11434/api/generate'
else:
    print("Ollama mode not currently supported.")
    exit(1)

# Finally, instantiate the testing process.

if choices_split is not None:
	choices_split = choices_split[offset:size]

if prompting == Prompt.SystemOfThought:
    print("Beginning sampling with System of Thought...")
    engine = sot.SystemOfThought(question_split[offset:size], answer_split[offset:size], choices_split, -1, input_model, output_model, ollama_addr)
    engine.sample(size, offset)
elif prompting == Prompt.ChainOfThought:
    print("Beginning sampling with Chain of Thought...")
    engine = cot.ChainOfThought(question_split[offset:size], answer_split[offset:size], choices_split, input_model)
    engine.sample(size, offset)
else:
    print("Beginning sampling with Standard Prompting...")
    engine = standard.StandardPrompt(question_split[offset:size], answer_split[offset:size], choices_split, input_model)
    engine.sample(size, offset)
