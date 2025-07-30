"""
洛希尔地区生物模块
翡翠之森·洛希尔的完整生物志实现
"""

from .canopy_creatures import CelestWeaver, GlaiveKestrel, WindWhistlerVine
from .bridge_creatures import MirrorMarten, CanopyBridgeBeetle, StardustSilkworm
from .undergrowth_creatures import MoonRoe, MossBackTapir, LoopRoot
from .root_creatures import UmbralPanther, GloomNewt, SilenceMoss
from .swamp_creatures import MirrorHeron, StarAlgaeLotus, StillwaterViper
from .legendary_creatures import CelestialStag, ForestUmbraPack, CircadianGemini

# 按层级分类的生物
CANOPY_CREATURES = {
    "星辉织蛛": CelestWeaver,
    "光刃隼": GlaiveKestrel,
    "风哨藤群": WindWhistlerVine
}

BRIDGE_CREATURES = {
    "镜羽貂": MirrorMarten,
    "叶桥甲虫": CanopyBridgeBeetle,
    "星露蚕": StardustSilkworm
}

UNDERGROUND_CREATURES = {
    "月轮狍": MoonRoe,
    "苔背貘": MossBackTapir,
    "回环根须": LoopRoot
}

ROOT_CREATURES = {
    "影纹豹": UmbralPanther,
    "幽沼鲵": GloomNewt,
    "静语苔": SilenceMoss
}

SWAMP_CREATURES = {
    "镜沼鹭": MirrorHeron,
    "星藻浮莲": StarAlgaeLotus,
    "静水蛇": StillwaterViper
}

LEGENDARY_CREATURES = {
    "星穹牡鹿": CelestialStag,
    "林影狼群": ForestUmbraPack,
    "昼夜双生蝶": CircadianGemini
}

# 所有洛希尔生物
ALL_LOTHIR_CREATURES = {
    **CANOPY_CREATURES,
    **BRIDGE_CREATURES,
    **UNDERGROUND_CREATURES,
    **ROOT_CREATURES,
    **SWAMP_CREATURES,
    **LEGENDARY_CREATURES
}

# 按等级范围分类
LOW_LEVEL_CREATURES = {
    "星辉织蛛": CelestWeaver,
    "叶桥甲虫": CanopyBridgeBeetle,
    "星露蚕": StardustSilkworm,
    "回环根须": LoopRoot,
    "静语苔": SilenceMoss
}

MID_LEVEL_CREATURES = {
    "光刃隼": GlaiveKestrel,
    "风哨藤群": WindWhistlerVine,
    "镜羽貂": MirrorMarten,
    "月轮狍": MoonRoe,
    "苔背貘": MossBackTapir,
    "幽沼鲵": GloomNewt,
    "星藻浮莲": StarAlgaeLotus
}

HIGH_LEVEL_CREATURES = {
    "影纹豹": UmbralPanther,
    "镜沼鹭": MirrorHeron,
    "静水蛇": StillwaterViper
}

LEGENDARY_LEVEL_CREATURES = {
    "星穹牡鹿": CelestialStag,
    "林影狼群": ForestUmbraPack,
    "昼夜双生蝶": CircadianGemini
}

def get_creature_by_name(name: str, level: int = None):
    """根据名称获取生物实例"""
    if name in ALL_LOTHIR_CREATURES:
        creature_class = ALL_LOTHIR_CREATURES[name]
        if level is None:
            # 根据生物类型设置默认等级
            if name in LOW_LEVEL_CREATURES:
                level = 1
            elif name in MID_LEVEL_CREATURES:
                level = 5
            elif name in HIGH_LEVEL_CREATURES:
                level = 10
            else:
                level = 20
        return creature_class(level)
    return None

def get_random_creature_by_tier(tier: str, level: int = None):
    """根据层级随机获取生物"""
    import random
    
    tier_map = {
        "low": LOW_LEVEL_CREATURES,
        "mid": MID_LEVEL_CREATURES,
        "high": HIGH_LEVEL_CREATURES,
        "legendary": LEGENDARY_LEVEL_CREATURES
    }
    
    if tier in tier_map and tier_map[tier]:
        creature_name = random.choice(list(tier_map[tier].keys()))
        return get_creature_by_name(creature_name, level)
    return None

def get_creatures_by_habitat(habitat: str):
    """根据栖息地获取生物列表"""
    habitat_map = {
        "canopy": CANOPY_CREATURES,
        "bridge": BRIDGE_CREATURES,
        "underground": UNDERGROUND_CREATURES,
        "root": ROOT_CREATURES,
        "swamp": SWAMP_CREATURES
    }
    
    return habitat_map.get(habitat.lower(), {})

__all__ = [
    # 生物类
    'CelestWeaver', 'GlaiveKestrel', 'WindWhistlerVine',
    'MirrorMarten', 'CanopyBridgeBeetle', 'StardustSilkworm',
    'MoonRoe', 'MossBackTapir', 'LoopRoot',
    'UmbralPanther', 'GloomNewt', 'SilenceMoss',
    'MirrorHeron', 'StarAlgaeLotus', 'StillwaterViper',
    'CelestialStag', 'ForestUmbraPack', 'CircadianGemini',
    
    # 分类字典
    'CANOPY_CREATURES', 'BRIDGE_CREATURES', 'UNDERGROUND_CREATURES',
    'ROOT_CREATURES', 'SWAMP_CREATURES', 'LEGENDARY_CREATURES',
    'ALL_LOTHIR_CREATURES', 'LOW_LEVEL_CREATURES', 'MID_LEVEL_CREATURES',
    'HIGH_LEVEL_CREATURES', 'LEGENDARY_LEVEL_CREATURES',
    
    # 工具函数
    'get_creature_by_name', 'get_random_creature_by_tier', 'get_creatures_by_habitat'
]
