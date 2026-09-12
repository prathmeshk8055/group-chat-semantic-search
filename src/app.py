import json
from pathlib import Path

import streamlit as st

from search import semantic_search


# ==========================================
# PROJECT PATHS
# ==========================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

MESSAGES_PATH = PROJECT_ROOT / "data" / "messages.json"


# ==========================================
# LOAD MESSAGES
# ==========================================

with open(MESSAGES_PATH, "r", encoding="utf-8") as f:
    messages = json.load(f)


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Group Chat Semantic Search",
    page_icon="💬",
    layout="wide"
)


# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 36px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .subtitle {
        color: #777;
        font-size: 17px;
        margin-bottom: 25px;
    }

    .answer-box {
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #ddd;
        margin-top: 10px;
        margin-bottom: 20px;
    }

    .message-text {
        font-size: 21px;
        font-weight: 500;
        margin-top: 10px;
    }

    .metadata {
        color: #666;
        font-size: 14px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ==========================================
# HEADER
# ==========================================

st.markdown(
    '<div class="main-title">💬 Group Chat Semantic Search</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Find messages by meaning, even when the query and message '
    'share very few or no words.'
    '</div>',
    unsafe_allow_html=True
)


# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

    st.header("About")

    st.write(
        """
        This system searches a messy group chat containing:

        - 4,000+ messages
        - 8 participants
        - 6 months of conversations
        - Hinglish and English
        - Typos and short messages
        - Decision discussions
        """
    )

    st.divider()

    st.subheader("How it works")

    st.write(
        """
        **1. Query embedding**

        Converts the user's question into a semantic vector.

        **2. Semantic retrieval**

        Finds messages with similar meaning.

        **3. Intent-aware ranking**

        Gives additional weight to decision, outcome,
        and concrete-choice signals.

        **4. Context retrieval**

        Shows nearby messages so the result is not isolated.
        """
    )


# ==========================================
# SEARCH BOX
# ==========================================

query = st.text_input(
    "Search the group chat",
    placeholder="Example: When did we decide on the trip?"
)


# ==========================================
# EXAMPLE QUERIES
# ==========================================

st.markdown("**Try an example:**")

examples = [
    "When did we decide on the trip?",
    "Which hotel option did we choose?",
    "What was the final technical decision?",
    "Where and when was the event booked?"
]

columns = st.columns(4)

for i, example in enumerate(examples):

    with columns[i]:

        if st.button(
            example,
            key=f"example_{i}",
            use_container_width=True
        ):
            query = example


# ==========================================
# SEARCH
# ==========================================

if query:

    with st.spinner("Searching the conversation..."):

        results = semantic_search(
            query,
            top_k=5
        )


    # ======================================
    # BEST RESULT
    # ======================================

    best = results[0]

    message = best["message"]

    st.divider()

    st.subheader("Best Match")

    st.markdown(
        f"""
        <div class="answer-box">

        <div class="metadata">
        👤 <b>{message['sender']}</b>
        &nbsp;&nbsp;•&nbsp;&nbsp;
        🕒 {message['timestamp']}
        </div>

        <div class="message-text">
        "{message['text']}"
        </div>

        <div class="metadata">
        Message ID: {message['id']}
        &nbsp;&nbsp;•&nbsp;&nbsp;
        Relevance: {best['final_score']:.4f}
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    # ======================================
    # CONVERSATION CONTEXT
    # ======================================

    st.subheader("Conversation Context")

    best_index = next(
        (
            i
            for i, item in enumerate(messages)
            if item["id"] == message["id"]
        ),
        None
    )

    if best_index is not None:

        start = max(0, best_index - 3)
        end = min(
            len(messages),
            best_index + 4
        )

        context_messages = messages[start:end]

        for context_message in context_messages:

            is_best = (
                context_message["id"]
                == message["id"]
            )

            if is_best:

                st.markdown(
                    f"""
                    **⭐ {context_message['sender']}**
                    `{context_message['timestamp']}`

                    > {context_message['text']}
                    """
                )

            else:

                st.markdown(
                    f"""
                    **{context_message['sender']}**
                    `{context_message['timestamp']}`

                    {context_message['text']}
                    """
                )


    # ======================================
    # OTHER RESULTS
    # ======================================

    st.subheader("Other Relevant Messages")

    for rank, result in enumerate(
        results[1:],
        start=2
    ):

        result_message = result["message"]

        with st.expander(
            f"#{rank} • "
            f"{result_message['sender']} • "
            f"{result['final_score']:.4f}"
        ):

            st.write(
                result_message["text"]
            )

            st.caption(
                f"ID: {result_message['id']} | "
                f"Time: {result_message['timestamp']}"
            )


# ==========================================
# EMPTY STATE
# ==========================================

else:

    st.info(
        "Enter a natural-language question above to search "
        "the group conversation."
    )