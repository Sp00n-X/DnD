from typing import Dict, Optional, List, Tuple
from .floor_boss import FloorBoss
from .attack_patterns import RandomSkillPattern, PrioritySkillPattern, EnragedPattern
from .boss_skills import GOBLIN_CHEF_SKILLS

class BossManager:
    """Boss管理器 - 负责创建和管理所有层主"""
    
    def __init__(self):
        self.bosses: Dict[int, FloorBoss] = {}
        self._create_bosses()
    
    def _create_bosses(self) -> None:
        """创建各层层主"""
        boss_data: List[Tuple[int, str, int, int, int, int]] = [
            (1, "🧑‍🍳哥布林厨师长", 2, 80, 15, 3),
            (2, "💀⚔️骷髅骑士", 4, 150, 25, 8),
            (3, "🧙‍♂️暗影法师", 6, 120, 35, 5),
            (4, "🗿岩石巨人", 8, 300, 40, 15),
            (5, "🐉古龙领主", 10, 500, 60, 20)
        ]
        
        for floor, name, level, hp, attack, defense in boss_data:
            boss = FloorBoss(floor, name, level, hp, attack, defense)
            
            # 为特定Boss添加技能和攻击模式
            if floor == 1:
                # 哥布林厨师长 - 随机技能模式
                boss.add_skills(GOBLIN_CHEF_SKILLS)
                boss.set_attack_pattern(RandomSkillPattern())
            
            self.bosses[floor] = boss
    
    def get_boss(self, floor: int) -> Optional[FloorBoss]:
        """获取指定层的层主"""
        return self.bosses.get(floor)
    
    def get_all_bosses(self) -> Dict[int, FloorBoss]:
        """获取所有层主"""
        return self.bosses.copy()
    
    def get_total_floors(self) -> int:
        """获取总层数"""
        return len(self.bosses)
    
    def reset_boss(self, floor: int) -> bool:
        """重置指定层的Boss"""
        boss = self.get_boss(floor)
        if boss:
            boss.reset()
            return True
        return False
    
    def reset_all_bosses(self) -> None:
        """重置所有Boss"""
        for boss in self.bosses.values():
            boss.reset()
    
    def get_boss_info(self, floor: int) -> Optional[Dict]:
        """获取Boss详细信息"""
        boss = self.get_boss(floor)
        if boss:
            info = {
                'floor': boss.floor,
                'name': boss.name,
                'level': boss.level,
                'hp': boss.hp,
                'max_hp': boss.max_hp,
                'attack': boss.attack,
                'defense': boss.defense,
                'is_defeated': boss.is_defeated,
                'skills_count': len(boss.skills),
                'attack_pattern': boss.attack_pattern.name
            }
            
            # 添加技能信息
            if boss.skills:
                info['skills'] = boss.get_skills_info()
            
            return info
        return None
    
    def get_undefeated_bosses(self, defeated_floors: set) -> Dict[int, FloorBoss]:
        """获取未击败的Boss"""
        return {
            floor: boss for floor, boss in self.bosses.items()
            if floor not in defeated_floors
        }
