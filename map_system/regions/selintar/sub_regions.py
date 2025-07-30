"""
秘法之乡·赛林塔的九塔子区域详细定义
"""

class SelintarSubRegion:
    """赛林塔子区域的基类"""
    def __init__(self, name, description, level_range, features, enemies, loot, tower_level):
        self.name = name
        self.description = description
        self.level_range = level_range
        self.features = features
        self.enemies = enemies
        self.loot = loot
        self.tower_level = tower_level  # 1-9塔的等级
        self.connections = []

class FirstTowerStardust(SelintarSubRegion):
    """第一塔·星尘 - 初级法师学习之地"""
    def __init__(self):
        super().__init__(
            name="第一塔·星尘",
            description="倒悬的第一塔，星尘级法师学习基础以太操控的地方，空气中漂浮着发光的以太粒子",
            level_range=(1, 5),
            features=[
                "星尘教室",
                "基础实验室",
                "以太感知训练场",
                "学徒宿舍"
            ],
            enemies=[
                "失控的星尘",
                "以太元素",
                "调皮学徒",
                "实验事故"
            ],
            loot=[
                "星尘法杖",
                "初级法术卷轴",
                "以太水晶",
                "学徒徽章"
            ],
            tower_level=1
        )
        self.connections = ["Starbridge", "EthericLaboratory"]

class FifthTowerStarmap(SelintarSubRegion):
    """第五塔·星图 - 高级法师研究场所"""
    def __init__(self):
        super().__init__(
            name="第五塔·星图",
            description="第五塔的核心是星图室，巨大的真空管阵列模拟着星空，6阶法师在此研究领域展开",
            level_range=(10, 15),
            features=[
                "星图演算室",
                "真空管阵列",
                "领域实验室",
                "高级图书室"
            ],
            enemies=[
                "星图守护者",
                "以太投影",
                "疯狂研究员",
                "领域失控"
            ],
            loot=[
                "星图卷轴",
                "真空管核心",
                "领域石",
                "高级法袍"
            ],
            tower_level=5
        )
        self.connections = ["Starbridge", "ForbiddenArchive"]

class NinthTowerSpiral(SelintarSubRegion):
    """第九塔·螺旋顶点 - 最高魔法殿堂"""
    def __init__(self):
        super().__init__(
            name="第九塔·螺旋顶点",
            description="螺旋的顶点，9阶法师的归宿，一念千咒的圣地，以太在此凝聚成实体",
            level_range=(17, 20),
            features=[
                "螺旋顶点",
                "千咒之间",
                "以太实体化室",
                "时间观测台"
            ],
            enemies=[
                "螺旋守卫",
                "以太实体",
                "时间扭曲",
                "前任大法师"
            ],
            loot=[
                "螺旋法典",
                "千咒之石",
                "时间碎片",
                "大法师之杖"
            ],
            tower_level=9
        )
        self.connections = ["ForbiddenArchive", "Starbridge"]

class EthericLaboratory(SelintarSubRegion):
    """以太实验室 - 法术研究设施"""
    def __init__(self):
        super().__init__(
            name="以太实验室",
            description="连接各塔的实验设施，法师们在此进行危险的以太实验",
            level_range=(6, 12),
            features=[
                "元素实验室",
                "以太转换器",
                "法术测试场",
                "防护法阵"
            ],
            enemies=[
                "实验体",
                "元素暴动",
                "法术反噬",
                "失控的实验"
            ],
            loot=[
                "实验法杖",
                "元素核心",
                "法术材料",
                "研究笔记"
            ],
            tower_level=0  # 不属于特定塔
        )
        self.connections = ["FirstTowerStardust", "FifthTowerStarmap"]

class Starbridge(SelintarSubRegion):
    """星桥 - 连接各塔的光桥网络"""
    def __init__(self):
        super().__init__(
            name="星桥",
            description="由纯粹以太构成的光桥，连接着九座倒悬塔，行走其上如履星空",
            level_range=(3, 8),
            features=[
                "光桥通道",
                "星象观测点",
                "以太传送门",
                "观星平台"
            ],
            enemies=[
                "星桥守卫",
                "以太风暴",
                "空间扭曲",
                "星象投影"
            ],
            loot=[
                "星桥碎片",
                "星象图",
                "传送石",
                "观星仪"
            ],
            tower_level=0  # 连接设施
        )
        self.connections = ["FirstTowerStardust", "FifthTowerStarmap", "NinthTowerSpiral"]

class ForbiddenArchive(SelintarSubRegion):
    """禁书库 - 存放危险知识的秘密图书馆"""
    def __init__(self):
        super().__init__(
            name="禁书库",
            description="隐藏在第五塔深处的禁书库，存放着被禁止的魔法知识和危险的以太秘密",
            level_range=(13, 18),
            features=[
                "禁书区",
                "封印法阵",
                "知识守卫",
                "秘密研究室"
            ],
            enemies=[
                "知识守卫",
                "禁书投影",
                "疯狂学者",
                "封印生物"
            ],
            loot=[
                "禁书残页",
                "封印卷轴",
                "古代法典",
                "知识碎片"
            ],
            tower_level=0  # 隐藏设施
        )
        self.connections = ["FifthTowerStarmap", "NinthTowerSpiral"]

# 区域连接图
SUB_REGION_CONNECTIONS = {
    "FirstTowerStardust": ["Starbridge", "EthericLaboratory"],
    "FifthTowerStarmap": ["Starbridge", "ForbiddenArchive", "EthericLaboratory"],
    "NinthTowerSpiral": ["Starbridge", "ForbiddenArchive"],
    "EthericLaboratory": ["FirstTowerStardust", "FifthTowerStarmap"],
    "Starbridge": ["FirstTowerStardust", "FifthTowerStarmap", "NinthTowerSpiral"],
    "ForbiddenArchive": ["FifthTowerStarmap", "NinthTowerSpiral"]
}
