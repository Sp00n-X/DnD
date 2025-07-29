from characters.base_character import BaseCharacter
from characters.equipments.base_equipments import DamageEffect, DamageType, EquipSlot, PercentModifier, Stat, Weapon
from enemy.bosses.boss_manager import BossManager
from enemy.bosses.floor_boss import FloorBoss

import random
from typing import Dict, List, Optional, Any
from enum import Enum
from dataclasses import dataclass

class CharacterClass(Enum):
    WARRIOR = "战士"
    MAGE = "法师"
    ROGUE = "盗贼"
    CLERIC = "牧师"

class PlayerCharacter(BaseCharacter):
    """玩家角色类"""
    def __init__(self, name: str, character_class: CharacterClass):
        super().__init__(name, level=1)
        self.character_class = character_class
        self.current_floor = 1
        self.defeated_bosses = set()  # 已击败的层主
        
        # 根据职业设置初始属性
        self._set_class_attributes()
    
    def _set_class_attributes(self):
        """基于职业设置属性"""
        if self.character_class == CharacterClass.WARRIOR:
            self.base_hp += 20
            self.base_attack += 5
            self.base_defense += 3
        elif self.character_class == CharacterClass.MAGE:
            self.base_mp += 30
            self.base_spell_power += 5
            self.base_attack -= 2
            from characters.skills.mage_skills import Fireball, FrostBolt, DefenseBoost, ManaHeal
            from characters.equipments.mage.mage_weapons import FirelordStaff
            from characters.equipments.mage.mage_armors import ArcaneRobes
            
            self.skills.extend([
                Fireball(),
                FrostBolt(),
                DefenseBoost(),
                ManaHeal()
                ])
            
            # 为法师初始化装备：火焰之王法杖和奥术长袍
            firelord_staff = FirelordStaff()
            arcane_robes = ArcaneRobes()
            
            # 装备武器和防具
            self.equip(firelord_staff)
            self.equip(arcane_robes)
            
        elif self.character_class == CharacterClass.ROGUE:
            self.base_attack += 3
            self.base_defense += 1
            self.base_hp += 10
        elif self.character_class == CharacterClass.CLERIC:
            self.base_hp += 15
            self.base_mp += 20
            self.base_spell_power += 3
            self.base_defense += 2
            
        # 重新计算属性
        self.recalc_stats()
        self.hp = self.max_hp
        self.mp = self.max_mp

class Castle:
    """城堡类"""
    def __init__(self):
        self.boss_manager = BossManager()
        self.floors = self.boss_manager.get_total_floors()
    
    def get_boss(self, floor: int) -> Optional[FloorBoss]:
        """获取指定层的层主"""
        return self.boss_manager.get_boss(floor)
    
    def can_access_floor(self, current_floor: int, target_floor: int) -> bool:
        """检查是否可以进入目标层"""
        return abs(current_floor - target_floor) == 1 and 1 <= target_floor <= self.floors

