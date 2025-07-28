from characters.base_character import BaseCharacter
from characters.equipments.base_equipments import DamageType
from typing import Any, Dict, Optional, List
from .attack_patterns import AttackPattern, RandomSkillPattern
from characters.skills.base_skill import Skill

class FloorBoss(BaseCharacter):
    """层主类 - 继承自BaseCharacter以获得状态效果支持"""
    
    def __init__(self, floor: int, name: str, level: int, hp: int, attack: int, defense: int):
        super().__init__(name, level)
        self.floor = floor
        
        # 覆盖基础属性
        self.base_hp = hp
        self.base_attack = attack
        self.base_defense = defense
        
        # 重新计算属性
        self.recalc_stats()
        self.hp = self.max_hp
        self.mp = 50  # 给Boss一些MP
        
        # 技能系统
        self.skills: List[Skill] = []
        self.attack_pattern: AttackPattern = RandomSkillPattern()
        
        # 标记是否被击败
        self.is_defeated = False
    
    def take_damage(self, damage: int, dmg_type: Optional[DamageType] = None):
        """受到伤害"""
        super().take_damage(damage, dmg_type)
        if self.hp == 0:
            self.is_defeated = True
    
    def is_alive(self) -> bool:
        """检查是否存活"""
        return self.hp > 0
    
    def add_skill(self, skill: Skill):
        """添加技能"""
        self.skills.append(skill)
    
    def add_skills(self, skills: List[Skill]):
        """批量添加技能"""
        self.skills.extend(skills)
    
    def set_attack_pattern(self, pattern: AttackPattern):
        """设置攻击模式"""
        self.attack_pattern = pattern
    
    def select_action(self, target) -> Dict[str, Any]:
        """选择要执行的动作"""
        # 减少所有技能的冷却时间
        for skill in self.skills:
            skill.reduce_cooldown()
        
        return self.attack_pattern.select_action(self, target, self.skills)
    
    def execute_action(self, action: Dict[str, Any]) -> Dict[str, Any]:
        """执行选择的动作"""
        if action['type'] == 'skill':
            skill = action['skill']
            target = action['target']
            return skill.execute(self, target)
        elif action['type'] == 'attack':
            target = action['target']
            damage = self.attack
            target.take_damage(damage, DamageType.PHYSICAL)
            return {
                'success': True,
                'damage': damage,
                'type': 'normal_attack',
                'message': f"{self.name}进行了普通攻击，造成{damage}点伤害！"
            }
    
    def get_status(self) -> str:
        """获取状态信息"""
        skills_info = f" 技能: {len(self.skills)}个" if self.skills else " 无技能"
        return f"{self.name} - 等级{self.level} - 生命值: {self.hp}/{self.max_hp}{skills_info}"
    
    def get_skills_info(self) -> List[Dict[str, Any]]:
        """获取技能信息"""
        return [{
            'name': skill.name,
            'description': skill.description,
            'mp_cost': skill.mp_cost,
            'cooldown': skill.cooldown,
            'current_cooldown': skill.current_cooldown,
            'can_use': skill.can_use(self)
        } for skill in self.skills]
    
    def reset(self):
        """重置Boss状态（用于重新挑战）"""
        self.hp = self.max_hp
        self.mp = 50
        self.is_defeated = False
        
        # 重置技能冷却
        for skill in self.skills:
            skill.current_cooldown = 0
        
        # 清除所有状态效果
        self.clear_all_status_effects()
