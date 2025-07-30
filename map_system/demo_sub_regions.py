#!/usr/bin/env python3
"""
子区域系统演示脚本
展示如何访问和使用各个区域的子区域
"""

from regions import (
    get_sub_regions, 
    get_region_module,
    gearhaven,
    selintar,
    lothir,
    wulong
)

def demo_region_overview():
    """展示所有区域的子区域概览"""
    print("🗺️  艾兰提亚世界子区域系统演示")
    print("=" * 60)
    
    regions = ["齿轮之城", "秘法之乡", "翡翠之森", "天穹武朝"]
    
    for region in regions:
        print(f"\n🏛️  {region}")
        print("-" * 40)
        
        sub_regions = get_sub_regions(region)
        for sub_region in sub_regions:
            print(f"   • {sub_region}")

def demo_detailed_sub_regions():
    """展示详细的子区域信息"""
    print("\n" + "=" * 60)
    print("📊 详细子区域信息")
    print("=" * 60)
    
    # 齿轮之城示例
    print("\n⚙️  齿轮之城 - 子区域详情:")
    parliament = gearhaven.SevenFurnaceParliament()
    print(f"   📍 {parliament.name}")
    print(f"   📝 {parliament.description}")
    print(f"   📊 等级: {parliament.level_range[0]}-{parliament.level_range[1]}")
    print(f"   👥 敌人: {', '.join(parliament.enemies[:3])}...")
    print(f"   💎 战利品: {', '.join(parliament.loot[:3])}...")
    
    # 秘法之乡示例
    print("\n🔮 秘法之乡 - 子区域详情:")
    stardust = selintar.FirstTowerStardust()
    print(f"   📍 {stardust.name}")
    print(f"   📝 {stardust.description}")
    print(f"   📊 等级: {stardust.level_range[0]}-{stardust.level_range[1]}")
    print(f"   🏰 塔层: {stardust.tower_level}")
    
    # 翡翠之森示例
    print("\n🌿 翡翠之森 - 子区域详情:")
    moss = lothir.MossStepSettlement()
    print(f"   📍 {moss.name}")
    print(f"   📝 {moss.description}")
    print(f"   📊 等级: {moss.level_range[0]}-{moss.level_range[1]}")
    print(f"   🧝 精灵亲和: {moss.elven_affinity}")
    
    # 天穹武朝示例
    print("\n⚔️  天穹武朝 - 子区域详情:")
    arena = wulong.WhiteTigerArena()
    print(f"   📍 {arena.name}")
    print(f"   📝 {arena.description}")
    print(f"   📊 等级: {arena.level_range[0]}-{arena.level_range[1]}")
    print(f"   🌪️ 真气需求: {arena.qi_requirement}")

def demo_connections():
    """展示子区域连接关系"""
    print("\n" + "=" * 60)
    print("🔗 子区域连接关系")
    print("=" * 60)
    
    # 齿轮之城连接
    print("\n⚙️  齿轮之城连接:")
    from regions.gearhaven.sub_regions import SUB_REGION_CONNECTIONS as gear_connections
    for region, connections in gear_connections.items():
        print(f"   {region} → {', '.join(connections)}")
    
    # 秘法之乡连接
    print("\n🔮 秘法之乡连接:")
    from regions.selintar.sub_regions import SUB_REGION_CONNECTIONS as sel_connections
    for region, connections in sel_connections.items():
        if connections:
            print(f"   {region} → {', '.join(connections)}")
    
    # 翡翠之森连接
    print("\n🌿 翡翠之森连接:")
    from regions.lothir.sub_regions import SUB_REGION_CONNECTIONS as loth_connections
    for region, connections in loth_connections.items():
        print(f"   {region} → {', '.join(connections)}")
    
    # 天穹武朝连接
    print("\n⚔️  天穹武朝连接:")
    from regions.wulong.sub_regions import SUB_REGION_CONNECTIONS as wulong_connections
    for region, connections in wulong_connections.items():
        print(f"   {region} → {', '.join(connections)}")

def demo_integration():
    """展示如何集成到现有系统"""
    print("\n" + "=" * 60)
    print("🔄 系统集成示例")
    print("=" * 60)
    
    # 示例：根据玩家等级推荐子区域
    player_level = 12
    
    print(f"\n🎯 等级 {player_level} 玩家推荐区域:")
    
    regions_data = [
        ("齿轮之城", gearhaven.SevenFurnaceParliament()),
        ("秘法之乡", selintar.FifthTowerStarmap()),
        ("翡翠之森", lothir.RingDwelling()),
        ("天穹武朝", wulong.SkySwordWall())
    ]
    
    for region_name, sub_region in regions_data:
        min_level, max_level = sub_region.level_range
        if min_level <= player_level <= max_level:
            print(f"   ✅ {region_name} - {sub_region.name}")
        else:
            print(f"   ⚠️  {region_name} - {sub_region.name} (需要等级 {min_level}-{max_level})")

if __name__ == "__main__":
    demo_region_overview()
    demo_detailed_sub_regions()
    demo_connections()
    demo_integration()
