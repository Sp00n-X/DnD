#!/usr/bin/env python3
"""
增强版艾兰提亚世界地图系统
支持主区域和子区域导航，集成战斗系统
"""

import json
import os
import sys
import random
from typing import Dict, List, Tuple, Optional, Any
import cmd
import importlib

# 添加模块路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from regions import (
    get_sub_regions, 
    get_region_module,
    SUB_REGION_CLASSES,
    get_sub_region_class
)

# 战斗系统集成
from battle_system import BattleEngine, BattleConfig
from battle_integration import BattleEncounterManager
from characters.base_character import BaseCharacter
from characters.base_character import CharacterClass
from characters.player_character import PlayerCharacter

class EnhancedAetheriaMap:
    """增强版地图系统，支持子区域导航"""
    
    def __init__(self):
        self.current_location = "裂星集"  # 起始点
        self.current_sub_region = None   # 当前子区域
        self.current_region = None       # 当前主区域
        self.visited_locations = {"裂星集"}
        self.visited_sub_regions = set()
        self.map_data = self._initialize_world()
        
    def _initialize_world(self) -> Dict:
        """初始化世界地图"""
        return {
            "裂星集": {
                "description": "中立城寨，四国交汇的冒险者聚集地",
                "connections": ["齿轮之城", "秘法之乡", "翡翠之森", "天穹武朝"],
                "type": "hub",
                "lore": "四国轨道/航线/商路在此交汇，中立城寨聚集冒险者、走私客、以太黑市",
                "coordinates": (0, 0),
                "level_range": "1-20",
                "has_sub_regions": False
            },
            "齿轮之城": {
                "description": "阿斯图里亚 - 云层都市，真空管科技巅峰",
                "connections": ["裂星集"],
                "type": "city",
                "lore": "1960-70年代地球科技水平，真空管+仿生学，海拔3-6km",
                "coordinates": (-2, 1),
                "level_range": "5-18",
                "has_sub_regions": True,
                "sub_regions": get_sub_regions("齿轮之城")
            },
            "秘法之乡": {
                "description": "赛林塔 - 九座倒悬塔构成的魔法圣地",
                "connections": ["裂星集"],
                "type": "magical",
                "lore": "阶梯式以太科学，1-9阶官方认证，真空管阵列+星图运算",
                "coordinates": (2, 1),
                "level_range": "1-20",
                "has_sub_regions": True,
                "sub_regions": get_sub_regions("秘法之乡")
            },
            "翡翠之森": {
                "description": "洛希尔 - 精灵的翡翠森林，800年寿命的奥秘",
                "connections": ["裂星集"],
                "type": "forest",
                "lore": "非人精灵，四叶脑+800年寿命，情感淡薄，敬畏自然循环",
                "coordinates": (-1, -2),
                "level_range": "5-20",
                "has_sub_regions": True,
                "sub_regions": get_sub_regions("翡翠之森")
            },
            "天穹武朝": {
                "description": "龙阙 - 九宫格山水构成的武道圣地",
                "connections": ["裂星集"],
                "type": "martial",
                "lore": "真气=以太×经络×意志，官方9阶度量，巨构即基建",
                "coordinates": (1, -2),
                "level_range": "5-20",
                "has_sub_regions": True,
                "sub_regions": get_sub_regions("天穹武朝")
            }
        }
    
    def get_current_location_info(self) -> Dict:
        """获取当前位置详细信息"""
        if self.current_sub_region:
            # 在子区域中
            return self._get_sub_region_info()
        else:
            # 在主区域或裂星集
            location = self.map_data[self.current_location]
            return {
                "name": self.current_location,
                "description": location["description"],
                "type": location["type"],
                "connections": location["connections"],
                "lore": location.get("lore", ""),
                "level_range": location.get("level_range", "1-20"),
                "has_sub_regions": location.get("has_sub_regions", False),
                "sub_regions": location.get("sub_regions", [])
            }
    
    def _get_sub_region_info(self) -> Dict:
        """获取子区域详细信息"""
        if not self.current_sub_region:
            return {}
        
        # 动态导入子区域类
        region_module = get_region_module(self.current_region)
        if not region_module:
            return {}
        
        try:
            module = importlib.import_module(f'regions.{region_module}.sub_regions')
            sub_region_class = getattr(module, self.current_sub_region)
            instance = sub_region_class()
            
            return {
                "name": instance.name,
                "description": instance.description,
                "type": "sub_region",
                "level_range": f"{instance.level_range[0]}-{instance.level_range[1]}",
                "enemies": instance.enemies,
                "loot": instance.loot,
                "features": instance.features,
                "connections": instance.connections,
                "parent_region": self.current_region
            }
        except (ImportError, AttributeError) as e:
            print(f"Error loading sub region: {e}")
            return {}
    
    def move_to(self, destination: str) -> bool:
        """移动到主区域"""
        if destination not in self.map_data:
            return False
        
        if destination in self.map_data[self.current_location]["connections"]:
            self.current_location = destination
            self.current_region = destination if destination != "裂星集" else None
            self.current_sub_region = None
            self.visited_locations.add(destination)
            return True
        return False
    
    def enter_sub_region(self, sub_region_name: str) -> bool:
        """进入子区域"""
        if not self.current_region or self.current_location != self.current_region:
            return False
        
        available_sub_regions = get_sub_regions(self.current_region)
        if sub_region_name in available_sub_regions:
            class_name = get_sub_region_class(self.current_region, sub_region_name)
            if class_name:
                self.current_sub_region = class_name
                self.visited_sub_regions.add(f"{self.current_region}:{sub_region_name}")
                return True
        return False
    
    def exit_sub_region(self) -> bool:
        """退出子区域，返回主区域"""
        if self.current_sub_region:
            self.current_sub_region = None
            return True
        return False
    
    def get_available_moves(self) -> List[str]:
        """获取可前往的位置"""
        if self.current_sub_region:
            # 在子区域中，可以前往其他连接的子区域或返回主区域
            moves = ["返回" + self.current_region]
            # 添加子区域连接
            sub_connections = self.get_sub_region_connections()
            if sub_connections:
                # 将类名转换为显示名称
                connection_names = []
                for conn in sub_connections:
                    # 从类名获取显示名称
                    region_module = get_region_module(self.current_region)
                    try:
                        module = importlib.import_module(f'regions.{region_module}.sub_regions')
                        sub_region_class = getattr(module, conn)
                        instance = sub_region_class()
                        connection_names.append(instance.name)
                    except:
                        connection_names.append(conn)
                moves.extend(connection_names)
            return moves
        else:
            # 在主区域中
            moves = self.map_data[self.current_location]["connections"].copy()
            # 如果有子区域，添加子区域选项
            if self.map_data[self.current_location].get("has_sub_regions", False):
                sub_regions = self.map_data[self.current_location].get("sub_regions", [])
                moves.extend([f"探索：{sub}" for sub in sub_regions])
            return moves
    
    def get_sub_region_connections(self) -> List[str]:
        """获取子区域间的连接"""
        if not self.current_sub_region or not self.current_region:
            return []
        
        try:
            region_module = get_region_module(self.current_region)
            module = importlib.import_module(f'regions.{region_module}.sub_regions')
            connections = getattr(module, 'SUB_REGION_CONNECTIONS', {})
            return connections.get(self.current_sub_region, [])
        except ImportError:
            return []

