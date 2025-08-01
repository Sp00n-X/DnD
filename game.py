"""
主游戏入口 - 集成增强地图系统和角色保存功能
"""

import os
import sys
import time
from typing import Optional

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from characters.base_character import CharacterClass
from map_system.enhanced_map_system import MapNavigator
from save_system import SaveSystem

class GameLauncher:
    """游戏启动器 - 提供直观的游戏入口"""
    
    def __init__(self):
        self.save_system = SaveSystem()
    
    def start(self):
        """启动游戏"""
        print("\n" + "="*60)
        print("🏰 欢迎来到世界! 🏰")
        print("="*60)
        print("🎮 一个充满魔法、战斗与探索的奇幻世界")
        print("="*60)
        
        while True:
            self.show_main_menu()
            choice = input("\n请选择: ").strip()
            
            if choice == "1":
                self.new_game()
            elif choice == "2":
                self.load_game()
            elif choice == "3":
                self.show_saved_games()
            elif choice == "4":
                self.delete_character()
            elif choice == "0":
                self.exit_game()
            else:
                print("❗ 无效选择，请重新输入！")
    
    def show_main_menu(self):
        """显示主菜单"""
        print("\n" + "-"*40)
        print("🎯 主菜单:")
        print("1. 🆕 开始新游戏")
        print("2. 📂 加载游戏")
        print("3. 💾 查看存档")
        print("4. 🗑️ 删除角色")
        print("0. 🚪 退出游戏")
        print("-"*40)
    
    def new_game(self):
        """开始新游戏"""
        print("\n🎭 创建你的冒险者")
        print("=" * 40)
        
        # 获取角色名字
        name = input("请输入角色名字: ").strip()
        if not name:
            name = "冒险者"
        
        # 检查角色名是否已存在
        if self.save_system.character_exists(name):
            print(f"❌ 角色 '{name}' 已存在！")
            choice = input("是否覆盖？(y/N): ").strip().lower()
            if choice != 'y':
                return
        
        # 选择职业
        print("\n⚔️ 选择你的职业:")
        classes = list(CharacterClass)
        for i, cls in enumerate(classes, 1):
            emoji = "⚔️" if cls.value == "战士" else \
                   "🔮" if cls.value == "法师" else \
                   "🗡️" if cls.value == "盗贼" else "✨"
            print(f"{i}. {emoji} {cls.value}")
        
        while True:
            try:
                choice = int(input("请选择职业 (1-4): "))
                if 1 <= choice <= len(classes):
                    selected_class = classes[choice - 1]
                    break
                else:
                    print("❗ 请输入有效数字!")
            except ValueError:
                print("❗ 请输入数字!")
        
        # 启动增强地图系统
        print(f"\n✅ 角色创建成功！")
        print(f"🎭 名字: {name}")
        print(f"⚔️ 职业: {selected_class.value}")
        print("\n🗺️ 正在进入艾兰提亚世界...")
        time.sleep(1)
        
        # 启动新的地图导航系统
        navigator = MapNavigator()
        navigator.player_name = name
        navigator.player_class = selected_class
        navigator.save_system = self.save_system  # 传递保存系统
        navigator.start()
    
    def load_game(self):
        """加载游戏"""
        saved_games = self.save_system.list_saved_characters()
        
        if not saved_games:
            print("\n❌ 没有找到存档！")
            return
        
        print("\n📂 选择要加载的角色:")
        print("-" * 40)
        
        for i, game in enumerate(saved_games, 1):
            progress = f"{game['defeated_bosses']}/{game['total_bosses']}"
            print(f"{i}. {game['name']} - {game['character_class']} (Lv.{game['level']})")
            print(f"   📍 第{game['current_floor']}层 | 🏆 进度: {progress} | 💾 {game['last_saved']}")
        
        while True:
            try:
                choice = int(input("\n选择角色 (0返回): "))
                if choice == 0:
                    return
                if 1 <= choice <= len(saved_games):
                    selected_game = saved_games[choice - 1]
                    name = selected_game['name']
                    
                    # 加载角色
                    character = self.save_system.load_character(name)
                    if character:
                        print(f"\n✅ 成功加载角色: {name}")
                        print("🗺️ 正在进入艾兰提亚世界...")
                        time.sleep(1)
                        
                        # 启动新的地图导航系统并加载角色
                        navigator = MapNavigator()
                        navigator.player = character
                        navigator.start()
                        return
                    else:
                        print("❌ 加载失败！")
                        return
                else:
                    print("❗ 请输入有效数字!")
            except ValueError:
                print("❗ 请输入数字!")
    
    def show_saved_games(self):
        """显示已保存的游戏"""
        saved_games = self.save_system.list_saved_characters()
        
        if not saved_games:
            print("\n💾 没有存档")
            return
        
        print("\n💾 已保存的角色:")
        print("=" * 60)
        
        for game in saved_games:
            progress = f"{game['defeated_bosses']}/{game['total_bosses']}"
            print(f"🎭 {game['name']} - {game['character_class']} (Lv.{game['level']})")
            print(f"   📍 当前层数: {game['current_floor']}")
            print(f"   🏆 进度: {progress}")
            print(f"   💾 最后保存: {game['last_saved']}")
            print("-" * 40)
    
    def delete_character(self):
        """删除角色"""
        saved_games = self.save_system.list_saved_characters()
        
        if not saved_games:
            print("\n❌ 没有找到存档！")
            return
        
        print("\n🗑️ 选择要删除的角色:")
        print("-" * 40)
        
        for i, game in enumerate(saved_games, 1):
            print(f"{i}. {game['name']} - {game['character_class']} (Lv.{game['level']})")
        
        while True:
            try:
                choice = int(input("\n选择要删除的角色 (0返回): "))
                if choice == 0:
                    return
                if 1 <= choice <= len(saved_games):
                    selected_game = saved_games[choice - 1]
                    name = selected_game['name']
                    
                    confirm = input(f"确定要删除 '{name}' 吗？(y/N): ").strip().lower()
                    if confirm == 'y':
                        if self.save_system.delete_character(name):
                            print(f"✅ 已删除角色: {name}")
                        else:
                            print("❌ 删除失败！")
                    return
                else:
                    print("❗ 请输入有效数字!")
            except ValueError:
                print("❗ 请输入数字!")
    
    def exit_game(self):
        """退出游戏"""
        print("\n👋 感谢游玩！期待你的下次冒险！")
        sys.exit(0)

def main():
    """主入口点"""
    try:
        launcher = GameLauncher()
        launcher.start()
    except KeyboardInterrupt:
        print("\n\n👋 感谢游玩！期待你的下次冒险！")
        sys.exit(0)

if __name__ == "__main__":
    main()
