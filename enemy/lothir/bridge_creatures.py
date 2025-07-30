from enemy.base_enemy import BaseEnemy, EnemyType
from characters.skills.base_skill import Skill
from typing import List

class MirrorMarten(BaseEnemy):
    """镜羽貂 - 枝桥层生物"""
    
    def __init__(self, level: int = 2):
        super().__init__("镜羽貂", level, EnemyType.NORMAL)
        
        # 基础属性
        self.base_hp = 30 + level * 4
        self.base_attack = 10 + level * 2
        self.base_defense = 6 + level
        self.base_mp = 25 + level * 3
        
        # 重新计算属性
        self.recalc_stats()
        self.hp = self.max_hp
        self.mp = self.max_mp
        
        # 生态信息
        self.habitat = "枝桥层（10-30米）"
        self.description = "每片尾羽是一面3秒延迟的镜像，充当'移动潜望镜'预警地面掠食者"
        self.behavior = "敏捷灵活，善于利用镜像迷惑敌人"
        
        # 添加技能
        from enemy.lothir.lothir_skills import MirrorImage, QuickStrike
        self.add_skill(MirrorImage())
        self.add_skill(QuickStrike())
        
        # 计算奖励
        self.calculate_rewards()
        
        # 特殊掉落
        self.drop_items = [
            ("mirror_feather", 0.75),  # 镜像羽毛
            ("marten_fur", 0.5),       # 貂皮
            ("reflective_scale", 0.15) # 反射鳞片
        ]

class CanopyBridgeBeetle(BaseEnemy):
    """叶桥甲虫 - 枝桥层辅助生物"""
    
    def __init__(self, level: int = 1):
        super().__init__("叶桥甲虫", level, EnemyType.NORMAL)
        
        # 基础属性 - 高防御型
        self.base_hp = 45 + level * 10
        self.base_attack = 4 + level
        self.base_defense = 15 + level * 4
        self.base_mp = 10 + level * 2
        
        # 重新计算属性
        self.recalc_stats()
        self.hp = self.max_hp
        self.mp = self.max_mp
        
        # 生态信息
        self.habitat = "枝桥层枝隙"
        self.description = "背甲可展开成2米宽叶状桥板，精灵幼芽踩其背甲跨越枝隙"
        self.behavior = "防御性强，会用坚硬甲壳保护自己和同伴"
        
        # 添加技能
        from enemy.lothir.lothir_skills import ShellShield, RamAttack
        self.add_skill(ShellShield())
        self.add_skill(RamAttack())
        
        # 计算奖励
        self.calculate_rewards()
        
        # 特殊掉落
        self.drop_items = [
            ("beetle_shell", 0.8),     # 甲虫壳
            ("bridge_plate", 0.3),     # 桥板
            ("hardened_resin", 0.2)    # 硬化树脂
        ]

class StardustSilkworm(BaseEnemy):
    """星露蚕 - 枝桥层特殊生物"""
    
    def __init__(self, level: int = 1):
        super().__init__("星露蚕", level, EnemyType.NORMAL)
        
        # 基础属性 - 低攻击高魔法
        self.base_hp = 20 + level * 3
        self.base_attack = 3 + level
        self.base_defense = 4 + level
        self.base_mp = 40 + level * 5
        
        # 重新计算属性
        self.recalc_stats()
        self.hp = self.max_hp
        self.mp = self.max_mp
        
        # 生态信息
        self.habitat = "枝桥层叶片背面"
        self.description = "吐丝含星辉微粒，夜晚发光，精灵礼服原料，每十年一次'星裳祭'"
        self.behavior = "吐丝攻击，能释放星辉能量进行治疗"
        
        # 添加技能
        from enemy.lothir.lothir_skills import VineWhip, Regeneration
        self.add_skill(VineWhip())
        self.add_skill(Regeneration())
        
        # 计算奖励
        self.calculate_rewards()
        
        # 特殊掉落
        self.drop_items = [
            ("stardust_silk", 0.9),    # 星尘丝
            ("luminescent_gland", 0.4), # 发光腺
            ("silk_cocoon", 0.1)       # 蚕茧
        ]
        
        # 特殊能力：发光
        self.has_glow = True
        self.glow_radius = 3 + level
