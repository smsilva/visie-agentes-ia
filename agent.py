from agno.agent import Agent
from agno.models.openai import OpenAIChat

model_id = "bedrock/anthropic.claude-4-6-sonnet"

agent = Agent(
    name="cloud-team",
    model=OpenAIChat(id=model_id),
    markdown=True,
)

agent.print_response("Qual é a capital do Brasil?")
