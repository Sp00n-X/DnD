"""攻击模式系统 - 为敌人设计不同的攻击策略"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import random
from characters.skills.base_skill import Skill
from characters.base_character import BaseCharacter


class AttackPattern(ABC):
    """攻击模式基类"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
    
    @abstractmethod
    def select_action(self, attacker: BaseCharacter, target: BaseCharacter, 
                     available_skills: List[Skill]) -> Dict[str, Any]:
        """选择要执行的动作（技能或普通攻击）"""
        pass
    
    def can_use_skill(self, skill: Skill, attacker: BaseCharacter) -> bool:
        """检查是否可以使用技能"""
        return skill.can_use(attacker)


class RandomSkillPattern(AttackPattern):
    """随机技能模式 - 随机选择可用技能"""
    
    def __init__(self):
        super().__init__("随机技能", "随机选择可用的技能进行攻击")
    
    def select_action(self, attacker: BaseCharacter, target: BaseCharacter, 
                     available_skills: List[Skill]) -> Dict[str, Any]:
        """随机选择技能或普通攻击"""
        usable_skills = [skill for skill in available_skills if self.can_use_skill(skill, attacker)]
        
        if usable_skills and random.random() < 0.7:  # 70%概率使用技能
            selected_skill = random.choice(usable_skills)
            return {
                'type': 'skill',
                'skill': selected_skill,
                'target': target
            }
        else:
            return {
                'type': 'attack',
                'target': target
            }


class SequentialSkillPattern(AttackPattern):
    """顺序技能模式 - 按顺序使用技能"""
    
    def __init__(self):
        super().__init__("顺序技能", "按固定顺序循环使用技能")
        self.current_index = 0
    
    def select_action(self, attacker: BaseCharacter, target: BaseCharacter, 
                     available_skills: List[Skill]) -> Dict[str, Any]:
        """按顺序选择技能"""
        usable_skills = [skill for skill in available_skills if self.can_use_skill(skill, attacker)]
        
        if usable_skills:
            selected_skill = usable_skills[self.current_index % len(usable_skills)]
            self.current_index += 1
            return {
                'type': 'skill',
                'skill': selected_skill,
                'target': target
            }
        else:
            return {
                'type': 'attack',
                'target': target
            }


class PrioritySkillPattern(AttackPattern):
    """优先级技能模式 - 根据优先级选择技能"""
    
    def __init__(self, priority_rules: Dict[str, Any] = None):
        super().__init__("优先级技能", "根据血量等条件优先选择技能")
        self.priority_rules = priority_rules or {}
    
    def select_action(self, attacker: BaseCharacter, target: BaseCharacter, 
                     available_skills: List[Skill]) -> Dict[str, Any]:
        """根据优先级选择技能"""
        usable_skills = [skill for skill in available_skills if self.can_use_skill(skill, attacker)]
        
        if not usable_skills:
            return {
                'type': 'attack',
                'target': target
            }
        
        # 根据血量选择技能
        hp_ratio = attacker.hp / attacker.max_hp
        
        if hp_ratio < 0.3 and any("治疗" in skill.name for skill in usable_skills):
            # 优先使用治疗技能
            heal_skill = next(skill for skill in usable_skills if "治疗" in skill.name)
            return {
                'type': 'skill',
                'skill': heal_skill,
                'target': attacker
            }
        elif hp_ratio < 0.5 and any("防御" in skill.name for skill in usable_skills):
            # 优先使用防御技能
            defense_skill = next(skill for skill in usable_skills if "防御" in skill.name)
            return {
                'type': 'skill',
                'skill': defense_skill,
                'target': attacker
            }
        else:
            # 随机选择攻击技能
            attack_skills = [skill for skill in usable_skills if "攻击" in skill.name or "伤害" in skill.name]
            if attack_skills:
                selected_skill = random.choice(attack_skills)
            else:
                selected_skill = random.choice(usable_skills)
            
            return {
                'type': 'skill',
                'skill': selected_skill,
                'target': target
            }


class EnragedPattern(AttackPattern):
    """狂暴模式 - 低血量时增强攻击"""
    
    def __init__(self, enrage_threshold: float = 0.3):
        super().__init__("狂暴", "生命值低于阈值时进入狂暴状态")
        self.enrage_threshold = enrage_threshold
        self.is_enraged = False
    
    def select_action(self, attacker: BaseCharacter, target: BaseCharacter, 
                     available_skills: List[Skill]) -> Dict[str, Any]:
        """狂暴状态下的攻击选择"""
        hp_ratio = attacker.hp / attacker.max_hp
        
        if hp_ratio <= self.enrage_threshold:
            self.is_enraged = True
        
        usable_skills = [skill for skill in available_skills if self.can_use_skill(skill, attacker)]
        
        if self.is_enraged and usable_skills:
            # 狂暴状态下优先使用最强技能
            strongest_skill = max(usable_skills, key=lambda s: getattr(s, 'damage', 0))
            return {
                'type': 'skill',
                'skill': strongest_skill,
                'target': target,
                'enraged': True
            }
        elif usable_skills and random.random() < 0.5:
            selected_skill = random.choice(usable_skills)
            return {
                'type': 'skill',
                'skill': selected_skill,
                'target': target
            }
        else:
            return {
                'type': 'attack',
                'target': target,
                'enraged': self.is_enraged
            }
