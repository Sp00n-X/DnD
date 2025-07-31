#!/usr/bin/env python3
"""
游戏启动脚本 - 简化游戏入口
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from game import GameLauncher

def main():
    """主入口点"""
    print("🎮 启动艾兰提亚冒险世界...")
    launcher = GameLauncher()
    launcher.start()

if __name__ == "__main__":
    main()
