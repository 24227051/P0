import os
import sys
from dotenv import load_dotenv
from ollama import Client

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Nome do modelo especificado no requisito
MODEL_NAME = "qwen3.5:9b-q4_K_M"


def main():
    # 1. Recupera o endereço do host das variáveis de ambiente
    ollama_host = os.getenv("OLLAMA_HOST")

    if not ollama_host:
        print(
            "❌ Erro: A variável de ambiente OLLAMA_HOST não foi configurada.",
            file=sys.stderr,
        )
        print(
            "Certifique-se de criar o arquivo .env conforme as instruções do README.",
            file=sys.stderr,
        )
        sys.exit(1)

    print("🤖 Inicializando cliente LLM...")
    # Inicializa o cliente apontando para a URL interna
    client = Client(host=ollama_host)

    print("\n--- Resumidor de Textos Longos via LLM ---")
    print("Digite ou cole o texto longo que deseja resumir.")
    print("Digite o texto. Escreva FIM em uma linha separada:")

    linhas = []
    for linha in sys.stdin:
        if linha.rstrip("\r\n") == "FIM":
            break
        linhas.append(linha)

    user_input = "".join(linhas).strip()

    if not user_input:
        print("⚠️ Nenhum texto foi inserido. Encerrando aplicação.")
        sys.exit(0)

    # Engenharia de prompt básica para focar no objetivo: Resumir
    prompt_sistema = (
        "Você é um assistente especializado em síntese de informações. "
        "Seu objetivo é resumir o texto fornecido pelo usuário de forma clara, "
        "concisa e destacando os pontos principais em português."
    )

    print("\n🔄 Enviando solicitação ao LLM e processando resposta...\n")

    # 3. Envia a solicitação à interface programática (API)
    try:
        response = client.chat(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": prompt_sistema},
                {"role": "user", "content": user_input},
            ],
        )

        # 4. Processa e apresenta o resultado ao usuário
        resumo = response["message"]["content"]
        print("📝 --- RESUMO GERADO ---")
        print(resumo)
        print("------------------------")

    except Exception as e:
        print(f"❌ Erro ao comunicar-se com o servidor LLM: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
