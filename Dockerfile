FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# Le conteneur exécute la porte qualité : le build CI échoue si une métrique régresse.
CMD ["python", "scripts/eval_gate.py", "results/candidate.json", "baseline.json"]
