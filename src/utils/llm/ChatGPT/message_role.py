from enum import Enum

class MessageRole(Enum):
    DEVELOPER = "developer"
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"
    FUNCTION = "function"