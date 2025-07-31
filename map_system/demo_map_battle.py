"""地图系统与战斗系统集成的演示程序"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from enhanced_map_system import EnhancedAetheriaMap
from battle_integration import MapBattleSystem
from main_process import PlayerCharacter, CharacterClass

class MapBattleDemo:
    """地图战斗集成演示"""
    
    def __init__(self):
        self.player = None
        self.map = None
        self.battle_system = None
        
    def setup_demo(self):
        """设置演示环境"""
        print("🎮 设置地图战斗演示环境...")
        
        # 创建玩家
        print("\n🎭 创建角色...")
        name = input("请输入角色名字: ").strip() or "冒险者"
        
        print("\n⚔️ 选择职业:")
        print("1. ⚔️ 战士")
        print("2. 🔮 法师")
        print("3. 🗡️ 盗贼")
        print("4. ✨ 牧师")
        
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
        self.map = EnhancedAetheriaMap()
        
        # 直接移动到翡翠之森（洛希尔）
        self.map.current_location = "翡翠之森"
        self.map.current_region = "翡翠之森"
        self.map.visited_locations.add("翡翠之森")
        
        self.battle_system = MapBattleSystem(self.player)
        
        print(f"\n✅ 角色创建成功！{name} - {selected_class.value}")
        print(f"📊 等级: {self.player.level}")
        print(f"❤️ 生命值: {self.player.hp}/{self.player.max_hp}")
        print(f"📍 起始位置: 翡翠之森（洛希尔）")
        
    def run_demo(self):
        """运行演示"""
        if not self.player:
            self.setup_demo()
        
        print("\n" + "="*60)
        print("🗺️ 地图战斗集成演示")
        print("="*60)
        print("在地图探索过程中，你可能会遇到随机敌人！")
        print("使用 'explore' 命令来探索当前区域。")
        print("使用 'status' 查看角色状态。")
        print("使用 'quit' 退出演示。")
        
        while True:
            try:
                # 显示当前位置
                if self.map.current_sub_region:
                    location_info = self.map._get_sub_region_info()
                    current_name = location_info.get('name', '未知')
                    print(f"\n📍 当前位置: {self.map.current_location} - {current_name}")
                else:
                    print(f"\n📍 当前位置: {self.map.current_location}")
                
                # 获取用户输入
                command = input("\n> ").strip().lower()
                
                if command in ['quit', 'exit', 'q']:
                    break
                    
                elif command == 'status':
                    self.show_player_status()
                    
                elif command == 'explore':
                    self.explore_current_area()
                    
                elif command == 'boss':
                    self.challenge_boss()
                    
                elif command == 'move':
                    self.move_to_area()
                    
                elif command == 'help':
                    self.show_help()
                    
                else:
                    print("❗ 未知命令。输入 'help' 查看可用命令。")
                    
            except KeyboardInterrupt:
                print("\n\n👋 感谢使用地图战斗演示！")
                break
    
    def show_player_status(self):
        """显示玩家状态"""
        print(f"\n🎭 {self.player.name} ({self.player.character_class.value})")
        print(f"📊 等级: {self.player.level}")
        print(f"❤️ 生命值: {self.player.hp}/{self.player.max_hp}")
        print(f"🔮 法力值: {self.player.mp}/{self.player.max_mp}")
        print(f"⚔️ 攻击力: {self.player.attack}")
        print(f"🛡️ 防御力: {self.player.defense}")
        
        # 显示已击败的Boss
        if hasattr(self.player, 'defeated_bosses'):
            print(f"🏆 已击败Boss: {len(self.player.defeated_bosses)}")
    
    def explore_current_area(self):
        """探索当前区域"""
        region = self.map.current_location
        
        # 如果在子区域中，使用子区域名称
        sub_region = None
        if self.map.current_sub_region:
            sub_region_info = self.map._get_sub_region_info()
            sub_region = sub_region_info.get('name', '')
        
        print(f"\n🗺️ 开始探索 {region}" + (f" - {sub_region}" if sub_region else ""))
        
        # 触发战斗检查
        result = self.battle_system.check_random_encounter(region, sub_region)
        
        if not result:
            print("✅ 本次探索没有遇到敌人。")
        elif result == "victory":
            print("🎉 战斗胜利！")
        elif result == "defeat":
            print("💀 战斗失败！")
        elif result == "flee":
            print("🏃 成功逃脱！")
    
    def challenge_boss(self):
        """挑战Boss"""
        print("\n👹 挑战Boss")
        print("=" * 30)
        
        # 简单选择Boss层数
        try:
            floor = int(input("请输入Boss层数 (1-5): "))
            if 1 <= floor <= 5:
                result = self.battle_system.trigger_boss_battle(floor)
                print(f"Boss战结果: {result}")
            else:
                print("❗ 请输入1-5之间的数字")
        except ValueError:
            print("❗ 请输入有效数字")
    
    def move_to_area(self):
        """移动到指定区域"""
        print("\n🗺️ 可前往的区域:")
        available = self.map.get_available_moves()
        
        for i, move in enumerate(available, 1):
            print(f"{i}. {move}")
        
        try:
            choice = int(input("\n选择要前往的区域 (输入数字): "))
            if 1 <= choice <= len(available):
                selected = available[choice - 1]
                
                # 处理不同类型的移动
                if selected.startswith("探索："):
                    sub_region = selected[3:]  # 去掉"探索："前缀
                    if self.map.enter_sub_region(sub_region):
                        print(f"✅ 已进入子区域：{sub_region}")
                    else:
                        print("❌ 无法进入该子区域")
                elif selected.startswith("返回"):
                    if self.map.exit_sub_region():
                        print("✅ 已返回主区域")
                else:
                    if self.map.move_to(selected):
                        print(f"✅ 已前往：{selected}")
                    else:
                        print("❌ 无法前往该区域")
            else:
                print("❗ 无效选择")
        except ValueError:
            print("❗ 请输入有效数字")
    
    def show_help(self):
        """显示帮助信息"""
        print("""
🎮 地图战斗演示命令：
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
explore     - 探索当前区域，可能触发随机战斗
status      - 查看角色状态
boss        - 挑战指定层数的Boss
move        - 移动到指定区域
help        - 显示此帮助信息
quit/exit   - 退出演示
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 使用提示：
• 使用 'explore' 在当前区域探索，可能遇到随机敌人
• 使用 'move' 在不同区域间移动
• 使用 'boss' 挑战Boss敌人
• 战斗胜利可获得经验值和金币
        """)

def main():
    """主函数"""
    demo = MapBattleDemo()
    demo.run_demo()

if __name__ == "__main__":
    main()
