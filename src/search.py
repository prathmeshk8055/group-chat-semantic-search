import json
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer


# ==========================================
# 1. PROJECT PATHS
# ==========================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

MESSAGES_PATH = PROJECT_ROOT / "data" / "messages.json"
EMBEDDINGS_PATH = PROJECT_ROOT / "data" / "embeddings.npy"


# ==========================================
# 2. LOAD DATA
# ==========================================

with open(MESSAGES_PATH, "r", encoding="utf-8") as f:
    messages = json.load(f)

embeddings = np.load(EMBEDDINGS_PATH)

print(f"Loaded {len(messages)} messages.")
print(f"Loaded embeddings with shape: {embeddings.shape}")


# ==========================================
# 3. LOAD MODEL
# ==========================================

print("Loading embedding model...")

model = SentenceTransformer("BAAI/bge-m3")

print("Model loaded.")


# ==========================================
# 4. QUERY INTENT
# ==========================================

def detect_query_intent(query):

    query_lower = query.lower()

    decision_words = [
        "decide",
        "decided",
        "decision",
        "final",
        "finalize",
        "finalized",
        "settle",
        "settled",
        "choose",
        "chosen",
        "agreed",
        "agreement",
        "fix",
        "fixed",
        "booked",
    ]

    decision = any(
        word in query_lower
        for word in decision_words
    )

    return {
        "decision": decision
    }


# ==========================================
# 5. DECISION SIGNAL
# ==========================================

def decision_score(text):

    text_lower = text.lower()

    strong_phrases = [
        "fix hai",
        "fixed",
        "final hai",
        "finalized",
        "finalize",
        "booked",
        "book kar",
        "book karte",
        "decided",
        "decision",
        "confirmed",
        "agreed",
        "let's do it",
        "go ahead",
        "done",
        "sorted",
    ]

    score = 0.0

    for phrase in strong_phrases:

        if phrase in text_lower:
            score += 1.0

    return score


# ==========================================
# 6. ACTION / OUTCOME SIGNAL
# ==========================================

def outcome_score(text):

    text_lower = text.lower()

    outcome_phrases = [
        "book kar",
        "booked",
        "fix hai",
        "final hai",
        "finalized",
        "le lenge",
        "lenge",
        "kar dete",
        "kar diya",
        "confirm",
        "confirmed",
        "decided",
        "choose",
        "selected",
        "done",
    ]

    score = 0.0

    for phrase in outcome_phrases:

        if phrase in text_lower:
            score += 1.0

    return score


# ==========================================
# 7. CONCRETE CHOICE SIGNAL
# ==========================================

def concrete_choice_score(text):

    text_lower = text.lower()

    choice_words = [
        "manali",
        "goa",
        "option 1",
        "option 2",
        "option 3",
        "saturday",
        "sunday",
        "python",
        "java",
        "react",
        "hotel",
        "venue",
        "hall",
    ]

    score = 0.0

    for word in choice_words:

        if word in text_lower:
            score += 1.0

    return score


# ==========================================
# 8. GET LOCAL CONTEXT
# ==========================================

def get_context(index, window=3):

    start = max(0, index - window)
    end = min(len(messages), index + window + 1)

    return messages[start:end]


# ==========================================
# 9. SEARCH
# ==========================================

def semantic_search(query, top_k=10):

    # --------------------------------------
    # Step 1: Encode query
    # --------------------------------------

    query_embedding = model.encode(
        query,
        normalize_embeddings=True
    )

    # --------------------------------------
    # Step 2: Semantic similarity
    # --------------------------------------

    scores = embeddings @ query_embedding

    # --------------------------------------
    # Step 3: Get larger candidate pool
    # --------------------------------------

    candidate_count = min(100, len(messages))

    candidate_indices = np.argsort(scores)[::-1][
        :candidate_count
    ]

    # --------------------------------------
    # Step 4: Detect intent
    # --------------------------------------

    intent = detect_query_intent(query)

    results = []

    # --------------------------------------
    # Step 5: Score candidates
    # --------------------------------------

    for index in candidate_indices:

        message = messages[index]

        semantic = float(scores[index])

        final_score = semantic

        decision = decision_score(
            message["text"]
        )

        outcome = outcome_score(
            message["text"]
        )

        concrete = concrete_choice_score(
            message["text"]
        )

        # ----------------------------------
        # Decision-aware ranking
        # ----------------------------------

        if intent["decision"]:

            final_score += 0.030 * decision
            final_score += 0.015 * outcome
            final_score += 0.010 * concrete

        results.append({
            "message": message,
            "semantic_score": semantic,
            "decision_score": decision,
            "outcome_score": outcome,
            "concrete_score": concrete,
            "final_score": final_score,
        })

    # --------------------------------------
    # Step 6: Sort
    # --------------------------------------

    results.sort(
        key=lambda x: x["final_score"],
        reverse=True
    )

    return results[:top_k]


# ==========================================
# 10. PRINT RESULTS WITH CONTEXT
# ==========================================

def print_results(results):

    for rank, result in enumerate(
        results,
        start=1
    ):

        message = result["message"]

        print()
        print("-" * 70)

        print(
            f"#{rank}  "
            f"Semantic: {result['semantic_score']:.4f}  "
            f"Final: {result['final_score']:.4f}"
        )

        print(f"ID:        {message['id']}")
        print(f"Date:      {message['timestamp']}")
        print(f"Sender:    {message['sender']}")
        print(f"Message:   {message['text']}")
        print(f"Thread:    {message['thread']}")

        print(
            f"Decision:  {result['decision_score']:.1f}"
        )

        print(
            f"Outcome:   {result['outcome_score']:.1f}"
        )

        print(
            f"Concrete:  {result['concrete_score']:.1f}"
        )


# ==========================================
# 11. TEST
# ==========================================

if __name__ == "__main__":

    query = "When did we decide on the trip?"

    print()
    print("=" * 70)
    print(f"QUERY: {query}")
    print("=" * 70)

    results = semantic_search(
        query,
        top_k=10
    )

    print_results(results)