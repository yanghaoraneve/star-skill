#!/usr/bin/env python3
"""
歌词采集器 - 网易云音乐
根据歌手ID抓取所有歌曲歌词
"""

import argparse
import json
import os
import re
import time
import urllib.request
import urllib.parse
from pathlib import Path

# ========== 配置 ==========
NETEASE_API = "https://music.163.com/api/artists/{artist_id}/songs"
SONG_DETAIL_API = "https://music.163.com/api/v1/resource/comments/R_SO_4_{song_id}?limit=1&offset=0"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; StarSkill/1.0)",
    "Referer": "https://music.163.com/"
}

# ========== 采集歌词 ==========
def fetch_songs_by_artist(artist_id: str, output_dir: str):
    """根据歌手ID获取歌曲列表"""
    url = NETEASE_API.format(artist_id=artist_id)
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode('utf-8'))
    except Exception as e:
        print(f"[ERROR] 获取歌曲列表失败: {e}")
        return []

    songs = []
    if "hotSongs" in data:
        for song in data["hotSongs"]:
            songs.append({
                "id": str(song["id"]),
                "name": song["name"],
                "album": song.get("album", {}).get("name", "未知专辑"),
                "duration": song.get("duration", 0),
            })
    return songs


def fetch_lyrics(song_id: str) -> str:
    """获取歌曲歌词"""
    # 歌词在歌曲详情页
    url = f"https://music.163.com/api/song/{song_id}/lyrics"
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode('utf-8'))
        if data.get("code") == 200 and data.get("lrc"):
            lrc_text = data["lrc"].get("lyric", "")
            # 去除时间标签 [00:00.00]
            lyrics = re.sub(r'\[.*?\]', '', lrc_text).strip()
            return lyrics
    except Exception as e:
        print(f"[WARN] 获取歌词失败 {song_id}: {e}")
    return ""


def main():
    parser = argparse.ArgumentParser(description="网易云歌词采集器")
    parser.add_argument("--artist-id", required=True, help="网易云歌手ID")
    parser.add_argument("--output", default="knowledge/lyrics", help="输出目录")
    parser.add_argument("--limit", type=int, default=0, help="限制采集数量（0=全部）")
    args = parser.parse_args()

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"[INFO] 正在获取歌曲列表，artist_id={args.artist_id}")
    songs = fetch_songs_by_artist(args.artist_id, args.output)
    if not songs:
        print("[ERROR] 没有获取到歌曲")
        return

    print(f"[INFO] 获取到 {len(songs)} 首歌曲")

    if args.limit > 0:
        songs = songs[:args.limit]

    song_list = []
    for i, song in enumerate(songs):
        print(f"[{i+1}/{len(songs)}] 采集《{song['name']}》... ", end="", flush=True)
        lyrics = fetch_lyrics(song["id"])

        filename = f"{song['id']}_{song['name']}.txt"
        filepath = output_dir / filename
        filepath.write_text(lyrics, encoding='utf-8')

        song_list.append({
            "id": song["id"],
            "name": song["name"],
            "album": song["album"],
            "has_lyrics": bool(lyrics.strip())
        })
        print(f"✅ {'有歌词' if lyrics.strip() else '纯音乐/无歌词'}")

        if i < len(songs) - 1:
            time.sleep(0.3)

    # 写入歌曲列表
    list_file = output_dir.parent / "song_list_full.json"
    with open(list_file, 'w', encoding='utf-8') as f:
        json.dump(song_list, f, ensure_ascii=False, indent=2)

    print(f"\n[完成] 歌词已保存到 {output_dir}/")
    print(f"[完成] 歌曲列表已保存到 {list_file}")


if __name__ == "__main__":
    main()
