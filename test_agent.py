from app.database.db import init_db
from app.agent.scorer import run_agent

init_db()
run_agent()