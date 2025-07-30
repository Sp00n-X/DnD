"""具体的状态效果实现"""

from typing import Dict, Any
from .base_status import BaseStatusEffect, StatusEffectData, StatusType, StatusPriority


class BurnEffect(BaseStatusEffect):
    """灼烧效果 - 每回合造成固定伤害"""
    
    def __init__(self, duration: int = 3, damage_per_turn: int = 10):
        data = StatusEffectData(
            name="灼烧",
            duration=duration,
            max_stacks=3,
            refresh_on_reapply=True,
            exclusive_with=["冰冻"]
        )
        super().__init__(data)
        self.damage_per_turn = damage_per_turn
    
    def get_status_type(self) -> StatusType:
        return StatusType.DOT
    
    def get_priority(self) -> StatusPriority:
        return StatusPriority.MEDIUM
    
    def on_tick(self, character) -> Dict[str, Any]:
        """每回合造成伤害"""
        from characters.equipments.base_equipments import DamageType
        damage = self.damage_per_turn * self.stacks
        character.take_damage(damage, DamageType.MAGICAL)
        
        result = super().on_tick(character)
        result.update({
            "damage": damage,
            "message": f"{character.name} 受到 {damage} 点灼烧伤害"
        })
        return result


class PoisonEffect(BaseStatusEffect):
    """中毒效果 - 每回合造成百分比伤害"""
    
    def __init__(self, duration: int = 5, percent_per_turn: float = 0.05):
        data = StatusEffectData(
            name="中毒",
            duration=duration,
            max_stacks=5,
            refresh_on_reapply=True,
            exclusive_with=["灼烧"]
        )
        super().__init__(data)
        self.percent_per_turn = percent_per_turn
    
    def get_status_type(self) -> StatusType:
        return StatusType.DOT
    
    def get_priority(self) -> StatusPriority:
        return StatusPriority.MEDIUM
    
    def on_tick(self, character) -> Dict[str, Any]:
        """每回合造成最大生命值的百分比伤害"""
        from characters.equipments.base_equipments import DamageType
        damage = int(character.max_hp * self.percent_per_turn * self.stacks)
        character.take_damage(damage, DamageType.MAGICAL)
        
        result = super().on_tick(character)
        result.update({
            "damage": damage,
            "message": f"{character.name} 受到 {damage} 点中毒伤害"
        })
        return result


class FreezeEffect(BaseStatusEffect):
    """冰冻效果 - 控制类，阻止行动"""
    
    def __init__(self, duration: int = 2):
        data = StatusEffectData(
            name="冰冻",
            duration=duration,
            max_stacks=1,
            refresh_on_reapply=False,
            exclusive_with=["灼烧", "中毒"]
        )
        super().__init__(data)
    
    def get_status_type(self) -> StatusType:
        return StatusType.CROWD_CONTROL
    
    def get_priority(self) -> StatusPriority:
        return StatusPriority.HIGH
    
    def on_apply(self, character) -> Dict[str, Any]:
        """应用冰冻效果"""
        character.can_act = False
        return {
            "success": True,
            "message": f"{character.name} 被冰冻了，无法行动"
        }
    
    def on_tick(self, character) -> Dict[str, Any]:
        """每回合持续冰冻效果"""
        character.can_act = False
        
        self.remaining_duration -= 1
        if self.remaining_duration <= 0:
            self.is_active = False
            
        return {
            "success": True,
            "message": f"{character.name} 仍处于冰冻状态"
        }
    
    def on_remove(self, character) -> Dict[str, Any]:
        """移除冰冻效果"""
        character.can_act = True
        return {
            "success": True,
            "message": f"{character.name} 从冰冻中恢复"
        }


class DefenseBuffEffect(BaseStatusEffect):
    """防御增益效果"""
    
    def __init__(self, duration: int = 3, defense_bonus: int = 20):
        data = StatusEffectData(
            name="防御强化",
            duration=duration,
            max_stacks=3,
            refresh_on_reapply=True
        )
        super().__init__(data)
        self.defense_bonus = defense_bonus
        self.original_defense = None
    
    def get_status_type(self) -> StatusType:
        return StatusType.BUFF
    
    def get_priority(self) -> StatusPriority:
        return StatusPriority.MEDIUM
    
    def on_apply(self, character) -> Dict[str, Any]:
        """应用防御增益"""
        self.original_defense = character.defense
        character.defense += self.defense_bonus * self.stacks
        return {
            "success": True,
            "message": f"{character.name} 的防御力提升了 {self.defense_bonus * self.stacks} 点"
        }
    
    def on_remove(self, character) -> Dict[str, Any]:
        """移除防御增益"""
        if self.original_defense is not None:
            character.defense = self.original_defense
        return {
            "success": True,
            "message": f"{character.name} 的防御强化效果消失"
        }


