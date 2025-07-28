"""状态效果基类定义"""

from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict, Any, Optional
from dataclasses import dataclass


class StatusType(Enum):
    """状态效果类型"""
    BUFF = "buff"      # 增益效果
    DEBUFF = "debuff"  # 减益效果
    DOT = "dot"        # 持续伤害
    HOT = "hot"        # 持续治疗
    CROWD_CONTROL = "crowd_control"  # 控制效果


class StatusPriority(Enum):
    """状态效果优先级"""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    HIGHEST = 4


@dataclass
class StatusEffectData:
    """状态效果数据容器"""
    name: str
    duration: int
    max_stacks: int = 1
    refresh_on_reapply: bool = True
    exclusive_with: list = None
    
    def __post_init__(self):
        if self.exclusive_with is None:
            self.exclusive_with = []


class BaseStatusEffect(ABC):
    """状态效果基类"""
    
    def __init__(self, data: StatusEffectData):
        self.data = data
        self.remaining_duration = data.duration
        self.stacks = 1
        self.is_active = True
        
    @property
    def name(self) -> str:
        return self.data.name
    
    @property
    def duration(self) -> int:
        return self.data.duration
    
    @property
    def max_stacks(self) -> int:
        return self.data.max_stacks
    
    @abstractmethod
    def get_status_type(self) -> StatusType:
        """获取状态类型"""
        pass
    
    @abstractmethod
    def get_priority(self) -> StatusPriority:
        """获取优先级"""
        pass
    
    def can_stack_with(self, other: 'BaseStatusEffect') -> bool:
        """检查是否可以与另一个状态叠加"""
        return self.data.name not in other.data.exclusive_with
    
    def on_apply(self, character) -> Dict[str, Any]:
        """状态被应用时调用"""
        return {"success": True, "message": f"{self.name} 已施加"}
    
    def on_remove(self, character) -> Dict[str, Any]:
        """状态被移除时调用"""
        return {"success": True, "message": f"{self.name} 已移除"}
    
    def on_tick(self, character) -> Dict[str, Any]:
        """每回合调用"""
        self.remaining_duration -= 1
        if self.remaining_duration <= 0:
            self.is_active = False
        return {"success": True, "message": f"{self.name} 持续中"}
    
    def refresh(self):
        """刷新持续时间"""
        self.remaining_duration = self.data.duration
    
    def add_stack(self) -> bool:
        """增加层数"""
        if self.stacks < self.max_stacks:
            self.stacks += 1
            return True
        return False
    
    def merge(self, new_effect: 'BaseStatusEffect') -> bool:
        """合并相同类型的状态效果"""
        if type(self) != type(new_effect):
            return False
            
        if self.data.refresh_on_reapply:
            self.refresh()
            
        if self.stacks < self.max_stacks:
            self.add_stack()
            
        return True
    
    def get_description(self) -> str:
        """获取状态描述"""
        stack_text = f" ({self.stacks}层)" if self.stacks > 1 else ""
        return f"{self.name}{stack_text} - 剩余{self.remaining_duration}回合"
    
    def to_dict(self) -> Dict[str, Any]:
        """序列化为字典"""
        return {
            "name": self.name,
            "duration": self.remaining_duration,
            "stacks": self.stacks,
            "type": self.get_status_type().value,
            "description": self.get_description()
        }
