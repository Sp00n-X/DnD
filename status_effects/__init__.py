"""状态效果系统 - 统一管理所有角色状态"""

from .base_status import BaseStatusEffect, StatusType, StatusPriority
from .status_manager import StatusManager
from .status_effects import *

__all__ = [
    'BaseStatusEffect',
    'StatusType', 
    'StatusPriority',
    'StatusManager',
    'BurnEffect',
    'PoisonEffect',
    'FreezeEffect',
    'DefenseBuffEffect',
    'AttackBuffEffect',
    'HealOverTimeEffect',
    'StunEffect',
    'SpeedDebuffEffect',
    'DodgeBuffEffect'
]
