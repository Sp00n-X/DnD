from enemy.base_enemy import BaseEnemy, EnemyType
from characters.skills.base_skill import Skill
from typing import List

class UmbralPanther(BaseEnemy):
    """影纹豹 - 苔根层顶级掠食者"""
    
    def __init__(self, level: int = 5):
        super().__init__("影纹豹", level, EnemyType.ELITE)
        
        # 基础属性 - 高敏捷高攻击
        self.base_hp = 45 + level * 8
        self.base_attack = 15 + level * 4
        self.base_defense = 10 + level * 2
        self.base_mp = 30 + level * 3
        
        # 重新计算属性
        self.recalc_stats()
        self.hp = self.max_hp
        self.mp = self.max_mp
        
        # 生态信息
        self.habitat = "苔根层（地下0-5米）"
        self.description = "皮毛折射光线形成'延迟影子'，实体可在影间瞬闪3米，地精天敌，精灵盟友，巡林队坐骑"
        self.behavior = "潜行伏击，利用影子瞬移，高爆发伤害"
        
        # 添加技能
        from enemy.lothir.lothir_skills import ShadowStep, Pounce
        self.add_skill(ShadowStep())
        self.add_skill(Pounce())
        
        # 计算奖励
        self.calculate_rewards()
        
        # 特殊掉落
        self.drop_items = [
            ("shadow_pelt", 0.7),      # 影纹毛皮
            ("panther_claw", 0.5),     # 豹爪
            ("shadow_essence", 0.3),   # 暗影精华
            ("umbral_fang", 0.1)       # 暗影獠牙
        ]
        
        # 特殊能力：暗影步
        self.has_shadow_step = True
        self.shadow_range = 3

class GloomNewt(BaseEnemy):
    """幽沼鲵 - 苔根层两栖生物"""
    
    def __init__(self, level: int = 3):
        super().__init__("幽沼鲵", level, EnemyType.NORMAL)
        
        # 基础属性 - 均衡型
        self.base_hp = 40 + level * 7
        self.base_attack = 8 + level * 2
        self.base_defense = 12 + level * 3
        self.base_mp = 35 + level * 4
        
        # 重新计算属性
        self.recalc_stats()
        self.hp = self.max_hp
        self.mp = self.max_mp
        
        # 生态信息
        self.habitat = "苔根层幽暗水域"
        self.description = "皮肤吸收星辉后呈现夜空星图，精灵儿童'活体星象馆'"
        self.behavior = "水陆两栖，能释放星图魔法攻击"
        
        # 添加技能
        from enemy.lothir.lothir_skills import StarlightBurst, VenomStrike
        self.add_skill(StarlightBurst())
        self.add_skill(VenomStrike())
        
        # 计算奖励
        self.calculate_rewards()
        
        # 特殊掉落
        self.drop_items = [
            ("newt_skin", 0.8),        # 鲵皮
            ("star_map_fragment", 0.4), # 星图碎片
            ("amphibious_gland", 0.2), # 两栖腺
            ("astral_scale", 0.1)      # 星鳞
        ]
        
        # 特殊能力：星图显示
        self.has_star_map = True
        self.map_reveal_radius = 5

class SilenceMoss(BaseEnemy):
    """静语苔 - 苔根层特殊植物"""
    
    def __init__(self, level: int = 2):
        super().__init__("静语苔", level, EnemyType.NORMAL)
        
        # 基础属性 - 高魔法型
        self.base_hp = 35 + level * 5
        self.base_attack = 5 + level
        self.base_defense = 8 + level * 2
        self.base_mp = 50 + level * 6
        
        # 重新计算属性
        self.recalc_stats()
        self.hp = self.max_hp
        self.mp = self.max_mp
        
        # 生态信息
        self.habitat = "苔根层阴影处"
        self.description = "覆盖区域声音衰减90%，精灵狩猎队埋伏点，也是长老冥想垫"
        self.behavior = "释放沉默领域，用魔法攻击敌人"
        
        # 添加技能
        from enemy.lothir.lothir_skills import StarlightBurst, VenomStrike
        self.add_skill(StarlightBurst())
        self.add_skill(VenomStrike())
        
        # 计算奖励
        self.calculate_rewards()
        
        # 特殊掉落
        self.drop_items = [
            ("silence_moss", 0.9),     # 静语苔
            ("sound_dampener", 0.3),   # 消音器
            ("meditation_mat", 0.1)    # 冥想垫
        ]
        
        # 特殊能力：沉默领域
        self.has_silence = True
        self.silence_radius = 2
