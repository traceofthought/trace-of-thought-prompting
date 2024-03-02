# Trace-of-Thought Prompting
### Anonymous ACL Submission

---
### Purpose
The purpose of this repository is to enable a quick deployment of Trace-of-Thought's functionality, without placing the onus on the reviewer for developing a test suite.

The extent to which human involvement is needed in this repo is **configuring Ollama (remote^ or local) as well as an OpenAI API key.**

(^ - remote may be unsupported at time of viewing. We are currently working towards deploying remote capabilities.)

### Structure
`/`
- Contains the README, attributions once anonymity is lifted post-reviews, and all scripts.

- Contains the `main.py` script that enables easy deployment of quick experiments.
- Contains the `autotester.py` script that enables full-scale reproduction on an entire suite of models. **USE AT YOUR OWN FINANCIAL AND COMPUTATIONAL RISK!**
- Contains the `trace_analyzer.py` script that quickly and easily processes your output traces for various key metrics.


`/output`
- Contains user-conducted outputs.
- `/output/traces` contains traces obtained from Trace-of-Thought for post-hoc analysis. Tokens that were used to prompt GPT-4 or 3.5 are deemed cost tokens - all others are deemed regular tokens.

### Setup
1. Obtain an **OpenAI API Key** from [OpenAI's API Portal](https://platform.openai.com/api-keys). Place this in the provided `.env.example` file as an argument for OPENAI_KEY=.
2. Install the requisite packages: `pip install datasets python-dotenv openai`
3. Navigate to `main.py`.
4. Select your dataset. The bundled options are `Dataset.GSM8K` and `Dataset.MATH` - see the Enums section for details on adding novel extensions.
5. Select your sample size. The default, and recommended, option is 200 samples. Don't worry about exceeding dataset lengths - we prevent this later on in the backend by selecting the minimum of your dataset's length and your desired length.
6. If applicable, select your offset amount. This value is only intended for experiments that are being resumed from somewhere in the middle of datasets. An offset of 100 will start at the provided dataset's 100th index.
7. Select your models. You must select an input and output model, but they can be the same. For simplicity, we bundle `Model.GPT4` as both the input and output. See the Enums section for more details.
8. Select your Ollama mode, either Remote or Local. We recommend Local for ease of use, but this is hardware dependent.
9. Select your prompting method. Again, while we bundle `Prompt.StandardPrompt`, `Prompt.ChainOfThought`, and `Prompt.TraceOfThought`, the Enums section provides further clarity.
10. Run `main.py` using your interpreter of choice!
aceOfThought`