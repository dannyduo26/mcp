'''
Author: duyulin@kingsoft.com
Date: 2025-11-24 18:05:08
LastEditors: duyulin@kingsoft.com
LastEditTime: 2025-12-05 16:52:41
'''
import os
import logging
from typing import Any, Dict, List
from fastmcp import FastMCP
import httpx
import jisilu_mcp_server as j
import wechat_server as w

# 配置日志（如果在 Docker 环境中运行）
try:
    from logging_config import setup_logging
    logger = setup_logging()
except Exception:
    # 如果日志配置失败，使用基本配置
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger('mcp_server')

# 初始化 MCP 服务器
mcp = FastMCP("arbitrage-suite")

@mcp.tool(description="获取QDII溢价套利候选列表")
def fetch_qdii_candidates(threshold: float = 2.0) -> str:
    """
    获取QDII溢价套利候选列表

    Args:
        threshold: 溢价率阈值，默认为2.0%
    """
    import json
    logger.info(f"调用 fetch_qdii_candidates, threshold={threshold}")
    result = j.qdii_candidates(threshold)
    logger.info(f"获取到 {len(result)} 只候选基金")
    return json.dumps(result, ensure_ascii=False)

@mcp.tool(description="发送微信通知")
async def send_wechat(title: str, desp: str) -> str:
    """
    发送微信通知

    Args:
        title: 通知的标题
        desp: 通知的详细内容
    """
    import json
    logger.info(f"调用 send_wechat, title={title}")
    result = await w.send_wechat(title, desp)
    logger.info(f"微信通知发送完成: {result.get('status_code', 'unknown')}")
    return json.dumps(result, ensure_ascii=False)

if __name__ == "__main__":
    # 获取端口，默认使用 4567
    port = int(os.getenv("PORT", 4567))
    
    logger.info(f"启动 MCP 服务器: arbitrage-suite")
    logger.info(f"监听端口: {port}")
    logger.info(f"传输协议: SSE")
    
    # 以 SSE 模式启动服务器，使其支持 HTTP 远程调用
    mcp.run(
        transport="sse", 
        host="0.0.0.0", 
        port=port
    )