"""Run retrieval and generation evaluation against the project RAG pipeline."""
import argparse
from pathlib import Path
import re

import matplotlib.pyplot as plt
import pandas as pd

from .adapter import generate_answer, retrieve
from .metrics_generation import (
    bleu_score,
    clean_reference_answer,
    exact_match,
    rouge_scores,
    token_f1,
)
from .metrics_retrieval import (
    average_similarity,
    f1_score,
    precision_at_k,
    recall_at_k,
    reciprocal_rank,
)


EVALUATION_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DATASET = EVALUATION_ROOT / "data" / "common_questions.xlsx"
RESULTS_ROOT = EVALUATION_ROOT / "results"
K = 5


def _text(value):
    return "" if pd.isna(value) else str(value).strip()


def _tokens(value):
    return set(re.findall(r"[a-z0-9]+", _text(value).casefold()))


def _is_relevant(retrieved_question, expected_question, expected_keywords):
    if _text(retrieved_question).casefold() == _text(expected_question).casefold():
        return 1

    expected_tokens = _tokens(expected_question) | _tokens(expected_keywords)
    retrieved_tokens = _tokens(retrieved_question)
    if not expected_tokens:
        return 0

    overlap = len(expected_tokens & retrieved_tokens) / len(expected_tokens)
    return int(overlap >= 0.15)


def _context(results):
    return "\n\n".join(
        f"Question: {result['question']}\nIdeal answer: {result.get('answer', '')}"
        for result in results
    )


def _plot_metrics(retrieval_df, generation_df):
    RESULTS_ROOT.mkdir(parents=True, exist_ok=True)

    retrieval_columns = ["similarity_score", "precision@5", "recall@5", "mrr", "f1"]
    generation_columns = ["exact_match", "bleu", "rouge1", "rouge2", "rougeL", "token_f1"]

    figure, axes = plt.subplots(1, 2, figsize=(14, 5))
    retrieval_df[retrieval_columns].mean().plot.bar(ax=axes[0], color="#2563eb")
    axes[0].set_title("Retrieval metrics")
    axes[0].set_ylim(0, 1)
    axes[0].tick_params(axis="x", rotation=35)

    generation_df[generation_columns].mean().plot.bar(ax=axes[1], color="#16a34a")
    axes[1].set_title("Generation metrics")
    axes[1].set_ylim(0, 1)
    axes[1].tick_params(axis="x", rotation=35)

    figure.tight_layout()
    figure.savefig(RESULTS_ROOT / "evaluation_metrics.png", dpi=160)
    plt.close(figure)

    for frame, columns, color, title, filename in (
        (
            retrieval_df,
            retrieval_columns,
            "#2563eb",
            "Retrieval metrics",
            "retrieval_metrics.png",
        ),
        (
            generation_df,
            generation_columns,
            "#16a34a",
            "Generation metrics",
            "generation_metrics.png",
        ),
    ):
        figure, axis = plt.subplots(figsize=(8, 5))
        frame[columns].mean().plot.bar(ax=axis, color=color)
        axis.set_title(title)
        axis.set_ylim(0, 1)
        axis.tick_params(axis="x", rotation=35)
        figure.tight_layout()
        figure.savefig(RESULTS_ROOT / filename, dpi=160)
        plt.close(figure)


def evaluate(dataset_path=DEFAULT_DATASET):
    RESULTS_ROOT.mkdir(parents=True, exist_ok=True)
    data = pd.read_excel(dataset_path)
    required_columns = {"question", "ideal_answer", "roles"}
    missing_columns = required_columns.difference(data.columns)
    if missing_columns:
        raise ValueError(
            f"Dataset is missing required columns: {', '.join(sorted(missing_columns))}"
        )

    retrieval_rows = []
    generation_rows = []

    for index, row in data.iterrows():
        query = _text(row["question"])
        reference_answer = clean_reference_answer(
            _text(row["ideal_answer"]),
            query,
        )
        role = _text(row["roles"])
        keywords = _text(row.get("keywords", ""))
        if not query:
            continue

        print(f"[{index + 1}/{len(data)}] Evaluating: {query}", flush=True)
        retrieval_response = retrieve(query, role=role or None, top_k=K)
        retrieved = retrieval_response["results"]
        relevance = [
            _is_relevant(item["question"], query, keywords)
            for item in retrieved
        ]
        similarity_scores = [item["score"] for item in retrieved]
        precision = precision_at_k(relevance, K)
        recall = recall_at_k(relevance, 1, K)

        retrieval_rows.append(
            {
                "query": query,
                "role": role,
                "retrieved_questions": " || ".join(item["question"] for item in retrieved),
                "similarity_score": average_similarity(similarity_scores),
                "precision@5": precision,
                "recall@5": recall,
                "mrr": reciprocal_rank(relevance),
                "f1": f1_score(precision, recall),
            }
        )

        generated = generate_answer(query, _context(retrieved))
        rouge = rouge_scores(reference_answer, generated)
        generation_rows.append(
            {
                "query": query,
                "reference_answer": reference_answer,
                "generated_answer": generated,
                "exact_match": exact_match(reference_answer, generated),
                "bleu": bleu_score(reference_answer, generated),
                **rouge,
                "token_f1": token_f1(reference_answer, generated),
            }
        )

    retrieval_df = pd.DataFrame(retrieval_rows)
    generation_df = pd.DataFrame(generation_rows)
    retrieval_path = RESULTS_ROOT / "retrieval_results.csv"
    generation_path = RESULTS_ROOT / "generation_results.csv"
    retrieval_df.to_csv(retrieval_path, index=False)
    generation_df.to_csv(generation_path, index=False)
    _plot_metrics(retrieval_df, generation_df)

    print(f"Saved retrieval results to {retrieval_path}", flush=True)
    print(f"Saved generation results to {generation_path}", flush=True)
    print(f"Saved graphs to {RESULTS_ROOT}", flush=True)
    return retrieval_df, generation_df


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", type=Path, default=DEFAULT_DATASET)
    args = parser.parse_args()
    evaluate(args.dataset)


if __name__ == "__main__":
    main()