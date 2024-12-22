from __future__ import annotations

import re
from typing import Callable

from aiwolf_nlp_common.protocol.list.talk_list import TalkList
from aiwolf_nlp_common.role import Role


class Prompt:
    def format_text(func: Callable):
        def _wrapper(*args, **keywords):
            # execute function
            result: str = func(*args, **keywords)

            return re.sub(r"^\s+(.+)", r"\1", result, flags=re.MULTILINE)

        return _wrapper

    @classmethod
    @format_text
    def get_common_prompt(cls, agent_name: str, role: Role) -> str:
        return f"""あなたは人狼ゲームのプレイヤーの一員として、会話を行なってください。
        あなたのゲーム中での名前は{agent_name}です。
        あなたの役職は{role.ja}です。
        """

    @classmethod
    @format_text
    def get_talk_prompt(cls, talk_history: TalkList) -> str:
        talk_history_text = "\n".join([f"{talk.agent}:{talk.text}" for talk in talk_history])
        return f"""以下は今までの会話履歴です。会話に次ぐ発言をしてください。
        {talk_history_text}
        """
