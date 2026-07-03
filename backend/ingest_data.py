import os
from dotenv import load_dotenv

from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter
from langchain_core.documents import Document

# 1. Load environment variables
load_dotenv()

# Sahi variable check karein (aapki .env file mein GOOGLE_API_KEY hona chahiye)
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", "db")

if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in .env file")

# 2. Define Documents
documents = [
    Document(page_content="Meeting notes: Discuss project X deliverables."),
    Document(page_content="Reminder: Submit report by Friday."),
    Document(page_content="Upcoming event: Tech conference next Wednesday."),
]

# 3. Initialize Google Embedding Model
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-2",
    google_api_key=GOOGLE_API_KEY
)

# 4. Split text
text_splitter = CharacterTextSplitter(chunk_size=200, chunk_overlap=50)
docs = text_splitter.split_documents(documents)

# 5. Indexing in ChromaDB
vector_db = Chroma.from_documents(
    documents=docs,
    embedding=embeddings,
    persist_directory=CHROMA_DB_PATH,
)

print("Documents successfully indexed using Gemini Embeddings!")



# import os
# from dotenv import load_dotenv

# from langchain_chroma import Chroma
# from langchain_google_genai import GoogleGenerativeAIEmbeddings
# from langchain_text_splitters import CharacterTextSplitter
# from langchain_core.documents import Document

# # Load environment variables
# load_dotenv()

# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
# CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", "db")

# if not GOOGLE_API_KEY:
#     raise ValueError("Google API Key not found in .env")

# documents = [
#     Document(page_content="Meeting notes: Discuss project X deliverables."),
#     Document(page_content="Reminder: Submit report by Friday."),
#     Document(page_content="Upcoming event: Tech conference next Wednesday."),
# ]

# embeddings = GoogleGenerativeAIEmbeddings(
#     model="models/text-embedding-004", 
#     google_api_key=GOOGLE_API_KEY,
# )

# text_splitter = CharacterTextSplitter(
#     chunk_size=200,
#     chunk_overlap=50,
# )

# docs = text_splitter.split_documents(documents)

# vector_db = Chroma.from_documents(
#     documents=docs,
#     embedding=embeddings,
#     persist_directory=CHROMA_DB_PATH,
# )

# print("Documents successfully indexed!")

