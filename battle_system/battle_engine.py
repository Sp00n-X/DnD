"""战斗引擎核心类"""

import random
from typing import Optional, List, Dict, Any
from characters.equipments.base_equipments import DamageType
from .battle_types import BattleAction, BattleResult, BattleLog, TurnPhase, BattleRewards
from .battle_context import BattleContext
from .battle_ui import BattleUI

class BattleEngine:
    """战斗引擎核心类"""
    
    def __init__(self, player, enemy, config=None):
        """初始化战斗引擎"""
        self.context = BattleContext(player, enemy, config)
        self.ui = BattleUI(self.context)
        
    def start_battle(self) -> BattleResult:
        """开始战斗"""
        self.ui.display_battle_start()
        
        while not self.context.is_battle_over():
            self.context.next_turn()
            self._process_turn()
        
        result = self.context.get_battle_result()
        self.ui.display_battle_end(result)
        
        # 处理战斗结果
        self._process_battle_result(result)
        
        return result
    
    def _process_turn(self):
        """处理一个回合"""
        # 玩家回合
        if not self.context.player_stunned:
            self._process_player_turn()
        else:
            print(f"\n💫 {self.context.player.name}被眩晕，无法行动！")
            self.context.player_stunned = False
        
        if self.context.is_battle_over():
            return
        
        # 敌人回合
        if not self.context.enemy_stunned:
            self._process_enemy_turn()
        else:
            print(f"\n💫 {self.context.enemy.name}被眩晕，无法行动！")
            self.context.enemy_stunned = False
        
        # 回合结束时更新状态（包括技能冷却）
        self.context.player.update_status_effects()
        self.context.enemy.update_status_effects()
    
    def _process_player_turn(self):
        """处理玩家回合"""
        self.context.current_phase = TurnPhase.PLAYER_TURN
        
        # 显示回合信息
        self.ui.display_turn_start()
        
        # 获取玩家行动
        action_choice = self.ui.display_player_actions()
        
        # 执行玩家行动
        self._execute_player_action(action_choice)
    
    def _execute_player_action(self, action_choice: int):
        """执行玩家行动"""
        player = self.context.player
        enemy = self.context.enemy
        
        # 获取可用技能
        usable_skills = [s for s in player.skills if s.can_use(player)]
        
        if action_choice == 1:  # 普通攻击
            damage = max(1, player.attack - enemy.defense)
            enemy.take_damage(damage, DamageType.PHYSICAL)
            
            log = BattleLog(
                turn=self.context.turn_count,
                phase=TurnPhase.PLAYER_TURN,
                actor=player.name,
                action=BattleAction.ATTACK,
                target=enemy.name,
                damage=damage,
                message=f"💥 {player.name}对{enemy.name}造成了{damage}点物理伤害！"
            )
            self.context.add_log(log)
            
            # 触发装备效果
            self._trigger_equipment_effects(player, enemy)
            
        elif action_choice == 2:  # 防御
            self.context.player_defending = True
            log = BattleLog(
                turn=self.context.turn_count,
                phase=TurnPhase.PLAYER_TURN,
                actor=player.name,
                action=BattleAction.DEFEND,
                target=player.name,
                message=f"🛡️ {player.name}进入了防御姿态！"
            )
            self.context.add_log(log)
            
        elif action_choice <= 2 + len(usable_skills):  # 使用技能
            skill_index = action_choice - 3
            skill = usable_skills[skill_index]
            
            result = player.use_skill(skill.name, target=enemy)
            
            log = BattleLog(
                turn=self.context.turn_count,
                phase=TurnPhase.PLAYER_TURN,
                actor=player.name,
                action=BattleAction.SKILL,
                target=enemy.name,
                message=result["message"]
            )
            self.context.add_log(log)
            
            if result.get("damage", 0) > 0:
                log.damage = result["damage"]
                
            # 触发装备效果
            self._trigger_equipment_effects(player, enemy)
            
        elif action_choice == 3 + len(usable_skills):  # 使用物品
            self._use_item()
            
        elif action_choice == 4 + len(usable_skills):  # 逃跑
            if self._attempt_flee():
                return
    
    def _process_enemy_turn(self):
        """处理敌人回合"""
        self.context.current_phase = TurnPhase.ENEMY_TURN
        
        enemy = self.context.enemy
        player = self.context.player
        
        # Boss使用技能系统
        if hasattr(enemy, 'select_action') and hasattr(enemy, 'execute_action'):
            action = enemy.select_action(player)
            result = enemy.execute_action(action)
            
            log = BattleLog(
                turn=self.context.turn_count,
                phase=TurnPhase.ENEMY_TURN,
                actor=enemy.name,
                action=BattleAction.SKILL,
                target=player.name,
                message=result['message']
            )
            
            if 'damage' in result:
                damage = int(result['damage'])
                if self.context.player_defending:
                    damage = int(damage * 0.5)
                    log.message += f" (防御减少50%伤害)"
                log.damage = damage
                
            if 'heal_amount' in result:
                log.heal = result['heal_amount']
                
            self.context.add_log(log)
            
            # 处理状态效果
            if result.get('burn_applied'):
                self.context.add_status_effect("player", "burn", 3)
            if result.get('poison_applied'):
                self.context.add_status_effect("player", "poison", 3)
            if result.get('stun_applied'):
                self.context.player_stunned = True
                
        else:  # 普通敌人攻击
            damage = max(1, enemy.attack - player.defense)
            if self.context.player_defending:
                damage = int(damage * 0.5)
                
            player.take_damage(damage, DamageType.PHYSICAL)
            
            log = BattleLog(
                turn=self.context.turn_count,
                phase=TurnPhase.ENEMY_TURN,
                actor=enemy.name,
                action=BattleAction.ATTACK,
                target=player.name,
                damage=damage,
                message=f"💥 {enemy.name}对{player.name}造成了{damage}点物理伤害！"
            )
            self.context.add_log(log)
    
    def _trigger_equipment_effects(self, attacker, target):
        """触发装备效果"""
        for equipment in attacker.equipment.values():
            if equipment and hasattr(equipment, 'effects'):
                for effect in equipment.effects:
                    effect_class = effect.__class__.__name__
                    
                    # 处理不同类型的装备效果
                    if effect_class == 'DamageEffect':
                        scale_value = getattr(attacker, effect.scale_stat.name.lower(), 0)
                        extra_damage = int(scale_value * effect.coefficient)
                        if extra_damage > 0:
                            target.take_damage(extra_damage, effect.dmg_type)
                            print(f"[{equipment.name}] 追加 {extra_damage} {effect.dmg_type.name} 伤害!")
                    
                    elif effect_class == 'ManaSurgeEffect':
                        if random.random() < effect.chance:
                            attacker.mp = min(attacker.mp + effect.mana_restore, attacker.max_mp)
                            print(f"[{equipment.name}] 恢复了 {effect.mana_restore} 点法力值!")
                    
                    elif effect_class == 'ArcaneExplosionEffect':
                        if random.random() < effect.chance:
                            damage = int(attacker.spell_power * effect.damage_scale)
                            target.take_damage(damage, DamageType.MAGICAL)
                            print(f"[{equipment.name}] 引发奥术爆炸，造成 {damage} 点额外魔法伤害!")
    
    def _use_item(self):
        """使用物品"""
        # 这里可以扩展物品系统
        print("🧪 物品系统暂未实现")
    
    def _attempt_flee(self) -> bool:
        """尝试逃跑"""
        if not self.context.config.allow_flee:
            print("❌ 当前战斗无法逃跑！")
            return False
            
        # 50%逃跑成功率
        if random.random() < 0.5:
            print("🏃 成功逃跑！")
            return True
        else:
            print("❌ 逃跑失败！")
            return False
    
    def _process_battle_result(self, result: str):
        """处理战斗结果"""
        if result == "victory":
            enemy = self.context.enemy
            
            # 计算奖励
            exp_reward = enemy.level * 50
            gold_reward = enemy.level * 10
            
            self.context.rewards.experience = exp_reward
            self.context.rewards.gold = gold_reward
            
            # 给予经验值
            self.context.player.gain_experience(exp_reward)
            
            # 如果是Boss，标记为已击败
            if hasattr(enemy, '__class__') and 'FloorBoss' in str(type(enemy)):
                if hasattr(self.context.player, 'defeated_bosses'):
                    self.context.player.defeated_bosses.add(
                        getattr(self.context.player, 'current_floor', 1)
                    )
    
    def get_battle_summary(self) -> Dict[str, Any]:
        """获取战斗摘要"""
        return {
            "result": self.context.get_battle_result(),
            "turns": self.context.turn_count,
            "rewards": {
                "experience": self.context.rewards.experience,
                "gold": self.context.rewards.gold,
                "items": self.context.rewards.items
            },
            "log": [log.__dict__ for log in self.context.battle_log]
        }
