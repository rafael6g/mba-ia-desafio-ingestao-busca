# from search import search_prompt

# def main():
#     chain = search_prompt()

#     if not chain:
#         print("Não foi possível iniciar o chat. Verifique os erros de inicialização.")
#         return
    
#     pass

# if __name__ == "__main__":
#     main()

import os
from dotenv import load_dotenv
from search import realizar_busca, search_prompt
from langchain_google_genai import ChatGoogleGenerativeAI

# 1. Carregar variáveis de ambiente
load_dotenv()

def main():
    # Inicializa o LLM conforme os requisitos
    # Usamos o nome exato validado no seu check_llm.py
    llm = ChatGoogleGenerativeAI(
        model=os.getenv("GOOGLE_CHAT_MODEL", "models/gemini-2.5-flash-lite"),
        temperature=0
    )

    print("\n" + "="*50)
    print(" MBA IA - CLI CHATBOT ATIVADO ".center(50, "="))
    print("="*50)
    print("Digite sua pergunta ou 'sair' para encerrar.")

    while True:
        try:
            # Entrada do usuário
            pergunta_usuario = input("\nPERGUNTA: ")
            
            # Condição de saída
            if pergunta_usuario.lower().strip() in ['sair', 'exit', 'quit']:
                print("\nEncerrando o chat. Até logo!")
                break
            
            if not pergunta_usuario.strip():
                continue

            # 1. Busca os 10 resultados mais relevantes (Requisito k=10)
            # A função retornar uma lista de tuplas (Document, Score)
            resultados = realizar_busca(pergunta_usuario, k=10)
            
            # 2. Concatena o conteúdo dos documentos recuperados para o contexto
            contexto_concatenado = "\n\n".join([doc.page_content for doc, score in resultados])

            # 3. Monta o prompt final usando a função do search.py
            # Isso aplica as REGRAS e os EXEMPLOS exigidos no desafio
            prompt_final = search_prompt(contexto=contexto_concatenado, pergunta=pergunta_usuario)

            # 4. Chama a LLM para gerar a resposta baseada apenas no contexto
            resposta = llm.invoke(prompt_final)

            # Exibe a resposta final para o usuário
            print(f"RESPOSTA: {resposta.content}")
            print("-" * 50)

        except KeyboardInterrupt:
            print("\nOperação cancelada pelo usuário.")
            break
        except Exception as e:
            print(f"❌ Ocorreu um erro durante a interação: {e}")

if __name__ == "__main__":
    main()