from enum import Enum

class MessageRole(Enum):
    DEVELOPER = "developer"
    SYSTEM = "system"
    USER = "user"
    TOOL = "tool"
    FUNCTION = "function"