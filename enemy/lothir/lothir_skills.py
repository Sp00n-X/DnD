"""洛希尔地区敌人技能"""

from characters.skills.base_skill import Skill, SkillType
from characters.equipments.base_equipments import DamageType
from typing import Dict, Any
import random

class WaterMirror(Skill):
    """水镜术 - 制造幻象分身"""
    
    def __init__(self):
        super().__init__(
            name="水镜术",
            skill_type=SkillType.ACTIVE,
            mp_cost=15,
            cooldown=3,
            description="制造一个水分身，增加自身防御力"
        )
    
    def execute(self, caster, target) -> Dict[str, Any]:
        """执行技能"""
        if not self.can_use(caster):
            return {"success": False, "message": f"{caster.name}无法使用{self.name}！"}
        
        caster.mp -= self.mp_cost
        self.current_cooldown = self.cooldown
        
        # 增加防御力
        caster.base_defense += 5
        caster.recalc_stats()
        
        return {
            "success": True,
            "message": f"{caster.name}使用{self.name}，防御力提升了！",
            "damage": 0
        }

class VenomStrike(Skill):
    """毒击 - 造成中毒效果"""
    
    def __init__(self):
        super().__init__(
            name="毒击",
            skill_type=SkillType.ACTIVE,
            mp_cost=10,
            cooldown=2,
            description="用毒液攻击敌人，造成中毒效果"
        )
    
    def execute(self, caster, target) -> Dict[str, Any]:
        """执行技能"""
        if not self.can_use(caster):
            return {"success": False, "message": f"{caster.name}无法使用{self.name}！"}
        
        caster.mp -= self.mp_cost
        self.current_cooldown = self.cooldown
        
        # 计算伤害
        damage = max(1, 15 + caster.attack - target.defense)
        target.take_damage(damage, DamageType.PHYSICAL)
        
        # 50%概率造成中毒
        poison_applied = False
        if random.random() < 0.5:
            poison_applied = True
        
        message = f"{caster.name}使用{self.name}，对{target.name}造成{damage}点伤害！"
        if poison_applied:
            message += " 并附加了中毒效果！"
        
        return {
            "success": True,
            "message": message,
            "damage": damage,
            "poison_applied": poison_applied
        }

class StarlightBurst(Skill):
    """星辉爆发 - 魔法攻击"""
    
    def __init__(self):
        super().__init__(
            name="星辉爆发",
            skill_type=SkillType.ACTIVE,
            mp_cost=20,
            cooldown=3,
            description="释放星辉能量进行魔法攻击"
        )
    
    def execute(self, caster, target) -> Dict[str, Any]:
        """执行技能"""
        if not self.can_use(caster):
            return {"success": False, "message": f"{caster.name}无法使用{self.name}！"}
        
        caster.mp -= self.mp_cost
        self.current_cooldown = self.cooldown
        
        # 计算伤害
        damage = max(1, 25 + caster.spell_power - target.defense)
        target.take_damage(damage, DamageType.MAGICAL)
        
        return {
            "success": True,
            "message": f"{caster.name}使用{self.name}，对{target.name}造成{damage}点魔法伤害！",
            "damage": damage
        }

class Regeneration(Skill):
    """再生 - 恢复生命值"""
    
    def __init__(self):
        super().__init__(
            name="再生",
            skill_type=SkillType.ACTIVE,
            mp_cost=15,
            cooldown=4,
            description="恢复自身生命值"
        )
    
    def execute(self, caster, target) -> Dict[str, Any]:
        """执行技能"""
        if not self.can_use(caster):
            return {"success": False, "message": f"{caster.name}无法使用{self.name}！"}
        
        caster.mp -= self.mp_cost
        self.current_cooldown = self.cooldown
        
        # 恢复生命值
        heal_amount = 20 + caster.spell_power // 2
        caster.hp = min(caster.hp + heal_amount, caster.max_hp)
        
        return {
            "success": True,
            "message": f"{caster.name}使用{self.name}，恢复了{heal_amount}点生命值！",
            "heal_amount": heal_amount
        }

class RootStrike(Skill):
    """根须打击 - 物理攻击"""
    
    def __init__(self):
        super().__init__(
            name="根须打击",
            skill_type=SkillType.ACTIVE,
            mp_cost=12,
            cooldown=2,
            description="用根须进行强力物理攻击"
        )
    
    def execute(self, caster, target) -> Dict[str, Any]:
        """执行技能"""
        if not self.can_use(caster):
            return {"success": False, "message": f"{caster.name}无法使用{self.name}！"}
        
        caster.mp -= self.mp_cost
        self.current_cooldown = self.cooldown
        
        # 计算伤害
        damage = max(1, 20 + caster.attack - target.defense)
        target.take_damage(damage, DamageType.PHYSICAL)
        
        return {
            "success": True,
            "message": f"{caster.name}使用{self.name}，对{target.name}造成{damage}点物理伤害！",
            "damage": damage
        }

class CanopySlash(Skill):
    """树冠斩击 - 高伤害物理攻击"""
    
    def __init__(self):
        super().__init__(
            name="树冠斩击",
            skill_type=SkillType.ACTIVE,
            mp_cost=18,
            cooldown=3,
            description="从高处发动强力斩击"
        )
    
    def execute(self, caster, target) -> Dict[str, Any]:
        """执行技能"""
        if not self.can_use(caster):
            return {"success": False, "message": f"{caster.name}无法使用{self.name}！"}
        
        caster.mp -= self.mp_cost
        self.current_cooldown = self.cooldown
        
        # 计算伤害
        damage = max(1, 30 + caster.attack - target.defense)
        target.take_damage(damage, DamageType.PHYSICAL)
        
        return {
            "success": True,
            "message": f"{caster.name}使用{self.name}，对{target.name}造成{damage}点物理伤害！",
            "damage": damage
        }

class UndergrowthAmbush(Skill):
    """灌木伏击 - 突袭攻击"""
    
    def __init__(self):
        super().__init__(
            name="灌木伏击",
            skill_type=SkillType.ACTIVE,
            mp_cost=15,
            cooldown=2,
            description="从灌木中发动突袭"
        )
    
    def execute(self, caster, target) -> Dict[str, Any]:
        """执行技能"""
        if not self.can_use(caster):
            return {"success": False, "message": f"{caster.name}无法使用{self.name}！"}
        
        caster.mp -= self.mp_cost
        self.current_cooldown = self.cooldown
        
        # 计算伤害
        damage = max(1, 22 + caster.attack - target.defense)
        target.take_damage(damage, DamageType.PHYSICAL)
        
        return {
            "success": True,
            "message": f"{caster.name}使用{self.name}，对{target.name}造成{damage}点物理伤害！",
            "damage": damage
        }

class BridgeCharge(Skill):
    """桥梁冲锋 - 冲锋攻击"""
    
    def __init__(self):
        super().__init__(
            name="桥梁冲锋",
            skill_type=SkillType.ACTIVE,
            mp_cost=20,
            cooldown=3,
            description="从桥梁上发动冲锋攻击"
        )
    
    def execute(self, caster, target) -> Dict[str, Any]:
        """执行技能"""
        if not self.can_use(caster):
            return {"success": False, "message": f"{caster.name}无法使用{self.name}！"}
        
        caster.mp -= self.mp_cost
        self.current_cooldown = self.cooldown
        
        # 计算伤害
        damage = max(1, 28 + caster.attack - target.defense)
        target.take_damage(damage, DamageType.PHYSICAL)
        
        return {
            "success": True,
            "message": f"{caster.name}使用{self.name}，对{target.name}造成{damage}点物理伤害！",
            "damage": damage
        }
