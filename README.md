# Group Chat Semantic Search

A semantic search engine for finding relevant messages in a large, messy group chat.

The system is designed to answer natural-language questions even when the query and the relevant message use different words or contain little to no word overlap.

## Problem

Searching a large group chat using keyword matching is often ineffective.

For example:

> "When did we decide on the trip?"

The actual message may be:

> "Chalo Manali fix hai. Hotel option 2 book kar dete hain."

The query and answer do not share the important words needed for a simple keyword search.

This project uses semantic embeddings and intent-aware ranking to retrieve the relevant message.

---

## Features

- Semantic search using BGE-M3 embeddings
- Handles English and Hinglish/code-mixed messages
- Works with noisy chat data
- Decision-aware ranking
- Outcome and concrete-choice detection
- Conversation context around the retrieved message
- Supports natural-language queries
- Evaluation on 40 test queries
- Includes 8 hard zero-word-overlap queries
- Interactive Streamlit demo

---

## Dataset

The synthetic dataset contains:

- 4,115 messages
- 8 participants
- 6 months of conversation
- English and Hinglish messages
- Typos
- Short replies
- Forwarded-style messages
- Media-omitted messages
- Decision-oriented conversations
- Three structured decision threads

The three major decision threads cover:

1. Trip planning
2. Project implementation
3. Event planning

---
## What's Mocked

The chat corpus is synthetic and generated specifically for this assignment.

The following are mocked:

- Group chat messages
- Participant names
- Timestamps
- Conversation history
- Decision-making conversations
- Test queries and ground-truth message IDs

The semantic search pipeline itself is implemented and runs locally using the BGE-M3 embedding model.

## Architecture

```text
User Query
    |
    v
Query Embedding
    |
    v
BGE-M3 Semantic Retrieval
    |
    v
Candidate Messages
    |
    v
Intent-Aware Reranking
    |
    +---- Decision signals
    |
    +---- Outcome signals
    |
    +---- Concrete choice signals
    |
    v
Best Matching Message
    |
    v
Conversation Context
