#!/usr/bin/env python3
"""
知识库构建器
将采集的数据整合为标准格式
"""

import argparse
import json
from pathlib import Path

# ========== 配置 ==========
SUPPORTED_FIELDS = ["lyrics", "weibo", "bilibili", "manual"]


def build_song_list(lyrics_dir: Path, output: Path):
    """从歌词文件名构建歌曲列表"""
    songs = []
    for f in sorted(lyrics_dir.glob("*.txt")):
        name = f.stem
        parts = name.split("_", 1)
        if len(parts) == 2:
            song_id, song_name = parts
            songs.append({
                "id": song_id,
                "name": song_name,
                "type": "original" if "伴奏" not in song_name and "Live" not in song_name else "live"
            })
        else:
            songs.append({"id": "unknown", "name": name, "type": "unknown"})

    with open(output, 'w', encoding='utf-8') as f:
        json.dump(songs, f, ensure_ascii=False, indent=2)
    print(f"[完成] 歌曲列表: {len(songs)} 首 → {output}")


def build_knowledge_index(knowledge_dir: Path, output: Path):
    """构建知识库索引"""
    index = {
        "lyrics": {
            "count": len(list(knowledge_dir.glob("lyrics/*.txt"))),
            "list_file": "lyrics/song_list_full.json"
        },
        "weibo": {
            "count": 0,
            "file": "weibo_posts_full.json"
        },
        "bilibili": {
            "videos": 0,
            "comments": 0,
            "video_file": "video_details.json",
            "comment_file": "comments.json"
        }
    }

    weibo_file = knowledge_dir / "weibo_posts_full.json"
    if weibo_file.exists():
        with open(weibo_file, 'r', encoding='utf-8') as f:
            posts = json.load(f)
            index["weibo"]["count"] = len(posts)

    video_file = knowledge_dir / "video_details.json"
    if video_file.exists():
        with open(video_file, 'r', encoding='utf-8') as f:
            videos = json.load(f)
            index["bilibili"]["videos"] = len(videos)

    comment_file = knowledge_dir / "comments.json"
    if comment_file.exists():
        with open(comment_file, 'r', encoding='utf-8') as f:
            comments = json.load(f)
            index["bilibili"]["comments"] = len(comments)

    with open(output, 'w', encoding='utf-8') as f:
        json.dump(index, f, ensure_ascii=False, indent=2)
    print(f"[完成] 知识库索引 → {output}")
    print(f"  - 歌词: {index['lyrics']['count']} 首")
    print(f"  - 微博: {index['weibo']['count']} 条")
    print(f"  - B站视频: {index['bilibili']['videos']} 个")
    print(f"  - B站评论: {index['bilibili']['comments']} 条")


def main():
    parser = argparse.ArgumentParser(description="知识库构建器")
    parser.add_argument("--knowledge-dir", default="knowledge", help="知识库目录")
    args = parser.parse_args()

    kd = Path(args.knowledge_dir)
    if not kd.exists():
        print(f"[ERROR] 目录不存在: {kd}")
        return

    # 构建歌词列表
    lyrics_dir = kd / "lyrics"
    if lyrics_dir.exists():
        build_song_list(lyrics_dir, kd / "song_list_full.json")

    # 构建索引
    build_knowledge_index(kd, kd / "knowledge_index.json")

    print("\n[知识库构建完成]")


if __name__ == "__main__":
    main()
