"""角色基类 - 使用新的状态效果系统"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional, Any

from .equipments.base_equipments import Armor, DamageEffect, DamageType, EquipSlot, Equipment, PercentModifier, Stat, Weapon
from status_effects import StatusManager
from .skills.base_skill import Skill, SkillType


class CharacterClass(Enum):
    WARRIOR = "战士"
    MAGE = "法师"
    ROGUE = "盗贼"
    CLERIC = "牧师"

class ItemType(Enum):
    WEAPON = "weapon"
    ARMOR = "armor"
    ACCESSORY = "accessory"
    CONSUMABLE = "consumable"
    MATERIAL = "material"


class Item:
    """物品基类"""
    def __init__(self, name: str, item_type: ItemType, description: str = "", 
                 value: int = 0, stackable: bool = False, max_stack: int = 1):
        self.name = name
        self.item_type = item_type
        self.description = description
        self.value = value
        self.stackable = stackable
        self.max_stack = max_stack
        self.quantity = 1

    def use(self, character) -> bool:
        """使用物品，子类重写实现具体效果"""
        return False

    def to_dict(self) -> Dict:
        return {
            'name': self.name,
            'item_type': self.item_type.value,
            'description': self.description,
            'value': self.value,
            'quantity': self.quantity
        }


class Inventory:
    """背包系统"""
    def __init__(self, max_slots: int = 30):
        self.items: List[Item] = []
        self.max_slots = max_slots

    def add_item(self, item: Item, quantity: int = 1) -> bool:
        """添加物品到背包"""
        if item.stackable:
            for existing_item in self.items:
                if (existing_item.name == item.name and 
                    existing_item.quantity + quantity <= existing_item.max_stack):
                    existing_item.quantity += quantity
                    return True
        
        if len(self.items) >= self.max_slots:
            return False
        
        item.quantity = quantity
        self.items.append(item)
        return True

    def remove_item(self, item_name: str, quantity: int = 1) -> bool:
        """从背包移除物品"""
        for item in self.items:
            if item.name == item_name:
                if item.quantity >= quantity:
                    item.quantity -= quantity
                    if item.quantity <= 0:
                        self.items.remove(item)
                    return True
        return False

    def get_item(self, item_name: str) -> Optional[Item]:
        """获取指定物品"""
        for item in self.items:
            if item.name == item_name:
                return item
        return None

    def list_items(self) -> List[Dict]:
        """列出所有物品"""
        return [item.to_dict() for item in self.items]


class BaseCharacter(ABC):
    """角色基类"""
    
    def __init__(self, name: str, level: int = 1):
        # 基本信息
        self.name = name
        self.level = level
        self.experience = 0
        self.experience_to_next_level = self._calculate_exp_required(level)
        
        # 基础属性
        self.base_hp = 100
        self.base_attack = 10
        self.base_defense = 5
        self.base_mp = 50
        self.base_spell_power = 8
        
        # 当前属性（受状态效果影响）
        self.max_hp = self.base_hp
        self.hp = self.max_hp
        self.attack = self.base_attack
        self.defense = self.base_defense
        self.max_mp = self.base_mp
        self.mp = self.max_mp
        self.spell_power = self.base_spell_power
        
        # 系统组件
        self.inventory = Inventory()
        self.weapon: Optional[Weapon] = None
        self.armor: Dict[EquipSlot, Optional[Armor]] = {
            slot: None for slot in [EquipSlot.UPPER, EquipSlot.LOWER, EquipSlot.ACCESSORY]
        }
        self.skills: List[Skill] = []
        
        # 状态管理器 - 管理所有状态效果
        self.status_manager = StatusManager(self)
        
        # 状态相关属性
        self.can_act = True
        self.can_cast = True
        
        # 装备系统
        self.equipment: Dict[EquipSlot, Optional[Equipment]] = {
            slot: None for slot in EquipSlot
        }
        self._percent_pool: Dict[Stat, float] = {s: 0.0 for s in Stat}
        
        # 初始化属性
        self.recalc_stats()

    def recalc_stats(self):
        """重新计算属性（包括装备和状态效果）"""
        # 基础属性计算（装备加成）
        mult = {s: 1 + self._percent_pool[s] for s in Stat}
        
        # 计算状态效果提供的属性加成
        status_hp_bonus = self.status_manager.get_total_effect_value('hp_bonus')
        status_attack_bonus = self.status_manager.get_total_effect_value('attack_bonus')
        status_defense_bonus = self.status_manager.get_total_effect_value('defense_bonus')
        status_mp_bonus = self.status_manager.get_total_effect_value('mp_bonus')
        status_spell_power_bonus = self.status_manager.get_total_effect_value('spell_power_bonus')
        
        # 应用所有加成
        self.max_hp = int(self.base_hp * mult[Stat.HP] + status_hp_bonus)
        self.attack = int(self.base_attack * mult[Stat.ATTACK] + status_attack_bonus)
        self.defense = int(self.base_defense * mult[Stat.DEFENSE] + status_defense_bonus)
        self.max_mp = int(self.base_mp * mult[Stat.MP] + status_mp_bonus)
        self.spell_power = int(self.base_spell_power * mult[Stat.SPELL_POWER] + status_spell_power_bonus)
        
        # 确保当前值不超过最大值
        self.hp = min(self.hp, self.max_hp)
        self.mp = min(self.mp, self.max_mp)

    def equip(self, eq: Equipment) -> None:
        """装备物品"""
        old = self.equipment[eq.slot]
        if old:
            self._apply_modifiers_from_equipment(old, remove=True)
        self._apply_modifiers_from_equipment(eq, remove=False)
        
        self.equipment[eq.slot] = eq
        self.recalc_stats()
        print(f"{self.name} 装备了 {eq.name}")

    def unequip(self, slot: EquipSlot) -> None:
        """卸下装备"""
        eq = self.equipment.get(slot)
        if not eq:
            return
        self._apply_modifiers_from_equipment(eq, remove=True)
        self.equipment[slot] = None
        self.recalc_stats()
        print(f"{self.name} 卸下了 {eq.name}")

    def _apply_modifiers_from_equipment(self, eq: Equipment, remove: bool = False):
        """应用装备修饰符"""
        sign = -1 if remove else 1
        for mod in eq.percent_mods:
            self._percent_pool[mod.stat] += sign * mod.percent

    def attack_target(self, target: "BaseCharacter"):
        """攻击目标"""
        if not self.can_act:
            print(f"{self.name} 无法行动！")
            return
            
        damage = max(1, self.attack - target.defense)
        target.take_damage(damage, DamageType.PHYSICAL)
        print(f"{self.name} 普攻造成 {damage} 点伤害")
        
        # 触发装备效果
        for eq in self.equipment.values():
            if eq:
                for eff in eq.effects:
                    eff.on_hit(self, target)

    def take_damage(self, dmg: int, dmg_type: DamageType):
        """受到伤害"""
        self.hp -= dmg
        if self.hp < 0:
            self.hp = 0

    def heal(self, amount: int):
        """治疗"""
        self.hp = min(self.max_hp, self.hp + amount)

    def restore_mp(self, amount: int):
        """恢复法力值"""
        self.mp = min(self.max_mp, self.mp + amount)

    def add_status_effect(self, effect):
        """添加状态效果"""
        return self.status_manager.add_status(effect)

    def remove_status_effect(self, effect_name: str):
        """移除状态效果"""
        return self.status_manager.remove_status(effect_name)

    def update_status_effects(self):
        """更新状态效果（每回合调用）"""
        # 重置行动能力（状态效果会重新设置这些）
        self.can_act = True
        self.can_cast = True
        
        # 更新所有状态效果
        results = self.status_manager.update_all()
        
        # 重新计算属性（状态效果可能影响属性）
        self.recalc_stats()
        
        # 更新技能冷却
        for skill in self.skills:
            skill.reduce_cooldown()
        
        return results

    def get_status_effects(self):
        """获取状态效果摘要"""
        return self.status_manager.get_status_summary()

    def has_status_effect(self, effect_name: str):
        """检查是否拥有指定状态效果"""
        return effect_name in self.status_manager

    def clear_all_status_effects(self):
        """清除所有状态效果"""
        return self.status_manager.clear_all_status()

    def get_status_effect_by_name(self, effect_name: str):
        """通过名称获取状态效果"""
        return self.status_manager.get_status_by_name(effect_name)

    def get_status_effects_by_type(self, status_type):
        """获取指定类型的所有状态效果"""
        return self.status_manager.get_status_by_type(status_type)

    def apply_status_effect(self, effect_name: str, **kwargs):
        """便捷方法：应用状态效果"""
        from status_effects import (
            BurnEffect, PoisonEffect, FreezeEffect, 
            DefenseBuffEffect, AttackBuffEffect, HealOverTimeEffect,
            StunEffect
        )
        
        effect_map = {
            "灼烧": BurnEffect,
            "burn": BurnEffect,
            "中毒": PoisonEffect,
            "poison": PoisonEffect,
            "冰冻": FreezeEffect,
            "freeze": FreezeEffect,
            "防御强化": DefenseBuffEffect,
            "defense_buff": DefenseBuffEffect,
            "攻击强化": AttackBuffEffect,
            "attack_buff": AttackBuffEffect,
            "持续治疗": HealOverTimeEffect,
            "heal_over_time": HealOverTimeEffect,
            "眩晕": StunEffect,
            "stun": StunEffect
        }
        
        if effect_name in effect_map:
            effect_class = effect_map[effect_name]
            effect = effect_class(**kwargs)
            return self.add_status_effect(effect)
        
        return {"success": False, "message": f"未知的状态效果: {effect_name}"}

    def learn_skill(self, skill: Skill) -> bool:
        """学习技能"""
        if self.level >= skill.level_requirement:
            self.skills.append(skill)
            return True
        return False

    def use_skill(self, skill_name: str, target=None) -> Dict[str, Any]:
        """使用技能"""
        if not self.can_act:
            return {"success": False, "message": f"{self.name} 无法行动"}
            
        if not self.can_cast and skill_name != "普通攻击":
            return {"success": False, "message": f"{self.name} 无法施法"}
        
        skill = next((s for s in self.skills if s.name == skill_name), None)
        if not skill:
            return {"success": False, "message": "技能不存在"}
        
        if not skill.can_use(self):
            return {"success": False, "message": "无法使用技能"}
        
        self.mp -= skill.mp_cost
        skill.current_cooldown = skill.cooldown
        
        return skill.execute(self, target)

    def _calculate_exp_required(self, level: int) -> int:
        """计算升级所需经验"""
        return level * 100 + (level - 1) * 50

    def gain_experience(self, exp: int):
        """获得经验值"""
        self.experience += exp
        while self.experience >= self.experience_to_next_level:
            self.level_up()

    def level_up(self):
        """升级"""
        self.experience -= self.experience_to_next_level
        self.level += 1
        self.experience_to_next_level = self._calculate_exp_required(self.level)
        
        self.base_hp += 15
        self.base_attack += 2
        self.base_defense += 1
        self.base_mp += 10
        self.base_spell_power += 1
        
        old_max_hp = self.max_hp
        old_max_mp = self.max_mp
        self.recalc_stats()
        
        hp_ratio = self.hp / old_max_hp if old_max_hp > 0 else 1
        mp_ratio = self.mp / old_max_mp if old_max_mp > 0 else 1
        self.hp = int(self.max_hp * hp_ratio)
        self.mp = int(self.max_mp * mp_ratio)

    def get_status(self) -> Dict[str, Any]:
        """获取角色状态"""
        status_effects = [effect.get_description() for effect in self.status_manager]
        
        return {
            "name": self.name,
            "level": self.level,
            "hp": f"{self.hp}/{self.max_hp}",
            "mp": f"{self.mp}/{self.max_mp}",
            "attack": self.attack,
            "defense": self.defense,
            "spell_power": self.spell_power,
            "experience": f"{self.experience}/{self.experience_to_next_level}",
            "status_effects": status_effects,
            "can_act": self.can_act,
            "can_cast": self.can_cast
        }

    def save_character(self) -> Dict[str, Any]:
        """保存角色数据"""
        return {
            "name": self.name,
            "level": self.level,
            "experience": self.experience,
            "hp": self.hp,
            "mp": self.mp,
            "inventory": self.inventory.list_items(),
            "weapon": self.weapon.to_dict() if self.weapon else None,
            "armor": {slot.value: armor.to_dict() if armor else None 
                     for slot, armor in self.armor.items()},
            "status_effects": self.get_status_effects()["status_effects"]
        }

    def is_alive(self) -> bool:
        """检查角色是否存活"""
        return self.hp > 0
    
    def is_dead(self) -> bool:
        """检查角色是否死亡"""
        return self.hp <= 0
