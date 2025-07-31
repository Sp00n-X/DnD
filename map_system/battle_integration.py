"""地图系统与战斗系统的集成模块"""

import sys
import os
import random
from typing import Dict, List, Optional, Any

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from battle_system import BattleEngine, BattleConfig
from characters.base_character import BaseCharacter
from enemy.lothir import swamp_creatures, root_creatures, canopy_creatures, undergrowth_creatures, bridge_creatures
from enemy.bosses.boss_manager import BossManager

class BattleEncounterManager:
    """战斗遭遇管理器"""
    
    def __init__(self):
        self.boss_manager = BossManager()
        self.enemy_pools = {
            "翡翠之森": {
                "swamp": swamp_creatures,
                "root": root_creatures,
                "canopy": canopy_creatures,
                "undergrowth": undergrowth_creatures,
                "bridge": bridge_creatures
            }
        }
        
    def generate_random_enemy(self, region: str, level_range: tuple) -> Optional[BaseCharacter]:
        """根据区域和等级范围生成随机敌人"""
        if region not in self.enemy_pools:
            return None
            
        region_enemies = self.enemy_pools[region]
        
        # 根据等级范围选择合适的敌人
        possible_enemies = []
        for area, module in region_enemies.items():
            if hasattr(module, 'ENEMIES'):
                for enemy_class in module.ENEMIES:
                    enemy = enemy_class()
                    if level_range[0] <= enemy.level <= level_range[1]:
                        possible_enemies.append(enemy)
        
        if possible_enemies:
            return random.choice(possible_enemies)
        return None
    
    def generate_boss_enemy(self, floor: int) -> Optional[Any]:
        """生成Boss敌人"""
        return self.boss_manager.get_boss(floor)
    
    def calculate_encounter_chance(self, region: str, sub_region: str = None) -> float:
        """计算遭遇敌人的概率"""
        base_chance = 0.8  # 基础80%遭遇率（演示用）
        
        # 根据区域调整
        region_modifiers = {
            "裂星集": 0.3,      # 安全区域
            "齿轮之城": 0.5,    # 城市区域
            "秘法之乡": 0.6,   # 魔法区域
            "翡翠之森": 0.9,    # 森林区域
            "天穹武朝": 0.8    # 武道区域
        }
        
        modifier = region_modifiers.get(region, 0.7)
        
        # 子区域可能有额外调整
        if sub_region:
            # 某些子区域可能有更高的遭遇率
            dangerous_areas = ["沼泽深处", "根须迷宫", "树冠顶层"]
            if any(area in sub_region for area in dangerous_areas):
                modifier += 0.1
        
        return min(base_chance * modifier, 1.0)  # 最高100%

class MapBattleSystem:
    """地图战斗系统集成"""
    
    def __init__(self, player):
        self.player = player
        self.encounter_manager = BattleEncounterManager()
        
    def check_random_encounter(self, region: str, sub_region: str = None) -> Optional[str]:
        """检查是否触发随机遭遇"""
        chance = self.encounter_manager.calculate_encounter_chance(region, sub_region)
        
        if random.random() < chance:
            return self.trigger_encounter(region, sub_region)
        return None
    
    def trigger_encounter(self, region: str, sub_region: str = None) -> str:
        """触发战斗遭遇"""
        # 根据区域确定等级范围
        level_ranges = {
            "裂星集": (1, 5),
            "齿轮之城": (5, 15),
            "秘法之乡": (1, 20),
            "翡翠之森": (5, 20),
            "天穹武朝": (5, 20)
        }
        
        level_range = level_ranges.get(region, (1, 10))
        
        # 生成敌人
        enemy = self.encounter_manager.generate_random_enemy(region, level_range)
        
        if enemy:
            print(f"\n⚠️ 遭遇敌人：{enemy.name} (等级 {enemy.level})")
            
            # 创建战斗配置
            config = BattleConfig(
                allow_flee=True,
                show_detailed_log=True,
                turn_limit=50
            )
            
            # 开始战斗
            battle = BattleEngine(self.player, enemy, config)
            result = battle.start_battle()
            
            # 处理战斗结果
            return self._process_battle_result(result, enemy)
        
        return "no_encounter"
    
    def trigger_boss_battle(self, floor: int) -> str:
        """触发Boss战斗"""
        boss = self.encounter_manager.generate_boss_enemy(floor)
        
        if boss:
            print(f"\n⚠️ 遭遇Boss：{boss.name} (等级 {boss.level})")
            
            # Boss战斗不允许逃跑
            config = BattleConfig(
                allow_flee=False,
                show_detailed_log=True,
                turn_limit=100
            )
            
            battle = BattleEngine(self.player, boss, config)
            result = battle.start_battle()
            
            return self._process_battle_result(result, boss, is_boss=True)
        
        return "no_boss"
    
    def _process_battle_result(self, result: str, enemy, is_boss: bool = False) -> str:
        """处理战斗结果"""
        if result == "victory":
            # 计算奖励
            exp_reward = enemy.level * 50
            gold_reward = enemy.level * 10
            
            # 给予经验值
            self.player.gain_experience(exp_reward)
            
            print(f"\n✨ 获得 {exp_reward} 经验值和 {gold_reward} 金币！")
            
            # 如果是Boss，标记为已击败
            if is_boss and hasattr(self.player, 'defeated_bosses'):
                self.player.defeated_bosses.add(getattr(self.player, 'current_floor', 1))
            
            return "victory"
            
        elif result == "defeat":
            print("\n💀 你被击败了！")
            # 可以添加复活机制
            self.player.hp = max(1, self.player.max_hp // 2)
            return "defeat"
            
        elif result == "flee":
            print("\n🏃 你成功逃脱了！")
            return "flee"
            
        return result

# 集成示例
class EnhancedMapWithBattles:
    """增强地图系统，集成战斗功能"""
    
    def __init__(self, player):
        self.player = player
        self.battle_system = MapBattleSystem(player)
        
    def explore_area(self, region: str, sub_region: str = None):
        """探索区域，可能触发战斗"""
        print(f"\n🗺️ 正在探索 {region}" + (f" - {sub_region}" if sub_region else ""))
        
        # 检查随机遭遇
        result = self.battle_system.check_random_encounter(region, sub_region)
        
        if result:
            print(f"战斗结果：{result}")
        
        return result
    
    def challenge_boss(self, floor: int):
        """挑战Boss"""
        return self.battle_system.trigger_boss_battle(floor)

# 使用示例
if __name__ == "__main__":
    # 创建测试玩家
    from main_process import PlayerCharacter, CharacterClass
    
    player = PlayerCharacter("测试冒险者", CharacterClass.MAGE)
    player.level = 5
    
    # 创建集成系统
    map_battle = EnhancedMapWithBattles(player)
    
    # 测试探索
    print("🎮 测试地图战斗集成")
    print("=" * 50)
    
    # 测试随机遭遇
    result = map_battle.explore_area("翡翠之森", "沼泽区域")
    print(f"探索结果：{result}")
    
    # 测试Boss战斗
    result = map_battle.challenge_boss(1)
    print(f"Boss战结果：{result}")
