#!/usr/bin/env python3
"""
B站数据采集器
采集视频详情 + 评论
"""

import argparse
import json
import time
import urllib.request
import urllib.parse
from pathlib import Path

# ========== 配置 ==========
BILIBILI_API = "https://api.bilibili.com/x/space/arc/search"
VIDEO_DETAIL_API = "https://api.bilibili.com/x/web-interface/view"
COMMENT_API = "https://api.bilibili.com/x/v2/reply"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; StarSkill/1.0)",
    "Referer": "https://www.bilibili.com/"
}

# ========== 采集 ==========
def fetch_videos(mid: str, limit: int = 20) -> list:
    """获取用户视频列表"""
    videos = []
    pn = 1
    ps = 30

    while len(videos) < limit or limit == 0:
        url = f"{BILIBILI_API}?mid={mid}&pn={pn}&ps={ps}&order=pubdate"
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode('utf-8'))
            if data.get("code") != 0:
                break
            vlist = data["data"]["list"]["vlist"]
            if not vlist:
                break
            for v in vlist:
                videos.append({
                    "bvid": v["bvid"],
                    "title": v["title"],
                    "desc": v["description"],
                    "play_count": v["play"],
                    "comment_count": v["comment"],
                    "pubdate": time.strftime("%Y-%m-%d", time.localtime(v["pubdate"]))
                })
                if limit > 0 and len(videos) >= limit:
                    break
            pn += 1
            time.sleep(0.3)
        except Exception as e:
            print(f"[WARN] 获取视频列表失败: {e}")
            break

    return videos


def fetch_video_detail(bvid: str) -> dict:
    """获取视频详情（含分P）"""
    url = f"{VIDEO_DETAIL_API}?bvid={bvid}"
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode('utf-8'))
        if data.get("code") == 0:
            d = data["data"]
            return {
                "bvid": bvid,
                "title": d["title"],
                "desc": d["desc"],
                "play_count": d["stat"]["view"],
                "like_count": d["stat"]["like"],
                "coin_count": d["stat"]["coin"],
                "favorite_count": d["stat"]["favorite"],
                "share_count": d["stat"]["share"],
                "comment_count": d["stat"]["reply"],
                "duration": d["duration"],
                "pubdate": time.strftime("%Y-%m-%d", time.localtime(d["pubdate"]))
            }
    except Exception as e:
        print(f"[WARN] 获取视频详情失败 {bvid}: {e}")
    return {}


def fetch_comments(bvid: str, limit: int = 20) -> list:
    """获取视频评论"""
    comments = []
    pn = 1
    while len(comments) < limit:
        url = f"{COMMENT_API}?type=1&oid={bvid}&pn={pn}&ps=20&sort=2"
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode('utf-8'))
            if data.get("code") != 0:
                break
            replies = data["data"].get("replies") or []
            if not replies:
                break
            for r in replies:
                comments.append({
                    "text": r["content"]["message"],
                    "author": r["member"]["uname"],
                    "like_count": r["like"],
                    "ctime": time.strftime("%Y-%m-%d", time.localtime(r["ctime"]))
                })
                if len(comments) >= limit:
                    break
            pn += 1
            time.sleep(0.2)
        except Exception as e:
            break
    return comments


def main():
    parser = argparse.ArgumentParser(description="B站数据采集器")
    parser.add_argument("--uid", required=True, help="B站 UID")
    parser.add_argument("--output", default="knowledge", help="输出目录")
    parser.add_argument("--video-limit", type=int, default=20, help="采集视频数量")
    parser.add_argument("--comment-limit", type=int, default=20, help="每视频评论数")
    args = parser.parse_args()

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"[INFO] 正在采集 B站 UID={args.uid}")
    videos = fetch_videos(args.uid, args.video_limit)
    print(f"[INFO] 获取到 {len(videos)} 个视频")

    video_details = []
    all_comments = []

    for i, v in enumerate(videos):
        print(f"[{i+1}/{len(videos)}] 《{v['title']}》... ", end="", flush=True)

        # 获取详情
        detail = fetch_video_detail(v["bvid"])
        if detail:
            video_details.append(detail)

            # 获取评论
            comments = fetch_comments(v["bvid"], args.comment_limit)
            for c in comments:
                c["video_bvid"] = v["bvid"]
                c["video_title"] = v["title"]
            all_comments.extend(comments)
            print(f"✅ 播放:{detail.get('play_count',0)} 评论:{len(comments)}")
        else:
            print("⚠️ 详情获取失败")

        if i < len(videos) - 1:
            time.sleep(0.5)

    # 保存
    with open(output_dir / "video_details.json", 'w', encoding='utf-8') as f:
        json.dump(video_details, f, ensure_ascii=False, indent=2)

    with open(output_dir / "comments.json", 'w', encoding='utf-8') as f:
        json.dump(all_comments, f, ensure_ascii=False, indent=2)

    print(f"\n[完成] 视频详情: {len(video_details)} 条 → {output_dir}/video_details.json")
    print(f"[完成] 评论: {len(all_comments)} 条 → {output_dir}/comments.json")


if __name__ == "__main__":
    main()
