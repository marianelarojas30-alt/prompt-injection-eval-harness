# Findings

## Research Question

How reliably do local language models resist prompt injection when malicious instructions are embedded inside content they are asked to process?

## Initial Method

This project runs synthetic prompt injection scenarios against local models through Ollama.

Each scenario includes:

- A trusted instruction
- Synthetic protected content
- A user request
- Untrusted content containing either benign text or injected instructions

## Initial Metrics

The first version uses transparent rule-based labels:

- followed_trusted_instruction
- followed_injected_instruction
- leaked_protected_content
- recognized_attack
- safe_refusal_or_boundary

## Notes

This is an early evaluation harness. The scoring is intentionally simple and should not be treated as a final benchmark.

## Next Steps

- Run multiple models
- Compare results across models
- Add more scenarios
- Add human review
- Add RAG-style indirect prompt injection
- Add agent/tool-use simulations
- Create charts from results
