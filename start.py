#!/usr/bin/env python3
"""
Library Management System - FastAPI启动脚本
ISYS3001 配置管理和采购管理演示项目
"""

import uvicorn
import os
import sys

def main():
    """启动FastAPI服务器"""
    
    # 确保在正确的目录
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # 添加当前目录到Python路径
    sys.path.insert(0, os.getcwd())
    
    print("""
╔════════════════════════════════════════════════════════════╗
║                图书管理系统 - FastAPI版本                   ║
║                                                            ║
║  🚀 启动服务器...                                           ║
║  📍 项目目录: {}
║                                                            ║
║  ISYS3001 配置管理演示项目                                  ║
╚════════════════════════════════════════════════════════════╝
    """.format(os.getcwd()))
    
    # 启动服务器
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_dirs=["app", "frontend"],
        log_level="info"
    )

if __name__ == "__main__":
    main()
