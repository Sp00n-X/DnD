"""技能基类 - 更新为与角色系统兼容"""

from abc import ABC, abstractmethod
from typing import Dict, Any
from enum import Enum


class SkillType(Enum):
    """技能类型"""
    ACTIVE = "active"
    PASSIVE = "passive"
    ULTIMATE = "ultimate"


class Skill(ABC):
    """技能基类"""
    
    def __init__(self, name: str, skill_type: SkillType, mp_cost: int = 0, 
                 cooldown: int = 0, description: str = "", level_requirement: int = 1):
        self.name = name
        self.skill_type = skill_type
        self.mp_cost = mp_cost
        self.cooldown = cooldown
        self.current_cooldown = 0
        self.description = description
        self.level_requirement = level_requirement
    
    def can_use(self, character) -> bool:
        """检查是否可以使用技能"""
        return (character.mp >= self.mp_cost and 
                self.current_cooldown <= 0 and
                character.level >= self.level_requirement)
    
    @abstractmethod
    def execute(self, caster, target=None) -> Dict[str, Any]:
        """执行技能，子类实现具体效果"""
        pass
    
    def reduce_cooldown(self):
        """减少冷却时间"""
        if self.current_cooldown > 0:
            self.current_cooldown -= 1
    
    def get_current_description(self) -> str:
        """获取当前技能描述"""
        return f"{self.name} - {self.description} (MP: {self.mp_cost}, CD: {self.cooldown})"
