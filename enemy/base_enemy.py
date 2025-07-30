from characters.base_character import BaseCharacter
from characters.equipments.base_equipments import DamageType
from typing import Any, Dict, Optional, List
from characters.skills.base_skill import Skill
from enum import Enum

class EnemyType(Enum):
    """敌人类型枚举"""
    NORMAL = "普通"
    ELITE = "精英"
    BOSS = "首领"
    LEGENDARY = "传说"

class EnemyTier(Enum):
    """敌人层级枚举"""
    LOW = "低级"
    MID = "中级" 
    HIGH = "高级"
    LEGENDARY = "传说级"

class BaseEnemy(BaseCharacter):
    """基础敌人类 - 继承自BaseCharacter以获得状态效果支持"""
    
    def __init__(self, name: str, level: int, enemy_type: EnemyType = EnemyType.NORMAL):
        super().__init__(name, level)
        self.enemy_type = enemy_type
        self.tier = self._determine_tier()
        
        # 基础属性将在子类中设置
        self.base_hp = 0
        self.base_attack = 0
        self.base_defense = 0
        self.base_mp = 0
        
        # 掉落相关
        self.experience_reward = 0
        self.gold_reward = 0
        self.drop_items = []  # [(item_id, drop_rate), ...]
        
        # 技能系统
        self.skills: List[Skill] = []
        
        # 生态信息
        self.habitat = ""  # 栖息地
        self.description = ""  # 描述
        self.behavior = ""  # 行为模式
        
        # 战斗AI
        self.ai_pattern = "normal"  # normal, aggressive, defensive, caster
        
    def _determine_tier(self) -> EnemyTier:
        """根据等级确定层级"""
        if self.level <= 5:
            return EnemyTier.LOW
        elif self.level <= 15:
            return EnemyTier.MID
        elif self.level <= 25:
            return EnemyTier.HIGH
        else:
            return EnemyTier.LEGENDARY
    
    def take_damage(self, damage: int, dmg_type: Optional[DamageType] = None):
        """受到伤害"""
        super().take_damage(damage, dmg_type)
    
    def is_alive(self) -> bool:
        """检查是否存活"""
        return self.hp > 0
    
    def add_skill(self, skill: Skill):
        """添加技能"""
        self.skills.append(skill)
    
    def add_skills(self, skills: List[Skill]):
        """批量添加技能"""
        self.skills.extend(skills)
    
    def select_action(self, target) -> Dict[str, Any]:
        """选择要执行的动作 - 基础AI"""
        if not self.skills:
            return {
                'type': 'attack',
                'target': target,
                'damage': self.attack
            }
        
        # 简单AI：如果有可用技能，50%概率使用技能
        usable_skills = [s for s in self.skills if s.can_use(self)]
        if usable_skills and len(usable_skills) > 0:
            import random
            if random.random() < 0.5:
                skill = random.choice(usable_skills)
                return {
                    'type': 'skill',
                    'skill': skill,
                    'target': target
                }
        
        # 普通攻击
        return {
            'type': 'attack',
            'target': target,
            'damage': self.attack
        }
    
    def execute_action(self, action: Dict[str, Any]) -> Dict[str, Any]:
        """执行选择的动作"""
        if action['type'] == 'skill':
            skill = action['skill']
            target = action['target']
            return skill.execute(self, target)
        elif action['type'] == 'attack':
            target = action['target']
            damage = action['damage']
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
        tier_info = f" [{self.tier.value}]"
        type_info = f" [{self.enemy_type.value}]"
        return f"{self.name}{type_info}{tier_info} - 等级{self.level} - 生命值: {self.hp}/{self.max_hp}{skills_info}"
    
    def get_detailed_info(self) -> Dict[str, Any]:
        """获取详细信息"""
        return {
            'name': self.name,
            'level': self.level,
            'type': self.enemy_type.value,
            'tier': self.tier.value,
            'hp': f"{self.hp}/{self.max_hp}",
            'attack': self.attack,
            'defense': self.defense,
            'habitat': self.habitat,
            'description': self.description,
            'behavior': self.behavior,
            'skills': [skill.name for skill in self.skills],
            'rewards': {
                'experience': self.experience_reward,
                'gold': self.gold_reward,
                'items': self.drop_items
            }
        }
    
    def calculate_rewards(self):
        """计算奖励"""
        base_exp = self.level * 10
        base_gold = self.level * 5
        
        # 根据类型调整
        if self.enemy_type == EnemyType.ELITE:
            base_exp *= 2
            base_gold *= 1.5
        elif self.enemy_type == EnemyType.BOSS:
            base_exp *= 5
            base_gold *= 3
        elif self.enemy_type == EnemyType.LEGENDARY:
            base_exp *= 10
            base_gold *= 5
            
        self.experience_reward = int(base_exp)
        self.gold_reward = int(base_gold)
