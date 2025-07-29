#!/usr/bin/env python3
"""
D&D Command-Line Map System for Aetheria World
Supports navigation between four major regions and their sub-locations
"""

import json
import os
import sys
from typing import Dict, List, Tuple, Optional
import cmd

class AetheriaMap:
    """Core map system for the Aetheria world"""
    
    def __init__(self):
        self.current_location = "裂星集"  # Starting hub
        self.visited_locations = {"裂星集"}
        self.map_data = self._initialize_world()
        self.discovered_lore = {}
        
    def _initialize_world(self) -> Dict:
        """Initialize the world map with all locations"""
        return {
            "裂星集": {
                "description": "中立城寨，四国交汇的冒险者聚集地",
                "connections": ["齿轮之城", "秘法之乡", "翡翠之森", "天穹武朝"],
                "type": "hub",
                "lore": "四国轨道/航线/商路在此交汇，中立城寨聚集冒险者、走私客、以太黑市",
                "coordinates": (0, 0),
                "level_range": "1-20"
            },
            "齿轮之城": {
                "description": "阿斯图里亚 - 云层都市，真空管科技巅峰",
                "connections": ["裂星集", "七炉议会", "黑扳手总部", "废弃雾根"],
                "type": "city",
                "lore": "1960-70年代地球科技水平，真空管+仿生学，海拔3-6km",
                "coordinates": (-2, 1),
                "level_range": "5-15",
                "sub_locations": {
                    "七炉议会": "齿轮城最高权力机构，七位公爵轮流执政",
                    "黑扳手总部": "工人行会秘密基地，暗中对抗七炉议会",
                    "废弃雾根": "地表废弃区域，隐藏着古老秘密"
                }
            },
            "秘法之乡": {
                "description": "赛林塔 - 九座倒悬塔构成的魔法圣地",
                "connections": ["裂星集", "第一塔·星尘", "第五塔·星图", "第九塔·螺旋顶点"],
                "type": "magical",
                "lore": "阶梯式以太科学，1-9阶官方认证，真空管阵列+星图运算",
                "coordinates": (2, 1),
                "level_range": "3-18",
                "sub_locations": {
                    "第一塔·星尘": "初级法师学习之地，1-3阶法术",
                    "第五塔·星图": "高级法师研究场所，6阶领域展开",
                    "第九塔·螺旋顶点": "最高魔法殿堂，9阶法师的归宿"
                }
            },
            "翡翠之森": {
                "description": "洛希尔 - 精灵的翡翠森林，800年寿命的奥秘",
                "connections": ["裂星集", "苔阶聚落", "环居", "苔堡"],
                "type": "forest",
                "lore": "非人精灵，四叶脑+800年寿命，情感淡薄，敬畏自然循环",
                "coordinates": (-1, -2),
                "level_range": "7-20",
                "sub_locations": {
                    "苔阶聚落": "精灵初级聚落，与自然和谐共处",
                    "环居": "精灵中级聚落，巨树环绕的神秘居所",
                    "苔堡": "精灵最高议会所在地，九苔议会"
                }
            },
            "天穹武朝": {
                "description": "龙阙 - 九宫格山水构成的武道圣地",
                "connections": ["裂星集", "天剑壁", "倒岳城", "赤霄剑冢"],
                "type": "martial",
                "lore": "真气=以太×经络×意志，官方9阶度量，巨构即基建",
                "coordinates": (1, -2),
                "level_range": "4-17",
                "sub_locations": {
                    "天剑壁": "武道修炼圣地，剑痕刻上天壁",
                    "倒岳城": "倒立城市，武朝奇观之一",
                    "赤霄剑冢": "历代剑圣埋剑之地，蕴含强大剑意"
                }
            }
        }
    
    def get_current_location_info(self) -> Dict:
        """Get detailed information about current location"""
        location = self.map_data[self.current_location]
        return {
            "name": self.current_location,
            "description": location["description"],
            "type": location["type"],
            "connections": location["connections"],
            "lore": location.get("lore", ""),
            "level_range": location.get("level_range", "1-20"),
            "sub_locations": location.get("sub_locations", {})
        }
    
    def move_to(self, destination: str) -> bool:
        """Attempt to move to a new location"""
        if destination not in self.map_data:
            return False
        
        current_info = self.map_data[self.current_location]
        if destination in current_info["connections"]:
            self.current_location = destination
            self.visited_locations.add(destination)
            return True
        return False
    
    def get_available_moves(self) -> List[str]:
        """Get list of available destinations from current location"""
        return self.map_data[self.current_location]["connections"]
    
    def get_distance(self, location1: str, location2: str) -> float:
        """Calculate distance between two locations using coordinates"""
        if location1 not in self.map_data or location2 not in self.map_data:
            return float('inf')
        
        coord1 = self.map_data[location1]["coordinates"]
        coord2 = self.map_data[location2]["coordinates"]
        
        return ((coord1[0] - coord2[0]) ** 2 + (coord1[1] - coord2[1]) ** 2) ** 0.5
    
    def find_path(self, start: str, end: str) -> List[str]:
        """Find shortest path between two locations using BFS"""
        if start not in self.map_data or end not in self.map_data:
            return []
        
        from collections import deque
        
        queue = deque([[start]])
        visited = {start}
        
        while queue:
            path = queue.popleft()
            current = path[-1]
            
            if current == end:
                return path
            
            for neighbor in self.map_data[current]["connections"]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    new_path = list(path)
                    new_path.append(neighbor)
                    queue.append(new_path)
        
        return []