class MapNavigator:
    """纯数字选择的地图导航系统"""
    
    def __init__(self):
        self.map = EnhancedAetheriaMap()
        self.player = None
        self.battle_manager = None
        self.save_system = None
        self.player_name = None
        self.player_class = None
        
    def start(self):
        """启动地图导航系统"""
        print("""
╔══════════════════════════════════════════════════════════════╗
║              艾兰提亚世界地图导航系统                        ║
║         纯数字选择，无需输入文字！                           ║
║                                                              ║
║         🎯 输入数字即可导航                                  ║
╚══════════════════════════════════════════════════════════════╝
""")
        if not self.player:
            self.create_character()
        else:
            # 使用已加载的角色
            self.battle_manager = BattleEncounterManager()
            print(f"\n✅ 角色加载成功！")
            print(f"🎭 名字: {self.player.name}")
            print(f"⚔️ 职业: {self.player.character_class.value}")
            print(f"📊 等级: {self.player.level}")
            print(f"❤️ 生命值: {self.player.hp}/{self.player.max_hp}")
            print(f"🔮 法力值: {self.player.mp}/{self.player.max_mp}")
            print("\n🗺️ 欢迎来到艾兰提亚世界！")
            print(f"你现在位于{self.map.current_location}，可以开始你的冒险了。")
        self._main_loop()
    
    def _main_loop(self):
        """主循环"""
        while True:
            try:
                self._display_current_location()
                choice = self._get_user_choice()
                if choice == -1:  # 退出
                    break
                self._process_choice(choice)
            except KeyboardInterrupt:
                print("\n\n👋 感谢使用艾兰提亚地图系统！")
                break
    
    def _display_current_location(self):
        """显示当前位置和选项"""
        print("\n" + "="*60)
        print(f"📍 当前位置: {self.map.current_location}")
        
        if self.map.current_sub_region:
            sub_info = self.map._get_sub_region_info()
            print(f"🏛️ 子区域: {sub_info.get('name', '未知')}")
        
        print("="*60)
        self._display_movement_menu()
    
    def _get_user_choice(self) -> int:
        """获取用户选择"""
        available_moves = self._get_available_moves_list()
        
        if not available_moves:
            print("❌ 没有可用的移动选项")
            return -1
        
        while True:
            try:
                choice = input("\n请选择目的地 (输入数字，或 q 退出): ").strip()
                if choice.lower() in ['q', 'quit', 'exit']:
                    return -1
                if choice.isdigit():
                    num = int(choice)
                    if 1 <= num <= len(available_moves):
                        return num
                    else:
                        print(f"❌ 请输入 1-{len(available_moves)} 之间的数字")
                else:
                    print("❌ 请输入有效数字")
            except KeyboardInterrupt:
                return -1
    
    def _process_choice(self, choice: int):
        """处理用户选择"""
        available_moves = self._get_available_moves_list()
        display_name, action_type, target = available_moves[choice - 1]
        
        if action_type == "return":
            if self.map.exit_sub_region():
                print(f"\n✅ 已返回：{self.map.current_location}")
            else:
                print("\n❌ 无法返回")
        elif action_type == "sub_region":
            if self.map.enter_sub_region(target):
                sub_info = self.map._get_sub_region_info()
                print(f"\n✅ 已进入子区域：{sub_info.get('name', target)}")
            else:
                print(f"\n❌ 无法进入子区域：{target}")
        elif action_type == "main_region":
            if self.map.move_to(target):
                print(f"\n✅ 已前往：{target}")
                if target not in self.map.visited_locations:
                    print(f"🎉 发现新地点：{target}")
            else:
                print(f"\n❌ 无法前往：{target}")
        elif action_type == "explore_sub":
            if self.map.enter_sub_region(target):
                print(f"\n✅ 已进入子区域：{target}")
            else:
                print(f"\n❌ 无法进入子区域：{target}")
        elif action_type == "look":
            self._display_location_details()
        elif action_type == "explore_area":
            self._explore_current_area()
        elif action_type == "status":
            self._display_character_status()
        elif action_type == "rest":
            self._rest_at_safe_area()
        elif action_type == "boss":
            self._challenge_boss()
    
    def _display_movement_menu(self):
        """显示移动菜单"""
        print("\n🎯 移动选项:")
        available_moves = self._get_available_moves_list()
        
        for idx, (display_name, action_type, target) in enumerate(available_moves, 1):
            print(f"{idx}. {display_name}")
    
    def _get_available_moves_list(self) -> List[Tuple[str, str, str]]:
        """获取可用移动选项列表"""
        moves = []
        
        # 添加功能选项
        moves.append(("🗺️ 查看当前位置详情", "look", ""))
        moves.append(("⚔️ 探索当前区域", "explore_area", ""))
        moves.append(("🎭 查看角色状态", "status", ""))
        
        # 所有主区域都可以休息
        if not self.map.current_sub_region:
            moves.append(("😴 休息恢复", "rest", ""))
        
        # 添加战斗相关选项
        moves.append(("👹 挑战Boss", "boss", ""))
        
        if self.map.current_sub_region:
            # 在子区域中
            moves.append(("🔙 返回主区域", "return", self.map.current_region))
            
            # 添加子区域连接
            connections = self.map.get_sub_region_connections()
            if connections:
                for conn in connections:
                    # 将类名转换为显示名称
                    region_module = get_region_module(self.map.current_region)
                    try:
                        module = importlib.import_module(f'regions.{region_module}.sub_regions')
                        sub_region_class = getattr(module, conn)
                        instance = sub_region_class()
                        moves.append((f"🏛️ 前往：{instance.name}", "sub_region", conn))
                    except:
                        moves.append((f"🏛️ 前往：{conn}", "sub_region", conn))
        else:
            # 在主区域中
            # 添加主区域连接
            for conn in self.map.map_data[self.map.current_location]["connections"]:
                moves.append((f"🗺️ 前往：{conn}", "main_region", conn))
            
            # 添加子区域选项
            if self.map.map_data[self.map.current_location].get("has_sub_regions", False):
                sub_regions = self.map.map_data[self.map.current_location].get("sub_regions", [])
                for sub in sub_regions:
                    moves.append((f"🔍 探索：{sub}", "explore_sub", sub))
        
        return moves
    
    def create_character(self):
        """创建角色"""
        print("\n🎭 创建你的冒险者")
        print("=" * 40)
        
        # 获取角色名字
        name = input("请输入角色名字: ").strip()
        if not name:
            name = "冒险者"
        
        # 选择职业
        print("\n⚔️ 选择你的职业:")
        classes = list(CharacterClass)
        for i, cls in enumerate(classes, 1):
            print(f"{i}. {cls.value}")
        
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
        
        # 创建角色
        self.player = PlayerCharacter(name, selected_class)
        self.battle_manager = BattleEncounterManager()
        
        print(f"\n✅ 角色创建成功！")
        print(f"🎭 名字: {name}")
        print(f"⚔️ 职业: {selected_class.value}")
        print(f"📊 等级: {self.player.level}")
        print(f"❤️ 生命值: {self.player.hp}/{self.player.max_hp}")
        print(f"🔮 法力值: {self.player.mp}/{self.player.max_mp}")
        print("\n🗺️ 欢迎来到艾兰提亚世界！")
        print("你现在位于裂星集，可以开始你的冒险了。")

    def calculate_encounter_chance(self, region: str, sub_region: str = None) -> float:
        """计算遭遇概率"""
        # 基础概率
        base_chance = 0.7
        
        # 区域调整
        region_modifiers = {
            "裂星集": 0.0,      # 安全区域
            "齿轮之城": 0.4,    # 城市区域
            "秘法之乡": 0.5,   # 魔法区域
            "翡翠之森": 0.8,    # 森林区域
            "天穹武朝": 0.7    # 武道区域
        }
        
        modifier = region_modifiers.get(region, 0.6)
        
        # 子区域调整
        if sub_region:
            dangerous_subregions = ["苔堡", "远古圣林", "树冠顶层"]
            if any(area in sub_region for area in dangerous_subregions):
                modifier += 0.2
        
        return min(modifier, 1.0)

    def generate_enemy_for_location(self, region: str, sub_region: str = None) -> Optional[BaseCharacter]:
        """为特定位置生成敌人"""
        # 区域敌人映射
        region_enemies = {
            "翡翠之森": {
                "苔阶聚落": ["失控的植物", "暗影精灵"],
                "环居": ["堕落长老", "记忆盗贼"],
                "苔堡": ["苔堡守卫", "议会刺客"],
                "星辉池": ["池水守护者", "星光幻影"],
                "远古圣林": ["远古守卫", "精灵怨灵"]
            },
            "齿轮之城": {
                "工业区": ["机械守卫", "失控机器人"],
                "实验室": ["实验体", "变异科学家"]
            },
            "秘法之乡": {
                "第一塔": ["魔法生物", "失控元素"],
                "星桥": ["星辉守卫", "虚空生物"]
            },
            "天穹武朝": {
                "山门": ["武僧", "门派弟子"],
                "秘境": ["真气兽", "武道幻影"]
            }
        }
        
        # 获取敌人列表
        enemies = []
        if region in region_enemies:
            if sub_region and sub_region in region_enemies[region]:
                enemies = region_enemies[region][sub_region]
            else:
                # 合并所有子区域的敌人
                for sub_enemies in region_enemies[region].values():
                    enemies.extend(sub_enemies)
        
        if not enemies:
            return None
            
        # 随机选择敌人
        enemy_name = random.choice(enemies)
        
        # 根据区域和等级生成敌人
        level_ranges = {
            "翡翠之森": (5, 20),
            "齿轮之城": (5, 18),
            "秘法之乡": (1, 20),
            "天穹武朝": (5, 20)
        }
        
        level_range = level_ranges.get(region, (1, 10))
        
        # 创建基础敌人
        from enemy.base_enemy import BaseEnemy
        enemy = BaseEnemy(enemy_name, random.randint(*level_range))
        
        return enemy

    def process_battle_result(self, result: str, enemy):
        """处理战斗结果"""
        if result == "victory":
            # 计算奖励
            exp_gain = enemy.level * 30
            gold_gain = enemy.level * 5
            
            # 给予经验值
            self.player.gain_experience(exp_gain)
            
            print(f"\n✨ 战斗胜利！")
            print(f" 获得经验值: {exp_gain}")
            print(f"💰 获得金币: {gold_gain}")
            
        elif result == "defeat":
            print("\n💀 你被击败了！")
            # 复活机制
            self.player.hp = max(1, self.player.max_hp // 3)
            print("😵 你在最近的营地复活了，生命值恢复了一些...")
            
        elif result == "flee":
            print("\n🏃 你成功逃脱了！")

    def _display_location_details(self):
        """显示当前位置详细信息"""
        info = self.map.get_current_location_info()
        
        if self.map.current_sub_region:
            # 子区域详情
            print(f"\n📍 子区域: {info['name']}")
            print(f"📝 描述: {info['description']}")
            print(f"📊 等级范围: {info['level_range']}")
            print(f"🏛️ 所属区域: {info['parent_region']}")
            
            if info['features']:
                print(f"\n🏗️  特色:")
                for feature in info['features']:
                    print(f"   • {feature}")
            
            if info['enemies']:
                print(f"\n👥 敌人:")
                for enemy in info['enemies']:
                    print(f"   • {enemy}")
            
            if info['loot']:
                print(f"\n💎 战利品:")
                for loot in info['loot']:
                    print(f"   • {loot}")
        else:
            # 主区域详情
            print(f"\n📍 当前位置: {info['name']}")
            print(f"📝 描述: {info['description']}")
            print(f"🏷️ 类型: {info['type']}")
            print(f"📊 等级范围: {info['level_range']}")
            
            if info['lore']:
                print(f"\n📚 背景知识:")
                print(f"   {info['lore']}")
            
            if info['sub_regions']:
                print(f"\n🏛️ 可探索子区域:")
                for sub in info['sub_regions']:
                    print(f"   • {sub}")

    def _explore_current_area(self):
        """探索当前区域"""
        if not self.player:
            print("❌ 请先创建角色！")
            return
            
        # 获取当前区域信息
        region = self.map.current_location
        sub_region = None
        
        if self.map.current_sub_region:
            sub_info = self.map._get_sub_region_info()
            sub_region = sub_info.get('name', '')
        
        print(f"\n🗺️ 开始探索 {region}" + (f" - {sub_region}" if sub_region else ""))
        
        # 检查是否是安全区域
        if region == "裂星集":
            print("✅ 裂星集是安全区域，没有敌人。")
            return
            
        # 计算遭遇概率
        encounter_chance = self.calculate_encounter_chance(region, sub_region)
        
        if random.random() > encounter_chance:
            print("✅ 本次探索没有遇到敌人。")
            return
            
        # 生成敌人
        enemy = self.generate_enemy_for_location(region, sub_region)
        if not enemy:
            print("✅ 这个区域暂时没有敌人。")
            return
            
        print(f"\n⚠️ 遭遇敌人：{enemy.name} (等级 {enemy.level})")
        
        # 开始战斗
        config = BattleConfig(
            allow_flee=True,
            show_detailed_log=True,
            turn_limit=50
        )
        
        battle = BattleEngine(self.player, enemy, config)
        result = battle.start_battle()
        
        # 处理战斗结果
        self.process_battle_result(result, enemy)

    def _display_character_status(self):
        """显示角色状态"""
        if not self.player:
            print("❌ 请先创建角色！")
            return
            
        print(f"\n🎭 {self.player.name} ({self.player.character_class.value})")
        print("=" * 40)
        print(f"📊 等级: {self.player.level}")
        print(f"❤️ 生命值: {self.player.hp}/{self.player.max_hp}")
        print(f"🔮 法力值: {self.player.mp}/{self.player.max_mp}")
        print(f"⚔️ 攻击力: {self.player.attack}")
        print(f"🛡️ 防御力: {self.player.defense}")
        print(f"✨ 法术强度: {getattr(self.player, 'spell_power', 0)}")
        
        # 显示装备
        if hasattr(self.player, 'equipment') and self.player.equipment:
            print(f"\n🎒 装备:")
            for slot, item in self.player.equipment.items():
                if item:
                    print(f"   {slot}: {item.name}")
        
        # 显示已击败的Boss
        if hasattr(self.player, 'defeated_bosses'):
            print(f"\n🏆 已击败Boss: {len(self.player.defeated_bosses)} 层")

    def _rest_at_safe_area(self):
        """在所有主区域休息恢复"""
        if not self.player:
            print("❌ 请先创建角色！")
            return
            
        # 检查是否在主区域（子区域不能休息）
        if self.map.current_sub_region:
            print("❌ 子区域不安全，无法休息！请返回主区域。")
            return
            
        # 根据区域类型调整恢复效果
        rest_effects = {
            "裂星集": {"hp": 0.8, "mp": 0.8, "desc": "冒险者营地"},
            "齿轮之城": {"hp": 0.6, "mp": 0.7, "desc": "科技旅馆"},
            "秘法之乡": {"hp": 0.7, "mp": 0.9, "desc": "魔法旅馆"},
            "翡翠之森": {"hp": 0.5, "mp": 0.6, "desc": "精灵树屋"},
            "天穹武朝": {"hp": 0.6, "mp": 0.5, "desc": "武道客栈"}
        }
        
        effect = rest_effects.get(self.map.current_location, {"hp": 0.5, "mp": 0.5, "desc": "休息点"})
        
        # 恢复生命值和法力值
        heal_amount = int(self.player.max_hp * effect["hp"])
        mana_restore = int(self.player.max_mp * effect["mp"])
        
        self.player.hp = min(self.player.max_hp, self.player.hp + heal_amount)
        self.player.mp = min(self.player.max_mp, self.player.mp + mana_restore)
        
        print(f"\n😴 你在{self.map.current_location}的{effect['desc']}休息了一会儿...")
        print(f"❤️ 恢复了 {heal_amount} 点生命值")
        print(f"🔮 恢复了 {mana_restore} 点法力值")
        
        # 额外效果提示
        if self.map.current_location == "秘法之乡":
            print("✨ 魔法能量充沛，法力恢复效果提升！")
        elif self.map.current_location == "裂星集":
            print("🏕️ 冒险者营地提供最完善的休息服务！")

    def _challenge_boss(self):
        """挑战Boss"""
        if not self.player:
            print("❌ 请先创建角色！")
            return
            
        print("\n👹 选择要挑战的Boss层数 (1-10):")
        try:
            floor = int(input("请输入层数: "))
            if floor < 1 or floor > 10:
                print("❌ 请输入1-10之间的层数！")
                return
                
            print(f"\n👹 挑战第 {floor} 层 Boss...")
            
            # 获取Boss
            from enemy.bosses.boss_manager import BossManager
            boss_manager = BossManager()
            boss = boss_manager.get_boss(floor)
            
            if not boss:
                print("❌ 该层Boss尚未开放！")
                return
                
            print(f"\n⚠️ 遭遇Boss：{boss.name} (等级 {boss.level})")
            
            # Boss战斗配置
            config = BattleConfig(
                allow_flee=False,
                show_detailed_log=True,
                turn_limit=100
            )
            
            battle = BattleEngine(self.player, boss, config)
            result = battle.start_battle()
            
            # 处理Boss战结果
            if result == "victory":
                self.player.defeated_bosses.add(floor)
                print(f"\n🎉 恭喜！你击败了第 {floor} 层Boss！")
                
        except ValueError:
            print("❌ 请输入有效数字！")

def main():
    """主入口点"""
    try:
        navigator = MapNavigator()
        navigator.start()
    except KeyboardInterrupt:
        print("\n\n👋 感谢使用艾兰提亚地图系统！")
        sys.exit(0)

if __name__ == "__main__":
    main()
