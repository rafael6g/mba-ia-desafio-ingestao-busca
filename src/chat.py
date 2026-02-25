
import os
from dotenv import load_dotenv
from search import realizar_busca, search_prompt
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

def main():
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
            pergunta_usuario = input("\nPERGUNTA: ")
            
            if pergunta_usuario.lower().strip() in ['sair', 'exit', 'quit']:
                print("\nEncerrando o chat. Até logo!")
                break
            
            if not pergunta_usuario.strip():
                continue

            resultados = realizar_busca(pergunta_usuario, k=10)
            contexto_concatenado = "\n\n".join([doc.page_content for doc, score in resultados])
            prompt_final = search_prompt(contexto=contexto_concatenado, pergunta=pergunta_usuario)
            resposta = llm.invoke(prompt_final)

            print(f"RESPOSTA: {resposta.content}")
            print("-" * 50)

        except KeyboardInterrupt:
            print("\nOperação cancelada pelo usuário.")
            break
        except Exception as e:
            print(f"❌ Ocorreu um erro durante a interação: {e}")

if __name__ == "__main__":
    main()