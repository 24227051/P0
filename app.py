import os
import requests
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# Configurações do LLM interno
OLLAMA_URL = os.getenv("OLLAMA_URL")
MODELO = "qwen3.5:9b-q4_K_M"


@app.route("/", methods=["GET"])
def pagina_inicial():
    # Interface web para incluir o prompt e enviar para a LLM interna
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Interface LLM - P0 - Resumidor de Textos</title>
        <meta charset="utf-8">
    </head>
    <body style="font-family: Arial, sans-serif; margin: 40px; background-color: #f4f4f9;">
        <h2>Incluir Texto para Resumo (limite 1000 caracteres)</h2>
        <form action="/perguntar" method="POST" style="margin-bottom: 20px;">
            <textarea name="texto_resumo" rows="5" cols="60" maxlength="1000" placeholder="Digite seu texto aqui..." required></textarea><br><br>
            <button type="submit" style="padding: 10px 20px; cursor: pointer;">Enviar para LLM</button>
        </form>
    </body>
    </html>
    """
    return render_template_string(html_content)


@app.route("/perguntar", methods=["POST"])
def perguntar_llm():

    MAX_INPUT_CHARS = 1_000

    user_input = request.form.get("texto_resumo").strip()

    if not user_input:
        return jsonify({"erro": "O texto não pode estar vazio"}), 400

    if len(user_input) > MAX_INPUT_CHARS:
        return jsonify({
            "erro": f"O texto excede o limite de {MAX_INPUT_CHARS} caracteres"
        }), 413

    prompt_sistema = "Você é um assistente especializado em síntese de informações. Seu objetivo é resumir o texto fornecido pelo usuário de forma clara, concisa e destacando os pontos principais em português."
    prompt = f"{prompt_sistema}\n\nTexto do usuário:\n{user_input}"

    payload = {"model": MODELO, "prompt": prompt, "stream": False}
    headers = {"Content-Type": "application/json"}

    try:
        # IMPORTANTE (Conforme Manual pág 3): Manter validação SSL ativa em produção.
        # Caso ocorra falha de CA interna da instituição, o administrador deve fornecer
        # o certificado para ser configurado no container, em vez de desativar a verificação.
        resposta = requests.post(
            OLLAMA_URL,
            json=payload,
            headers=headers,
            verify=False,  # DESATIVADO APENAS PARA TESTE LOCAL; em produção deve ser True
            timeout=(5, 360),  # conexão, resposta
        )
        resposta.raise_for_status()

        dados_retorno = resposta.json()
        resultado = dados_retorno.get("response", "Sem resposta da LLM.")

        # return jsonify({"prompt_enviado": prompt, "resposta_llm": resultado})
        return render_template_string(
            """
            <!DOCTYPE html>
            <html lang="pt-BR">
            <head>
                <meta charset="UTF-8">
                <title>Resumo</title>
            </head>
            <body style="font-family: Arial; margin: 40px;">
                <h2>Resumo gerado</h2>
                <p><strong>Texto enviado:</strong></p>
                <p>{{ prompt }}</p>

                <p><strong>Resposta da LLM:</strong></p>
                <div style="white-space: pre-wrap;">{{ resposta }}</div>

                <br>
                <a href="/">Fazer outro resumo</a>
            </body>
            </html>
            """,
            prompt=prompt,
            resposta=resultado,
        )

    except requests.exceptions.SSLError as ssl_err:
        return (
            jsonify(
                {
                    "erro": "Falha na verificação do certificado SSL da LLM.",
                    "detalhes": str(ssl_err),
                    "ajuda": "Verifique os certificados CA ou a data/hora do servidor conforme o FAQ do manual.",
                }
            ),
            500,
        )

    except requests.exceptions.Timeout:
        return jsonify({"erro": "Timeout ao conectar ou aguardar a LLM"}), 504
    except requests.exceptions.ConnectionError as err:
        return jsonify({"erro": "LLM inacessível", "detalhes": str(err)}), 502

    except Exception as e:
        return (
            jsonify({"erro": "Erro ao conectar na LLM interna", "detalhes": str(e)}),
            500,
        )


if __name__ == "__main__":
    # Localmente para desenvolvimento (em produção o Gunicorn assumirá na porta 80 continuamente)
    app.run(host="0.0.0.0", port=8080)