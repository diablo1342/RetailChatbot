<h1> RetailChatbot </h1>

## 📝 Overview 📝

Retail Chatbot is a conversational AI application designed to assist customers with product inquiries, recommendations, and order-related questions. It requires users to input their own database in pdf format, and it will search the pdf and provide users with the items that fit their desires.

## How I built it
Backend Framework: FastAPI for serving chatbot queries via REST API.

LLM Engine: OpenAI GPT-4o via LlamaIndex.

Document Indexing: PDF product data loaded using SimpleDirectoryReader and stored in a VectorStoreIndex.

Memory: ChatMemoryBuffer to maintain conversation history for each session.

Session Management: Each session ID maps to an independent OpenAIAgent instance.


## Built with
Python

FastAPI

LlamaIndex

OpenAI GPT-4o

Uvicorn
