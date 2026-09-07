# AI Interview Evaluation

This evaluator uses the existing backend embedding model, pgvector retrieval,
and interview answer-generation pipeline. It does not write to the application
chat or asked-question tables.

## Structure

- `data/common_questions.xlsx`: evaluation dataset with `question`,
  `ideal_answer`, `roles`, and `keywords` columns
- `evaluation/`: metrics, adapters, evaluation pipeline, and judge utilities
- `results/`: generated evaluation outputs

## Setup

```bash
python -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
```

Run from the `backend/` directory with the project virtual environment active:

```bash
python -m Evaluation.AI_Interview_Evaluation.evaluation.evaluate
```

The command evaluates every row in `data/common_questions.xlsx` and writes
`retrieval_results.csv`, `generation_results.csv`, and
`evaluation_metrics.png` to `results/`.
