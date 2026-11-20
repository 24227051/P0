import os
import requests
from flask import Flask, current_app, jsonify, render_template_string, request

HTML_INDEX = """
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

HTML_RESULTADO = """
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
"""

PROMPT_SISTEMA = (
    "Você é um assistente especializado em síntese de informações. "
    "Seu objetivo é resumir o texto fornecido pelo usuário de forma clara, "
    "concisa e destacando os pontos principais em português."
)


def gerar_resumo(texto_usuario: str, ollama_url: str, modelo: str, verify_ssl: bool = False) -> tuple[str, str]:
    """Monta o prompt e realiza a chamada HTTP para a API do Ollama."""
    if not ollama_url:
        raise ValueError("A variável de ambiente OLLAMA_URL não está configurada.")

    prompt = f"{PROMPT_SISTEMA}\n\nTexto do usuário:\n{texto_usuario}"
    payload = {"model": modelo, "prompt": prompt, "stream": False}
    headers = {"Content-Type": "application/json"}

    resposta = requests.post(
        ollama_url,
        json=payload,
        headers=headers,
        verify=verify_ssl,
        timeout=(5, 600),
    )
    resposta.raise_for_status()

    dados_retorno = resposta.json()
    resultado = dados_retorno.get("response", "Sem resposta da LLM.")
    return prompt, resultado


def create_app(test_config: dict | None = None) -> Flask:
    """Application Factory do Flask."""
    app = Flask(__name__)

    app.config.from_mapping(
        OLLAMA_URL=os.getenv("OLLAMA_URL"),
        MODELO="qwen3.5:9b-q4_K_M",
        MAX_INPUT_CHARS=1_000,
        VERIFY_SSL=False,
    )

    if test_config:
        app.config.update(test_config)

    @app.route("/", methods=["GET"])
    def pagina_inicial():
        return render_template_string(HTML_INDEX)

    @app.route("/perguntar", methods=["POST"])
    def perguntar_llm():
        max_chars = app.config["MAX_INPUT_CHARS"]
        user_input = (request.form.get("texto_resumo") or "").strip()

        if not user_input:
            return jsonify({"erro": "O texto não pode estar vazio"}), 400

        if len(user_input) > max_chars:
            return jsonify({"erro": f"O texto excede o limite de {max_chars} caracteres"}), 413

        try:
            prompt, resultado = gerar_resumo(
                texto_usuario=user_input,
                ollama_url=app.config["OLLAMA_URL"],
                modelo=app.config["MODELO"],
                verify_ssl=app.config["VERIFY_SSL"],
            )
            return render_template_string(HTML_RESULTADO, prompt=prompt, resposta=resultado)

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
            return jsonify({"erro": "Erro ao conectar na LLM interna", "detalhes": str(e)}), 500

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8080)