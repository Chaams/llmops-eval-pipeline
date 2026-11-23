"""Quality gate LLMOps : compare les résultats d'évaluation d'un prompt candidat à une baseline.

Usage :  python scripts/eval_gate.py results/candidate.json baseline.json
Code de sortie 1 si une métrique régresse au-delà de la tolérance -> le déploiement est bloqué.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HIGHER_IS_BETTER = {"faithfulness", "answer_relevance"}
LOWER_IS_BETTER = {"hallucination_rate", "p95_latency_ms", "cost_per_1k_requests_usd"}
TOLERANCE = 0.02  # 2 % de dégradation relative tolérée


def regressions(candidate: dict, baseline: dict, tol: float = TOLERANCE) -> list[str]:
    problems = []
    for metric in HIGHER_IS_BETTER:
        if candidate[metric] < baseline[metric] * (1 - tol):
            problems.append(f"{metric}: {candidate[metric]} < baseline {baseline[metric]}")
    for metric in LOWER_IS_BETTER:
        if candidate[metric] > baseline[metric] * (1 + tol):
            problems.append(f"{metric}: {candidate[metric]} > baseline {baseline[metric]}")
    return problems


def main(argv: list[str]) -> int:
    candidate = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
    baseline = json.loads(Path(argv[2]).read_text(encoding="utf-8"))
    problems = regressions(candidate, baseline)
    if problems:
        print("QUALITY GATE : ECHEC")
        print(*problems, sep="\n")
        return 1
    print("QUALITY GATE : OK — aucune régression")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
