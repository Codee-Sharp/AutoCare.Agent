import re

from autocare_agent.graph.state import AgentState

CONTROL_CHARS = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]")


async def validate_input(state: AgentState) -> dict[str, object]:
    request = state["request"]
    request.mensagem = CONTROL_CHARS.sub("", request.mensagem).strip()
    return {"request": request}
