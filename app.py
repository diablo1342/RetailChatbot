import streamlit as st
from llama_index.llms.openai import OpenAI
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.agent.openai import OpenAIAgent
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.core.memory import ChatMemoryBuffer

# -------------------
# Setup LlamaIndex
# -------------------
st.set_page_config(page_title="PDF Chatbot", layout="wide")

@st.cache_resource
def load_agent():
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
                "or descriptions. Always clarify color, price, and type of clothes before answering. "
                "Use the pdf, do not use the web at all. Your point is to browse the products in the pdf."

            )
        )
    )

    memory = ChatMemoryBuffer.from_defaults(token_limit=3000)
    agent = OpenAIAgent.from_tools([tool], llm=llm, verbose=True, memory=memory)
    return agent

agent = load_agent()

# -------------------
# Streamlit UI
# -------------------
st.title("📝 PDF Chatbot")
st.write("Ask me anything about your product PDFs!")

# Keep chat history in session
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display previous messages
for role, msg in st.session_state["messages"]:
    if role == "user":
        st.chat_message("user").write(msg)
    else:
        st.chat_message("assistant").write(msg)

# Input box
if prompt := st.chat_input("Type your question here..."):
    # Add user message
    st.session_state["messages"].append(("user", prompt))
    st.chat_message("user").write(prompt)

    # Run agent
    response = agent.chat(prompt)
    answer = response.response

    # Add assistant message
    st.session_state["messages"].append(("assistant", answer))
    st.chat_message("assistant").write(answer)
