"""Boss技能模板 - 为新Boss创建技能的参考模板"""

from characters.skills.base_skill import Skill, SkillType
from status_effects.status_effects import BurnEffect, PoisonEffect, AttackBuffEffect, StunEffect, DefenseBuffEffect
from characters.equipments.base_equipments import DamageType
from typing import Dict, Any
import random


# ============= 模板技能类 =============

class TemplateBasicAttack(Skill):
    """基础攻击 - 造成物理伤害"""
    
    def __init__(self):
        super().__init__(
            name="⚔️基础攻击",
            skill_type=SkillType.ACTIVE,
            mp_cost=5,
            cooldown=1,
            description="造成基础物理伤害"
        )
    
    def execute(self, caster, target=None) -> Dict[str, Any]:
        """执行技能"""
        damage = 15 + caster.attack * 0.6
        caster.mp -= self.mp_cost
        self.current_cooldown = self.cooldown
        
        if target:
            target.take_damage(int(damage), DamageType.PHYSICAL)
        
        return {
            'success': True,
            'damage': int(damage),
            'damage_type': 'physical',
            'message': f"{caster.name}进行了基础攻击！"
        }


class TemplateMagicAttack(Skill):
    """魔法攻击 - 造成魔法伤害"""
    
    def __init__(self):
        super().__init__(
            name="✨魔法攻击",
            skill_type=SkillType.ACTIVE,
            mp_cost=15,
            cooldown=2,
            description="释放魔法能量，造成魔法伤害"
        )
    
    def execute(self, caster, target=None) -> Dict[str, Any]:
        """执行技能"""
        damage = 25 + caster.attack * 0.8
        caster.mp -= self.mp_cost
        self.current_cooldown = self.cooldown
        
        if target:
            target.take_damage(int(damage), DamageType.MAGICAL)
        
        return {
            'success': True,
            'damage': int(damage),
            'damage_type': 'magical',
            'message': f"{caster.name}释放了魔法攻击！"
        }


class TemplateBuffSkill(Skill):
    """增益技能 - 提升自身属性"""
    
    def __init__(self):
        super().__init__(
            name="🛡️防御姿态",
            skill_type=SkillType.ACTIVE,
            mp_cost=20,
            cooldown=3,
            description="进入防御姿态，提升防御力"
        )
    
    def execute(self, caster, target=None) -> Dict[str, Any]:
        """执行技能"""
        caster.mp -= self.mp_cost
        self.current_cooldown = self.cooldown
        
        # 提升防御力
        defense_buff = DefenseBuffEffect(duration=3, defense_bonus=10)
        caster.status_manager.add_status(defense_buff)
        
        return {
            'success': True,
            'defense_boost': 10,
            'duration': 3,
            'message': f"{caster.name}进入了防御姿态！"
        }


class TemplateUltimateSkill(Skill):
    """终极技能 - 强力攻击"""
    
    def __init__(self):
        super().__init__(
            name="💥毁灭打击",
            skill_type=SkillType.ULTIMATE,
            mp_cost=50,
            cooldown=5,
            description="释放毁灭性的攻击，造成巨大伤害"
        )
    
    def execute(self, caster, target=None) -> Dict[str, Any]:
        """执行技能"""
        damage = 60 + caster.attack * 1.5
        caster.mp -= self.mp_cost
        self.current_cooldown = self.cooldown
        
        if target:
            target.take_damage(int(damage), DamageType.PHYSICAL)
        
        return {
            'success': True,
            'damage': int(damage),
            'message': f"{caster.name}释放了毁灭打击！"
        }


# ============= 新Boss技能示例 =============

class SecondBossFireBreath(Skill):
    """火焰吐息 - 造成范围火属性伤害"""
    
    def __init__(self):
        super().__init__(
            name="🔥火焰吐息",
            skill_type=SkillType.ACTIVE,
            mp_cost=25,
            cooldown=3,
            description="喷出炽热的火焰，造成火属性伤害"
        )
    
    def execute(self, caster, target=None) -> Dict[str, Any]:
        """执行技能"""
        damage = 35 + caster.attack * 1.0
        caster.mp -= self.mp_cost
        self.current_cooldown = self.cooldown
        
        # 50%几率附加灼烧
        burn_applied = False
        if random.random() < 0.5 and target:
            burn_effect = BurnEffect(duration=3, damage_per_turn=8)
            target.status_manager.add_status(burn_effect)
            burn_applied = True
        
        if target:
            target.take_damage(int(damage), DamageType.MAGICAL)
        
        return {
            'success': True,
            'damage': int(damage),
            'damage_type': 'fire',
            'burn_applied': burn_applied,
            'message': f"{caster.name}喷出了炽热的火焰！"
        }


class SecondBossTailSwipe(Skill):
    """尾巴横扫 - 造成物理伤害并有几率眩晕"""
    
    def __init__(self):
        super().__init__(
            name="🦎尾巴横扫",
            skill_type=SkillType.ACTIVE,
            mp_cost=20,
            cooldown=2,
            description="用巨大的尾巴横扫，造成物理伤害并有几率眩晕"
        )
    
    def execute(self, caster, target=None) -> Dict[str, Any]:
        """执行技能"""
        damage = 30 + caster.attack * 0.9
        caster.mp -= self.mp_cost
        self.current_cooldown = self.cooldown
        
        # 25%几率眩晕
        stun_applied = False
        if random.random() < 0.25 and target:
            stun_effect = StunEffect(duration=1)
            target.status_manager.add_status(stun_effect)
            stun_applied = True
        
        if target:
            target.take_damage(int(damage), DamageType.PHYSICAL)
        
        return {
            'success': True,
            'damage': int(damage),
            'stun_applied': stun_applied,
            'message': f"{caster.name}用尾巴进行了横扫攻击！"
        }


# ============= 技能集合 =============

# 模板Boss技能（用于参考）
TEMPLATE_BOSS_SKILLS = [
    TemplateBasicAttack(),
    TemplateMagicAttack(),
    TemplateBuffSkill(),
    TemplateUltimateSkill()
]

# 第二Boss技能示例（龙类Boss）
DRAGON_BOSS_SKILLS = [
    SecondBossFireBreath(),
    SecondBossTailSwipe(),
    TemplateBuffSkill(),  # 可以复用模板技能
    TemplateUltimateSkill()
]

# 第三Boss技能示例（法师类Boss）
MAGE_BOSS_SKILLS = [
    TemplateMagicAttack(),
    SecondBossFireBreath(),  # 可以复用其他Boss的技能
    TemplateBuffSkill(),
    TemplateUltimateSkill()
]
