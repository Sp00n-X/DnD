"""
角色保存和加载系统
提供角色数据的序列化和反序列化功能
"""

import json
import os
from typing import Dict, Any, Optional, List
from datetime import datetime
from characters.base_character import BaseCharacter, CharacterClass, Item, Inventory
from characters.equipments.base_equipments import Weapon, Armor, EquipSlot
from characters.skills.base_skill import Skill
import importlib

class SaveSystem:
    """角色保存和加载系统"""
    
    SAVE_DIR = "saves"
    
    def __init__(self):
        """初始化保存系统"""
        self.ensure_save_dir()
    
    def ensure_save_dir(self):
        """确保保存目录存在"""
        if not os.path.exists(self.SAVE_DIR):
            os.makedirs(self.SAVE_DIR)
    
    def save_character(self, character: BaseCharacter) -> bool:
        """保存角色数据"""
        try:
            save_data = self._serialize_character(character)
            filename = f"{character.name}.json"
            filepath = os.path.join(self.SAVE_DIR, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, ensure_ascii=False, indent=2)
            
            return True
        except Exception as e:
            print(f"保存角色失败: {e}")
            return False
    
    def load_character(self, character_name: str) -> Optional[BaseCharacter]:
        """加载角色数据"""
        try:
            filename = f"{character_name}.json"
            filepath = os.path.join(self.SAVE_DIR, filename)
            
            if not os.path.exists(filepath):
                return None
            
            with open(filepath, 'r', encoding='utf-8') as f:
                save_data = json.load(f)
            
            return self._deserialize_character(save_data)
        except Exception as e:
            print(f"加载角色失败: {e}")
            return None
    
    def list_saved_characters(self) -> List[Dict[str, Any]]:
        """列出所有已保存的角色"""
        saved_characters = []
        
        if not os.path.exists(self.SAVE_DIR):
            return saved_characters
        
        for filename in os.listdir(self.SAVE_DIR):
            if filename.endswith('.json'):
                filepath = os.path.join(self.SAVE_DIR, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    saved_characters.append({
                        'name': data.get('name', '未知'),
                        'level': data.get('level', 1),
                        'character_class': data.get('character_class', '未知'),
                        'current_floor': data.get('current_floor', 1),
                        'defeated_bosses': len(data.get('defeated_bosses', [])),
                        'total_bosses': data.get('total_bosses', 10),
                        'last_saved': data.get('last_saved', '未知'),
                        'play_time': data.get('play_time', 0)
                    })
                except Exception:
                    continue
        
        return saved_characters
    
    def delete_character(self, character_name: str) -> bool:
        """删除角色存档"""
        try:
            filename = f"{character_name}.json"
            filepath = os.path.join(self.SAVE_DIR, filename)
            
            if os.path.exists(filepath):
                os.remove(filepath)
                return True
            return False
        except Exception as e:
            print(f"删除角色失败: {e}")
            return False
    
    def _serialize_character(self, character: BaseCharacter) -> Dict[str, Any]:
        """序列化角色数据 - 简化版本"""
        from characters.player_character import PlayerCharacter
        
        save_data = {
            'name': character.name,
            'level': character.level,
            'experience': character.experience,
            'hp': character.hp,
            'mp': character.mp,
            'base_hp': character.base_hp,
            'base_attack': character.base_attack,
            'base_defense': character.base_defense,
            'base_mp': character.base_mp,
            'base_spell_power': character.base_spell_power,
            'last_saved': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'play_time': getattr(character, 'play_time', 0)
        }
        
        # 如果是PlayerCharacter，保存额外信息
        if isinstance(character, PlayerCharacter):
            save_data.update({
                'character_class': character.character_class.value,
                'current_floor': character.current_floor,
                'defeated_bosses': list(character.defeated_bosses),
                'total_bosses': 10
            })
        
        return save_data
    
    def _deserialize_character(self, save_data: Dict[str, Any]) -> Optional[BaseCharacter]:
        """反序列化角色数据 - 简化版本"""
        from characters.player_character import PlayerCharacter
        
        try:
            # 创建角色
            char_class = CharacterClass(save_data['character_class'])
            character = PlayerCharacter(save_data['name'], char_class)
            
            # 恢复基础属性
            character.level = save_data['level']
            character.experience = save_data['experience']
            character.hp = save_data['hp']
            character.mp = save_data['mp']
            character.base_hp = save_data['base_hp']
            character.base_attack = save_data['base_attack']
            character.base_defense = save_data['base_defense']
            character.base_mp = save_data['base_mp']
            character.base_spell_power = save_data['base_spell_power']
            character.current_floor = save_data.get('current_floor', 1)
            character.defeated_bosses = set(save_data.get('defeated_bosses', []))
            
            # 重新计算属性
            character.recalc_stats()
            
            return character
            
        except Exception as e:
            print(f"反序列化角色失败: {e}")
            return None
    
    def get_save_path(self, character_name: str) -> str:
        """获取角色存档路径"""
        return os.path.join(self.SAVE_DIR, f"{character_name}.json")
    
    def character_exists(self, character_name: str) -> bool:
        """检查角色是否存在"""
        return os.path.exists(self.get_save_path(character_name))
