from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.db.sqlite import SqliteDb
from agno.tools.local_file_system import LocalFileSystemTools
from agno.tools.file import FileTools
from agno.tools.shell import ShellTools

# model_id = "bedrock/anthropic.claude-4-6-sonnet"
model_id = "gpt-4o-mini"

agent_db = SqliteDb(db_file="/tmp/agents/claudio.db")

instructions = """
    Claudio is a software developer who can write code.
    
    Can use tools to interact with the local file system, run shell commands, and read/write files.
    
    Always try to use tools when possible.
"""

agent = Agent(
    model=OpenAIChat(id=model_id),
    name="claudio-developer",
    instructions=instructions,
    markdown=True,
    db=agent_db,
    enable_agentic_memory=True,
    add_datetime_to_context=True,
    add_history_to_context=True,
    num_history_runs=5,
    debug_mode=True,
    debug_level=1,
    tools=[
        LocalFileSystemTools(
            target_directory="./"
        ),
        FileTools(),
        ShellTools(
            enable_run_shell_command=True
        )
    ]
)

if __name__ == "__main__":
    while True:
        user_input = input("You: ")

        if user_input == "":
            break

        if user_input.lower() in ["exit", "quit"]:
            break

        agent.print_response(user_input)
