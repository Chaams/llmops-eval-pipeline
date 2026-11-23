import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent


def run(candidate: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "scripts/eval_gate.py", f"results/{candidate}", "baseline.json"],
        cwd=ROOT, capture_output=True, text=True,
    )


def test_better_candidate_passes():
    assert run("candidate.json").returncode == 0


def test_regression_blocks_deployment():
    result = run("regressed.json")
    assert result.returncode == 1
    assert "hallucination_rate" in result.stdout
    assert "faithfulness" in result.stdout


def test_prompts_are_versioned():
    versions = {p.stem for p in (ROOT / "prompts").glob("*.yaml")}
    baseline = json.loads((ROOT / "baseline.json").read_text(encoding="utf-8"))
    assert baseline["prompt_version"] in versions
