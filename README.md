# P0 — Primeiro fluxo com LLM (Resumidor de Textos)

Este projeto consiste em uma aplicação em Python executada via terminal que se conecta a um servidor interno do Ollama para resumir textos longos utilizando o modelo de linguagem **qwen3.5:9b-q4_K_M**.

## 🚀 Como Executar o Projeto

Siga os passos abaixo para configurar o ambiente e executar a aplicação na sua máquina.

### 📋 Pré-requisitos
* Python 3.8 ou superior instalado.
* Acesso à rede corporativa/institucional para alcançar o endpoint interno da LLM.

### 🔧 Configuração e Instalação

1. **Clonar o Repositório:**
   ```bash
   git clone https://github.com/24227051/P0.git
   cd meu-resumidor-llm
   ```

2. **Criar e Ativar um Ambiente Virtual (Recomendado):**
   * no Windows:
     ```bash
     python -m venv venv
     .\venv\Scripts\activate
     ```
   * no Linux/macOS:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Instalar as Dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar as Variáveis de Ambiente:**
   Crie um arquivo chamado `.env` na raiz do projeto e adicione a URL do servidor LLM conforme abaixo (troque server_url e port pela URL da LLM interna):
   ```env
   OLLAMA_HOST=https://server_url:port
   ```

### 💻 Executando a Aplicação

Com o ambiente virtual ativo e o arquivo `.env` configurado, execute o script principal:

```bash
python app.py
```

**Como usar:**
1. Cole ou digite o texto longo diretamente no terminal.
2. Para enviar o texto para a LLM:
   * No **Windows**: Pressione `Enter`, depois `Ctrl + Z` e pressione `Enter` novamente.
   * No **Linux/macOS**: Pressione `Enter`, depois `Ctrl + D`.
3. Aguarde o processamento e o resumo será exibido na tela.

### 🐳 Gerando a imagem Docker

Pré-requisitos:

* Docker Desktop instalado e em execução.
* Arquivo `Dockerfile` na raiz do projeto.

Na raiz do projeto, execute:

```powershell
docker build -t app:1.0 .
docker save -o app.tar app:1.0

Para testar localmente:

```powershell
docker run --rm -it --env-file .env app:1.0