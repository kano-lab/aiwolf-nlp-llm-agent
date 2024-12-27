import re

import configparser
from aiwolf_nlp_common.role import RoleInfo
from utils.llm.Gemini import Gemini
from utils.llm.ChatGPT import AIWolfNLPChatGPT

import player


def set_role(
    prev_agent: player.agent.Agent,
) -> player.agent.Agent:
    agent: player.agent.Agent
    if RoleInfo.is_villager(role=prev_agent.role):
        agent = player.villager.Villager()
    elif RoleInfo.is_werewolf(role=prev_agent.role):
        agent = player.werewolf.Werewolf()
    elif RoleInfo.is_seer(role=prev_agent.role):
        agent = player.seer.Seer()
    elif RoleInfo.is_possessed(role=prev_agent.role):
        agent = player.possessed.Possessed()
    else:
        raise ValueError(prev_agent.role, "Role is not defined")
    agent.transfer_state(prev_agent=prev_agent)
    return agent

def set_model(config: configparser.ConfigParser, system_instruction:str) -> AIWolfNLPChatGPT | Gemini:

    if config.getboolean("model", "ChatGPT", fallback=False):
        return AIWolfNLPChatGPT(config=config, system_instruction=system_instruction)
    
    return Gemini(config=config, system_instruction=system_instruction)

def agent_name_to_idx(name: str) -> int:
    match = re.search(r"\d+", name)
    if match is None:
        raise ValueError(name, "No number found in agent name")
    return int(match.group())


def agent_idx_to_agent(idx: int) -> str:
    return f"Agent[{idx:0>2d}]"
