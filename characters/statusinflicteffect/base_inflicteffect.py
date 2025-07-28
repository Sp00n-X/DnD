"""状态施加效果 - 更新为使用新的状态效果系统"""

import random
from typing import Callable
from ..status_effects import PoisonEffect, BurnEffect, StunEffect


class StatusInflictEffect:
    """装备附加的状态效果"""
    
    def __init__(self, status_factory: Callable, chance: float, **kwargs):
        """
        status_factory: 返回状态效果实例的工厂函数
        chance: 触发概率 0-1
        kwargs: 传递给状态工厂的额外参数
        """
        self.status_factory = status_factory
        self.chance = chance
        self.kwargs = kwargs
    
    def on_hit(self, attacker, target):
        """攻击命中时触发"""
        if random.random() < self.chance:
            status_effect = self.status_factory(**self.kwargs)
            result = target.add_status_effect(status_effect)
            if result["success"]:
                print(f"[效果] {attacker.name} 使 {target.name} 附加 {status_effect.name}")
            return result
        return {"success": False, "message": "未触发状态效果"}


# 预定义的状态工厂函数
def create_poison_effect(duration: int = 3, percent_per_turn: float = 0.03):
    """创建中毒效果"""
    return PoisonEffect(duration=duration, percent_per_turn=percent_per_turn)


def create_burn_effect(duration: int = 2, damage_per_turn: int = 8):
    """创建灼烧效果"""
    return BurnEffect(duration=duration, damage_per_turn=damage_per_turn)


def create_stun_effect(duration: int = 1):
    """创建眩晕效果"""
    return StunEffect(duration=duration)


# 示例装备效果
poison_blade_effect = StatusInflictEffect(
    status_factory=create_poison_effect,
    chance=0.25,
    duration=3,
    percent_per_turn=0.05
)

flame_weapon_effect = StatusInflictEffect(
    status_factory=create_burn_effect,
    chance=0.3,
    duration=2,
    damage_per_turn=10
)

stun_mace_effect = StatusInflictEffect(
    status_factory=create_stun_effect,
    chance=0.15,
    duration=1
)
