# Notas

- Agno
- Langchain
- Pydantic
- AgentOS
- AgentUI

Construir um agente para rodar na linha de comando lendo prompt de um arquivo

uv run uvicorn agent:app --reload 

```shell
OPENAI_BASE_URL
OPENAI_API_KEY
```

Dia 2

RAG

LanceDB - Vector Database suportado pelo Agno
Pinecone

uv ad lancedb

OpenAIEmbedder - default embedder do LanceDB

Agno Readers
- PDF Reader

Livro: Thinking in Python

Bruce Eckel

Agno Memory MemoryManager
agno.memory.MemoryManager

Dúvida sobre testes que não fazem parte da mudança.

Knowledge Base e Skills para os exercícios

- Dia 3

Exercício

- Criar um agente que responda perguntas sobre o fluxo de trabalho no cloud.ao

- Qual comando mostra o caminho do arquivo?

dir(OpenAIChat)

help(OpenAIChat)

# Dia 4

- Python cli: 

.venv/bin/python
import agno
agno
<module 'agno' from '/home/silvios/git/visie-agentes-ia/.venv/lib/python3.14/site-packages/agno/__init__.py'>

Python Click

Pydantic

curiosidade sobre importacao de classe e poder renomear

comentar sobre o play

Pensamentos
- modelo agarrado com jira
- tentar forçar o uso de papeis usado atualmente
- mocks para agentes
- salvar cache dos passos de um workflow que envolve ia

- agente de ia precisa ter ferramentas para:
  - ler arquivos
  - ler diretoiros
  - escrever arquivos
  - e executar código (os subprocess executando o que ele acabou de escrever e ver se deu erro ou não)
