#!/usr/bin/env python3
"""
增强版艾兰提亚世界地图系统
支持主区域和子区域导航
"""

import json
import os
import sys
from typing import Dict, List, Tuple, Optional, Any
import cmd
import importlib

# 添加regions模块路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from regions import (
    get_sub_regions, 
    get_region_module,
    SUB_REGION_CLASSES,
    get_sub_region_class
)

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

class EnhancedMapCommandInterface(cmd.Cmd):
    """增强版命令行界面"""
    
    def __init__(self):
        super().__init__()
        self.map = EnhancedAetheriaMap()
        self._update_prompt()
        self.intro = """
╔══════════════════════════════════════════════════════════════╗
║              增强版艾兰提亚世界地图系统                      ║
║         Enhanced Aetheria World Map Navigator                ║
║                                                              ║
║         支持主区域和子区域导航！                             ║
╚══════════════════════════════════════════════════════════════╝
输入 'help' 查看可用命令
"""
    
    def _update_prompt(self):
        """更新命令提示符"""
        if self.map.current_sub_region:
            # 在子区域中
            sub_region_name = self.map._get_sub_region_info().get("name", "未知")
            self.prompt = f"\n[🏛️  {self.map.current_region} - {sub_region_name}] > "
        else:
            # 在主区域中
            self.prompt = f"\n[🗺️  {self.map.current_location}] > "
    
    def do_look(self, arg):
        """查看当前位置详细信息"""
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
            
            # 子区域连接
            connections = self.map.get_sub_region_connections()
            if connections:
                print(f"\n🔗 可前往子区域:")
                for conn in connections:
                    # 将类名转换为显示名称
                    conn_name = conn.replace('HQ', '总部').replace('MK', 'MK-')
                    print(f"   • {conn_name}")
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
    
    def do_go(self, destination):
        """前往指定位置: go [位置名称]"""
        if not destination:
            print("❌ 请指定目的地")
            return
        
        # 处理子区域探索（支持中英文冒号）
        if destination.startswith("探索：") or destination.startswith("探索:"):
            prefix_len = 3 if destination.startswith("探索：") else 4
            sub_region = destination[prefix_len:]  # 去掉"探索："或"探索:"前缀
            if self.map.enter_sub_region(sub_region):
                print(f"✅ 已进入子区域：{sub_region}")
                self._update_prompt()
            else:
                print(f"❌ 无法进入子区域：{sub_region}")
            return
        
        # 处理子区域之间的移动
        if self.map.current_sub_region:
            # 获取当前子区域的连接
            connections = self.map.get_sub_region_connections()
            if connections:
                # 将显示名称转换为类名进行匹配
                region_module = self.map.get_region_module(self.map.current_region)
                try:
                    module = importlib.import_module(f'regions.{region_module}.sub_regions')
                    for conn_class in connections:
                        sub_region_class = getattr(module, conn_class)
                        instance = sub_region_class()
                        if instance.name == destination:
                            if self.map.enter_sub_region(instance.name):
                                print(f"✅ 已进入子区域：{instance.name}")
                                self._update_prompt()
                                return
                except:
                    pass
        
        # 处理返回主区域
        if destination.startswith("返回"):
            if self.map.exit_sub_region():
                print(f"✅ 已返回：{self.map.current_location}")
                self._update_prompt()
            else:
                print("❌ 当前不在子区域中")
            return
        
        # 处理主区域移动
        if self.map.move_to(destination):
            print(f"✅ 已前往：{destination}")
            self._update_prompt()
            
            if destination not in self.map.visited_locations:
                print(f"🎉 发现新地点：{destination}")
        else:
            print(f"❌ 无法前往：{destination}")
            self.do_where("")
    
    def do_where(self, arg):
        """显示当前位置和可前往地点"""
        print(f"\n📍 当前位置：{self.map.current_location}")
        
        if self.map.current_sub_region:
            print(f"🏛️ 子区域：{self.map._get_sub_region_info().get('name', '未知')}")
            print("🎯 可前往：返回" + self.map.current_region)
            
            # 显示子区域连接
            connections = self.map.get_available_moves()
            if len(connections) > 1:  # 除了"返回"还有其他选项
                print("\n🔗 可前往子区域：")
                for move in connections[1:]:  # 跳过第一个"返回"选项
                    print(f"   • {move}")
        else:
            available = self.map.get_available_moves()
            print("🎯 可前往：")
            for move in available:
                if move.startswith("探索："):
                    print(f"   • {move}")
                else:
                    print(f"   • {move}")
    
    def do_map(self, arg):
        """显示世界地图概览"""
        print("\n🗺️  艾兰提亚世界地图")
        print("   北")
        print("    ↑")
        print("西 ← → 东")
        print("    ↓")
        print("   南")
        
        # 简化地图
        grid = [
            ["   ", "   ", "   ", "   ", "   "],
            ["   ", "齿", "   ", "秘", "   "],
            ["   ", "   ", "裂", "   ", "   "],
            ["   ", "   ", "   ", "   ", "   "],
            ["   ", "翡", "   ", "天", "   "]
        ]
        
        print("\n简化地图:")
        for row in grid:
            print(" ".join(row))
        
        print("\n图例:")
        print("裂 = 裂星集 (中心枢纽)")
        print("齿 = 齿轮之城")
        print("秘 = 秘法之乡")
        print("翡 = 翡翠之森")
        print("天 = 天穹武朝")
    
    def do_regions(self, arg):
        """显示所有区域的子区域"""
        print("\n🏛️  各区域子区域:")
        print("=" * 50)
        
        regions = ["齿轮之城", "秘法之乡", "翡翠之森", "天穹武朝"]
        
        for region in regions:
            sub_regions = get_sub_regions(region)
            print(f"\n📍 {region}:")
            for sub in sub_regions:
                print(f"   • {sub}")
    
    def do_discovered(self, arg):
        """显示已发现的地点和子区域"""
        print(f"\n🌍 已发现的主区域 ({len(self.map.visited_locations)}):")
        for location in sorted(self.map.visited_locations):
            marker = "📍" if location == self.map.current_location else "•"
            print(f"   {marker} {location}")
        
        if self.map.visited_sub_regions:
            print(f"\n🏛️ 已探索的子区域 ({len(self.map.visited_sub_regions)}):")
            for sub_region in sorted(self.map.visited_sub_regions):
                region, sub = sub_region.split(":")
                print(f"   • {region} - {sub}")
    
    def do_search(self, keyword):
        """搜索地点或子区域: search [关键词]"""
        if not keyword:
            print("❌ 请提供搜索关键词")
            return
        
        keyword = keyword.lower()
        matches = []
        
        # 搜索主区域
        for name, data in self.map.map_data.items():
            if (keyword in name.lower() or 
                keyword in data["description"].lower() or
                keyword in data.get("lore", "").lower()):
                matches.append(("主区域", name))
        
        # 搜索子区域
        regions = ["齿轮之城", "秘法之乡", "翡翠之森", "天穹武朝"]
        for region in regions:
            sub_regions = get_sub_regions(region)
            for sub_region in sub_regions:
                if keyword in sub_region.lower():
                    matches.append((f"{region}子区域", sub_region))
        
        if matches:
            print(f"\n🔍 搜索结果 '{keyword}':")
            for type_name, match in matches:
                print(f"   • [{type_name}] {match}")
        else:
            print(f"❌ 未找到包含 '{keyword}' 的地点")
    
    def do_quit(self, arg):
        """退出地图系统"""
        print("\n👋 感谢使用增强版艾兰提亚地图系统！")
        return True
    
    def do_exit(self, arg):
        """退出地图系统"""
        return self.do_quit(arg)
    
    def do_help(self, arg):
        """显示帮助信息"""
        print("""
📖 增强版命令：
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
基础命令：
  look                    - 查看当前位置详细信息
  where                   - 显示当前位置和可前往地点
  map                     - 显示世界地图
  regions                 - 显示所有区域的子区域
  discovered              - 显示已发现的地点和子区域
  search [关键词]         - 搜索地点或子区域
  help                    - 显示此帮助信息
  quit/exit               - 退出系统

移动命令：
  go [主区域名]           - 前往主区域（如：go 齿轮之城）
  go 探索：[子区域名]     - 进入子区域（如：go 探索：星辉池）
  go 返回[主区域名]       - 从子区域返回主区域（如：go 返回翡翠之森）
  
子区域移动：
  在子区域中可直接输入子区域名称前往其他连接的子区域
  例如：在第一塔·星尘中输入 "go 星桥" 可直接前往星桥
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 使用提示：
• 从裂星集开始，先前往四大主区域
• 在主区域中使用 'go 探索：子区域名' 进入子区域
• 在子区域中可直接前往其他连接的子区域
• 子区域名称直接使用中文，如：go 探索：七炉议会
• 使用 'where' 查看当前可前往的所有地点
        """)

def main():
    """主入口点"""
    try:
        interface = EnhancedMapCommandInterface()
        interface.cmdloop()
    except KeyboardInterrupt:
        print("\n\n👋 感谢使用增强版艾兰提亚地图系统！")
        sys.exit(0)

if __name__ == "__main__":
    main()
