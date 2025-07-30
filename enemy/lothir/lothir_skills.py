"""
洛希尔生物专用技能
基于翡翠之森·洛希尔的生态特征设计
"""

from typing import Any, Dict, List
from characters.skills.base_skill import Skill, SkillType
from characters.equipments.base_equipments import DamageType
from status_effects import BurnEffect, FreezeEffect, PoisonEffect, StunEffect

# 冠幕层技能
class WebShot(Skill):
    """蛛网射击：束缚敌人"""
    
    def __init__(self):
        super().__init__(
            name="蛛网射击",
            skill_type=SkillType.ACTIVE,
            mp_cost=5,
            cooldown=1,
            description="发射粘性蛛网束缚目标，降低其移动速度",
            level_requirement=1
        )
    
    def execute(self, caster, target=None) -> Dict[str, Any]:
        if not target:
            return {"success": False, "message": "需要指定目标"}
        
        damage = 8 + caster.attack // 3
        target.take_damage(damage, DamageType.PHYSICAL)
        
        # 添加减速效果
        from status_effects import SpeedDebuffEffect
        slow_effect = SpeedDebuffEffect(duration=2, speed_reduction=30)
        target.add_status_effect(slow_effect)
        
        return {
            "success": True,
            "message": f"{caster.name} 的蛛网射击对 {target.name} 造成 {damage} 点伤害并使其减速！"
        }

class StarlightBurst(Skill):
    """星辉爆发：魔法伤害"""
    
    def __init__(self):
        super().__init__(
            name="星辉爆发",
            skill_type=SkillType.ACTIVE,
            mp_cost=12,
            cooldown=2,
            description="释放储存的星辉能量造成魔法伤害",
            level_requirement=2
        )
    
    def execute(self, caster, target=None) -> Dict[str, Any]:
        if not target:
            return {"success": False, "message": "需要指定目标"}
        
        damage = 15 + caster.spell_power // 2
        target.take_damage(damage, DamageType.MAGICAL)
        
        return {
            "success": True,
            "message": f"{caster.name} 的星辉爆发对 {target.name} 造成 {damage} 点魔法伤害！"
        }

class WindBlade(Skill):
    """风刃：风属性攻击"""
    
    def __init__(self):
        super().__init__(
            name="风刃",
            skill_type=SkillType.ACTIVE,
            mp_cost=8,
            cooldown=1,
            description="挥动翅膀发射锋利的风刃",
            level_requirement=1
        )
    
    def execute(self, caster, target=None) -> Dict[str, Any]:
        if not target:
            return {"success": False, "message": "需要指定目标"}
        
        damage = 12 + caster.attack // 2
        target.take_damage(damage, DamageType.MAGICAL)
        
        return {
            "success": True,
            "message": f"{caster.name} 的风刃对 {target.name} 造成 {damage} 点风属性伤害！"
        }

class DiveAttack(Skill):
    """俯冲攻击：高伤害物理攻击"""
    
    def __init__(self):
        super().__init__(
            name="俯冲攻击",
            skill_type=SkillType.ACTIVE,
            mp_cost=10,
            cooldown=2,
            description="从高空俯冲而下，造成巨大物理伤害",
            level_requirement=3
        )
    
    def execute(self, caster, target=None) -> Dict[str, Any]:
        if not target:
            return {"success": False, "message": "需要指定目标"}
        
        damage = 20 + caster.attack
        target.take_damage(damage, DamageType.PHYSICAL)
        
        return {
            "success": True,
            "message": f"{caster.name} 的俯冲攻击对 {target.name} 造成 {damage} 点物理伤害！"
        }

# 枝桥层技能
class MirrorImage(Skill):
    """镜像分身：创建幻象"""
    
    def __init__(self):
        super().__init__(
            name="镜像分身",
            skill_type=SkillType.ACTIVE,
            mp_cost=15,
            cooldown=3,
            description="创建镜像分身迷惑敌人",
            level_requirement=2
        )
    
    def execute(self, caster, target=None) -> Dict[str, Any]:
        # 添加闪避提升效果
        from status_effects import DodgeBuffEffect
        dodge_buff = DodgeBuffEffect(duration=2, dodge_chance=30)
        caster.add_status_effect(dodge_buff)
        
        return {
            "success": True,
            "message": f"{caster.name} 使用镜像分身，闪避率大幅提升！"
        }

