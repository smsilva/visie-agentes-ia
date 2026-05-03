from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.db.sqlite import SqliteDb

model_id = "bedrock/anthropic.claude-4-6-sonnet"

agent_instructions = """
    Você saber responder perguntas sobre o time de Cloud do Projeto Projeto Exemplo.

    - Início do projeto: 2023
    - Membros: 10
    - Tecnologias: AWS, Azure, GCP, Kubernetes, Terraform, Ansible
    - Principais responsabilidades: Gerenciamento de infraestrutura, automação de deploy, monitoramento e segurança.
    - Ao ser perguntado sobre Capitais de Países, responda apenas o nome da Capital. Só forneça mais detalhes sobre a cidade se for perguntado especificamente sobre esses detalhes.
    """

agent_db = SqliteDb(db_file="/tmp/agents/claudio.db")

agent = Agent(
    name="cloud-team",
    model=OpenAIChat(id=model_id),
    instructions=agent_instructions,
    markdown=True,
    db=agent_db,
    enable_agentic_memory=True,
    add_datetime_to_context=True,
    add_history_to_context=True,
    num_history_runs=5,
    debug_mode=True,
    debug_level=1
)


while True:
    user_input = input("Prompt: ")
    if user_input == "":
        break

    agent.print_response(user_input)
