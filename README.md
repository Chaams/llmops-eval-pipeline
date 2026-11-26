> **Archived: this project now lives in [Qistas](https://github.com/Chaams/qistas)**, the quality gate for Arabic LLM applications, which uses a real LLM judge and is evaluated in CI.
> This repository is kept read-only as the history of the work.

# llmops-eval-pipeline

Pipeline **LLMOps** : prompts versionnés, évaluation continue et **porte qualité** qui bloque le déploiement
d'un nouveau prompt/modèle s'il dégrade la fidélité, les hallucinations, la latence p95 ou le coût.

```bash
pip install -r requirements.txt
pytest -v
python scripts/eval_gate.py results/candidate.json baseline.json   # OK
python scripts/eval_gate.py results/regressed.json baseline.json   # échec (code 1)
```

| Élément | Rôle |
|---|---|
| `prompts/*.yaml` | Prompts versionnés dans Git |
| `baseline.json` | Métriques de la version en production |
| `results/` | Résultats d'évaluation des candidats (produits par votre banc d'évaluation, ex. `rag-eval-bench`) |
| `scripts/eval_gate.py` | Compare candidat et baseline, tolérance 2 % |
| `.github/workflows/llm-ci.yml` | Bloque la PR en cas de régression |
| `Dockerfile` | Exécute la porte qualité dans un conteneur reproductible |