class GameEngine:
    """游戏引擎"""
    def __init__(self):
        self.player: Optional[PlayerCharacter] = None
        self.castle = Castle()
        self.game_running = True
    
    def start_game(self):
        """开始游戏"""
        print("=" * 50)
        print("🏰 欢迎来到神秘城堡! 🏰")
        print("=" * 50)
        
        self.create_character()
        self.main_game_loop()
    
    def create_character(self):
        """角色创建"""
        print("\n🎭 --- 角色创建 --- 🎭")
        name = input("请输入角色名字: ").strip()
        if not name:
            name = "冒险者"
        
        print("\n⚔️ 选择职业:")
        for i, char_class in enumerate(CharacterClass, 1):
            emoji = "⚔️" if char_class == CharacterClass.WARRIOR else \
                   "🔮" if char_class == CharacterClass.MAGE else \
                   "🗡️" if char_class == CharacterClass.ROGUE else "✨"
            print(f"{i}. {emoji} {char_class.value}")
        
        while True:
            try:
                choice = int(input("请选择职业 (1-4): "))
                if 1 <= choice <= 4:
                    selected_class = list(CharacterClass)[choice - 1]
                    break
                else:
                    print("❗ 请输入1-4之间的数字!")
            except ValueError:
                print("❗ 请输入有效数字!")
        
        self.player = PlayerCharacter(name, selected_class)
        print(f"\n🎉 角色创建成功! {name} - {selected_class.value}")
        self.show_character_status()
    
    def main_game_loop(self):
        """主游戏循环"""
        while self.game_running and self.player.is_alive():
            self.show_current_location()
            self.show_menu()
            
            choice = input("\n请选择操作: ").strip()
            
            if choice == "1":
                self.move_floors()
            elif choice == "2":
                self.challenge_boss()
            elif choice == "3":
                self.show_character_status()
            elif choice == "4":
                self.show_castle_status()
            elif choice == "5":
                self.rest()
            elif choice == "0":
                self.quit_game()
            else:
                print("无效选择，请重新输入!")
        
        if not self.player.is_alive():
            print("\n💀 游戏结束！你的冒险到此为止...")
            print("🌟 感谢你的精彩冒险！")
    
    def show_current_location(self):
        """显示当前位置"""
        floor = self.player.current_floor
        boss = self.castle.get_boss(floor)
        boss_status = "✅ 已击败" if floor in self.player.defeated_bosses else "❌ 未挑战"
        
        print(f"\n" + "=" * 30)
        print(f"📍 当前位置: 城堡第{floor}层")
        print(f"👹 层主: {boss.name} ({boss_status})")
        print("=" * 30)
    
    def show_menu(self):
        """显示菜单"""
        print("\n🎯 可选操作:")
        print("1. 🚶 移动到其他层")
        print("2. ⚔️ 挑战层主")
        print("3. 📊 查看角色状态")
        print("4. 🏰 查看城堡状态")
        print("5. 🛌 休息恢复")
        print("0. 🚪 退出游戏")
    
    def move_floors(self):
        """移动到其他层"""
        current = self.player.current_floor
        available_floors = []
        
        if current > 1:
            available_floors.append(current - 1)
        if current < self.castle.floors:
            available_floors.append(current + 1)
        
        if not available_floors:
            print("❌ 没有可移动的层数!")
            return
        
        print(f"\n🗺️ 可移动到的层数: {available_floors}")
        
        try:
            target = int(input("请选择目标层数: "))
            if target in available_floors:
                self.player.current_floor = target
                print(f"✅ 成功移动到第{target}层! 🎉")
                
                # 移动后立即遇到层主
                boss = self.castle.get_boss(target)
                if target not in self.player.defeated_bosses:
                    print(f"\n⚠️ 你遇到了层主: {boss.name}!")
                    print("⚔️ 准备战斗!")
            else:
                print("❌ 无法移动到该层!")
        except ValueError:
            print("❗ 请输入有效数字!")
    
    def challenge_boss(self):
        """挑战层主"""
        floor = self.player.current_floor
        
        if floor in self.player.defeated_bosses:
            print("⚠️ 该层层主已被击败!")
            return
        
        boss = self.castle.get_boss(floor)
        print(f"\n⚔️ 开始挑战层主: {boss.name}!")
        
        self.battle(boss)
    
    def battle(self, boss: FloorBoss):
        """战斗系统 - 集成新Boss技能系统"""
        print(f"\n{'='*40}")
        print(f"⚔️ 战斗开始: {self.player.name} VS {boss.name} ⚔️")
        print('=' * 40)

        turn = 1
        while self.player.is_alive() and boss.is_alive():
            print(f"\n🔄 --- 第{turn}回合 --- 🔄")
            print(f"🧑‍🎤 玩家: ❤️ {self.player.hp}/{self.player.max_hp}, 🔮 {self.player.mp}/{self.player.max_mp}")
            print(f"👹 {boss.name}: ❤️ {boss.hp}/{boss.max_hp}, 🔮 {boss.mp}/{boss.max_mp}")
            
            # 显示Boss技能状态
            if boss.skills:
                print(f"🎯 Boss攻击模式: {boss.attack_pattern.name}")
                usable_skills = [s for s in boss.skills if s.can_use(boss)]
                if usable_skills:
                    print(f"⚡ Boss可用技能: {len(usable_skills)}个")

            # ---------- 玩家回合 ----------
            # 1. 列出可用行动
            print("\n🎮 你的回合:")
            print("1. 🗡️ 普通攻击")
            print("2. 🛡️ 防御 (减少50%伤害)")
            usable_skills = [s for s in self.player.skills if s.can_use(self.player)]
            for idx, sk in enumerate(usable_skills, start=3):
                print(f"{idx}. ✨ {sk.name} (🔮:{sk.mp_cost})" +(f" ⏰:{sk.current_cooldown}" if sk.current_cooldown else ""))

            # 2. 读取玩家选择
            while True:
                try:
                    action = int(input("选择行动: "))
                    if 1 <= action <= 2 + len(usable_skills):
                        break
                except ValueError:
                    pass
                print("❗ 无效输入，请重选！")

            # 3. 执行玩家行动
            damage_reduction = 1.0     # 默认不防御
            if action == 1:
                dmg = max(1, self.player.attack - boss.defense)
                boss.take_damage(dmg, DamageType.PHYSICAL)
                print(f"💥 你对{boss.name}造成了{dmg}点伤害！")
                # 触发装备效果（普通攻击）
                self._trigger_equipment_effects(self.player, boss)
            elif action == 2:
                damage_reduction = 0.5
                print("🛡️ 你进入了防御姿态！")
            else:  # 使用技能
                skill = usable_skills[action - 3]
                result = self.player.use_skill(skill.name, target=boss)
                print(result["message"])
                if result["success"]:
                    # 触发装备效果（技能攻击）
                    self._trigger_equipment_effects(self.player, boss)

            # Boss 已死则提前结束
            if not boss.is_alive():
                break

            # ---------- Boss 回合 ----------
            print(f"\n👹 {boss.name}的回合:")
            
            # Boss选择并执行动作
            action = boss.select_action(self.player)
            result = boss.execute_action(action)
            
            print(result['message'])
            if 'damage' in result:
                damage = int(result['damage'] * damage_reduction)
                print(f"💥 {boss.name}造成了{damage}点伤害！")
            if 'heal_amount' in result:
                print(f"💚 {boss.name}恢复了{result['heal_amount']}点生命值！")
            if result.get('burn_applied'):
                print("🔥 你被灼烧了！")
            if result.get('poison_applied'):
                print("☠️ 你中毒了！")
            if result.get('stun_applied'):
                print("💫 你被眩晕了，下回合无法行动！")

            turn += 1

        # ---------- 战斗结果 ----------
        print("\n" + "=" * 40)
        if self.player.is_alive():
            print("🎉 胜利！")
            self.player.defeated_bosses.add(self.player.current_floor)

            exp_reward = boss.level * 50
            self.player.gain_experience(exp_reward)
            print(f"✨ 获得{exp_reward}点经验值！")

            if len(self.player.defeated_bosses) == self.castle.floors:
                print("\n" + "=" * 50)
                print("🏆 恭喜！你已经征服了整个城堡！")
                print("=" * 50)
                self.game_running = False
        else:
            print("💀 败北...")
        print("=" * 40)
    
    def show_character_status(self):
        """显示角色状态"""
        status = self.player.get_status()
        print(f"\n🎭 --- {self.player.name} ({self.player.character_class.value}) ---")
        for key, value in status.items():
            if key != "name":
                emoji = "❤️" if "hp" in key.lower() else \
                       "🔮" if "mp" in key.lower() else \
                       "⚔️" if "attack" in key.lower() else \
                       "🛡️" if "defense" in key.lower() else \
                       "✨" if "spell" in key.lower() else "📊"
                print(f"{emoji} {key}: {value}")
        print(f"📍 当前层数: {self.player.current_floor}")
        print(f"🏆 已击败层主: {len(self.player.defeated_bosses)}/{self.castle.floors}")
        
        # 显示装备信息
        print("\n🛡️ --- 装备信息 ---")
        for slot, equipment in self.player.equipment.items():
            if equipment:
                print(f"📦 {slot.value}: {equipment.name}")
            else:
                print(f"📦 {slot.value}: 无")
        
        # 显示背包物品
        print("\n🎒 --- 背包物品 ---")
        inventory_items = self.player.inventory.list_items()
        if inventory_items:
            for item in inventory_items:
                print(f"📍 {item['name']} x{item['quantity']}")
        else:
            print("🎒 背包为空")
    
    def show_castle_status(self):
        """显示城堡状态"""
        print(f"\n🏰 --- 城堡状态 ---")
        for floor in range(1, self.castle.floors + 1):
            boss = self.castle.get_boss(floor)
            status = "✅ 已击败" if floor in self.player.defeated_bosses else "❌ 未击败"
            current = " 📍 当前位置" if floor == self.player.current_floor else ""
            print(f"🏰 第{floor}层: 👹 {boss.name} (等级{boss.level}) {status}{current}")
            
            # 显示Boss技能信息
            if boss.skills:
                print(f"    ⚔️ 技能: {len(boss.skills)}个 | 🎯 攻击模式: {boss.attack_pattern.name}")
    
    def rest(self):
        """休息恢复"""
        if self.player.hp == self.player.max_hp and self.player.mp == self.player.max_mp:
            print("😊 你的状态已经很好了!")
            return
        
        heal_amount = self.player.max_hp // 4
        mp_amount = self.player.max_mp // 4
        
        self.player.heal(heal_amount)
        self.player.restore_mp(mp_amount)
        
        print(f"💤 休息后恢复了❤️ {heal_amount}点生命值和🔮 {mp_amount}点法力值!")
    
    def _trigger_equipment_effects(self, attacker, target):
        """触发装备效果（在攻击后调用）"""
        # 遍历所有装备槽
        for equipment in attacker.equipment.values():
            if equipment and hasattr(equipment, 'effects'):
                for effect in equipment.effects:
                    if hasattr(effect, 'on_hit'):
                        # 根据效果类型进行判断和处理
                        effect_class_name = effect.__class__.__name__
                        
                        # 处理DamageEffect
                        if effect_class_name == 'DamageEffect':
                            # 计算额外伤害
                            scale_value = getattr(attacker, effect.scale_stat.name.lower(), 0)
                            extra_damage = int(scale_value * effect.coefficient)
                            if extra_damage > 0:
                                target.take_damage(extra_damage, effect.dmg_type)
                                print(f"[{equipment.name}] 追加 {extra_damage} {effect.dmg_type.name} 伤害!")
                        
                        # 处理ManaSurgeEffect
                        elif effect_class_name == 'ManaSurgeEffect':
                            import random
                            if random.random() < effect.chance:
                                attacker.mp = min(attacker.mp + effect.mana_restore, attacker.max_mp)
                                print(f"[{equipment.name}] 恢复了 {effect.mana_restore} 点法力值!")
                        
                        # 处理ArcaneExplosionEffect
                        elif effect_class_name == 'ArcaneExplosionEffect':
                            import random
                            if random.random() < effect.chance:
                                damage = int(attacker.spell_power * effect.damage_scale)
                                target.take_damage(damage, DamageType.MAGICAL)
                                print(f"[{equipment.name}] 引发奥术爆炸，造成 {damage} 点额外魔法伤害!")
                        
                        # 其他效果直接触发
                        else:
                            effect.on_hit(attacker, target)

    def quit_game(self):
        """退出游戏"""
        print("👋 感谢游玩! 期待你的下次冒险!")
        self.game_running = False

def main():
    """主函数"""
    game = GameEngine()
    game.start_game()

if __name__ == "__main__":
    main()
