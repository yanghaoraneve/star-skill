# ⭐ Star Skill Framework

> 「用她的声音说话，用她的方式爱你。」

数字人格创建工坊。将歌手/偶像/公众人物转化为可对话的 AI Skill。

## 理念

受 [colleague-skill](https://github.com/titanwings/colleague-skill) 启发，专注于**公众人物**场景：

- 同事跑了 → [colleague-skill](https://github.com/titanwings/colleague-skill)
- 前任跑了 → [ex-skill](https://github.com/titanwings/ex-skill)
- 喜欢的歌手 → **star-skill** ⭐

## 架构

```
star-skill/
├── prompts/          tools/           docs/
├── intake.md       lyrics_fetcher.py  PRC.md
├── persona.md      bilibili_fetcher.py
├── meta.json       weibo_fetcher.py
└── correction       version_manager.py

用户输入 → intake向导 → 数据采集 → persona构建 → 对话调校
```

## 数据来源

| 来源 | 内容 | 采集方式 |
|------|------|---------|
| 网易云音乐 | 歌词（50首+） | `lyrics_fetcher.py` |
| B站 | 视频详情 + 评论 | `bilibili_fetcher.py` |
| 微博 | 动态 | `weibo_fetcher.py` |

> ⚠️ 网易云歌词接口需认证，B站接口需 wbi 签名。微博采集依赖 `weibo-cli`。

## Persona 结构（5层）

| Layer | 内容 |
|-------|------|
| Layer 0 | 核心规则 |
| Layer 1 | 身份认知 |
| Layer 2 | 表达风格 |
| Layer 3 | 情感行为 |
| Layer 4 | 专业知识 |
| Layer 5 | 边界雷区 |

## 生成产物

运行 `/create-star` 后，在 `star/` 目录下生成：

```
star/
├── SKILL.md
├── meta.json
├── persona/persona.md
├── knowledge/
│   ├── lyrics/
│   ├── song_list_full.json
│   ├── weibo_posts_full.json
│   ├── video_details.json
│   └── comments.json
└── frontend/
```

## 参考项目

- [colleague-skill](https://github.com/titanwings/colleague-skill) — 同事 Skill
- [ex-skill](https://github.com/titanwings/ex-skill) — 前任 Skill

---

*Star Skill Framework · 赛博追星一条龙 ⭐*
