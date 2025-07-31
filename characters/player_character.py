"""
玩家角色类 - 替代main_process.py中的PlayerCharacter
"""

from characters.base_character import BaseCharacter, CharacterClass
from characters.skills.mage_skills import Fireball, FrostBolt, DefenseBoost, ManaHeal
from characters.equipments.mage.mage_weapons import FirelordStaff
from characters.equipments.mage.mage_armors import ArcaneRobes

class PlayerCharacter(BaseCharacter):
    """玩家角色类"""
    
    def __init__(self, name: str, character_class: CharacterClass):
        super().__init__(name, level=1)
        self.character_class = character_class
        self.current_floor = 1
        self.defeated_bosses = set()  # 已击败的层主
        
        # 根据职业设置初始属性
        self._set_class_attributes()
    
    def _set_class_attributes(self):
        """基于职业设置属性"""
        if self.character_class == CharacterClass.WARRIOR:
            self.base_hp += 20
            self.base_attack += 5
            self.base_defense += 3
        elif self.character_class == CharacterClass.MAGE:
            self.base_mp += 30
            self.base_spell_power += 5
            self.base_attack -= 2
            
            self.skills.extend([
                Fireball(),
                FrostBolt(),
                DefenseBoost(),
                ManaHeal()
            ])
            
            # 为法师初始化装备：火焰之王法杖和奥术长袍
            firelord_staff = FirelordStaff()
            arcane_robes = ArcaneRobes()
            
            # 装备武器和防具
            self.equip(firelord_staff)
            self.equip(arcane_robes)
            
        elif self.character_class == CharacterClass.ROGUE:
            self.base_attack += 3
            self.base_defense += 1
            self.base_hp += 10
        elif self.character_class == CharacterClass.CLERIC:
            self.base_hp += 15
            self.base_mp += 20
            self.base_spell_power += 3
            self.base_defense += 2
            
        # 重新计算属性
        self.recalc_stats()
        self.hp = self.max_hp
        self.mp = self.max_mp
