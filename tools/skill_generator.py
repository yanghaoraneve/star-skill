#!/usr/bin/env python3
"""
Skill 文件生成器
根据模板生成完整的 Skill 目录
"""

import argparse
import json
import shutil
from pathlib import Path
from datetime import datetime

# ========== 配置 ==========
TEMPLATE_DIR = Path(__file__).parent.parent / "TEMPLATES"


def load_template(name: str) -> str:
    """加载模板文件"""
    tpl = TEMPLATE_DIR / name
    if tpl.exists():
        return tpl.read_text(encoding='utf-8')
    return ""


def generate_persona(data: dict, template: str = "persona.md") -> str:
    """生成 persona.md"""
    tpl = load_template(template)
    # 简单替换 {placeholder}
    for k, v in data.items():
        if isinstance(v, (str, int, float)):
            tpl = tpl.replace(f"{{{k}}}", str(v))
        elif isinstance(v, list):
            # 表格处理
            pass
    return tpl


def generate_skill(slug: str, data: dict, output_dir: Path):
    """生成完整的 Skill 目录"""
    skill_dir = output_dir / slug
    persona_dir = skill_dir / "persona"
    knowledge_dir = skill_dir / "knowledge"
    frontend_dir = skill_dir / "frontend"

    # 创建目录
    for d in [persona_dir, knowledge_dir, frontend_dir]:
        d.mkdir(parents=True, exist_ok=True)

    # 生成 meta.json
    meta = data.get("meta", {})
    meta["slug"] = slug
    meta["created_at"] = datetime.now().strftime("%Y-%m-%d")
    with open(skill_dir / "meta.json", 'w', encoding='utf-8') as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

    # 生成 persona.md
    persona_content = data.get("persona_content", "")
    with open(persona_dir / "persona.md", 'w', encoding='utf-8') as f:
        f.write(persona_content)

    # 生成 SKILL.md
    skill_md = f"""---
name: {slug}
description: {meta.get('note', '数字人格 Skill')}
version: "1.0"
read:
  - persona/persona.md
  - meta.json
user-invocable: true
triggers:
  - /{slug}
---

# {meta.get('name', slug)} 数字人格

> 「{meta.get('signature', '')}」

## 基本信息

- **真实姓名**: {meta.get('name', '')}
- **艺名**: {meta.get('stage_name', '')}
- **MBTI**: {meta.get('basic_info', {}).get('mbti', '')}
- **生日**: {meta.get('basic_info', {}).get('birth_date', '')}

## 使用方式

| 命令 | 说明 |
|------|------|
| /{slug} | 调用完整人格 |
| /{slug}-persona | 仅人格部分 |

## 知识库

详见 persona/persona.md 中的知识库访问说明。
"""
    with open(skill_dir / "SKILL.md", 'w', encoding='utf-8') as f:
        f.write(skill_md)

    print(f"[完成] Skill 已生成: {skill_dir}/")
    print(f"  ├── SKILL.md")
    print(f"  ├── meta.json")
    print(f"  ├── persona/persona.md")
    print(f"  ├── knowledge/")
    print(f"  └── frontend/")


def main():
    parser = argparse.ArgumentParser(description="Skill 文件生成器")
    parser.add_argument("--slug", required=True, help="Skill slug（英文标识）")
    parser.add_argument("--meta", required=True, help="meta.json 文件路径")
    parser.add_argument("--persona", required=True, help="persona.md 文件路径")
    parser.add_argument("--output", default="examples", help="输出目录")
    args = parser.parse_args()

    output_dir = Path(args.output)

    # 加载数据
    with open(args.meta, 'r', encoding='utf-8') as f:
        meta = json.load(f)

    with open(args.persona, 'r', encoding='utf-8') as f:
        persona_content = f.read()

    data = {
        "meta": meta,
        "persona_content": persona_content
    }

    generate_skill(args.slug, data, output_dir)


if __name__ == "__main__":
    main()
