# P0 — Resumidor de Textos com LLM

## Problema escolhido
Resumidor de Textos com LLM. Aplicação web desenvolvida em Python e Flask para enviar textos a um servidor
interno do Ollama e exibir o resumo gerado pelo modelo
`qwen3.5:9b-q4_K_M`.

## Usuário ou público
Interessados na área de tecnologia com objetivo de interagir com um modelo de LLM

## Justificativa para utilizar um LLM
A capacidade da LLM de resumir textos. O modelo entende o contexto e escreve as idéias principais. Ao invés de apenas recortar frases soltas do texto original.

## Funcionamento da solução
- Flask recebe as requisições HTTP.
- A rota `/` exibe o formulário web.
- A rota `/perguntar` envia o texto para a API do Ollama.
- Gunicorn é utilizado para executar a aplicação em produção.

## Pré-requisitos
- Python 3.12 ou superior
- Acesso ao servidor interno do Ollama
- Docker Desktop

## Limites do projeto
- O limite do texto para resumo é de 1000 caracteres.

## Implantação e Execução no Devel LLM Portal

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

### 5. Implantar

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

## Implantação e Execução local (Opcional)

Requer recursos de processamento e memória

### Instalar o Ollama
- Subir o Ollama no Docker
```powershell
docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
```

- Baixar o Modelo de Testes Local
```powershell
docker exec -it ollama ollama run qwen3.5:9b-q4_K_M
```

- Ajustar o arquivo .env para Testes Locais
```env
OLLAMA_URL=http://host.docker.internal:11434/api/generate
```

### Repetir os passos de 1 a 4

### Iniciar a aplicação
```powershell
docker run --rm -it --env-file .env -p 8080:8080 p0-resumidor:1.0
```

- Clique em: Abra o browser em http://localhost:8080/
- Digite o texto no formulário e clique em **Enviar para LLM**.

## Configuração dos testes unitários
- Instalar as dependências de teste (e cobertura de código):
```bash
pip install pytest pytest-cov
```

## Exemplos de entrada e saída
Resumo gerado

Texto enviado:

Você é um assistente especializado em síntese de informações. Seu objetivo é resumir o texto fornecido pelo usuário de forma clara, concisa e destacando os pontos principais em português: Segundo a empresa, os novos modelos pertencem à família Mythos, considerada sua geração mais avançada de inteligência artificial. A Anthropic afirma que a tecnologia se destaca em tarefas como engenharia de software, análise de dados, pesquisa científica, visão computacional e resolução de problemas complexos. A companhia também informou que mantém salvaguardas para determinados tipos de solicitações por considerar que modelos dessa categoria podem ser especialmente eficazes na descoberta e exploração de vulnerabilidades em softwares e outras aplicações consideradas sensíveis. Em apresentações anteriores, a empresa destacou ainda o potencial da tecnologia para aplicações científicas. Segundo a Anthropic, modelos da linha Mythos foram capazes de auxiliar pesquisas relacionadas ao desenvolvimento de medicamentos, ao design de proteínas e à formulação de hipóteses em biologia molecular que passaram a ser avaliadas por pesquisadores.

Resposta da LLM:

**Síntese: Novos Modelos de IA Anthropic (Família Mythos)**

*   **Avanço Tecnológico:** A Anthropic lançou novos modelos da família *Mythos*, considerada sua geração mais avançada de inteligência artificial.
*   **Principais Habilidades:** Excelência em tarefas como engenharia de software, análise de dados, visão computacional e resolução de problemas complexos.
*   **Segurança e Ética:** A empresa implementou salvaguardas para determinadas solicitações, devido à eficácia dos modelos na descoberta de vulnerabilidades em sistemas sensíveis.
*   **Impacto Científico:** A tecnologia já auxilia pesquisas práticas, como desenvolvimento de medicamentos, design de proteínas e formulação de hipóteses em biologia molecular.

Fazer outro resumo

## Execução dos testes
- Executar os testes no terminal
```bash
pytest -v
```

## Limitações conhecidas
- Timeout na resposta da LLM

## Link para o vídeo