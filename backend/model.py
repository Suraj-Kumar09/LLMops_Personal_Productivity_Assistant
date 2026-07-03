import os
from dotenv import load_dotenv

from langchain_chroma import Chroma
from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    GoogleGenerativeAIEmbeddings,
)
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 1. Load environment variables
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", "db")

if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in .env file")

# 3. Initialize Google Embedding Model
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-2",
    google_api_key=GOOGLE_API_KEY
)

# 3. Load Vector Database
vector_db = Chroma(
    persist_directory=CHROMA_DB_PATH, 
    embedding_function=embeddings
)
retriever = vector_db.as_retriever(search_kwargs={"k": 3})

# 4. Initialize Gemini LLM
# llm = ChatGoogleGenerativeAI(
#     model="gemini-2.5-flash",
#     temperature=1.7
# )

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=GOOGLE_API_KEY,
    temperature=0.3
)

# 5. Define Prompt Template
prompt = ChatPromptTemplate.from_template(
    """
You are an AI Personal Productivity Assistant.
Use the following context to answer the user's question. 
If the answer is not in the context, say you don't know.

Context:
{context}

Question:
{question}

Answer:
"""
)

parser = StrOutputParser()

# 6. Response Function

# 6. Response Function
def get_response(query: str):

    # -------------------------------
    # Greeting Handling
    # -------------------------------
    greetings = [
        "hi",
        "hello",
        "hey",
        "good morning",
        "good afternoon",
        "good evening"
    ]

    if query.lower().strip() in greetings:
        return "Hello! How can I help you today?"

    # -------------------------------
    # Retrieve Relevant Documents
    # -------------------------------
    docs = retriever.invoke(query)

    print("=" * 50)
    print("Retrieved Documents")
    print("=" * 50)

    for doc in docs:
        print(doc.page_content)

    context = "\n\n".join(doc.page_content for doc in docs)

    print("\nContext Sent to Gemini:\n")
    print(context)

    # -------------------------------
    # Generate Response
    # -------------------------------
    chain = prompt | llm | parser

    response = chain.invoke(
        {
            "context": context,
            "question": query
        }
    )

    return response
