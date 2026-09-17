from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_community.document_loaders import PDFMinerLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.tools import tool
import os
from config import llm, music_filepath, chroma_arch_path, chroma_music_path, archeology_filepath

pdf_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap = 150)
embeddings = OllamaEmbeddings(model = "nomic-embed-text")

# --------------------- General Functions for generating the retriever
def load_pdfs(file_path_pdf):
    loader = PDFMinerLoader(file_path=file_path_pdf)
    file = loader.load()
    return file

def pdf_chunks(file):
    split_pdf = pdf_splitter.split_documents(file)
    return split_pdf

def get_or_create_vectorstore_retriever(chroma_path: str, collection_name: str, file_path_pdf: str):
    if not os.path.exists(chroma_path) or not os.listdir(chroma_path):
        
        print("No existing directory --> creating new vectorstore\n")
        
        # -> load and split pdf
        file = load_pdfs(file_path_pdf=file_path_pdf)
        chunks = pdf_chunks(file)
        
        # create vectorstore
        vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            collection_name= collection_name,
            persist_directory=chroma_path
        )
        retriever = vectorstore.as_retriever()
        return retriever
    
    else:
        try:
            print("FOUND vectorstore --> LOADING existing vectorstore")
            vectorstore = Chroma(
                collection_name= collection_name,
                embedding_function= embeddings,
                persist_directory= chroma_path
            )
            m_retriever = vectorstore.as_retriever()
            return m_retriever
        except Exception as e:
            print(f"Error loading existing DB ({e}). Rebuilding from source...")
            # Fall back to creating a fresh vectorstore
            file = load_pdfs(file_path_pdf=file_path_pdf)
            chunks = pdf_chunks(file)
            vectorstore = Chroma.from_documents(
                documents=chunks,
                embedding=embeddings,
                collection_name=collection_name,
                persist_directory=chroma_path
            )
            return vectorstore.as_retriever()

# ----------------------- build retriever
m_retriever = get_or_create_vectorstore_retriever(chroma_music_path, "music", file_path_pdf= music_filepath)
arch_retriever = get_or_create_vectorstore_retriever(chroma_arch_path, "arch", file_path_pdf= archeology_filepath)

# ------------------------ create tools
def get_tools():
    """You get the two retriever tools"""
    # ----------------------- create retrievers tool
    @tool
    def music_retriever_tool(query:str):
        "In every question about music or music carrer use this tool to retrieve relevant documents"
        
        result = m_retriever.invoke(query)
        print("---- Tool was called----")
        return "\n\n".join([doc.page_content for doc in result])

    @tool
    def arch_retriever_tool(query:str):
        "In every question about archeology or archeology carrer use this tool to retrieve relevant documents"
        
        result = arch_retriever.invoke(query)
        print("---- Tool was called----")
        return "\n\n".join([doc.page_content for doc in result])
    
    return [music_retriever_tool, arch_retriever_tool]

tools = get_tools()

llm_with_tools = llm.bind_tools(tools=tools)