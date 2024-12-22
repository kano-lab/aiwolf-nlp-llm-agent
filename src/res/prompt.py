from aiwolf_nlp_common.role import Role
from aiwolf_nlp_common.protocol.list.talk_list import TalkList


class Prompt:

    @classmethod
    def get_common_prompt(cls, agent_name:str, role:Role) -> str:
        return f"""
        あなたは人狼ゲームのプレイヤーの一員として、会話を行なってください。
        あなたのゲーム中での名前は{agent_name}です。
        あなたの役職は{role.ja}です。
        """
    
    @classmethod
    def get_talk_prompt(cls, talk_history:TalkList) -> str:
        talk_history_text = "\n".join(talk_history)
        return f"""
        以下は今までの会話履歴です。会話に次ぐ発言をしてください。
        {talk_history_text}
        """