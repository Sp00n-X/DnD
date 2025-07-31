"""战斗界面和交互处理"""

from typing import List, Optional
from .battle_types import BattleAction, BattleLog
from .battle_context import BattleContext

class BattleUI:
    """战斗界面处理类"""
    
    def __init__(self, context: BattleContext):
        self.context = context
    
    def display_battle_start(self):
        """显示战斗开始界面"""
        print("\n" + "="*60)
        print(f"⚔️ 战斗开始: {self.context.player.name} VS {self.context.enemy.name} ⚔️")
        print("="*60)
        
        # 显示敌人信息
        enemy = self.context.enemy
        print(f"\n👹 敌人: {enemy.name} (等级 {enemy.level})")
        print(f"❤️ 生命值: {enemy.hp}/{enemy.max_hp}")
        if hasattr(enemy, 'mp'):
            print(f"🔮 法力值: {enemy.mp}/{enemy.max_mp}")
        
        # 显示技能信息
        if hasattr(enemy, 'skills') and enemy.skills:
            print(f"⚔️ 技能数量: {len(enemy.skills)}")
            print(f"🎯 攻击模式: {enemy.attack_pattern.name if hasattr(enemy, 'attack_pattern') else '普通'}")
    
    def display_turn_start(self):
        """显示回合开始信息"""
        print(f"\n🔄 --- 第{self.context.turn_count}回合 --- 🔄")
        
        # 显示双方状态
        player = self.context.player
        enemy = self.context.enemy
        
        print(f"🧑‍🎤 {player.name}: ❤️ {player.hp}/{player.max_hp}, 🔮 {player.mp}/{player.max_mp}")
        print(f"👹 {enemy.name}: ❤️ {enemy.hp}/{enemy.max_hp}", end="")
        if hasattr(enemy, 'mp'):
            print(f", 🔮 {enemy.mp}/{enemy.max_mp}")
        else:
            print()
        
        # 显示状态效果
        self._display_status_effects()
    
    def _display_status_effects(self):
        """显示状态效果"""
        player_effects = self.context.get_status_effects("player")
        enemy_effects = self.context.get_status_effects("enemy")
        
        if player_effects:
            effects_str = ", ".join([f"{effect}({duration}回合)" 
                                   for effect, duration in player_effects.items()])
            print(f"🧑‍🎤 状态效果: {effects_str}")
        
        if enemy_effects:
            effects_str = ", ".join([f"{effect}({duration}回合)" 
                                   for effect, duration in enemy_effects.items()])
            print(f"👹 状态效果: {effects_str}")
    
    def display_player_actions(self) -> int:
        """显示玩家可选行动并返回选择"""
        print("\n🎮 你的回合:")
        print("1. 🗡️ 普通攻击")
        print("2. 🛡️ 防御 (减少50%伤害)")
        
        # 显示可用技能
        usable_skills = [s for s in self.context.player.skills 
                        if s.can_use(self.context.player)]
        
        for idx, skill in enumerate(usable_skills, start=3):
            cooldown_info = f" ⏰:{skill.current_cooldown}" if skill.current_cooldown else ""
            print(f"{idx}. ✨ {skill.name} (🔮:{skill.mp_cost}){cooldown_info}")
        
        # 显示物品选项
        print(f"{len(usable_skills) + 3}. 🧪 使用物品")
        
        # 如果可以逃跑
        if self.context.config.allow_flee:
            print(f"{len(usable_skills) + 4}. 🏃 逃跑")
        
        # 获取玩家选择
        while True:
            try:
                max_choice = len(usable_skills) + 4 if self.context.config.allow_flee else len(usable_skills) + 3
                choice = int(input("选择行动: "))
                if 1 <= choice <= max_choice:
                    return choice
                else:
                    print(f"❗ 请输入1-{max_choice}之间的数字!")
            except ValueError:
                print("❗ 请输入有效数字!")
    
    def display_action_result(self, actor: str, action: BattleAction, 
                            target: str, damage: int = 0, heal: int = 0, 
                            effect: Optional[str] = None, message: str = ""):
        """显示行动结果"""
        if message:
            print(message)
        
        if damage > 0:
            print(f"💥 {actor}对{target}造成了{damage}点伤害！")
        if heal > 0:
            print(f"💚 {actor}恢复了{heal}点生命值！")
        if effect:
            print(f"✨ {target}获得了{effect}效果！")
    
    def display_battle_end(self, result: str):
        """显示战斗结束信息"""
        print("\n" + "="*40)
        
        if result == "victory":
            print("🎉 胜利！")
            rewards = self.context.rewards
            if rewards.experience > 0:
                print(f"✨ 获得{rewards.experience}点经验值！")
            if rewards.gold > 0:
                print(f"💰 获得{rewards.gold}金币！")
            if rewards.items:
                items_str = ", ".join(rewards.items)
                print(f"🎁 获得物品: {items_str}")
                
        elif result == "defeat":
            print("💀 败北...")
        elif result == "flee":
            print("🏃 成功逃跑！")
        elif result == "draw":
            print("🤝 平局！")
            
        print("="*40)
    
    def display_battle_log(self):
        """显示完整的战斗日志"""
        if not self.context.battle_log:
            print("📋 暂无战斗记录")
            return
            
        print("\n📋 --- 战斗日志 ---")
        for log in self.context.battle_log:
            print(f"[回合{log.turn}] {log.message}")
    
    def get_skill_choice(self, skills: List) -> Optional[int]:
        """获取技能选择"""
        if not skills:
            return None
            
        print("\n🎯 选择技能:")
        for idx, skill in enumerate(skills, start=1):
            print(f"{idx}. {skill.name} (消耗: {skill.mp_cost} MP)")
            
        while True:
            try:
                choice = int(input("选择技能: "))
                if 1 <= choice <= len(skills):
                    return choice - 1
                else:
                    print(f"❗ 请输入1-{len(skills)}之间的数字!")
            except ValueError:
                print("❗ 请输入有效数字!")
    
    def get_item_choice(self, items: List) -> Optional[int]:
        """获取物品选择"""
        if not items:
            print("🎒 没有可用物品")
            return None
            
        print("\n🧪 选择物品:")
        for idx, item in enumerate(items, start=1):
            print(f"{idx}. {item['name']} x{item['quantity']}")
            
        while True:
            try:
                choice = int(input("选择物品: "))
                if 1 <= choice <= len(items):
                    return choice - 1
                else:
                    print(f"❗ 请输入1-{len(items)}之间的数字!")
            except ValueError:
                print("❗ 请输入有效数字!")
    
    def confirm_action(self, action_desc: str) -> bool:
        """确认行动"""
        while True:
            choice = input(f"{action_desc} (y/n): ").lower().strip()
            if choice in ['y', 'yes']:
                return True
            elif choice in ['n', 'no']:
                return False
            else:
                print("❗ 请输入 y 或 n")
