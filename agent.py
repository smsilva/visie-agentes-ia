from agno.agent import Agent
from agno.models.openai import OpenAIChat

agent = Agent(
    model=OpenAIChat(id="gpt41"),
    instructions="You are a helpful assistant that provides information about the weather. Answer questions about current weather conditions, forecasts, and general weather-related inquiries.",
    markdown=True,
)

agent.print_response("What is the current weather in New York City?")
