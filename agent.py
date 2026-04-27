from pathlib import Path
from agno.os import AgentOS
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.db.sqlite import SqliteDb
from agno.tools.file import FileTools

instructions_file_name = "instructions.md"

with open(instructions_file_name) as instructions_file:
    instructions_lines = instructions_file.read()

agent = Agent(
    name="Tmux Helper",
    instructions=instructions_lines,
    model="openai:gpt-4o-mini",
    markdown=True,
    tools=[FileTools(
        base_dir=Path("."),
        enable_save_file=False,
        enable_delete_file=False,
        enable_replace_file_chunk=False,
    )],
)

agent_os = AgentOS(
    agents=[agent],
    tracing=True,
    db=SqliteDb(db_file="tmp/agentos.db"),
)

app = agent_os.get_app()

# agent.print_response("Como divido uma janela no tmux?")