class QuickStrike(Skill):
    """迅捷打击：快速攻击"""
    
    def __init__(self):
        super().__init__(
            name="迅捷打击",
            skill_type=SkillType.ACTIVE,
            mp_cost=5,
            cooldown=0,
            description="快速攻击目标",
            level_requirement=1
        )
    
    def execute(self, caster, target=None) -> Dict[str, Any]:
        if not target:
            return {"success": False, "message": "需要指定目标"}
        
        damage = 10 + caster.attack // 2
        target.take_damage(damage, DamageType.PHYSICAL)
        
        return {
            "success": True,
            "message": f"{caster.name} 的迅捷打击对 {target.name} 造成 {damage} 点伤害！"
        }

# 灌草层技能
class MoonAntlerStrike(Skill):
    """月角冲击：月属性攻击"""
    
    def __init__(self):
        super().__init__(
            name="月角冲击",
            skill_type=SkillType.ACTIVE,
            mp_cost=8,
            cooldown=1,
            description="用月轮角发动强力冲击",
            level_requirement=2
        )
    
    def execute(self, caster, target=None) -> Dict[str, Any]:
        if not target:
            return {"success": False, "message": "需要指定目标"}
        
        damage = 15 + caster.attack
        target.take_damage(damage, DamageType.MAGICAL)
        
        return {
            "success": True,
            "message": f"{caster.name} 的月角冲击对 {target.name} 造成 {damage} 点月属性伤害！"
        }

class LunarBlessing(Skill):
    """月之祝福：治疗技能"""
    
    def __init__(self):
        super().__init__(
            name="月之祝福",
            skill_type=SkillType.ACTIVE,
            mp_cost=20,
            cooldown=3,
            description="沐浴月光恢复生命值",
            level_requirement=3
        )
    
    def execute(self, caster, target=None) -> Dict[str, Any]:
        heal_amount = 25 + caster.spell_power
        caster.heal(heal_amount)
        
        return {
            "success": True,
            "message": f"{caster.name} 使用月之祝福恢复了 {heal_amount} 点生命值！"
        }

# 苔根层技能
class ShadowStep(Skill):
    """暗影步：瞬移攻击"""
    
    def __init__(self):
        super().__init__(
            name="暗影步",
            skill_type=SkillType.ACTIVE,
            mp_cost=15,
            cooldown=2,
            description="瞬移到敌人身后发动致命一击",
            level_requirement=4
        )
    
    def execute(self, caster, target=None) -> Dict[str, Any]:
        if not target:
            return {"success": False, "message": "需要指定目标"}
        
        damage = 25 + caster.attack * 1.5
        target.take_damage(int(damage), DamageType.PHYSICAL)
        
        return {
            "success": True,
            "message": f"{caster.name} 使用暗影步瞬移到 {target.name} 身后，造成 {int(damage)} 点致命伤害！"
        }

class Pounce(Skill):
    """猛扑：突袭攻击"""
    
    def __init__(self):
        super().__init__(
            name="猛扑",
            skill_type=SkillType.ACTIVE,
            mp_cost=12,
            cooldown=2,
            description="从阴影中猛扑而出",
            level_requirement=3
        )
    
    def execute(self, caster, target=None) -> Dict[str, Any]:
        if not target:
            return {"success": False, "message": "需要指定目标"}
        
        damage = 18 + caster.attack
        target.take_damage(damage, DamageType.PHYSICAL)
        
        # 添加眩晕效果
        stun_effect = StunEffect(duration=1)
        target.add_status_effect(stun_effect)
        
        return {
            "success": True,
            "message": f"{caster.name} 的猛扑对 {target.name} 造成 {damage} 点伤害并使其眩晕！"
        }

# 幽沼带技能
class WaterMirror(Skill):
    """水镜幻象：创造水分身"""
    
    def __init__(self):
        super().__init__(
            name="水镜幻象",
            skill_type=SkillType.ACTIVE,
            mp_cost=20,
            cooldown=3,
            description="用水面创造幻象分身",
            level_requirement=3
        )
    
    def execute(self, caster, target=None) -> Dict[str, Any]:
        # 添加闪避效果
        from status_effects import DodgeBuffEffect
        dodge_buff = DodgeBuffEffect(duration=2, dodge_chance=40)
        caster.add_status_effect(dodge_buff)
        
        return {
            "success": True,
            "message": f"{caster.name} 使用水镜幻象，创造出迷惑敌人的水分身！"
        }

