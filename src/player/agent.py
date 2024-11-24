import configparser
from threading import Thread
from typing import Callable

from aiwolf_nlp_common import Action, util
from aiwolf_nlp_common.protocol import CommunicationProtocol

from lib.log import AgentLog, LogInfo


class Agent:
    def __init__(
        self,
        inifile: configparser.ConfigParser,
        name: str,
        log_info: LogInfo,
        is_hand_over: bool = False,
    ):
        self.name: str = name
        self.received: list = []
        self.time_limit: int = 0
        self.gameContinue: bool = True

        if not is_hand_over:
            self.logger = AgentLog(inifile=inifile, agent_name=name, log_info=log_info)

        with open(inifile.get("filePath", "random_talk"), "r", encoding="utf-8") as f:
            self.comments: list[str] = f.read().splitlines()

    @staticmethod
    def timeout(func: Callable):
        def _wrapper(self, *args, **kwargs):
            result = None

            def execute_with_timeout():
                nonlocal result
                try:
                    result = func(self, *args, **kwargs)
                except Exception as e:
                    result = e

            thread = Thread(target=execute_with_timeout, daemon=True)
            thread.start()
            thread.join(timeout=self.time_limit)

            if isinstance(result, Exception):
                raise result

            return result

        return _wrapper

    def send_agent_index(func: Callable):
        def _wrapper(self, *args, **keywords):
            # execute function
            if len(keywords) == 0:
                result: int = func(self)
            else:
                result: int = func(self, *args, **keywords)

            if type(result) is not int:
                raise ValueError(
                    "Functions with the send_agent_index decorator must return an int type"
                )

            return util.get_name_from_index(agent_index=result)

        return _wrapper

    def set_received(self, received: list) -> None:
        self.received = received

    def parse_info(self, receive: str) -> None:
        self.received = receive

    def get_info(self):
        if not hasattr(self, "protocol"):
            self.protocol = CommunicationProtocol.initialize_from_json(
                received_str=self.received.pop(0)
            )
        else:
            self.protocol.update_from_json(received_str=self.received.pop(0))

    def initialize(self) -> None:
        self.agent_name: str = self.protocol.info.agent
        self.index: int = util.get_index_from_name(agent_name=self.agent_name)

        self.time_limit: int = self.protocol.setting.action_timeout
        self.role: str = self.protocol.info.role_map.get_role(agent=self.agent_name)

    def daily_initialize(self) -> None:
        self.alive: list = self.protocol.info.status_map.get_alive_agent_list()

    def daily_finish(self) -> None:
        pass

    @timeout
    def get_name(self) -> str:
        return self.name

    @timeout
    def get_role(self) -> str:
        return self.role

    @timeout
    def talk(self) -> str:
        comment: str = util.random_select(self.comments)
        self.logger.talk(comment=comment)
        return comment

    @timeout
    @send_agent_index
    def vote(self) -> int:
        vote_target: int = util.get_index_from_name(
            agent_name=util.random_select(self.alive)
        )
        self.logger.vote(vote_target=vote_target)
        return vote_target

    @timeout
    def whisper(self) -> None:
        pass

    def finish(self) -> str:
        self.gameContinue = False
        if self.logger.is_write:
            self.logger.close()

    def action(self) -> str:
        if Action.is_initialize(request=self.protocol.request):
            self.initialize()
        elif Action.is_name(request=self.protocol.request):
            return self.get_name()
        elif Action.is_role(request=self.protocol.request):
            return self.get_role()
        elif Action.is_daily_initialize(request=self.protocol.request):
            self.daily_initialize()
        elif Action.is_daily_finish(request=self.protocol.request):
            self.daily_finish()
        elif Action.is_talk(request=self.protocol.request):
            return self.talk()
        elif Action.is_vote(request=self.protocol.request):
            return self.vote()
        elif Action.is_whisper(request=self.protocol.request):
            self.whisper()
        elif Action.is_finish(request=self.protocol.request):
            self.finish()

        return ""

    def hand_over(self, new_agent) -> None:
        # __init__
        new_agent.name = self.name
        new_agent.received = self.received
        new_agent.gameContinue = self.gameContinue
        new_agent.comments = self.comments
        new_agent.received = self.received
        new_agent.logger = self.logger

        # get_info
        if hasattr(self, "gameInfo"):
            new_agent.gameInfo = self.gameInfo

        if hasattr(self, "gameSetting"):
            new_agent.gameSetting = self.gameSetting

        if hasattr(self, "talkHistory"):
            new_agent.talkHistory = self.talkHistory

        if hasattr(self, "whisperHistory"):
            new_agent.whisperHistory = self.whisperHistory

        new_agent.request = self.protocol.request

        # initialize
        new_agent.index = self.index
        new_agent.role = self.role
        new_agent.time_limit = self.time_limit