# 🛠️ Troubleshooting Guide

## 1. KIND Cluster Issues
- **Problem**: `kind create cluster` fails.
  - **Solution**: Ensure Docker is running. Run `docker system prune` if storage is full.
- **Problem**: Image not found in pods.
  - **Solution**: Run `kind load docker-image smartsupport-backend:latest --name smartsupport-cluster`.

## 2. API / Backend Issues
- **Problem**: 404 Model Not Found.
  - **Solution**: Check `.env` for correct API Keys. Ensure `gemini-flash-latest` is used.
- **Problem**: 429 Quota Exceeded.
  - **Solution**: Wait 60 seconds. Free tier has low rate limits.

## 3. RAG / Vector DB
- **Problem**: AI says "I don't know" for company policies.
  - **Solution**: Run `python smartsupport_ai/ingestion/embed_store.py` to re-index the data.