class AttackBuffEffect(BaseStatusEffect):
    """攻击增益效果"""
    
    def __init__(self, duration: int = 3, attack_bonus: int = 15):
        data = StatusEffectData(
            name="攻击强化",
            duration=duration,
            max_stacks=3,
            refresh_on_reapply=True
        )
        super().__init__(data)
        self.attack_bonus = attack_bonus
        self.original_attack = None
    
    def get_status_type(self) -> StatusType:
        return StatusType.BUFF
    
    def get_priority(self) -> StatusPriority:
        return StatusPriority.MEDIUM
    
    def on_apply(self, character) -> Dict[str, Any]:
        """应用攻击增益"""
        self.original_attack = character.attack
        character.attack += self.attack_bonus * self.stacks
        return {
            "success": True,
            "message": f"{character.name} 的攻击力提升了 {self.attack_bonus * self.stacks} 点"
        }
    
    def on_remove(self, character) -> Dict[str, Any]:
        """移除攻击增益"""
        if self.original_attack is not None:
            character.attack = self.original_attack
        return {
            "success": True,
            "message": f"{character.name} 的攻击强化效果消失"
        }


class HealOverTimeEffect(BaseStatusEffect):
    """持续治疗效果"""
    
    def __init__(self, duration: int = 3, heal_per_turn: int = 15):
        data = StatusEffectData(
            name="持续治疗",
            duration=duration,
            max_stacks=5,
            refresh_on_reapply=True
        )
        super().__init__(data)
        self.heal_per_turn = heal_per_turn
    
    def get_status_type(self) -> StatusType:
        return StatusType.HOT
    
    def get_priority(self) -> StatusPriority:
        return StatusPriority.LOW
    
    def on_tick(self, character) -> Dict[str, Any]:
        """每回合治疗"""
        heal_amount = self.heal_per_turn * self.stacks
        character.heal(heal_amount)
        
        result = super().on_tick(character)
        result.update({
            "heal": heal_amount,
            "message": f"{character.name} 恢复了 {heal_amount} 点生命值"
        })
        return result


class StunEffect(BaseStatusEffect):
    """眩晕效果 - 强力控制"""
    
    def __init__(self, duration: int = 1):
        data = StatusEffectData(
            name="眩晕",
            duration=duration,
            max_stacks=1,
            refresh_on_reapply=False,
            exclusive_with=["冰冻", "沉默"]
        )
        super().__init__(data)
    
    def get_status_type(self) -> StatusType:
        return StatusType.CROWD_CONTROL
    
    def get_priority(self) -> StatusPriority:
        return StatusPriority.HIGHEST
    
    def on_apply(self, character) -> Dict[str, Any]:
        """应用眩晕效果"""
        character.can_act = False
        character.can_cast = False
        return {
            "success": True,
            "message": f"{character.name} 被眩晕了，无法行动或施法"
        }
    
    def on_tick(self, character) -> Dict[str, Any]:
        """每回合持续眩晕效果"""
        # 确保眩晕期间持续生效
        character.can_act = False
        character.can_cast = False
        
        self.remaining_duration -= 1
        if self.remaining_duration <= 0:
            self.is_active = False
            
        return {
            "success": True,
            "message": f"{character.name} 仍处于眩晕状态"
        }
    
    def on_remove(self, character) -> Dict[str, Any]:
        """移除眩晕效果"""
        character.can_act = True
        character.can_cast = True
        return {
            "success": True,
            "message": f"{character.name} 从眩晕中恢复"
        }


# 新增的状态效果类
class SpeedDebuffEffect(BaseStatusEffect):
    """速度减益效果"""
    
    def __init__(self, duration: int = 2, speed_reduction: int = 30):
        data = StatusEffectData(
            name="减速",
            duration=duration,
            max_stacks=3,
            refresh_on_reapply=True
        )
        super().__init__(data)
        self.speed_reduction = speed_reduction
    
    def get_status_type(self) -> StatusType:
        return StatusType.DEBUFF
    
    def get_priority(self) -> StatusPriority:
        return StatusPriority.MEDIUM
    
    def on_apply(self, character) -> Dict[str, Any]:
        """应用减速效果"""
        return {
            "success": True,
            "message": f"{character.name} 的速度降低了 {self.speed_reduction * self.stacks}%"
        }


class DodgeBuffEffect(BaseStatusEffect):
    """闪避增益效果"""
    
    def __init__(self, duration: int = 2, dodge_chance: int = 30):
        data = StatusEffectData(
            name="闪避提升",
            duration=duration,
            max_stacks=3,
            refresh_on_reapply=True
        )
        super().__init__(data)
        self.dodge_chance = dodge_chance
    
    def get_status_type(self) -> StatusType:
        return StatusType.BUFF
    
    def get_priority(self) -> StatusPriority:
        return StatusPriority.MEDIUM
    
    def on_apply(self, character) -> Dict[str, Any]:
        """应用闪避提升效果"""
        return {
            "success": True,
            "message": f"{character.name} 的闪避率提升了 {self.dodge_chance * self.stacks}%"
        }