class MapCommandInterface(cmd.Cmd):
    """Command-line interface for the map system"""
    
    def __init__(self):
        super().__init__()
        self.map = AetheriaMap()
        self.prompt = f"\n[🗺️  {self.map.current_location}] > "
        self.intro = """
╔══════════════════════════════════════════════════════════════╗
║                    艾兰提亚世界地图系统                      ║
║                 Aetheria World Map Navigator                 ║
╚══════════════════════════════════════════════════════════════╝
输入 'help' 查看可用命令
"""
    
    def do_look(self, arg):
        """查看当前位置详细信息"""
        info = self.map.get_current_location_info()
        print(f"\n📍 当前位置: {info['name']}")
        print(f"📝 描述: {info['description']}")
        print(f"🏷️ 类型: {info['type']}")
        print(f"📊 等级范围: {info['level_range']}")
        print(f"🔗 可前往: {', '.join(info['connections'])}")
        
        if info['lore']:
            print(f"\n📚 背景知识:")
            print(f"   {info['lore']}")
        
        if info['sub_locations']:
            print(f"\n🏛️ 子区域:")
            for sub, desc in info['sub_locations'].items():
                print(f"   • {sub}: {desc}")
    
    def do_go(self, destination):
        """前往指定位置: go [位置名称]"""
        if not destination:
            print("❌ 请指定目的地")
            return
        
        if self.map.move_to(destination):
            print(f"✅ 已前往: {destination}")
            self.prompt = f"\n[🗺️  {self.map.current_location}] > "
            
            # Check if this is a new discovery
            if destination not in self.map.visited_locations:
                print(f"🎉 发现新地点: {destination}")
        else:
            print(f"❌ 无法前往: {destination}")
            available = self.map.get_available_moves()
            print(f"🎯 可前往: {', '.join(available)}")
    
    def do_map(self, arg):
        """显示世界地图概览"""
        print("\n🗺️  艾兰提亚世界地图")
        print("   北")
        print("    ↑")
        print("西 ← → 东")
        print("    ↓")
        print("   南")
        
        locations = {
            "齿轮之城": (-2, 1),
            "秘法之乡": (2, 1),
            "裂星集": (0, 0),
            "翡翠之森": (-1, -2),
            "天穹武朝": (1, -2)
        }
        
        # Simple ASCII map
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
    
    def do_path(self, destination):
        """显示到指定位置的路径: path [位置名称]"""
        if not destination:
            print("❌ 请指定目的地")
            return
        
        path = self.map.find_path(self.map.current_location, destination)
        if path:
            print(f"\n🛤️  从 {self.map.current_location} 到 {destination} 的路径:")
            for i, loc in enumerate(path, 1):
                marker = "→" if i < len(path) else "🏁"
                print(f"   {i}. {marker} {loc}")
        else:
            print(f"❌ 无法找到从 {self.map.current_location} 到 {destination} 的路径")
    
    def do_where(self, arg):
        """显示当前位置和可前往的地点"""
        print(f"\n📍 当前位置: {self.map.current_location}")
        available = self.map.get_available_moves()
        print(f"🎯 可前往: {', '.join(available)}")
    
    def do_discovered(self, arg):
        """显示已发现的地点"""
        print(f"\n🌍 已发现的地点 ({len(self.map.visited_locations)}):")
        for location in sorted(self.map.visited_locations):
            marker = "📍" if location == self.map.current_location else "•"
            print(f"   {marker} {location}")
    
    def do_search(self, keyword):
        """搜索地点: search [关键词]"""
        if not keyword:
            print("❌ 请提供搜索关键词")
            return
        
        keyword = keyword.lower()
        matches = []
        
        for name, data in self.map.map_data.items():
            if (keyword in name.lower() or 
                keyword in data["description"].lower() or
                keyword in data.get("lore", "").lower()):
                matches.append(name)
        
        if matches:
            print(f"\n🔍 搜索结果 '{keyword}':")
            for match in matches:
                print(f"   • {match}")
        else:
            print(f"❌ 未找到包含 '{keyword}' 的地点")
    
    def do_quit(self, arg):
        """退出地图系统"""
        print("\n👋 感谢使用艾兰提亚地图系统！")
        return True
    
    def do_exit(self, arg):
        """退出地图系统"""
        return self.do_quit(arg)
    
    def do_help(self, arg):
        """显示帮助信息"""
        print("""
📖 可用命令:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
look                    - 查看当前位置详细信息
go [地点]               - 前往指定位置
map                     - 显示世界地图
path [地点]             - 显示到指定位置的路径
where                   - 显示当前位置和可前往地点
discovered              - 显示已发现的地点
search [关键词]         - 搜索地点
help                    - 显示此帮助信息
quit/exit               - 退出系统
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        """)

def main():
    """Main entry point for the map system"""
    try:
        interface = MapCommandInterface()
        interface.cmdloop()
    except KeyboardInterrupt:
        print("\n\n👋 感谢使用艾兰提亚地图系统！")
        sys.exit(0)

if __name__ == "__main__":
    main()
