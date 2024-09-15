# 21BCE1310_ML

Backend for Document Retrieval

The development of a document retrieval system intended to provide context for Large Language Models (LLMs) in chat applications is available in this repository.

Features

Document Retrieval System: Effective backend that enables database-stored documents to be retrieved. Responses that have been cached are more quickly retrieved and provide the best possible system performance. Background Task: When the server first starts, it scrapes news articles in a different thread. Application Dockerized: Docker is used to containerize the backend. Rate-limiting: Provides a 5-request limit to customers before raising an HTTP 429 error. API Logging: Records all API calls, including the time it takes to interpret each one. Final Destinations

/health: Verifies that the API is operational. Top search results are returned via /search, which takes query parameters like text, top_k, and threshold into account. Beginning

Required conditions Docker Python 3.x or
