# Relatório de Execução

## Evolução por nível

### Básico
No Básico foi construída uma aplicação em Python com o objetivo de receber uma entrada textual, enviar para a LLM e apresentar a resposta recebida ao usuário. Para poder interagir com o Devel LLM Portal a aplicação evoluiu para aplicação web com Flask. 

### Intermediário
No Intermediário o código foi organizado de forma que as responsabilidades não ficassem misturadas em um único bloco. Ainda nesse nível foi criada uma branch no controle de versão que foi integrada a branch principal por meio de um Pull Request. O código foi preparado para receber testes unitários.

### Avançado
No Avançado foram acrescentados os testes unitários com o objetivo de cumprir as verificações exigidas e o restante da documentação da aplicação.

## Decisões principais

- A primeira decisão relevante para o projeto foi a evolução de um código Python para um Python com Flask. A justificativa é poder interagir com a plataforma;

- Outra decisão foi o desenvolvimento de testes unitários com o objetivo de cumprir as verificações exigidas;

## Testes e resultados
Apresente uma tabela como:

Teste	Entrada ou situação	Resultado esperado	Resultado obtido
Inclua testes de sucesso e de falha.

## Falhas e limitações

- A principal falha que foi corrigida foi em relação ao tempo de resposta da LLM. Tanto local quanto no ambiente Devel LLM Portal. Nesse caso aumentou-se o timeout no Dockerfile e no Request para 600 segundos. Também restringiu-se a entrada de texto para 1000 caracteres. Com esses duas modificações consguimos obter a resposta antes do timeout. Caso ocorra o erro, ele é tratado e apresentado ao usuário.

## Uso de IA no desenvolvimento

- Gemini.Usado para tirar dúvidas sobre instalação de ferramentas, bibliotecas, sugerir caminhos de codificação; 

- GitHub Copilot Pro. Usado principalmente dentro da IDE VSCode para corrigir erros;

## Reflexão final
Foram vários aprendizados, desde a instalação local de um LLM e sua utilização, o desenvolvimento com o uso de containers e da IDE VSCode. Dentre os pontos que precisam ser aprimoradas pode-se citar o aprimoramento da utilização do controle de versão.