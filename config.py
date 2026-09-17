from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

# ------------------------------------------------------------> Start Up Code -----------------------------------------------
load_dotenv()

# -------------------- File paths
music_filepath = "music/into_to_music.pdf"
archeology_filepath = "archeology/archeology_starter.pdf"

# ---------------------------------- chroma db filepaths
chroma_music_path = 'Chroma_db/music'
chroma_arch_path = 'Chroma_db/archeology'

DB_URI = os.getenv("DATABASE_URL")
print("DB_URI Loaded: ", bool(os.getenv("DATABASE_URL")))
print("Groq Key Loaded:", bool(os.getenv("GROQ_API_KEY")))

# ------------------------ RAG as a tool: END
llm = ChatGroq(model="openai/gpt-oss-20b", temperature=0)