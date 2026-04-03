---
name: create-star-skill
description: 创建明星/偶像/公众人物数字人格 Skill 的工坊框架。将歌手/偶像/明星转化为可对话的 AI 数字分身。
version: "1.0"
read:
  - README.md
  - prompts/intake.md
user-invocable: true
triggers:
  - /create-star
  - /star-wizard
---

# ⭐ 内娱.skill 工坊

> 这鱼这鱼可以，那鱼不行。那鱼为什么不行？那鱼完了。

---

## 是什么

内娱.skill 是一个**数字人格创建工坊**，将喜欢的歌手/明星转化为可对话的 AI Skill。

| 跑路了 | 用哪个 |
|--------|--------|
| 同事跑了 | [同事.skill](https://github.com/titanwings/colleague-skill) |
| 前任跑了 | [前任.skill](https://github.com/titanwings/ex-skill) |
| **喜欢的歌手/明星** | **⭐ 内娱.skill** |

---

## 快速开始

```bash
# 安装
git clone https://github.com/yanghaoraneve/star-skill ~/.openclaw/workspace/skills/create-star

# 输入 /create-star 开始创建向导
```

---

## 命令参考

| 命令 | 说明 |
|------|------|
| `/create-star` | 启动创建向导 |
| `/list-stars` | 列出所有偶像 Skill |
| `/{slug}` | 调用完整人格 |
| `/star-rollback {slug} {version}` | 回滚版本 |

---

## 生成产物

```
{slug}/
├── SKILL.md
├── meta.json
├── persona/persona.md     # 5层人格档案
└── knowledge/
    ├── lyrics/            # 歌词文件
    ├── song_list_full.json
    ├── weibo_posts_full.json
    ├── video_details.json
    └── comments.json
```

详见 [README.md](README.md) · [docs/PRC.md](docs/PRC.md)
