"""战斗上下文，存储战斗相关的状态和数据"""

from typing import Dict, List, Any, Optional
from .battle_types import BattleLog, BattleRewards, BattleConfig, TurnPhase, BattleAction

class BattleContext:
    """战斗上下文，存储战斗过程中的所有状态"""
    
    def __init__(self, player, enemy, config: BattleConfig = None):
        self.player = player
        self.enemy = enemy
        self.config = config or BattleConfig()
        
        # 战斗状态
        self.turn_count = 0
        self.current_phase = TurnPhase.BATTLE_START
        self.battle_log: List[BattleLog] = []
        self.rewards = BattleRewards()
        
        # 临时状态
        self.player_defending = False
        self.enemy_defending = False
        self.player_stunned = False
        self.enemy_stunned = False
        
        # 状态效果
        self.player_status_effects: Dict[str, int] = {}  # 效果名: 剩余回合
        self.enemy_status_effects: Dict[str, int] = {}
        
    def add_log(self, log: BattleLog):
        """添加战斗日志"""
        self.battle_log.append(log)
        if self.config.show_detailed_log:
            print(log.message)
    
    def get_last_log(self) -> Optional[BattleLog]:
        """获取最后一条日志"""
        return self.battle_log[-1] if self.battle_log else None
    
    def is_battle_over(self) -> bool:
        """检查战斗是否结束"""
        return (not self.player.is_alive() or 
                not self.enemy.is_alive() or 
                self.turn_count >= self.config.turn_limit)
    
    def get_battle_result(self) -> str:
        """获取战斗结果"""
        if not self.player.is_alive():
            return "defeat"
        elif not self.enemy.is_alive():
            return "victory"
        elif self.turn_count >= self.config.turn_limit:
            return "draw"
        else:
            return "ongoing"
    
    def apply_status_effects(self):
        """应用状态效果"""
        # 处理玩家状态效果
        effects_to_remove = []
        for effect_name, duration in self.player_status_effects.items():
            if effect_name == "burn":
                burn_damage = max(1, self.player.max_hp // 10)
                self.player.take_damage(burn_damage)
                self.add_log(BattleLog(
                    turn=self.turn_count,
                    phase=self.current_phase,
                    actor="system",
                    action=BattleAction.ITEM,
                    target=self.player.name,
                    damage=burn_damage,
                    message=f"🔥 {self.player.name}受到{burn_damage}点灼烧伤害！"
                ))
            elif effect_name == "poison":
                poison_damage = max(1, self.player.max_hp // 8)
                self.player.take_damage(poison_damage)
                self.add_log(BattleLog(
                    turn=self.turn_count,
                    phase=self.current_phase,
                    actor="system",
                    action=BattleAction.ITEM,
                    target=self.player.name,
                    damage=poison_damage,
                    message=f"☠️ {self.player.name}受到{poison_damage}点中毒伤害！"
                ))
            
            # 减少持续时间
            self.player_status_effects[effect_name] = duration - 1
            if self.player_status_effects[effect_name] <= 0:
                effects_to_remove.append(effect_name)
        
        # 移除过期效果
        for effect in effects_to_remove:
            del self.player_status_effects[effect]
            self.add_log(BattleLog(
                turn=self.turn_count,
                phase=self.current_phase,
                actor="system",
                action=BattleAction.ITEM,
                target=self.player.name,
                message=f"✨ {self.player.name}的{effect}效果已消失！"
            ))
        
        # 处理敌人状态效果（类似逻辑）
        effects_to_remove = []
        for effect_name, duration in self.enemy_status_effects.items():
            if effect_name == "burn":
                burn_damage = max(1, self.enemy.max_hp // 10)
                self.enemy.take_damage(burn_damage)
                self.add_log(BattleLog(
                    turn=self.turn_count,
                    phase=self.current_phase,
                    actor="system",
                    action=BattleAction.ITEM,
                    target=self.enemy.name,
                    damage=burn_damage,
                    message=f"🔥 {self.enemy.name}受到{burn_damage}点灼烧伤害！"
                ))
            elif effect_name == "poison":
                poison_damage = max(1, self.enemy.max_hp // 8)
                self.enemy.take_damage(poison_damage)
                self.add_log(BattleLog(
                    turn=self.turn_count,
                    phase=self.current_phase,
                    actor="system",
                    action=BattleAction.ITEM,
                    target=self.enemy.name,
                    damage=poison_damage,
                    message=f"☠️ {self.enemy.name}受到{poison_damage}点中毒伤害！"
                ))
            
            self.enemy_status_effects[effect_name] = duration - 1
            if self.enemy_status_effects[effect_name] <= 0:
                effects_to_remove.append(effect_name)
        
        for effect in effects_to_remove:
            del self.enemy_status_effects[effect]
            self.add_log(BattleLog(
                turn=self.turn_count,
                phase=self.current_phase,
                actor="system",
                action=BattleAction.ITEM,
                target=self.enemy.name,
                message=f"✨ {self.enemy.name}的{effect}效果已消失！"
            ))
    
    def add_status_effect(self, target: str, effect_name: str, duration: int):
        """添加状态效果"""
        if target == "player":
            self.player_status_effects[effect_name] = duration
        elif target == "enemy":
            self.enemy_status_effects[effect_name] = duration
    
    def get_status_effects(self, target: str) -> Dict[str, int]:
        """获取目标的状态效果"""
        if target == "player":
            return self.player_status_effects
        elif target == "enemy":
            return self.enemy_status_effects
        return {}
    
    def next_turn(self):
        """进入下一回合"""
        self.turn_count += 1
        self.player_defending = False
        self.enemy_defending = False
        
        # 应用状态效果
        self.apply_status_effects()
    
    def reset_defense_flags(self):
        """重置防御标志"""
        self.player_defending = False
        self.enemy_defending = False
