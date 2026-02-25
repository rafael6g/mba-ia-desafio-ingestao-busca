# import os
# from dotenv import load_dotenv
# from langchain_google_genai import GoogleGenerativeAIEmbeddings
# from langchain_postgres import PGVector

# load_dotenv()

# PROMPT_TEMPLATE = """CONTEXTO:
# {contexto}

# REGRAS:
# - Responda somente com base no CONTEXTO.
# - Se a informação não estiver explicitamente no CONTEXTO, responda:
#   "Não tenho informações necessárias para responder sua pergunta."
# - Nunca invente ou use conhecimento externo.
# - Nunca produza opiniões ou interpretações além do que está escrito.

# EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
# Pergunta: "Qual é a capital da França?"
# Resposta: "Não tenho informações necessárias para responder sua pergunta."

# Pergunta: "Quantos clientes temos em 2024?"
# Resposta: "Não tenho informações necessárias para responder sua pergunta."

# Pergunta: "Você acha isso bom ou ruim?"
# Resposta: "Não tenho informações necessárias para responder sua pergunta."

# PERGUNTA DO USUÁRIO:
# {pergunta}

# RESPONDA A "PERGUNTA DO USUÁRIO"
# """

# def realizar_busca(query, k=10):
#     """
#     Função obrigatória para buscar os 10 resultados mais relevantes no pgVector.
#     """
#     embeddings = GoogleGenerativeAIEmbeddings(model=os.getenv("GOOGLE_EMBEDDING_MODEL"))
    
#     vectorstore = PGVector(
#         connection=os.getenv("DATABASE_URL"),
#         embeddings=embeddings,
#         collection_name=os.getenv("PG_VECTOR_COLLECTION_NAME", "pdf_collection"),
#     )

#     # Retorna (Documento, Score)
#     return vectorstore.similarity_search_with_score(query, k=k)

# def search_prompt(contexto, pergunta):
#     """
#     Preenche o template com o contexto recuperado e a pergunta do usuário.
#     """
#     return PROMPT_TEMPLATE.format(contexto=contexto, pergunta=pergunta)

import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_postgres import PGVector

load_dotenv()

PROMPT_TEMPLATE = """CONTEXTO:
{contexto}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""

def realizar_busca(query, k=10):
    # Lemos do .env para manter a segurança
    api_key = os.getenv("GOOGLE_API_KEY")
    # Aqui usamos o nome correto do modelo que o Google exige agora
    model_name = os.getenv("GOOGLE_EMBEDDING_MODEL") 
    
    # Criamos o objeto de embeddings com as travas necessárias para Windows
    embeddings = GoogleGenerativeAIEmbeddings(
        model=model_name,
        google_api_key=api_key,
        transport="rest" # Isso evita que o código procure credenciais que não existem
    )
    
    vectorstore = PGVector(
        connection=os.getenv("DATABASE_URL"),
        embeddings=embeddings,
        collection_name=os.getenv("PG_VECTOR_COLLECTION_NAME", "pdf_collection"),
        use_jsonb=True # Garante compatibilidade com o que foi ingerido
    )

    # Retorna (Documento, Score)
    return vectorstore.similarity_search_with_score(query, k=k)

def search_prompt(contexto, pergunta):
    return PROMPT_TEMPLATE.format(contexto=contexto, pergunta=pergunta)