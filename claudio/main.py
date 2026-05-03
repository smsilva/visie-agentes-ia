from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.db.sqlite import SqliteDb

model_id = "bedrock/anthropic.claude-4-6-sonnet"

agent_db = SqliteDb(db_file="/tmp/agents/claudio.db")

agent = Agent(
    model=OpenAIChat(id=model_id),
    name="claudio-developer",
    description="Claudio is a software developer who can write code, debug, and provide explanations on programming concepts.",
    markdown=True,
    db=agent_db,
    enable_agentic_memory=True,
    add_datetime_to_context=True,
    add_history_to_context=True,
    num_history_runs=5,
    debug_mode=True,
    debug_level=1    
)

if __name__ == "__main__":
    while True:
        user_input = input("You: ")
        
        if user_input == "":
            break

        if user_input.lower() in ["exit", "quit"]:
            break
        
        agent.print_response(user_input)
