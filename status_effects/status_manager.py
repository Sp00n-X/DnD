"""状态效果管理器"""

from typing import List, Dict, Any, Optional, Type
from .base_status import BaseStatusEffect, StatusType, StatusPriority


class StatusManager:
    """集中管理角色的所有状态效果"""
    
    def __init__(self, character):
        self.character = character
        self.status_effects: List[BaseStatusEffect] = []
        self._status_cache: Dict[str, BaseStatusEffect] = {}
    
    def add_status(self, effect: BaseStatusEffect) -> Dict[str, Any]:
        """添加状态效果"""
        # 检查互斥状态
        for existing in self.status_effects:
            if not effect.can_stack_with(existing):
                return {
                    "success": False, 
                    "message": f"无法施加 {effect.name}，与 {existing.name} 互斥"
                }
        
        # 检查是否已存在相同类型的效果
        for existing in self.status_effects:
            if type(existing) == type(effect):
                if existing.merge(effect):
                    return {
                        "success": True,
                        "message": f"{effect.name} 已刷新/叠加",
                        "refreshed": True
                    }
        
        # 添加新状态
        self.status_effects.append(effect)
        self._status_cache[effect.name] = effect
        
        # 按优先级排序
        self._sort_by_priority()
        
        # 触发应用事件
        result = effect.on_apply(self.character)
        return {
            "success": True,
            "message": result.get("message", f"{effect.name} 已施加"),
            "new_effect": True
        }
    
    def remove_status(self, effect_name: str) -> Dict[str, Any]:
        """移除指定状态效果"""
        for effect in self.status_effects:
            if effect.name == effect_name:
                result = effect.on_remove(self.character)
                self.status_effects.remove(effect)
                if effect_name in self._status_cache:
                    del self._status_cache[effect_name]
                return {
                    "success": True,
                    "message": result.get("message", f"{effect_name} 已移除")
                }
        
        return {
            "success": False,
            "message": f"未找到状态效果: {effect_name}"
        }
    
    def update_all(self) -> List[Dict[str, Any]]:
        """更新所有状态效果（每回合调用）"""
        results = []
        expired_effects = []
        
        for effect in self.status_effects:
            if effect.is_active:
                result = effect.on_tick(self.character)
                results.append({
                    "effect": effect.name,
                    "result": result
                })
                
                if not effect.is_active:
                    expired_effects.append(effect)
        
        # 移除过期状态
        for effect in expired_effects:
            effect.on_remove(self.character)
            self.status_effects.remove(effect)
            if effect.name in self._status_cache:
                del self._status_cache[effect.name]
        
        return results
    
    def get_status_by_type(self, status_type: StatusType) -> List[BaseStatusEffect]:
        """获取指定类型的所有状态效果"""
        return [effect for effect in self.status_effects 
                if effect.get_status_type() == status_type]
    
    def get_status_by_name(self, name: str) -> Optional[BaseStatusEffect]:
        """通过名称获取状态效果"""
        return self._status_cache.get(name)
    
    def has_status(self, name: str) -> bool:
        """检查是否拥有指定状态效果"""
        return name in self._status_cache
    
    def clear_all_status(self) -> Dict[str, Any]:
        """清除所有状态效果"""
        removed_count = len(self.status_effects)
        for effect in self.status_effects:
            effect.on_remove(self.character)
        
        self.status_effects.clear()
        self._status_cache.clear()
        
        return {
            "success": True,
            "message": f"已清除 {removed_count} 个状态效果"
        }
    
    def get_total_effect_value(self, effect_type: str) -> float:
        """获取指定类型效果的总值"""
        total = 0.0
        for effect in self.status_effects:
            if hasattr(effect, effect_type):
                total += getattr(effect, effect_type) * effect.stacks
        return total
    
    def get_status_summary(self) -> Dict[str, Any]:
        """获取状态效果摘要"""
        summary = {
            "total_effects": len(self.status_effects),
            "effects": []
        }
        
        for effect in self.status_effects:
            summary["effects"].append(effect.to_dict())
        
        return summary
    
    def _sort_by_priority(self):
        """按优先级排序状态效果"""
        self.status_effects.sort(
            key=lambda x: (x.get_priority().value, x.name),
            reverse=True
        )
    
    def __len__(self) -> int:
        return len(self.status_effects)
    
    def __iter__(self):
        return iter(self.status_effects)
    
    def __contains__(self, name: str) -> bool:
        return self.has_status(name)
