"""
艾兰提亚世界四大区域子区域系统
提供统一的接口访问所有区域的子区域
"""

from .gearhaven import *
from .selintar import *
from .lothir import *
from .wulong import *

# 区域映射
REGION_MAPPING = {
    "齿轮之城": "gearhaven",
    "秘法之乡": "selintar", 
    "翡翠之森": "lothir",
    "天穹武朝": "wulong"
}

# 子区域名称映射
SUB_REGION_NAMES = {
    "齿轮之城": [
        "七炉议会",
        "黑扳手总部",
        "废弃雾根",
        "天空码头",
        "以太发电厂"
    ],
    "秘法之乡": [
        "第一塔·星尘",
        "第五塔·星图",
        "第九塔·螺旋顶点",
        "以太实验室",
        "星桥",
        "禁书库"
    ],
    "翡翠之森": [
        "苔阶聚落",
        "环居",
        "苔堡",
        "星辉池",
        "远古圣林"
    ],
    "天穹武朝": [
        "天剑壁",
        "倒岳城",
        "赤霄剑冢",
        "青龙峰",
        "朱雀宫",
        "白虎竞技场"
    ]
}

def get_sub_regions(region_name):
    """获取指定区域的所有子区域名称"""
    return SUB_REGION_NAMES.get(region_name, [])

def get_region_module(region_name):
    """获取指定区域的模块名"""
    return REGION_MAPPING.get(region_name)

# 子区域类映射
SUB_REGION_CLASSES = {
    "齿轮之城": {
        "七炉议会": "SevenFurnaceParliament",
        "黑扳手总部": "BlackWrenchHQ",
        "废弃雾根": "AbandonedFogRoot",
        "天空码头": "SkyDocks",
        "以太发电厂": "EthericPowerPlant"
    },
    "秘法之乡": {
        "第一塔·星尘": "FirstTowerStardust",
        "第五塔·星图": "FifthTowerStarmap",
        "第九塔·螺旋顶点": "NinthTowerSpiral",
        "以太实验室": "EthericLaboratory",
        "星桥": "Starbridge",
        "禁书库": "ForbiddenArchive"
    },
    "翡翠之森": {
        "苔阶聚落": "MossStepSettlement",
        "环居": "RingDwelling",
        "苔堡": "MossFortress",
        "星辉池": "StarlightPond",
        "远古圣林": "AncientGrove"
    },
    "天穹武朝": {
        "天剑壁": "SkySwordWall",
        "倒岳城": "InvertedMountainCity",
        "赤霄剑冢": "CrimsonSwordTomb",
        "青龙峰": "AzureDragonPeak",
        "朱雀宫": "VermilionBirdPalace",
        "白虎竞技场": "WhiteTigerArena"
    }
}

def get_sub_region_class(region_name, sub_region_name):
    """获取子区域类"""
    return SUB_REGION_CLASSES.get(region_name, {}).get(sub_region_name)
