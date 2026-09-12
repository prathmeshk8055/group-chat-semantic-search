import json
from pathlib import Path

from search import semantic_search


# ==========================================
# PROJECT PATHS
# ==========================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

QUERIES_PATH = PROJECT_ROOT / "data" / "test_queries.json"


# ==========================================
# LOAD TEST QUERIES
# ==========================================

with open(QUERIES_PATH, "r", encoding="utf-8") as f:
    test_queries = json.load(f)


# ==========================================
# EVALUATION
# ==========================================

def evaluate():

    total = len(test_queries)
    correct = 0

    results = []

    print()
    print("=" * 75)
    print("SEARCH ENGINE EVALUATION")
    print("=" * 75)

    for item in test_queries:

        query_id = item["id"]
        query = item["query"]
        expected_id = item["answer_id"]

        search_results = semantic_search(
            query,
            top_k=10
        )

        retrieved_ids = [
            result["message"]["id"]
            for result in search_results
        ]

        hit = expected_id in retrieved_ids

        if hit:
            correct += 1

        results.append({
            "id": query_id,
            "query": query,
            "expected": expected_id,
            "retrieved": retrieved_ids,
            "hit": hit
        })

        status = "✓" if hit else "✗"

        rank = (
            retrieved_ids.index(expected_id) + 1
            if hit
            else "-"
        )

        print(
            f"{status} {query_id} | "
            f"Rank: {rank} | "
            f"Expected: {expected_id} | "
            f"{query}"
        )

    # ======================================
    # OVERALL ACCURACY
    # ======================================

    accuracy = (correct / total) * 100

    print()
    print("=" * 75)
    print("OVERALL RESULTS")
    print("=" * 75)

    print(f"Total queries : {total}")
    print(f"Correct       : {correct}")
    print(f"Incorrect     : {total - correct}")
    print(f"Accuracy      : {accuracy:.2f}%")


    # ======================================
    # HARD QUERY RESULTS
    # ======================================

    # The first 8 queries are our designated
    # hard / zero-overlap evaluation queries.

    hard_results = results[:8]

    hard_correct = sum(
        result["hit"]
        for result in hard_results
    )

    hard_total = len(hard_results)

    hard_accuracy = (
        hard_correct / hard_total * 100
        if hard_total
        else 0
    )

    print()
    print("=" * 75)
    print("HARD QUERY RESULTS")
    print("=" * 75)

    print(f"Hard queries  : {hard_total}")
    print(f"Correct       : {hard_correct}")
    print(f"Incorrect     : {hard_total - hard_correct}")
    print(f"Accuracy      : {hard_accuracy:.2f}%")


    # ======================================
    # SAVE RESULTS
    # ======================================

    output_path = PROJECT_ROOT / "data" / "evaluation_results.json"

    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            {
                "total_queries": total,
                "correct": correct,
                "accuracy": accuracy,
                "hard_queries": hard_total,
                "hard_correct": hard_correct,
                "hard_accuracy": hard_accuracy,
                "results": results
            },
            f,
            indent=2,
            ensure_ascii=False
        )

    print()
    print(
        f"Detailed results saved to: "
        f"{output_path}"
    )


# ==========================================
# RUN
# ==========================================

if __name__ == "__main__":
    evaluate()