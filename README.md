# Desafio MBA Engenharia de Software com IA - Full Cycle

 a frase padrão de segurança:  *"Não tenho informações necessárias para responder sua pergunta."* .

Este projeto implementa um sistema de **RAG (Retrieval-Augmented Generation)** capaz de ler um arquivo PDF, processar seu conteúdo em vetores e permitir uma interação via chat por linha de comando (CLI). O sistema utiliza a pilha tecnológica do LangChain integrando o banco de dados PostgreSQL (com pgVector) e os modelos de IA do Google Gemini.

## Tecnologias Utilizadas

* **Linguagem:** Python 3.11+
* **Framework:** LangChain
* **Banco de Dados:** PostgreSQL com extensão **pgVector**
* **IA (LLM & Embeddings):** Google Gemini (Modelos: `gemini-2.5-flash-lite` e `gemini-embedding-001`)
* **Containerização:** Docker e Docker Compose

## Requisitos e Configuração

### 1. Ambiente Virtual e Dependências

Crie e ative um ambiente virtual antes de instalar as dependências:

**PowerShell**

```
python -m venv venv
.\venv\Scripts\activate  # No Windows
# ou
source venv/bin/activate  # No Linux/Mac
```

Instale os pacotes necessários:

**PowerShell**

```
pip install -r requirements.txt
```

### 2. Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto com as seguintes chaves:

**Snippet de código**

```
GOOGLE_API_KEY=Sua_Chave_Aqui
GOOGLE_EMBEDDING_MODEL=models/gemini-embedding-001
GOOGLE_CHAT_MODEL=models/gemini-2.5-flash-lite
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/rag
PG_VECTOR_COLLECTION_NAME=pdf_collection
PDF_PATH=document.pdf
```

## Ordem de Execução

Siga rigorosamente esta ordem para garantir o funcionamento do sistema:

### 1. Subir o Banco de Dados

Certifique-se de que o Docker Desktop esteja rodando e execute:

**PowerShell**

```
docker compose up -d
```

### 2. Executar Ingestão do PDF

Este script divide o PDF em chunks de 1000 caracteres (overlap de 150), gera os embeddings e salva no Postgres:

**PowerShell**

```
python src/ingest.py
```

### 3. Iniciar o Chat

Após a conclusão da ingestão, inicie a interface de conversa:

**PowerShell**

```
python src/chat.py
```

## Testes de Validação

O sistema foi configurado com regras rígidas para responder apenas com base no contexto do documento fornecido.

* **Pergunta no Contexto:** "Qual o faturamento da Empresa SuperTechIABrazil?" -> Deve responder o valor presente no PDF.
* **Pergunta fora do Contexto:** "Qual é a capital da França?" -> Deve responder a frase padrão de segurança:  *"Não tenho informações necessárias para responder sua pergunta."* .
