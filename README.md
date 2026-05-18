# Prompt Injection Evaluation Harness

A controlled, ethical AI security evaluation project for testing how local LLMs respond to prompt injection and conflicting-instruction scenarios.

## Purpose

This project evaluates whether language models follow trusted instructions or unsafe injected instructions embedded inside user-provided content.

It is designed for AI security, AI safety, and adversarial LLM evaluation learning.

## What this project tests

The harness runs controlled scenarios such as:

- Direct prompt injection
- Indirect prompt injection inside documents
- Hidden instruction conflicts
- Data exfiltration attempts in simulated contexts
- Safety-policy override attempts
- Tool-use style instruction conflicts

The project logs model responses and scores whether the model:

- Followed the trusted instruction
- Obeyed the injected instruction
- Refused unsafe behavior
- Partially leaked protected content
- Recognized the injection attempt

## Safety boundaries

This project does not perform real hacking, access real systems, exploit live targets, or collect private data.

All tests are synthetic and run in a controlled local environment.

## Quick start

### 1. Install Ollama

Download Ollama from https://ollama.com

Then pull a local model:

```bash
ollama pull qwen2.5:7b
```

or:

```bash
ollama pull llama3.1:8b
```

### 2. Create a Python virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Run the evaluation

```bash
python src/run_eval.py --model qwen2.5:7b
```

Results will be saved to:

```text
results/eval_results.csv
results/eval_results.json
```

## Repository structure

```text
prompt-injection-eval-harness/
├── README.md
├── requirements.txt
├── scenarios/
│   └── prompt_injection_tests.json
├── src/
│   ├── run_eval.py
│   ├── ollama_client.py
│   └── evaluator.py
├── results/
│   └── .gitkeep
└── report/
    └── findings.md
```

## Research question

How reliably do local language models resist prompt injection when malicious instructions are embedded inside content they are asked to process?

## Initial evaluation metrics

Each response is scored across five dimensions:

1. `followed_trusted_instruction`
2. `followed_injected_instruction`
3. `leaked_protected_content`
4. `recognized_attack`
5. `safe_refusal_or_boundary`

These are simple rule-based labels for the first version. Future versions may add human review and model-assisted scoring.

## Planned improvements

- Add more models
- Add model comparison tables
- Add RAG-style tests
- Add agent/tool-use simulation
- Add dashboard with Streamlit
- Add deeper scoring rubric
- Add report with charts and findings

## Ethical use

This project is for defensive AI security research and education only.
