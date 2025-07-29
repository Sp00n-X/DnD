"""哥布林厨师长的专属技能"""

from characters.skills.base_skill import Skill, SkillType
from status_effects.status_effects import BurnEffect, PoisonEffect, AttackBuffEffect, StunEffect
from characters.equipments.base_equipments import DamageType
from typing import Dict, Any
import random


class SpicySeasoning(Skill):
    """辛辣调料 - 造成火属性伤害并有几率附加灼烧"""
    
    def __init__(self):
        super().__init__(
            name="🔥辛辣调料",
            skill_type=SkillType.ACTIVE,
            mp_cost=10,
            cooldown=2,
            description="撒出辛辣调料，造成火属性伤害并有几率使目标灼烧"
        )
    
    def execute(self, caster, target=None) -> Dict[str, Any]:
        """执行技能"""
        damage = 20 + caster.attack * 0.8
        caster.mp -= self.mp_cost
        self.current_cooldown = self.cooldown
        
        # 50%几率附加灼烧
        burn_applied = False
        if random.random() < 0.5 and target:
            burn_effect = BurnEffect(duration=3, damage_per_turn=5)
            target.status_manager.add_status(burn_effect)
            burn_applied = True
        
        if target:
            target.take_damage(int(damage), DamageType.MAGICAL)
        
        return {
            'success': True,
            'damage': int(damage),
            'damage_type': 'fire',
            'burn_applied': burn_applied,
            'message': f"{caster.name}使用了辛辣调料！"
        }


class RottenIngredient(Skill):
    """腐烂食材 - 造成毒属性伤害并附加中毒"""
    
    def __init__(self):
        super().__init__(
            name="☠️腐烂食材",
            skill_type=SkillType.ACTIVE,
            mp_cost=15,
            cooldown=3,
            description="投掷腐烂的食材，造成毒属性伤害并使目标中毒"
        )
    
    def execute(self, caster, target=None) -> Dict[str, Any]:
        """执行技能"""
        damage = 25 + caster.attack * 0.9
        caster.mp -= self.mp_cost
        self.current_cooldown = self.cooldown
        
        # 必定附加中毒
        poison_applied = False
        if target:
            poison_effect = PoisonEffect(duration=4, percent_per_turn=0.08)
            target.status_manager.add_status(poison_effect)
            poison_applied = True
            target.take_damage(int(damage), DamageType.MAGICAL)
        
        return {
            'success': True,
            'damage': int(damage),
            'damage_type': 'poison',
            'poison_applied': poison_applied,
            'message': f"{caster.name}投掷了腐烂的食材！"
        }


class CookingFury(Skill):
    """烹饪狂怒 - 提升自身攻击力"""
    
    def __init__(self):
        super().__init__(
            name="🍳烹饪狂怒",
            skill_type=SkillType.ACTIVE,
            mp_cost=20,
            cooldown=4,
            description="进入烹饪狂怒状态，大幅提升攻击力"
        )
    
    def execute(self, caster, target=None) -> Dict[str, Any]:
        """执行技能"""
        caster.mp -= self.mp_cost
        self.current_cooldown = self.cooldown
        
        # 提升攻击力
        attack_buff = AttackBuffEffect(duration=3, attack_bonus=15)
        caster.status_manager.add_status(attack_buff)
        
        return {
            'success': True,
            'attack_boost': 15,
            'duration': 3,
            'message': f"{caster.name}进入了烹饪狂怒状态！"
        }


class ChefSpecial(Skill):
    """厨师特技 - 造成大量伤害并有几率眩晕"""
    
    def __init__(self):
        super().__init__(
            name="👨‍🍳厨师特技",
            skill_type=SkillType.ULTIMATE,
            mp_cost=30,
            cooldown=5,
            description="哥布林厨师长的招牌绝技，造成大量伤害并有几率眩晕目标"
        )
    
    def execute(self, caster, target=None) -> Dict[str, Any]:
        """执行技能"""
        damage = 40 + caster.attack * 1.2
        caster.mp -= self.mp_cost
        self.current_cooldown = self.cooldown
        
        # 30%几率眩晕
        stun_applied = False
        if random.random() < 0.3 and target:
            stun_effect = StunEffect(duration=1)
            target.status_manager.add_status(stun_effect)
            stun_applied = True
        
        if target:
            target.take_damage(int(damage), DamageType.MAGICAL)
        
        return {
            'success': True,
            'damage': int(damage),
            'stun_applied': stun_applied,
            'message': f"{caster.name}使出了厨师特技！"
        }


class LeftoverStew(Skill):
    """剩菜炖锅 - 恢复自身生命值"""
    
    def __init__(self):
        super().__init__(
            name="🥘剩菜炖锅",
            skill_type=SkillType.ACTIVE,
            mp_cost=15,
            cooldown=3,
            description="喝下一锅剩菜炖锅，恢复自身生命值"
        )
    
    def execute(self, caster, target=None) -> Dict[str, Any]:
        """执行技能"""
        caster.mp -= self.mp_cost
        self.current_cooldown = self.cooldown
        
        # 恢复生命值
        heal_amount = 30 + caster.level * 5
        actual_heal = min(heal_amount, caster.max_hp - caster.hp)
        caster.hp += actual_heal
        
        return {
            'success': True,
            'heal_amount': actual_heal,
            'message': f"{caster.name}喝下了剩菜炖锅，恢复了{actual_heal}点生命值！"
        }


# 哥布林厨师长的所有技能
GOBLIN_CHEF_SKILLS = [
    SpicySeasoning(),
    RottenIngredient(),
    CookingFury(),
    ChefSpecial(),
    LeftoverStew()
]
