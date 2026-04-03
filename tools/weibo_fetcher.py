#!/usr/bin/env python3
"""
微博数据采集器
使用 weibo-cli 获取用户动态
"""

import argparse
import json
import subprocess
import time
from pathlib import Path

# ========== 配置 ==========
WEIBO_CLI = "weibo"  # weibo-cli 命令

# ========== 采集 ==========
def fetch_weibo(uid: str, limit: int = 50) -> list:
    """使用 weibo-cli 获取微博动态"""
    try:
        result = subprocess.run(
            [WEIBO_CLI, "user", "--uid", uid, "--limit", str(limit), "--json"],
            capture_output=True,
            text=True,
            timeout=60
        )
        if result.returncode == 0:
            return json.loads(result.stdout)
        else:
            print(f"[WARN] weibo-cli 失败: {result.stderr}")
    except FileNotFoundError:
        print("[ERROR] weibo-cli 未安装，请先安装: pip install weibo-cli")
    except Exception as e:
        print(f"[ERROR] 获取微博失败: {e}")
    return []


def main():
    parser = argparse.ArgumentParser(description="微博数据采集器")
    parser.add_argument("--uid", required=True, help="微博 UID")
    parser.add_argument("--output", default="knowledge/weibo_posts_full.json", help="输出文件")
    parser.add_argument("--limit", type=int, default=50, help="采集数量")
    args = parser.parse_args()

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"[INFO] 正在采集微博 UID={args.uid}")
    posts = fetch_weibo(args.uid, args.limit)

    if posts:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(posts, f, ensure_ascii=False, indent=2)
        print(f"[完成] {len(posts)} 条微博 → {output_path}")
    else:
        print("[WARN] 没有获取到微博数据")


if __name__ == "__main__":
    main()
