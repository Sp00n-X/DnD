from enemy.base_enemy import BaseEnemy, EnemyType
from characters.skills.base_skill import Skill
from typing import List

class MirrorHeron(BaseEnemy):
    """镜沼鹭 - 幽沼带生物"""
    
    def __init__(self, level: int = 4):
        super().__init__("镜沼鹭", level, EnemyType.ELITE)
        
        # 基础属性
        self.base_hp = 42 + level * 7
        self.base_attack = 11 + level * 3
        self.base_defense = 9 + level * 2
        self.base_mp = 40 + level * 5
        
        # 重新计算属性
        self.recalc_stats()
        self.hp = self.max_hp
        self.mp = self.max_mp
        
        # 生态信息
        self.habitat = "幽沼带浅水区"
        self.description = "长喙可探入水面，啄起'水镜片'投向空中，制造短时幻象迷惑入侵者"
        self.behavior = "制造幻象分身，用喙进行精准攻击"
        
        # 添加技能
        from enemy.lothir.lothir_skills import WaterMirror, VenomStrike
        self.add_skill(WaterMirror())
        self.add_skill(VenomStrike())
        
        # 计算奖励
        self.calculate_rewards()
        
        # 特殊掉落
        self.drop_items = [
            ("heron_feather", 0.7),    # 鹭羽
            ("water_lens", 0.5),       # 水透镜
            ("mirror_fragment", 0.3),  # 镜片碎片
            ("illusion_crystal", 0.1)  # 幻象水晶
        ]

class StarAlgaeLotus(BaseEnemy):
    """星藻浮莲 - 幽沼带植物生物"""
    
    def __init__(self, level: int = 3):
        super().__init__("星藻浮莲", level, EnemyType.NORMAL)
        
        # 基础属性 - 高魔法型
        self.base_hp = 38 + level * 6
        self.base_attack = 6 + level
        self.base_defense = 10 + level * 2
        self.base_mp = 55 + level * 7
        
        # 重新计算属性
        self.recalc_stats()
        self.hp = self.max_hp
        self.mp = self.max_mp
        
        # 生态信息
        self.habitat = "幽沼带水面"
        self.description = "叶片背面寄生星辉藻，夜晚整片沼泽发光，精灵夜间航标，地精最痛恨的'光污染'"
        self.behavior = "释放星辉光芒，用魔法攻击入侵者"
        
        # 添加技能
        from enemy.lothir.lothir_skills import StarlightBurst, Regeneration
        self.add_skill(StarlightBurst())
        self.add_skill(Regeneration())
        
        # 计算奖励
        self.calculate_rewards()
        
        # 特殊掉落
        self.drop_items = [
            ("star_algae", 0.8),       # 星藻
            ("lotus_petal", 0.6),      # 莲瓣
            ("luminescent_pollen", 0.4), # 发光花粉
            ("starlight_nectar", 0.2)  # 星辉花蜜
        ]
        
        # 特殊能力：发光
        self.has_glow = True
        self.glow_intensity = 5 + level

class StillwaterViper(BaseEnemy):
    """静水蛇 - 幽沼带隐匿杀手"""
    
    def __init__(self, level: int = 5):
        super().__init__("静水蛇", level, EnemyType.ELITE)
        
        # 基础属性 - 高敏捷高毒伤
        self.base_hp = 35 + level * 5
        self.base_attack = 13 + level * 4
        self.base_defense = 7 + level
        self.base_mp = 25 + level * 3
        
        # 重新计算属性
        self.recalc_stats()
        self.hp = self.max_hp
        self.mp = self.max_mp
        
        # 生态信息
        self.habitat = "幽沼带静水区"
        self.description = "身体完全透明，仅心脏处一点星辉，精灵药剂师提取'隐形血清'"
        self.behavior = "隐形伏击，剧毒攻击，善于水下作战"
        
        # 添加技能
        from enemy.lothir.lothir_skills import VenomStrike
        self.add_skill(VenomStrike())
        
        # 计算奖励
        self.calculate_rewards()
        
        # 特殊掉落
        self.drop_items = [
            ("transparent_scale", 0.6), # 透明鳞片
            ("venom_sac", 0.7),        # 毒囊
            ("invisibility_serum", 0.2), # 隐形血清
            ("star_heart", 0.1)        # 星辉心脏
        ]
        
        # 特殊能力：隐形
        self.has_invisibility = True
        self.invisibility_duration = 2
