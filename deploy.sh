#!/bin/bash

# MCP 服务器 Docker 部署脚本

echo "开始部署 MCP 服务器..."

# 1. 创建日志目录
echo "1. 创建日志目录..."
sudo mkdir -p /data/logs/stock_arbitrade_notify_mcp
sudo chmod 755 /data/logs/stock_arbitrade_notify_mcp

# 2. 检查 config.json 是否存在
if [ ! -f "config.json" ]; then
    echo "错误: config.json 文件不存在"
    echo "请创建 config.json 文件并配置 SCT_KEY"
    exit 1
fi

# 3. 构建并启动容器
echo "2. 构建 Docker 镜像..."
docker-compose build

echo "3. 启动容器..."
docker-compose up -d

# 4. 检查容器状态
echo "4. 检查容器状态..."
sleep 3
docker-compose ps

echo ""
echo "部署完成！"
echo ""
echo "服务地址: http://localhost:4567/sse"
echo "日志位置: /data/logs/stock_arbitrade_notify_mcp/"
echo ""
echo "查看日志: docker-compose logs -f"
echo "停止服务: docker-compose down"
