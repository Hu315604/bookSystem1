#!/bin/bash

# Library Management System 部署脚本
# 用于自动化部署流程

set -e

echo "📚 开始部署 Library Management System..."

# 检查环境
check_requirements() {
    echo "📋 检查部署要求..."
    
    if ! command -v java &> /dev/null; then
        echo "❌ Java 未安装"
        exit 1
    fi
    
    if ! command -v mvn &> /dev/null; then
        echo "❌ Maven 未安装"
        exit 1
    fi
    
    echo "✅ 环境检查通过"
}

# 构建应用
build_application() {
    echo "🔨 构建应用..."
    
    # 清理之前的构建
    echo "🧹 清理之前的构建..."
    mvn clean
    
    # 编译和打包
    echo "📦 编译和打包应用..."
    mvn compile package -DskipTests
    
    # 创建必要的目录
    mkdir -p data
    mkdir -p logs
    
    echo "✅ 应用构建完成"
}

# 部署应用
deploy_application() {
    echo "🚢 启动应用..."
    
    # 停止可能运行的进程
    pkill -f "library-management-system" || true
    
    # 启动应用
    echo "🌟 启动 Library Management System..."
    nohup java -jar target/library-management-system-1.0.0.jar --spring.profiles.active=production > logs/app.log 2>&1 &
    
    echo "✅ 应用启动完成"
}

# 健康检查
health_check() {
    echo "🏥 执行健康检查..."
    
    # 等待服务启动
    sleep 10
    
    # 检查服务状态
    if curl -f http://localhost:8080/api/health > /dev/null 2>&1; then
        echo "✅ 应用健康检查通过"
    else
        echo "❌ 应用健康检查失败，请检查日志"
        echo "📄 最近的日志:"
        tail -20 logs/app.log
        exit 1
    fi
}

# 显示部署信息
show_deployment_info() {
    echo "
╔════════════════════════════════════════════════════════════╗
║                    部署完成！                               ║
║                                                            ║
║  📚 应用地址: http://localhost:8080                         ║
║  🏥 健康检查: http://localhost:8080/api/health              ║
║  📖 图书API: http://localhost:8080/api/books               ║
║  👤 用户API: http://localhost:8080/api/users               ║
║  📁 项目目录: $(pwd)                                        ║
║                                                            ║
║  管理命令:                                                  ║
║  • 查看日志: tail -f logs/app.log                          ║
║  • 停止服务: pkill -f 'library-management-system'          ║
║  • 重启服务: bash deployment/deploy.sh                     ║
╚════════════════════════════════════════════════════════════╝
    "
}

# 主函数
main() {
    check_requirements
    build_application
    deploy_application
    health_check
    show_deployment_info
}

# 执行部署
main
