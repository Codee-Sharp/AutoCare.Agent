class AgentError(Exception):
    code = "agent_error"


class DependencyUnavailable(AgentError):
    code = "dependency_unavailable"


class InvalidDependencyResponse(AgentError):
    code = "invalid_dependency_response"


class UnsafeAction(AgentError):
    code = "unsafe_action"
