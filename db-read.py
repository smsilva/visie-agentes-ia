import sqlite3
import json
import rich

conn = sqlite3.connect('tmp/agents.db')
cursor = conn.cursor()

cursor.execute("""
    SELECT
      agent_id,
      session_id,
      session_data,
      agent_data
    FROM
      agno_sessions
    """
)

for row in cursor:
    agent_id, session_id, session_data, agent_data = row
    raw_session_data = json.loads(session_data)
    raw_agent_data = json.loads(agent_data)

    print(f"Agent ID: {agent_id}, Session ID: {session_id}")
    print("---------------json session_data---------------")
    rich.print_json(raw_session_data)
    print("---------------json agent_data---------------")
    rich.print_json(raw_agent_data)
    print("")

conn.close()
