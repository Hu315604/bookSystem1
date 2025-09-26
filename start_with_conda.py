#!/usr/bin/env python3
"""
Library Management System - Conda Virtual Environment Startup Script
ISYS3001 Configuration Management and Procurement Management Demo Project
"""

import subprocess
import sys
import os

def main():
    """Start FastAPI server using specified conda virtual environment"""
    
    # 确保在正确的目录
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # 虚拟环境路径
    venv_python = r"D:\python\conda3\envs\isys3001-projects\python.exe"
    
    print("""
╔════════════════════════════════════════════════════════════╗
║              Library Management System - FastAPI           ║
║                                                            ║
║  🚀 Starting with Conda virtual environment...             ║
║  🐍 Python Environment: D:\python\conda3\envs\isys3001-projects   ║
║  📍 Project Directory: {}
║                                                            ║
║  ISYS3001 Configuration Management Demo Project            ║
╚════════════════════════════════════════════════════════════╝
    """.format(os.getcwd()))
    
    # 检查虚拟环境是否存在
    if not os.path.exists(venv_python):
        print("❌ 错误: 找不到conda虚拟环境!")
        print(f"请确保虚拟环境存在: {venv_python}")
        return
    
    try:
        # 使用虚拟环境的python启动uvicorn
        cmd = [
            venv_python, "-m", "uvicorn", 
            "app.main:app",
            "--host", "0.0.0.0",
            "--port", "8001",
            "--reload",
            "--log-level", "info"
        ]
        
        print("🚀 启动命令:", " ".join(cmd))
        print("🌐 访问地址:")
        print("   前端界面: http://localhost:8001")
        print("   API文档:  http://localhost:8001/docs")
        print("   健康检查: http://localhost:8001/api/health")
        print("   图书API:  http://localhost:8001/api/books")
        print("   用户API:  http://localhost:8001/api/users")
        print()
        
        # 启动服务器
        subprocess.run(cmd, check=True)
        
    except KeyboardInterrupt:
        print("\n👋 服务器已停止")
    except subprocess.CalledProcessError as e:
        print(f"❌ 启动失败: {e}")
    except Exception as e:
        print(f"❌ 未知错误: {e}")

if __name__ == "__main__":
    main()
