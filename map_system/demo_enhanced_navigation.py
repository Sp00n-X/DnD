#!/usr/bin/env python3
"""
增强版子区域导航演示
展示如何在主区域和子区域之间自由移动
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from enhanced_map_system import EnhancedAetheriaMap

def demo_enhanced_navigation():
    """演示增强版导航功能"""
    print("🗺️  增强版子区域导航演示")
    print("=" * 60)
    
    # 创建地图实例
    world = EnhancedAetheriaMap()
    
    # 演示1: 基础导航
    print("\n📍 演示1: 基础区域导航")
    print("-" * 40)
    
    print("当前位置:", world.current_location)
    print("可前往:", world.get_available_moves())
    
    # 前往齿轮之城
    print("\n🚀 前往齿轮之城...")
    world.move_to("齿轮之城")
    print("当前位置:", world.current_location)
    print("可探索子区域:", world.map_data["齿轮之城"]["sub_regions"])
    
    # 演示2: 进入子区域
    print("\n🏛️ 演示2: 进入子区域")
    print("-" * 40)
    
    print("进入七炉议会...")
    world.enter_sub_region("七炉议会")
    info = world.get_current_location_info()
    print("当前子区域:", info["name"])
    print("等级范围:", info["level_range"])
    if "features" in info and info["features"]:
        print("特色:", ", ".join(info["features"][:3]) + "...")
    
    # 演示3: 子区域信息
    print("\n📊 演示3: 子区域详细信息")
    print("-" * 40)
    
    info = world.get_current_location_info()
    print("子区域名称:", info["name"])
    print("描述:", info["description"])
    print("等级:", info["level_range"])
    print("敌人:", ", ".join(info["enemies"][:3]) + "...")
    print("战利品:", ", ".join(info["loot"][:3]) + "...")
    
    # 演示4: 返回主区域
    print("\n🔙 演示4: 返回主区域")
    print("-" * 40)
    
    print("返回齿轮之城...")
    world.exit_sub_region()
    print("当前位置:", world.current_location)
    print("是否已探索子区域:", "齿轮之城:七炉议会" in world.visited_sub_regions)
    
    # 演示5: 探索其他区域
    print("\n🌟 演示5: 探索其他区域")
    print("-" * 40)
    
    # 前往秘法之乡
    world.move_to("裂星集")
    world.move_to("秘法之乡")
    
    print("当前位置:", world.current_location)
    print("可探索子区域:", world.map_data["秘法之乡"]["sub_regions"][:3], "...")
    
    # 进入秘法之乡的子区域
    world.enter_sub_region("第一塔·星尘")
    info = world.get_current_location_info()
    print("当前子区域:", info["name"])
    print("所属区域:", info["parent_region"])

def demo_integration_example():
    """演示集成使用示例"""
    print("\n" + "=" * 60)
    print("🔄 集成使用示例")
    print("=" * 60)
    
    world = EnhancedAetheriaMap()
    
    # 示例：根据玩家等级推荐探索路线
    player_level = 8
    
    print(f"\n🎯 等级 {player_level} 玩家推荐探索路线:")
    
    # 推荐齿轮之城的子区域
    from regions.gearhaven.sub_regions import (
        SevenFurnaceParliament,
        BlackWrenchHQ,
        AbandonedFogRoot
    )
    
    gearhaven_subs = [
        ("废弃雾根", AbandonedFogRoot()),
        ("黑扳手总部", BlackWrenchHQ()),
        ("七炉议会", SevenFurnaceParliament())
    ]
    
    print("\n⚙️  齿轮之城推荐:")
    for name, sub_region in gearhaven_subs:
        min_level, max_level = sub_region.level_range
        if min_level <= player_level <= max_level:
            print(f"   ✅ {name} (等级 {min_level}-{max_level})")
        elif player_level < min_level:
            print(f"   ⚠️  {name} (需要等级 {min_level}-{max_level})")
        else:
            print(f"   🔶 {name} (等级 {min_level}-{max_level}, 可能过于简单)")
    
    # 显示已探索记录
    print(f"\n📊 探索记录:")
    world.move_to("齿轮之城")
    world.enter_sub_region("废弃雾根")
    world.exit_sub_region()
    world.enter_sub_region("黑扳手总部")
    
    print("已探索主区域:", len(world.visited_locations))
    print("已探索子区域:", len(world.visited_sub_regions))
    for sub_region in world.visited_sub_regions:
        region, sub = sub_region.split(":")
        print(f"   • {region} - {sub}")

if __name__ == "__main__":
    demo_enhanced_navigation()
    demo_integration_example()
    
    print("\n" + "=" * 60)
    print("✅ 演示完成！")
    print("使用 ./start_enhanced_map.sh 启动交互式地图系统")
    print("=" * 60)
