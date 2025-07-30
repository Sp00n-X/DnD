from enemy.base_enemy import BaseEnemy, EnemyType
from characters.skills.base_skill import Skill
from typing import List

class CelestWeaver(BaseEnemy):
    """星辉织蛛 - 冠幕层生物"""
    
    def __init__(self, level: int = 1):
        super().__init__("星辉织蛛", level, EnemyType.NORMAL)
        
        # 基础属性
        self.base_hp = 25 + level * 5
        self.base_attack = 8 + level * 2
        self.base_defense = 5 + level
        self.base_mp = 20 + level * 3
        
        # 重新计算属性
        self.recalc_stats()
        self.hp = self.max_hp
        self.mp = self.max_mp
        
        # 生态信息
        self.habitat = "冠幕层（30-60米高空）"
        self.description = "蛛丝折射星辉，织成'夜空补丁'的魔法蜘蛛，夜间修复树冠破损"
        self.behavior = "夜间活动，会编织星辉之网困住敌人"
        
        # 添加技能
        from enemy.lothir.lothir_skills import WebShot, StarlightBurst
        self.add_skill(WebShot())
        self.add_skill(StarlightBurst())
        
        # 计算奖励
        self.calculate_rewards()
        
        # 特殊掉落
        self.drop_items = [
            ("spider_silk", 0.7),      # 蛛丝
            ("starlight_shard", 0.3),  # 星辉碎片
            ("celestial_web", 0.1)     # 天界之网
        ]

class GlaiveKestrel(BaseEnemy):
    """光刃隼 - 冠幕层精英生物"""
    
    def __init__(self, level: int = 3):
        super().__init__("光刃隼", level, EnemyType.ELITE)
        
        # 基础属性
        self.base_hp = 35 + level * 6
        self.base_attack = 12 + level * 3
        self.base_defense = 7 + level * 2
        self.base_mp = 15 + level * 2
        
        # 重新计算属性
        self.recalc_stats()
        self.hp = self.max_hp
        self.mp = self.max_mp
        
        # 生态信息
        self.habitat = "冠幕层顶端"
        self.description = "翅骨边缘以太化，高速俯冲切出风刃的游隼，精灵用作'活体飞刀'"
        self.behavior = "高速俯冲攻击，善于利用风刃进行范围伤害"
        
        # 添加技能
        from enemy.lothir.lothir_skills import WindBlade, DiveAttack
        self.add_skill(WindBlade())
        self.add_skill(DiveAttack())
        
        # 计算奖励
        self.calculate_rewards()
        
        # 特殊掉落
        self.drop_items = [
            ("glaive_feather", 0.8),   # 光刃羽毛
            ("wind_crystal", 0.4),     # 风之水晶
            ("kestrel_talon", 0.2)     # 隼之爪
        ]

class WindWhistlerVine(BaseEnemy):
    """风哨藤群 - 冠幕层特殊植物生物"""
    
    def __init__(self, level: int = 2):
        super().__init__("风哨藤群", level, EnemyType.NORMAL)
        
        # 基础属性 - 植物特性，高防御低攻击
        self.base_hp = 40 + level * 8
        self.base_attack = 5 + level
        self.base_defense = 12 + level * 3
        self.base_mp = 30 + level * 4
        
        # 重新计算属性
        self.recalc_stats()
        self.hp = self.max_hp
        self.mp = self.max_mp
        
        # 生态信息
        self.habitat = "冠幕层枝桥"
        self.description = "藤蔓中空，气流穿过即奏乐的木质藤本，精灵哨兵靠音调变化判断入侵方向"
        self.behavior = "通过音波攻击和缠绕敌人，具有植物再生能力"
        
        # 添加技能
        from enemy.lothir.lothir_skills import VineWhip, Regeneration
        self.add_skill(VineWhip())
        self.add_skill(Regeneration())
        
        # 计算奖励
        self.calculate_rewards()
        
        # 特殊掉落
        self.drop_items = [
            ("whistler_vine", 0.6),    # 风哨藤
            ("music_resin", 0.3),      # 音乐树脂
            ("plant_essence", 0.2)     # 植物精华
        ]
        
        # 植物特性：再生
        self.has_regeneration = True
        self.regen_amount = 2 + level
