"""
翡翠之森·洛希尔的精灵聚落子区域详细定义
"""

class LothirSubRegion:
    """洛希尔子区域的基类"""
    def __init__(self, name, description, level_range, features, enemies, loot, elven_affinity):
        self.name = name
        self.description = description
        self.level_range = level_range
        self.features = features
        self.enemies = enemies
        self.loot = loot
        self.elven_affinity = elven_affinity  # 精灵亲和度要求
        self.connections = []

class MossStepSettlement(LothirSubRegion):
    """苔阶聚落 - 精灵初级聚落"""
    def __init__(self):
        super().__init__(
            name="苔阶聚落",
            description="建立在巨大苔阶上的精灵聚落，年轻的精灵在此学习与自然和谐共处",
            level_range=(5, 10),
            features=[
                "苔阶住宅",
                "自然祭坛",
                "精灵花园",
                "星辉训练场"
            ],
            enemies=[
                "失控的植物",
                "暗影精灵",
                "入侵的野兽",
                "腐化的自然灵"
            ],
            loot=[
                "精灵露水",
                "苔阶种子",
                "自然护符",
                "星辉箭矢"
            ],
            elven_affinity=1
        )
        self.connections = ["RingDwelling", "StarlightPond"]

class RingDwelling(LothirSubRegion):
    """环居 - 精灵中级聚落"""
    def __init__(self):
        super().__init__(
            name="环居",
            description="环绕着古老巨树建立的精灵居所，800年寿命的精灵长老在此传授智慧",
            level_range=(10, 15),
            features=[
                "巨树环屋",
                "长老议会厅",
                "星辉锻造坊",
                "记忆之树"
            ],
            enemies=[
                "堕落长老",
                "记忆盗贼",
                "暗影刺客",
                "腐化的星辉"
            ],
            loot=[
                "长老之泪",
                "星辉木",
                "记忆碎片",
                "精灵长袍"
            ],
            elven_affinity=3
        )
        self.connections = ["MossStepSettlement", "MossFortress", "AncientGrove"]

class MossFortress(LothirSubRegion):
    """苔堡 - 精灵最高议会所在地"""
    def __init__(self):
        super().__init__(
            name="苔堡",
            description="建立在巨大苔岩上的精灵堡垒，九苔议会的所在地，守护着森林最深的秘密",
            level_range=(15, 20),
            features=[
                "苔岩堡垒",
                "九苔议会厅",
                "星辉核心",
                "古树遗迹"
            ],
            enemies=[
                "苔堡守卫",
                "议会刺客",
                "腐化的古树",
                "堕落的星辉使者"
            ],
            loot=[
                "苔堡徽章",
                "议会卷轴",
                "星辉核心碎片",
                "古树心材"
            ],
            elven_affinity=5
        )
        self.connections = ["RingDwelling", "StarlightPond", "AncientGrove"]

class StarlightPond(LothirSubRegion):
    """星辉池 - 精灵的治愈圣地"""
    def __init__(self):
        super().__init__(
            name="星辉池",
            description="被星光照耀的神秘池塘，池水具有治愈和净化的力量",
            level_range=(7, 12),
            features=[
                "星辉池水",
                "治愈祭坛",
                "月光平台",
                "净化法阵"
            ],
            enemies=[
                "池水守护者",
                "星光幻影",
                "污染体",
                "堕落的水精灵"
            ],
            loot=[
                "星辉池水",
                "月光石",
                "治愈露珠",
                "净化护符"
            ],
            elven_affinity=2
        )
        self.connections = ["MossStepSettlement", "MossFortress"]

class AncientGrove(LothirSubRegion):
    """远古圣林 - 最古老的精灵遗迹"""
    def __init__(self):
        super().__init__(
            name="远古圣林",
            description="最古老的精灵遗迹，800年前的古老森林，隐藏着精灵与自然共生的秘密",
            level_range=(18, 20),
            features=[
                "远古遗迹",
                "精灵石碑",
                "自然共鸣区",
                "星辉古树"
            ],
            enemies=[
                "远古守卫",
                "自然失衡体",
                "精灵怨灵",
                "星辉古树化身"
            ],
            loot=[
                "远古精灵装备",
                "自然共鸣石",
                "精灵古卷",
                "星辉古树心材"
            ],
            elven_affinity=5
        )
        self.connections = ["RingDwelling", "MossFortress"]

# 区域连接图
SUB_REGION_CONNECTIONS = {
    "MossStepSettlement": ["RingDwelling", "StarlightPond"],
    "RingDwelling": ["MossStepSettlement", "MossFortress", "AncientGrove"],
    "MossFortress": ["RingDwelling", "StarlightPond", "AncientGrove"],
    "StarlightPond": ["MossStepSettlement", "MossFortress"],
    "AncientGrove": ["RingDwelling", "MossFortress"]
}
