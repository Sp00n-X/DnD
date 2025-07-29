"""Boss技能系统 - 统一管理所有Boss的技能"""

from enemy.bosses.goblin_chef_skills import GOBLIN_CHEF_SKILLS
from enemy.bosses.template_boss_skills import DRAGON_BOSS_SKILLS, MAGE_BOSS_SKILLS
from typing import Dict, List, Any

# Boss技能注册表
BOSS_SKILLS_REGISTRY = {
    "goblin_chef": GOBLIN_CHEF_SKILLS,
    "dragon_boss": DRAGON_BOSS_SKILLS,
    "mage_boss": MAGE_BOSS_SKILLS,
    # 这里可以添加其他boss的技能
    # "fourth_boss": FOURTH_BOSS_SKILLS,
}

def get_boss_skills(boss_name: str) -> List[Any]:
    """获取指定boss的所有技能
    
    Args:
        boss_name: boss的名称标识符
        
    Returns:
        该boss的技能列表
        
    Raises:
        KeyError: 如果boss名称不存在
    """
    if boss_name not in BOSS_SKILLS_REGISTRY:
        raise KeyError(f"Boss '{boss_name}' 的技能未找到")
    return BOSS_SKILLS_REGISTRY[boss_name]

def get_all_boss_names() -> List[str]:
    """获取所有已注册的boss名称
    
    Returns:
        所有boss名称的列表
    """
    return list(BOSS_SKILLS_REGISTRY.keys())

def register_boss_skills(boss_name: str, skills: List[Any]) -> None:
    """注册新boss的技能
    
    Args:
        boss_name: boss的唯一标识符
        skills: 该boss的技能列表
    """
    BOSS_SKILLS_REGISTRY[boss_name] = skills

# 导出常用技能列表供其他模块使用
__all__ = [
    'get_boss_skills',
    'get_all_boss_names', 
    'register_boss_skills',
    'BOSS_SKILLS_REGISTRY'
]
