import os
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from typing import Dict

from llama_index.llms.openai import OpenAI
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.agent.openai import OpenAIAgent
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.core.memory import ChatMemoryBuffer





documents = SimpleDirectoryReader("pdf folder").load_data()
index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine()


llm = OpenAI(model="gpt-4o", temperature=0)


tool = QueryEngineTool(
    query_engine=query_engine,
    metadata=ToolMetadata(
        name="ProductPDF",
        description=(
            "Answer any product-related questions, including listing, pricing, filtering, "
            "or descriptions. Always clarify color, price, and type of clothes before answering."
            "If the user clarifies only one of these things, ask them about the others before giving them a list of "
            "the products they want."
        )
    )
)

# -------------------
# Session Store
# -------------------
sessions: Dict[str, OpenAIAgent] = {}

def get_agent_for_session(session_id: str) -> OpenAIAgent:
    if session_id not in sessions:
        memory = ChatMemoryBuffer.from_defaults(token_limit=3000)
        sessions[session_id] = OpenAIAgent.from_tools(
            [tool],
            llm=llm,
            verbose=True,
            memory=memory
        )
        print(f"✅ Created new session: {session_id}")
    return sessions[session_id]


app = FastAPI()

class QueryInput(BaseModel):
    session_id: str
    prompt: str

@app.post("/query/")
def query_data(input: QueryInput):
    try:
        agent = get_agent_for_session(input.session_id)

        # Use chat(), not query(), so memory actually updates
        response = agent.chat(input.prompt)

        print(f"[{input.session_id}] User: {input.prompt}")
        print(f"[{input.session_id}] Agent: {response.response}")

        return {"response": response.response}
    except Exception as e:
        return {"error": str(e)}

# -------------------
# Run
# -------------------
if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000)  # No reload=True
