import os
from agno.agent import Agent
from agno.models.openai import OpenAIChat

instructions_file_name = "instructions.md"

with open(instructions_file_name) as instructions_file:
    instructions_lines = instructions_file.read()

agent = Agent(
    model="openai:gpt-4o-mini",
    instructions=instructions_lines,
    markdown=True,
)

agent.print_response("Como divido uma janela no tmux?")
