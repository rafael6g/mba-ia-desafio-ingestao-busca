import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_postgres import PGVector

load_dotenv()

PDF_PATH = os.getenv("PDF_PATH", "document.pdf")
CONNECTION_STRING = os.getenv("DATABASE_URL")
COLLECTION_NAME = "pdf_collection"

def ingest_pdf():
    print(f"1. Carregando o PDF: {PDF_PATH}...")
    loader = PyPDFLoader(PDF_PATH)
    docs = loader.load()

    print("2. Dividindo o documento em chunks (Requisito: 1000 chars, 150 overlap)...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=150
    )
    chunks = text_splitter.split_documents(docs)
    print(f"   -> Foram gerados {len(chunks)} chunks.")

    print("3. Gerando Embeddings e salvando no PostgreSQL (pgVector)...")
    api_key = os.getenv("GOOGLE_API_KEY")
    os.environ["GOOGLE_API_KEY"] = api_key
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        api_key=api_key,
        transport="rest"
    )

    vector_store = PGVector(
        embeddings=embeddings,
        collection_name=COLLECTION_NAME,
        connection=CONNECTION_STRING,
        use_jsonb=True,
    )

    vector_store.create_tables_if_not_exists()

    import time
    batch_size = 5
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i + batch_size]
        print(f"   -> Enviando lote {i//batch_size + 1} de {len(chunks)//batch_size + 1}...")
        vector_store.add_documents(batch)
        time.sleep(10)

    print("✅ Ingestão concluída com sucesso!")

if __name__ == "__main__":
    ingest_pdf()