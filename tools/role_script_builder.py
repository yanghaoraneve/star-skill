#!/usr/bin/env python3
"""
角色台词本构建器
将台词本数据整合为标准格式，支持：
- 台词本文件（{作品名}_{角色名}台词本.txt）
- 结构化 JSON 输出
- 角色分析
"""

import argparse
import json
import re
from pathlib import Path
from collections import Counter

# ========== 配置 ==========
SUPPORTED_EXTENSIONS = [".txt", ".md"]


def parse_script_file(filepath: Path) -> dict:
    """解析单个台词本文件"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 从文件名提取作品名和角色名
    # 格式：{作品名}_{角色名}台词本.txt 或 {作品名}_{角色名}台词本.md
    name = filepath.stem  # 无扩展名
    if "台词本" in name:
        parts = name.replace("台词本", "").split("_", 1)
        if len(parts) == 2:
            drama_name, role_name = parts[0].strip(), parts[1].strip()
        else:
            drama_name, role_name = parts[0].strip(), "未知角色"
    else:
        drama_name, role_name = name, "未知角色"

    # 提取所有引号内的台词
    quotes = re.findall(r'「([^」]+)」', content)
    stage_directions = re.findall(r'【([^】]+)】', content)

    # 按场景分组（以 【】 或 ===== 分割）
    scenes = []
    if "【" in content:
        scene_blocks = re.split(r'【', content)
        for block in scene_blocks[1:]:  # 跳过第一段空白
            header_match = re.match(r'([^】]+)】(.+)', block, re.DOTALL)
            if header_match:
                scene_header = header_match.group(1).strip()
                scene_content = header_match.group(2).strip()
                scene_quotes = re.findall(r'「([^」]+)」', scene_content)
                scenes.append({
                    "header": scene_header,
                    "quotes": scene_quotes,
                    "count": len(scene_quotes)
                })
    else:
        scenes.append({
            "header": "全文",
            "quotes": quotes,
            "count": len(quotes)
        })

    return {
        "drama_name": drama_name,
        "role_name": role_name,
        "total_quotes": len(quotes),
        "scenes": scenes,
        "all_quotes": quotes,
        "stage_directions": stage_directions
    }


def analyze_role(script_data: dict) -> dict:
    """分析角色特征"""
    all_quotes = script_data["all_quotes"]
    if not all_quotes:
        return {"error": "无台词数据"}

    # 合并所有台词
    full_text = " ".join(all_quotes)

    # 情绪词统计
    emotion_words = {
        "开心": ["开心", "高兴", "喜欢", "爱", "幸福", "太好了", "哈哈", "嘿嘿"],
        "难过": ["难过", "伤心", "哭", "痛苦", "对不起", "委屈"],
        "生气": ["生气", "讨厌", "可恶", "哼", "气", "烦"],
        "害羞": ["害羞", "脸红", "脸红", "羞", "不好意思"],
        "傲娇": ["才不", "哼", "才不是", "本座", "本仙女"],
    }

    emotion_counts = {}
    for emotion, words in emotion_words.items():
        count = sum(full_text.count(w) for w in words)
        if count > 0:
            emotion_counts[emotion] = count

    # 台词长度统计
    quote_lengths = [len(q) for q in all_quotes]
    avg_length = sum(quote_lengths) / len(quote_lengths) if quote_lengths else 0

    # 句式特征
    exclamation_count = sum(1 for q in all_quotes if "！" in q or "!" in q)
    question_count = sum(1 for q in all_quotes if "？" in q or "?" in q)
    ellipsis_count = sum(1 for q in all_quotes if "…" in q or "..." in q)

    # 高频词（简单统计）
    words = re.findall(r'[\u4e00-\u9fa5]+', full_text)
    word_freq = Counter(words)
    top_words = word_freq.most_common(20)

    return {
        "total_lines": len(all_quotes),
        "avg_line_length": round(avg_length, 1),
        "exclamation_ratio": round(exclamation_count / len(all_quotes), 2) if all_quotes else 0,
        "question_ratio": round(question_count / len(all_quotes), 2) if all_quotes else 0,
        "ellipsis_ratio": round(ellipsis_count / len(all_quotes), 2) if all_quotes else 0,
        "emotion_distribution": emotion_counts,
        "top_words": [{"word": w, "count": c} for w, c in top_words if len(w) > 1][:10]
    }


def build_role_script_index(knowledge_dir: Path, output: Path):
    """扫描目录下所有台词本，构建索引"""
    scripts = []
    for ext in SUPPORTED_EXTENSIONS:
        for f in knowledge_dir.glob(f"*{ext}"):
            if "台词本" in f.name or "台词" in f.name:
                print(f"  发现台词本: {f.name}")
                script = parse_script_file(f)
                analysis = analyze_role(script)
                script["analysis"] = analysis
                scripts.append(script)

    index = {
        "total_scripts": len(scripts),
        "total_lines": sum(s["total_quotes"] for s in scripts),
        "scripts": [
            {
                "drama_name": s["drama_name"],
                "role_name": s["role_name"],
                "total_quotes": s["total_quotes"],
                "file": f.name
            }
            for s in scripts
        ]
    }

    # 保存详细数据
    detail_file = output.parent / "role_scripts_full.json"
    with open(detail_file, 'w', encoding='utf-8') as f:
        json.dump(scripts, f, ensure_ascii=False, indent=2)
    print(f"  详细数据 → {detail_file}")

    # 保存索引
    with open(output, 'w', encoding='utf-8') as f:
        json.dump(index, f, ensure_ascii=False, indent=2)
    print(f"  索引 → {output}")

    return index


def main():
    parser = argparse.ArgumentParser(description="角色台词本构建器")
    parser.add_argument("--knowledge-dir", default="knowledge", help="知识库目录")
    args = parser.parse_args()

    kd = Path(args.knowledge_dir)
    if not kd.exists():
        print(f"[ERROR] 目录不存在: {kd}")
        return

    print(f"[角色台词本构建器] 扫描目录: {kd}")
    index = build_role_script_index(kd, kd / "role_scripts_index.json")

    print(f"\n[完成] 共发现 {index['total_scripts']} 个角色台词本，{index['total_lines']} 条台词")


if __name__ == "__main__":
    main()
