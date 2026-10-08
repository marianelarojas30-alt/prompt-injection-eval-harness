import argparse
import csv
import json
from pathlib import Path
from datetime import datetime

from ollama_client import generate_with_ollama
from evaluator import build_prompt, pass_hat_k, score_response

ROOT = Path(__file__).resolve().parents[1]
SCENARIOS_PATH = ROOT / "scenarios" / "prompt_injection_tests.json"
RESULTS_DIR = ROOT / "results"


def load_scenarios():
    with open(SCENARIOS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    parser = argparse.ArgumentParser(description="Run prompt injection evaluations against a local Ollama model.")
    parser.add_argument("--model", default="qwen3.5:4b", help="Ollama model name, for example qwen3.5:4b")
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--trials", type=int, default=1,
                        help="attempts per scenario; use a temperature above 0 so trials differ, then read pass^k")
    args = parser.parse_args()
    if args.trials < 1:
        parser.error("--trials must be at least 1")

    RESULTS_DIR.mkdir(exist_ok=True)

    scenarios = load_scenarios()
    results = []

    for scenario in scenarios:
        prompt = build_prompt(scenario)
        for trial in range(1, args.trials + 1):
            print(f"Running {scenario['id']} - {scenario['title']} (trial {trial}/{args.trials})")

            response = generate_with_ollama(
                model=args.model,
                prompt=prompt,
                temperature=args.temperature
            )

            score = score_response(scenario, response)

            record = {
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "model": args.model,
                "scenario_id": scenario["id"],
                "trial": trial,
                "category": scenario["category"],
                "title": scenario["title"],
                "expected_safe_behavior": scenario["expected_safe_behavior"],
                "response": response,
                **score
            }

            results.append(record)

    json_path = RESULTS_DIR / "eval_results.json"
    csv_path = RESULTS_DIR / "eval_results.csv"

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    fieldnames = list(results[0].keys()) if results else []
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    print("pass^k per scenario (all trials followed the trusted instruction):")
    for sid, row in pass_hat_k(results).items():
        print(f"  {sid}: pass^{row['trials']}={'yes' if row['pass_hat_k'] else 'no'}  pass_rate={row['pass_rate']:.0%}")

    print(f"Saved JSON results to {json_path}")
    print(f"Saved CSV results to {csv_path}")


if __name__ == "__main__":
    main()
