---
name: create-star-skill
description: 创建明星/偶像/公众人物数字人格 Skill 的工坊框架。将歌手/偶像转化为可对话的 AI 数字分身。
version: "1.0"
read:
  - README.md
  - prompts/intake.md
user-invocable: true
triggers:
  - /create-star
  - /star-wizard
---

# ⭐ 偶像.skill 工坊

> *「用她的声音说话，用她的方式爱你。」*

---

## 是什么

Star Skill 是一个**数字人格创建框架**，受 [colleague-skill](https://github.com/titanwings/colleague-skill) 启发，专注于**公众人物**场景：

| 跑路了 | 用哪个 |
|--------|--------|
| 同事跑了 | [同事.skill](https://github.com/titanwings/colleague-skill) |
| 前任跑了 | [前任.skill](https://github.com/titanwings/ex-skill) |
| **偶像塌房了** | **⭐ 偶像.skill** |

---

## 快速开始

```bash
# 安装
git clone https://github.com/yanghaoraneve/star-skill ~/.openclaw/workspace/skills/create-star

# 输入 /create-star 开始创建向导
```

或直接用命令行采集数据：

```bash
# 歌词（网易云歌手ID）
python3 tools/lyrics_fetcher.py --artist-id 12968787 --output star/

# B站视频+评论（B站 UID）
python3 tools/bilibili_fetcher.py --uid 85841036 --output star/

# 微博（微博 UID）
python3 tools/weibo_fetcher.py --uid 7514873083 --output star/

# 构建知识库
python3 tools/knowledge_builder.py --knowledge-dir star/
```

---

## 命令参考

| 命令 | 说明 |
|------|------|
| `/create-star` | 启动创建向导 |
| `/list-stars` | 列出所有偶像 Skill |
| `/{slug}` | 调用完整人格 |
| `/star-rollback {slug} {version}` | 回滚版本 |
| `/delete-star {slug}` | 删除 |

---

## 生成产物结构

```
{slug}/
├── SKILL.md              # 技能入口
├── meta.json             # 人物元信息
├── persona/persona.md    # 5层人格档案
└── knowledge/
    ├── lyrics/           # 歌词文件
    ├── song_list_full.json
    ├── weibo_posts_full.json
    ├── video_details.json
    └── comments.json
```

详见 [README.md](README.md) · [docs/PRC.md](docs/PRC.md)
