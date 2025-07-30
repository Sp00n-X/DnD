from enemy.base_enemy import BaseEnemy, EnemyType
from characters.skills.base_skill import Skill
from typing import List

class CelestialStag(BaseEnemy):
    """星穹牡鹿 - 传说级生物"""
    
    def __init__(self, level: int = 20):
        super().__init__("星穹牡鹿", level, EnemyType.LEGENDARY)
        
        # 基础属性 - 传说级
        self.base_hp = 200 + level * 25
        self.base_attack = 25 + level * 5
        self.base_defense = 20 + level * 4
        self.base_mp = 100 + level * 10
        
        # 重新计算属性
        self.recalc_stats()
        self.hp = self.max_hp
        self.mp = self.max_mp
        
        # 生态信息
        self.habitat = "洛希尔森林深处"
        self.description = "九苔议会表决出现4:4僵局时现身，角枝指向破局之人，'神性预兆'，禁止猎杀"
        self.behavior = "神圣不可侵犯，只在特殊时刻出现，拥有星穹之力"
        
        # 添加技能
        from enemy.lothir.lothir_skills import StarlightBurst, VenomStrike
        self.add_skill(StarlightBurst())
        self.add_skill(VenomStrike())
        
        # 计算奖励
        self.calculate_rewards()
        
        # 特殊掉落 - 传说级物品
        self.drop_items = [
            ("celestial_antler", 1.0), # 星穹鹿角
            ("divine_horn", 0.8),      # 神圣之角
            ("star_fragment", 0.5),    # 星之碎片
            ("cosmic_essence", 0.3),   # 宇宙精华
            ("prophecy_shard", 0.1)    # 预言碎片
        ]
        
        # 特殊能力：神圣光环
        self.has_divine_aura = True
        self.aura_radius = 5

class ForestUmbraPack(BaseEnemy):
    """林影狼群 - 传说级群体生物"""
    
    def __init__(self, level: int = 15):
        super().__init__("林影狼群", level, EnemyType.LEGENDARY)
        
        # 基础属性 - 群体特性
        self.base_hp = 120 + level * 15  # 代表整个狼群
        self.base_attack = 20 + level * 4
        self.base_defense = 15 + level * 3
        self.base_mp = 60 + level * 8
        
        # 重新计算属性
        self.recalc_stats()
        self.hp = self.max_hp
        self.mp = self.max_mp
        
        # 生态信息
        self.habitat = "灰林边缘"
        self.description = "长老过度预视导致情感枯竭，其影子化为实体狼，被放生至灰林"
        self.behavior = "群体作战，影子分身，情感攻击"
        
        # 添加技能
        from enemy.lothir.lothir_skills import ShadowStep, Pounce
        self.add_skill(ShadowStep())
        self.add_skill(Pounce())
        
        # 计算奖励
        self.calculate_rewards()
        
        # 特殊掉落
        self.drop_items = [
            ("shadow_fur", 0.9),       # 影之毛皮
            ("pack_leader_claw", 0.6), # 狼王爪
            ("emotional_crystal", 0.4), # 情感水晶
            ("umbra_heart", 0.2)       # 暗影之心
        ]
        
        # 特殊能力：群体作战
        self.is_pack_creature = True
        self.pack_bonus = 1.5

class CircadianGemini(BaseEnemy):
    """昼夜双生蝶 - 传说级时间生物"""
    
    def __init__(self, level: int = 25):
        super().__init__("昼夜双生蝶", level, EnemyType.LEGENDARY)
        
        # 基础属性 - 时间魔法
        self.base_hp = 80 + level * 10
        self.base_attack = 18 + level * 3
        self.base_defense = 16 + level * 3
        self.base_mp = 150 + level * 15
        
        # 重新计算属性
        self.recalc_stats()
        self.hp = self.max_hp
        self.mp = self.max_mp
        
        # 生态信息
        self.habitat = "时间裂缝"
        self.description = "左翼为昼纹，右翼为夜纹；仅在昼夜交替瞬间现身1秒，'时间裂缝的守门人'"
        self.behavior = "掌控时间流速，昼夜交替攻击"
        
        # 添加技能
        from enemy.lothir.lothir_skills import StarlightBurst, VenomStrike
        self.add_skill(StarlightBurst())
        self.add_skill(VenomStrike())
        
        # 计算奖励
        self.calculate_rewards()
        
        # 特殊掉落
        self.drop_items = [
            ("day_wing", 0.8),         # 昼之翼
            ("night_wing", 0.8),       # 夜之翼
            ("time_fragment", 0.5),    # 时间碎片
            ("chronosphere", 0.3),     # 时间球
            ("gemini_essence", 0.1)    # 双生精华
        ]
        
        # 特殊能力：时间操控
        self.has_time_control = True
        self.time_slow_factor = 0.5
