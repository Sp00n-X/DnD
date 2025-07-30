"""
齿轮之城·阿斯图里亚的子区域详细定义
"""

class GearhavenSubRegion:
    """齿轮之城子区域的基类"""
    def __init__(self, name, description, level_range, features, enemies, loot):
        self.name = name
        self.description = description
        self.level_range = level_range
        self.features = features
        self.enemies = enemies
        self.loot = loot
        self.connections = []

class SevenFurnaceParliament(GearhavenSubRegion):
    """七炉议会 - 齿轮城最高权力机构"""
    def __init__(self):
        super().__init__(
            name="七炉议会",
            description="七位公爵轮流执政的权力中枢，巨大的真空管阵列控制着整个城市的以太电流",
            level_range=(10, 15),
            features=[
                "真空管议会大厅",
                "以太电流控制室",
                "公爵私人实验室",
                "机密档案库"
            ],
            enemies=[
                "机械守卫MK-III",
                "以太监察官",
                "议会保镖",
                "叛变的工程师"
            ],
            loot=[
                "真空管核心",
                "议会通行证",
                "以太电路图",
                "公爵徽章"
            ]
        )
        self.connections = ["BlackWrenchHQ", "SkyDocks"]

class BlackWrenchHQ(GearhavenSubRegion):
    """黑扳手总部 - 工人行会秘密基地"""
    def __init__(self):
        super().__init__(
            name="黑扳手总部",
            description="隐藏在废弃工厂下的工人行会总部，昏暗的灯泡下是精密的反抗计划",
            level_range=(8, 12),
            features=[
                "秘密会议室",
                "武器改装车间",
                "情报交换所",
                "地下通道网络"
            ],
            enemies=[
                "黑扳手特工",
                "改造工人",
                "工业间谍",
                "叛徒线人"
            ],
            loot=[
                "黑扳手徽章",
                "改装工具箱",
                "反抗军地图",
                "机密情报"
            ]
        )
        self.connections = ["SevenFurnaceParliament", "AbandonedFogRoot"]

class AbandonedFogRoot(GearhavenSubRegion):
    """废弃雾根 - 地表废弃区域"""
    def __init__(self):
        super().__init__(
            name="废弃雾根",
            description="曾经繁华的工业区，现在被浓雾和废弃机械覆盖，隐藏着古老的秘密",
            level_range=(5, 10),
            features=[
                "锈蚀的工厂",
                "以太泄漏区",
                "古代机械残骸",
                "隐藏的地下入口"
            ],
            enemies=[
                "锈蚀机械",
                "以太幽灵",
                "拾荒者",
                "变异生物"
            ],
            loot=[
                "古代零件",
                "以太结晶",
                "技术蓝图",
                "稀有金属"
            ]
        )
        self.connections = ["BlackWrenchHQ", "EthericPowerPlant"]

class SkyDocks(GearhavenSubRegion):
    """天空码头 - 飞鳍梭起降区"""
    def __init__(self):
        super().__init__(
            name="天空码头",
            description="悬浮在云层中的巨大码头，蝠鲼飞梭和鲸索电梯在此起降",
            level_range=(7, 13),
            features=[
                "飞梭停机坪",
                "货物转运区",
                "海关检查站",
                "黑市交易点"
            ],
            enemies=[
                "海关官员",
                "走私者",
                "空贼",
                "机械维修工"
            ],
            loot=[
                "飞梭零件",
                "走私货物",
                "海关文件",
                "空贼藏宝图"
            ]
        )
        self.connections = ["SevenFurnaceParliament", "EthericPowerPlant"]

class EthericPowerPlant(GearhavenSubRegion):
    """以太发电厂 - 城市的能源核心"""
    def __init__(self):
        super().__init__(
            name="以太发电厂",
            description="巨大的真空管阵列将以太转化为电能，是整个城市的能源心脏",
            level_range=(12, 18),
            features=[
                "主反应炉",
                "控制室",
                "冷却系统",
                "以太储存罐"
            ],
            enemies=[
                "电厂守卫",
                "以太泄漏体",
                "失控的机械",
                "破坏分子"
            ],
            loot=[
                "以太电池",
                "真空管",
                "能源核心",
                "技术手册"
            ]
        )
        self.connections = ["AbandonedFogRoot", "SkyDocks"]

# 区域连接图
SUB_REGION_CONNECTIONS = {
    "SevenFurnaceParliament": ["BlackWrenchHQ", "SkyDocks"],
    "BlackWrenchHQ": ["SevenFurnaceParliament", "AbandonedFogRoot"],
    "AbandonedFogRoot": ["BlackWrenchHQ", "EthericPowerPlant"],
    "SkyDocks": ["SevenFurnaceParliament", "EthericPowerPlant"],
    "EthericPowerPlant": ["AbandonedFogRoot", "SkyDocks"]
}
