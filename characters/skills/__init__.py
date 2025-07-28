"""技能系统"""

from .base_skill import Skill, SkillType
from .mage_skills import (
    Fireball,
    FrostBolt,
    DefenseBoost,
    ManaHeal,
    LightningBolt,
    ArcaneIntellect,
    MeteorShower
)

__all__ = [
    'Skill',
    'SkillType',
    'Fireball',
    'FrostBolt',
    'DefenseBoost',
    'ManaHeal',
    'LightningBolt',
    'ArcaneIntellect',
    'MeteorShower'
]
