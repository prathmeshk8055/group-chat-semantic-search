import json
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer


# -----------------------------
# 1. Paths
# -----------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

MESSAGES_PATH = PROJECT_ROOT / "data" / "messages.json"
EMBEDDINGS_PATH = PROJECT_ROOT / "data" / "embeddings.npy"


# -----------------------------
# 2. Load the chat messages
# -----------------------------

with open(MESSAGES_PATH, "r", encoding="utf-8") as f:
    messages = json.load(f)


print(f"Loaded {len(messages)} messages.")


# -----------------------------
# 3. Load the embedding model
# -----------------------------

print("Loading embedding model...")

model = SentenceTransformer("BAAI/bge-m3")

print("Embedding model loaded.")


# -----------------------------
# 4. Extract message text
# -----------------------------

def build_context(messages, index, window=2):
    """
    Build a small conversation context around a message.

    The current message is included together with
    a few messages before and after it.
    """

    start = max(0, index - window)
    end = min(len(messages), index + window + 1)

    context_parts = []

    for i in range(start, end):
        message = messages[i]

        if i == index:
            prefix = "CURRENT MESSAGE"
        elif i < index:
            prefix = "PREVIOUS MESSAGE"
        else:
            prefix = "NEXT MESSAGE"

        context_parts.append(
            f"{prefix} | "
            f"{message['sender']}: "
            f"{message['text']}"
        )

    return "\n".join(context_parts)


texts = [
    build_context(messages, index, window=2)
    for index in range(len(messages))
]

# -----------------------------
# 5. Generate embeddings
# -----------------------------

print("Generating embeddings...")

embeddings = model.encode(
    texts,
    batch_size=32,
    show_progress_bar=True,
    normalize_embeddings=True,
)

embeddings = np.asarray(embeddings)


# -----------------------------
# 6. Save embeddings
# -----------------------------

np.save(EMBEDDINGS_PATH, embeddings)


# -----------------------------
# 7. Display information
# -----------------------------

print()
print("=" * 50)
print("Embeddings generated successfully!")
print("=" * 50)

print(f"Messages:   {len(messages)}")
print(f"Shape:      {embeddings.shape}")
print(f"Saved to:   {EMBEDDINGS_PATH}")