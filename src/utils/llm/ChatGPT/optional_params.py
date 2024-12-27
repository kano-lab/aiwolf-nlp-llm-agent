from __future__ import annotations

import dataclasses

@dataclasses.dataclass
class OptionalParams:
    frequency_penalty: float | None = None
    max_completion_tokens:int | None  = None
    n:int | None = None
    presence_penalty:int | None = None
    seed:int | None = None
    temperature: float | None = None
    top_p: float | None = None