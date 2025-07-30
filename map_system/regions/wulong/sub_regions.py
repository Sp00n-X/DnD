"""
天穹武朝·龙阙的九宫格山水子区域详细定义
"""

class WulongSubRegion:
    """龙阙子区域的基类"""
    def __init__(self, name, description, level_range, features, enemies, loot, qi_requirement):
        self.name = name
        self.description = description
        self.level_range = level_range
        self.features = features
        self.enemies = enemies
        self.loot = loot
        self.qi_requirement = qi_requirement  # 真气需求等级
        self.connections = []

class SkySwordWall(WulongSubRegion):
    """天剑壁 - 剑痕刻天的修炼圣地"""
    def __init__(self):
        super().__init__(
            name="天剑壁",
            description="高达千米的石壁上刻满了历代剑圣的剑痕，每一道剑痕都蕴含着强大的剑意",
            level_range=(12, 18),
            features=[
                "剑痕石壁",
                "剑意感悟台",
                "剑圣雕像",
                "剑气试炼场"
            ],
            enemies=[
                "剑意化身",
                "剑痕守卫",
                "挑战者剑魂",
                "堕落的剑圣"
            ],
            loot=[
                "剑痕碎片",
                "剑意结晶",
                "剑圣佩剑",
                "剑法秘籍"
            ],
            qi_requirement=6
        )
        self.connections = ["InvertedMountainCity", "AzureDragonPeak"]

class InvertedMountainCity(WulongSubRegion):
    """倒岳城 - 倒立城市的奇观"""
    def __init__(self):
        super().__init__(
            name="倒岳城",
            description="整座山峰被倒立建造的城市，建筑悬挂在岩壁之下，违背常理却稳固如山",
            level_range=(8, 14),
            features=[
                "倒挂建筑",
                "反重力广场",
                "天空集市",
                "倒立武馆"
            ],
            enemies=[
                "倒立守卫",
                "重力扭曲者",
                "空贼",
                "堕落的武者"
            ],
            loot=[
                "反重力石",
                "倒立身法秘籍",
                "天空特产",
                "武馆令牌"
            ],
            qi_requirement=4
        )
        self.connections = ["SkySwordWall", "CrimsonSwordTomb", "VermilionBirdPalace"]

class CrimsonSwordTomb(WulongSubRegion):
    """赤霄剑冢 - 历代剑圣埋剑之地"""
    def __init__(self):
        super().__init__(
            name="赤霄剑冢",
            description="赤红色的山峰上插满了历代剑圣的佩剑，每一把剑都蕴含着剑圣的意志",
            level_range=(15, 20),
            features=[
                "万剑之冢",
                "剑灵祭坛",
                "血剑池",
                "剑意传承地"
            ],
            enemies=[
                "剑灵",
                "血剑守卫",
                "剑冢幽魂",
                "堕落的剑圣意志"
            ],
            loot=[
                "赤霄剑",
                "剑灵结晶",
                "剑圣传承",
                "血剑精华"
            ],
            qi_requirement=8
        )
        self.connections = ["InvertedMountainCity", "AzureDragonPeak"]

class AzureDragonPeak(WulongSubRegion):
    """青龙峰 - 东方神兽的修炼之地"""
    def __init__(self):
        super().__init__(
            name="青龙峰",
            description="形似青龙的山峰，传说中青龙曾在此修炼，山峰蕴含着强大的东方真气",
            level_range=(10, 16),
            features=[
                "青龙雕像",
                "真气泉眼",
                "龙形石阶",
                "东方武场"
            ],
            enemies=[
                "青龙守卫",
                "真气化身",
                "东方武者",
                "堕落的龙卫"
            ],
            loot=[
                "青龙鳞片",
                "真气结晶",
                "东方武学",
                "龙形玉佩"
            ],
            qi_requirement=5
        )
        self.connections = ["SkySwordWall", "CrimsonSwordTomb", "WhiteTigerArena"]

class VermilionBirdPalace(WulongSubRegion):
    """朱雀宫 - 南方神兽的宫殿"""
    def __init__(self):
        super().__init__(
            name="朱雀宫",
            description="建立在火山口的宫殿，朱雀的火焰真气在此燃烧，温度极高",
            level_range=(13, 19),
            features=[
                "朱雀雕像",
                "火焰真气池",
                "熔岩武场",
                "火羽祭坛"
            ],
            enemies=[
                "朱雀守卫",
                "火焰真气",
                "熔岩武者",
                "火毒侵蚀者"
            ],
            loot=[
                "朱雀火羽",
                "火焰真气结晶",
                "火系武学",
                "朱雀令牌"
            ],
            qi_requirement=7
        )
        self.connections = ["InvertedMountainCity", "WhiteTigerArena"]

class WhiteTigerArena(WulongSubRegion):
    """白虎竞技场 - 武者对决的圣地"""
    def __init__(self):
        super().__init__(
            name="白虎竞技场",
            description="巨大的圆形竞技场，白虎的金属真气在此凝聚，是武者对决的圣地",
            level_range=(5, 12),
            features=[
                "白虎雕像",
                "金属真气场",
                "对决擂台",
                "荣誉石碑"
            ],
            enemies=[
                "白虎守卫",
                "金属真气",
                "挑战武者",
                "荣誉捍卫者"
            ],
            loot=[
                "白虎利爪",
                "金属真气结晶",
                "对决奖励",
                "白虎令牌"
            ],
            qi_requirement=3
        )
        self.connections = ["AzureDragonPeak", "VermilionBirdPalace"]

# 区域连接图
SUB_REGION_CONNECTIONS = {
    "SkySwordWall": ["InvertedMountainCity", "AzureDragonPeak"],
    "InvertedMountainCity": ["SkySwordWall", "CrimsonSwordTomb", "VermilionBirdPalace"],
    "CrimsonSwordTomb": ["InvertedMountainCity", "AzureDragonPeak"],
    "AzureDragonPeak": ["SkySwordWall", "CrimsonSwordTomb", "WhiteTigerArena"],
    "VermilionBirdPalace": ["InvertedMountainCity", "WhiteTigerArena"],
    "WhiteTigerArena": ["AzureDragonPeak", "VermilionBirdPalace"]
}
