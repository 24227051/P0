# P0 — Resumidor de Textos com LLM

Aplicação web desenvolvida em Python e Flask para enviar textos a um servidor
interno do Ollama e exibir o resumo gerado pelo modelo
`qwen3.5:9b-q4_K_M`.

## Arquitetura

- Flask recebe as requisições HTTP.
- A rota `/` exibe o formulário web.
- A rota `/perguntar` envia o texto para a API do Ollama.
- Gunicorn é utilizado para executar a aplicação em produção.

## Pré-requisitos

- Python 3.12 ou superior
- Acesso ao servidor interno do Ollama
- Docker Desktop

## Execução

### 1. Clonar o repositório

```bash
git clone https://github.com/24227051/P0.git
cd P0
```

### 2. Criar e ativar o ambiente virtual

No Windows:

```powershell
python -m venv venv
.\venv\Scripts\activate
```

No Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 4. Criar container

- Criar a imagem

```powershell
docker build -t p0-resumidor:1.0 .
```

- Para gerar um arquivo da imagem:

```powershell
docker save -o p0-resumidor.tar p0-resumidor:1.0
```

### 5. Implantar no Devel LLM Portal

Acesse o ambiente de institucional:

- Clique em: Enviar container

- Preencha a Porta do container
```env
8080
```

- Preencha as Variáveis de ambiente
```env
OLLAMA_URL=https://llm-internal.softex:9001/api/generate
```

- Em Arquivo .tar da Imagem Docker, Clique em Escolher Arquivo
e selecione o arquivo .tar gerado anteriormente

- Clique em: Enviar

### 6. Iniciar a aplicação

- Clique em: Iniciar
- Clique em: Abrir 8080/tcp
- Digite o texto no formulário e clique em **Enviar para LLM**.