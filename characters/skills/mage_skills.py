"""法师技能 - 使用新的状态效果系统"""

from typing import Any, Dict
from status_effects import BurnEffect, FreezeEffect, DefenseBuffEffect, HealOverTimeEffect
from .base_skill import Skill, SkillType
from ..equipments.base_equipments import DamageType


class Fireball(Skill):
    """火球术：造成直接伤害并附加灼烧效果"""
    
    def __init__(self):
        super().__init__(
            name="火球术",
            skill_type=SkillType.ACTIVE,
            mp_cost=10,
            cooldown=0,
            description="发射火球造成魔法伤害，并附加灼烧效果",
            level_requirement=1
        )
    
    def execute(self, caster, target=None) -> Dict[str, Any]:
        if not target:
            return {"success": False, "message": "需要指定目标"}
        
        # 计算伤害
        damage = 20 + caster.spell_power // 2
        
        # 造成伤害
        target.take_damage(damage, DamageType.MAGICAL)
        
        # 添加灼烧效果
        burn_effect = BurnEffect(duration=2, damage_per_turn=5 + caster.spell_power // 4)
        target.add_status_effect(burn_effect)
        
        return {
            "success": True,
            "message": f"{caster.name} 的火球术对 {target.name} 造成 {damage} 点魔法伤害，并附加灼烧效果！"
        }


class FrostBolt(Skill):
    """冰冻术：造成伤害并有几率冰冻目标"""
    
    def __init__(self):
        super().__init__(
            name="冰冻术",
            skill_type=SkillType.ACTIVE,
            mp_cost=15,
            cooldown=1,
            description="发射冰箭造成伤害，并有几率冰冻目标",
            level_requirement=1
        )
    
    def execute(self, caster, target=None) -> Dict[str, Any]:
        if not target:
            return {"success": False, "message": "需要指定目标"}
        
        # 计算伤害
        damage = 15 + caster.spell_power // 2
        
        # 造成伤害
        target.take_damage(damage, DamageType.MAGICAL)
        
        # 添加冰冻效果
        freeze_effect = FreezeEffect(duration=1)
        target.add_status_effect(freeze_effect)
        
        return {
            "success": True,
            "message": f"{caster.name} 的冰冻术对 {target.name} 造成 {damage} 点魔法伤害，并使其冰冻！"
        }


class DefenseBoost(Skill):
    """防御强化：提升自身防御力"""
    
    def __init__(self):
        super().__init__(
            name="防御强化",
            skill_type=SkillType.ACTIVE,
            mp_cost=10,
            cooldown=2,
            description="短时间内大幅提升防御力",
            level_requirement=1
        )
    
    def execute(self, caster, target=None) -> Dict[str, Any]:
        # 添加防御强化效果
        defense_buff = DefenseBuffEffect(duration=3, defense_bonus=15 + caster.level * 2)
        caster.add_status_effect(defense_buff)
        
        return {
            "success": True,
            "message": f"{caster.name} 使用防御强化，防御力大幅提升！"
        }


class ManaHeal(Skill):
    """法术回复：恢复法力和生命值"""
    
    def __init__(self):
        super().__init__(
            name="法术回复",
            skill_type=SkillType.ACTIVE,
            mp_cost=0,
            cooldown=3,
            description="立即恢复法力和少量生命",
            level_requirement=1
        )
    
    def execute(self, caster, target=None) -> Dict[str, Any]:
        # 恢复法力值
        mp_restore = 30 + caster.spell_power // 2
        caster.restore_mp(mp_restore)
        
        # 恢复生命值
        hp_restore = 20 + caster.spell_power // 3
        caster.heal(hp_restore)
        
        return {
            "success": True,
            "message": f"{caster.name} 使用法术回复，恢复 {mp_restore} 点法力和 {hp_restore} 点生命！"
        }


class LightningBolt(Skill):
    """闪电术：高伤害单体魔法攻击"""
    
    def __init__(self):
        super().__init__(
            name="闪电术",
            skill_type=SkillType.ACTIVE,
            mp_cost=25,
            cooldown=2,
            description="召唤闪电造成大量魔法伤害",
            level_requirement=3
        )
    
    def execute(self, caster, target=None) -> Dict[str, Any]:
        if not target:
            return {"success": False, "message": "需要指定目标"}
        
        # 计算伤害
        damage = 35 + caster.spell_power
        
        # 造成伤害
        target.take_damage(damage, DamageType.MAGICAL)
        
        return {
            "success": True,
            "message": f"{caster.name} 的闪电术对 {target.name} 造成 {damage} 点魔法伤害！"
        }


class ArcaneIntellect(Skill):
    """奥术智慧：提升法术强度"""
    
    def __init__(self):
        super().__init__(
            name="奥术智慧",
            skill_type=SkillType.ACTIVE,
            mp_cost=15,
            cooldown=3,
            description="提升法术强度，增强魔法伤害",
            level_requirement=2
        )
    
    def execute(self, caster, target=None) -> Dict[str, Any]:
        from status_effects import AttackBuffEffect
        
        # 添加法术强度提升效果
        spell_buff = AttackBuffEffect(
            duration=4, 
            attack_bonus=10 + caster.level * 3
        )
        caster.add_status_effect(spell_buff)
        
        return {
            "success": True,
            "message": f"{caster.name} 激活奥术智慧，法术强度大幅提升！"
        }


class MeteorShower(Skill):
    """陨石术：群体伤害技能"""
    
    def __init__(self):
        super().__init__(
            name="陨石术",
            skill_type=SkillType.ACTIVE,
            mp_cost=40,
            cooldown=4,
            description="召唤陨石对所有敌人造成伤害",
            level_requirement=5
        )
    
    def execute(self, caster, targets=None) -> Dict[str, Any]:
        if not targets:
            return {"success": False, "message": "需要指定目标列表"}
        
        total_damage = 0
        messages = []
        
        for target in targets:
            # 计算伤害
            damage = 25 + caster.spell_power * 0.8
            
            # 造成伤害
            target.take_damage(int(damage), DamageType.MAGICAL)
            total_damage += int(damage)
            
            # 添加灼烧效果
            burn_effect = BurnEffect(duration=2, damage_per_turn=5)
            target.add_status_effect(burn_effect)
            
            messages.append(f"{target.name} 受到 {int(damage)} 点伤害")
        
        return {
            "success": True,
            "message": f"{caster.name} 的陨石术对所有敌人造成 {total_damage} 点总伤害！"
        }
