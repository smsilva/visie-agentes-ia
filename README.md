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
