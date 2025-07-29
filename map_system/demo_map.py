#!/usr/bin/env python3
"""
Demo script for the Aetheria Map System
Shows basic usage and integration examples
"""

from map_system import AetheriaMap

def demo_basic_navigation():
    """Demonstrate basic map navigation"""
    print("🗺️  艾兰提亚地图系统演示")
    print("=" * 50)
    
    # Initialize map
    world = AetheriaMap()
    
    # Show starting position
    print(f"起始位置: {world.current_location}")
    print(f"描述: {world.map_data[world.current_location]['description']}")
    
    # Show available moves
    print(f"\n可前往的地点: {', '.join(world.get_available_moves())}")
    
    # Demonstrate movement
    destinations = ["齿轮之城", "秘法之乡", "翡翠之森", "天穹武朝"]
    
    for dest in destinations[:2]:  # Demo first two
        print(f"\n🚶 前往 {dest}...")
        if world.move_to(dest):
            info = world.get_current_location_info()
            print(f"✅ 到达 {dest}")
            print(f"   类型: {info['type']}")
            print(f"   等级范围: {info['level_range']}")
            print(f"   可前往: {', '.join(info['connections'])}")
            
            if info['sub_locations']:
                print(f"   子区域: {', '.join(info['sub_locations'].keys())}")
    
    # Show path finding
    print(f"\n🛤️  路径规划演示:")
    world.current_location = "裂星集"  # Reset to hub
    path = world.find_path("裂星集", "翡翠之森")
    print(f"从 裂星集 到 翡翠之森 的路径: {' → '.join(path)}")
    
    # Show distance calculation
    print(f"\n📏 距离计算:")
    for loc in ["齿轮之城", "秘法之乡", "翡翠之森", "天穹武朝"]:
        dist = world.get_distance("裂星集", loc)
        print(f"裂星集 到 {loc}: {dist:.2f} 单位")

def demo_integration_with_existing_system():
    """Show how to integrate with existing D&D systems"""
    print("\n" + "=" * 50)
    print("🔄 与现有系统集成演示")
    print("=" * 50)
    
    world = AetheriaMap()
    
    # Example: Location-based encounter generation
    location_encounters = {
        "齿轮之城": ["机械守卫", "黑扳手间谍", "以太电流泄漏"],
        "秘法之乡": ["星图研究员", "阶梯法师", "以太病感染者"],
        "翡翠之森": ["精灵哨兵", "星辉兽", "母树守卫"],
        "天穹武朝": ["真气武者", "剑圣传人", "巨构守卫"]
    }
    
    current_loc = "齿轮之城"
    world.current_location = current_loc
    
    print(f"在 {current_loc} 可能遇到的敌人:")
    for enemy in location_encounters.get(current_loc, []):
        print(f"   • {enemy}")
    
    # Example: Level-based area restriction
    player_level = 8
    print(f"\n🎯 等级 {player_level} 玩家适合的地点:")
    
    for loc_name, loc_data in world.map_data.items():
        level_range = loc_data.get("level_range", "1-20")
        min_level, max_level = map(int, level_range.split("-"))
        
        if min_level <= player_level <= max_level:
            print(f"   ✅ {loc_name} ({level_range})")
        elif player_level < min_level:
            print(f"   ⚠️  {loc_name} ({level_range}) - 等级过高")
        else:
            print(f"   ⚠️  {loc_name} ({level_range}) - 等级过低")

if __name__ == "__main__":
    demo_basic_navigation()
    demo_integration_with_existing_system()