class VenomStrike(Skill):
    """剧毒打击：毒属性攻击"""
    
    def __init__(self):
        super().__init__(
            name="剧毒打击",
            skill_type=SkillType.ACTIVE,
            mp_cost=10,
            cooldown=2,
            description="注入致命毒素",
            level_requirement=2
        )
    
    def execute(self, caster, target=None) -> Dict[str, Any]:
        if not target:
            return {"success": False, "message": "需要指定目标"}
        
        damage = 12 + caster.attack // 2
        target.take_damage(damage, DamageType.PHYSICAL)
        
        # 添加中毒效果
        poison_effect = PoisonEffect(duration=3, damage_per_turn=8)
        target.add_status_effect(poison_effect)
        
        return {
            "success": True,
            "message": f"{caster.name} 的剧毒打击对 {target.name} 造成 {damage} 点伤害并附加中毒效果！"
        }

# 植物类技能
class VineWhip(Skill):
    """藤鞭抽打：植物攻击"""
    
    def __init__(self):
        super().__init__(
            name="藤鞭抽打",
            skill_type=SkillType.ACTIVE,
            mp_cost=8,
            cooldown=1,
            description="用藤蔓鞭打敌人",
            level_requirement=1
        )
    
    def execute(self, caster, target=None) -> Dict[str, Any]:
        if not target:
            return {"success": False, "message": "需要指定目标"}
        
        damage = 10 + caster.attack // 2
        target.take_damage(damage, DamageType.PHYSICAL)
        
        return {
            "success": True,
            "message": f"{caster.name} 的藤鞭抽打对 {target.name} 造成 {damage} 点伤害！"
        }

class Regeneration(Skill):
    """再生：恢复生命值"""
    
    def __init__(self):
        super().__init__(
            name="再生",
            skill_type=SkillType.ACTIVE,
            mp_cost=15,
            cooldown=3,
            description="激活植物再生能力",
            level_requirement=2
        )
    
    def execute(self, caster, target=None) -> Dict[str, Any]:
        heal_amount = 20 + caster.spell_power
        caster.heal(heal_amount)
        
        # 添加持续恢复效果
        from status_effects import HealOverTimeEffect
        regen_effect = HealOverTimeEffect(duration=3, heal_per_turn=5)
        caster.add_status_effect(regen_effect)
        
        return {
            "success": True,
            "message": f"{caster.name} 使用再生恢复了 {heal_amount} 点生命值，并获得持续恢复效果！"
        }

# 通用技能
class ShellShield(Skill):
    """甲壳防御：提升防御"""
    
    def __init__(self):
        super().__init__(
            name="甲壳防御",
            skill_type=SkillType.ACTIVE,
            mp_cost=10,
            cooldown=2,
            description="用坚硬甲壳保护自己",
            level_requirement=1
        )
    
    def execute(self, caster, target=None) -> Dict[str, Any]:
        # 添加防御提升效果
        from status_effects import DefenseBuffEffect
        defense_buff = DefenseBuffEffect(duration=3, defense_bonus=20)
        caster.add_status_effect(defense_buff)
        
        return {
            "success": True,
            "message": f"{caster.name} 使用甲壳防御，防御力大幅提升！"
        }

class RamAttack(Skill):
    """冲撞攻击：物理攻击"""
    
    def __init__(self):
        super().__init__(
            name="冲撞攻击",
            skill_type=SkillType.ACTIVE,
            mp_cost=5,
            cooldown=1,
            description="用身体冲撞敌人",
            level_requirement=1
        )
    
    def execute(self, caster, target=None) -> Dict[str, Any]:
        if not target:
            return {"success": False, "message": "需要指定目标"}
        
        damage = 15 + caster.attack
        target.take_damage(damage, DamageType.PHYSICAL)
        
        return {
            "success": True,
            "message": f"{caster.name} 的冲撞攻击对 {target.name} 造成 {damage} 点伤害！"
        }

# 导出所有技能
__all__ = [
    # 冠幕层技能
    'WebShot', 'StarlightBurst', 'WindBlade', 'DiveAttack',
    
    # 枝桥层技能
    'MirrorImage', 'QuickStrike',
    
    # 灌草层技能
    'MoonAntlerStrike', 'LunarBlessing',
    
    # 苔根层技能
    'ShadowStep', 'Pounce',
    
    # 幽沼带技能
    'WaterMirror', 'VenomStrike',
    
    # 植物技能
    'VineWhip', 'Regeneration',
    
    # 通用技能
    'ShellShield', 'RamAttack'
]
