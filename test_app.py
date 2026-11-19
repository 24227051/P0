from unittest.mock import MagicMock, patch
import pytest
import requests

from app import create_app


@pytest.fixture
def client():
    """Cria uma instância da aplicação configurada para testes."""
    app = create_app(
        {
            "TESTING": True,
            "OLLAMA_URL": "http://ollama-mock.local",
            "MODELO": "qwen3.5:9b-q4_K_M",
            "MAX_INPUT_CHARS": 1000,
            "VERIFY_SSL": False,
        }
    )
    with app.test_client() as client:
        yield client


def test_pagina_inicial_retorna_formulario(client):
    """Testa se a rota GET / carrega o HTML inicial corretamente."""
    response = client.get("/")
    html = response.data.decode("utf-8")

    assert response.status_code == 200
    assert "Incluir Texto para Resumo" in html
    assert '<form action="/perguntar" method="POST"' in html


@patch("app.requests.post")
def test_perguntar_llm_sucesso(mock_post, client):
    """Testa o caminho feliz: envio de texto válido e retorno HTML renderizado."""
    mock_response = MagicMock()
    mock_response.json.return_value = {"response": "Resumo gerado com sucesso."}
    mock_response.raise_for_status.return_value = None
    mock_post.return_value = mock_response

    response = client.post("/perguntar", data={"texto_resumo": "Texto longo de exemplo."})
    html = response.data.decode("utf-8")

    assert response.status_code == 200
    assert "Resumo gerado" in html
    assert "Texto longo de exemplo." in html
    assert "Resumo gerado com sucesso." in html

    # Valida se o requests.post foi chamado com os argumentos esperados
    mock_post.assert_called_once()
    args, kwargs = mock_post.call_args
    assert args[0] == "http://ollama-mock.local"
    assert kwargs["json"]["model"] == "qwen3.5:9b-q4_K_M"
    assert kwargs["json"]["stream"] is False
    assert "Texto longo de exemplo." in kwargs["json"]["prompt"]


@pytest.mark.parametrize("payload", [{}, {"texto_resumo": ""}, {"texto_resumo": "   "}])
def test_perguntar_llm_texto_vazio_ou_ausente(client, payload):
    """Testa validação de entrada vazia, apenas espaços ou campo ausente (HTTP 400)."""
    response = client.post("/perguntar", data=payload)
    dados = response.get_json()

    assert response.status_code == 400
    assert dados["erro"] == "O texto não pode estar vazio"


def test_perguntar_llm_excede_limite_caracteres(client):
    """Testa bloqueio quando o texto ultrapassa 1000 caracteres (HTTP 413)."""
    texto_grande = "a" * 1001
    response = client.post("/perguntar", data={"texto_resumo": texto_grande})
    dados = response.get_json()

    assert response.status_code == 413
    assert "excede o limite de 1000 caracteres" in dados["erro"]


@patch("app.requests.post")
def test_perguntar_llm_erro_ssl(mock_post, client):
    """Testa tratamento de erro de certificado SSL (HTTP 500)."""
    mock_post.side_effect = requests.exceptions.SSLError("Certificado inválido")

    response = client.post("/perguntar", data={"texto_resumo": "Texto válido"})
    dados = response.get_json()

    assert response.status_code == 500
    assert dados["erro"] == "Falha na verificação do certificado SSL da LLM."
    assert "Certificado inválido" in dados["detalhes"]


@patch("app.requests.post")
def test_perguntar_llm_timeout(mock_post, client):
    """Testa tratamento de timeout na comunicação com o Ollama (HTTP 504)."""
    mock_post.side_effect = requests.exceptions.Timeout("Tempo esgotado")

    response = client.post("/perguntar", data={"texto_resumo": "Texto válido"})
    dados = response.get_json()

    assert response.status_code == 504
    assert dados["erro"] == "Timeout ao conectar ou aguardar a LLM"


@patch("app.requests.post")
def test_perguntar_llm_connection_error(mock_post, client):
    """Testa tratamento quando o servidor da LLM está fora do ar (HTTP 502)."""
    mock_post.side_effect = requests.exceptions.ConnectionError("Conexão recusada")

    response = client.post("/perguntar", data={"texto_resumo": "Texto válido"})
    dados = response.get_json()

    assert response.status_code == 502
    assert dados["erro"] == "LLM inacessível"
    assert "Conexão recusada" in dados["detalhes"]


@patch("app.requests.post")
def test_perguntar_llm_erro_http_generico(mock_post, client):
    """Testa tratamento de erro HTTP retornado pelo Ollama, ex: 500 ou 404 (HTTP 500)."""
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("500 Server Error")
    mock_post.return_value = mock_response

    response = client.post("/perguntar", data={"texto_resumo": "Texto válido"})
    dados = response.get_json()

    assert response.status_code == 500
    assert dados["erro"] == "Erro ao conectar na LLM interna"