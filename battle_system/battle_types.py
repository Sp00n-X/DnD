"""战斗系统相关的类型定义"""

from enum import Enum
from dataclasses import dataclass
from typing import Dict, Any, Optional

class BattleAction(Enum):
    """战斗行动类型"""
    ATTACK = "attack"
    DEFEND = "defend"
    SKILL = "skill"
    ITEM = "item"
    FLEE = "flee"

class TurnPhase(Enum):
    """回合阶段"""
    PLAYER_TURN = "player_turn"
    ENEMY_TURN = "enemy_turn"
    BATTLE_START = "battle_start"
    BATTLE_END = "battle_end"

class BattleResult(Enum):
    """战斗结果"""
    VICTORY = "victory"
    DEFEAT = "defeat"
    FLEE = "flee"
    DRAW = "draw"

@dataclass
class BattleLog:
    """战斗日志条目"""
    turn: int
    phase: TurnPhase
    actor: str
    action: BattleAction
    target: str
    damage: int = 0
    heal: int = 0
    effect: Optional[str] = None
    message: str = ""

@dataclass
class BattleRewards:
    """战斗奖励"""
    experience: int = 0
    gold: int = 0
    items: list = None
    
    def __post_init__(self):
        if self.items is None:
            self.items = []

@dataclass
class BattleConfig:
    """战斗配置"""
    allow_flee: bool = True
    show_detailed_log: bool = True
    auto_battle: bool = False
    turn_limit: int = 100
