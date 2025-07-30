from enemy.base_enemy import BaseEnemy, EnemyType
from characters.skills.base_skill import Skill
from typing import List

class MoonRoe(BaseEnemy):
    """月轮狍 - 灌草层生物"""
    
    def __init__(self, level: int = 3):
        super().__init__("月轮狍", level, EnemyType.NORMAL)
        
        # 基础属性
        self.base_hp = 35 + level * 6
        self.base_attack = 9 + level * 2
        self.base_defense = 8 + level * 2
        self.base_mp = 15 + level * 2
        
        # 重新计算属性
        self.recalc_stats()
        self.hp = self.max_hp
        self.mp = self.max_mp
        
        # 生态信息
        self.habitat = "灌草层（0-10米）"
        self.description = "角枝每年脱落一次，断面呈月相纹，角片磨成粉作为'月相墨水'记录长老预言"
        self.behavior = "温顺但受惊时会用角攻击，角具有月相魔法"
        
        # 添加技能
        from enemy.lothir.lothir_skills import MoonAntlerStrike, LunarBlessing
        self.add_skill(MoonAntlerStrike())
        self.add_skill(LunarBlessing())
        
        # 计算奖励
        self.calculate_rewards()
        
        # 特殊掉落
        self.drop_items = [
            ("moon_antler", 0.6),      # 月轮角
            ("roe_meat", 0.8),         # 狍肉
            ("lunar_dust", 0.3)        # 月尘
        ]

class MossBackTapir(BaseEnemy):
    """苔背貘 - 灌草层清道夫"""
    
    def __init__(self, level: int = 4):
        super().__init__("苔背貘", level, EnemyType.NORMAL)
        
        # 基础属性 - 高血量高防御
        self.base_hp = 60 + level * 12
        self.base_attack = 6 + level
        self.base_defense = 15 + level * 3
        self.base_mp = 20 + level * 3
        
        # 重新计算属性
        self.recalc_stats()
        self.hp = self.max_hp
        self.mp = self.max_mp
        
        # 生态信息
        self.habitat = "灌草层地面"
        self.description = "背部共生苔藓，可光合供能，森林清道夫，粪便即高肥力'苔壤'"
        self.behavior = "缓慢移动，用长鼻攻击，苔藓具有治疗效果"
        
        # 添加技能
        from enemy.lothir.lothir_skills import ShellShield, RamAttack, Regeneration
        self.add_skill(ShellShield())
        self.add_skill(RamAttack())
        self.add_skill(Regeneration())
        
        # 计算奖励
        self.calculate_rewards()
        
        # 特殊掉落
        self.drop_items = [
            ("moss_patch", 0.7),       # 苔藓块
            ("tapir_hide", 0.5),       # 貘皮
            ("fertile_dung", 0.9),     # 肥沃粪便
            ("photosynthesis_crystal", 0.2)  # 光合水晶
        ]
        
        # 特殊能力：光合作用恢复
        self.has_photosynthesis = True
        self.photosynthesis_heal = 3 + level

class LoopRoot(BaseEnemy):
    """回环根须 - 灌草层植物生物"""
    
    def __init__(self, level: int = 2):
        super().__init__("回环根须", level, EnemyType.NORMAL)
        
        # 基础属性 - 植物特性
        self.base_hp = 50 + level * 8
        self.base_attack = 7 + level * 2
        self.base_defense = 12 + level * 3
        self.base_mp = 25 + level * 4
        
        # 重新计算属性
        self.recalc_stats()
        self.hp = self.max_hp
        self.mp = self.max_mp
        
        # 生态信息
        self.habitat = "灌草层地下0-5米"
        self.description = "根尖长出小型'光合叶'，死后24小时内能量返还土壤，精灵'归还日'仪式核心道具"
        self.behavior = "从地下钻出缠绕敌人，死亡时释放生命能量"
        
        # 添加技能
        from enemy.lothir.lothir_skills import VineWhip, Regeneration
        self.add_skill(VineWhip())
        self.add_skill(Regeneration())
        
        # 计算奖励
        self.calculate_rewards()
        
        # 特殊掉落
        self.drop_items = [
            ("root_fragment", 0.8),    # 根须碎片
            ("photosynthetic_leaf", 0.4), # 光合叶
            ("life_essence", 0.1)      # 生命精华
        ]
        
        # 特殊能力：死亡时治疗周围友军
        self.death_heal = 10 + level * 2
