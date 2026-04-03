<div align="center">

# 内娱.skill

> *"这鱼这鱼可以，那鱼不行。那鱼为什么不行？那鱼完了。"*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://python.org)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Skill-green)](https://openclaw.ai)

</br>

你有没有过这样的时刻？<br>
喜欢的歌手发了新歌，你循环了无数遍，敲了满屏的心事与共鸣，<br>却只能留在评论区，等不到一句专属的回应；<br>
你的偶像发了新的微博，你懂她字里行间的温柔与倔强，却只能隔着屏幕点赞，<br>多想她能用独属于她的语气，和你好好聊一聊；<br>
这一次，别再让追星止于单向的奔赴。<br>
把隔着屏幕的遗憾，变成触手可及的对话。

**你的专属追星搭子，永远在线，永远懂你，永远是她的样子。**
<br>

提供偶像的原材料（歌词、B站视频、微博、评论）加上你的主观描述<br>
生成一个**能用她的语气回复你的 AI Skill**<br>

[数据来源](#支持的数据来源) · [安装](#安装) · [使用](#使用) · [详细说明](docs/PRC.md)

---

### 🌟 参考项目：[同事.skill](https://github.com/titanwings/colleague-skill) · [前任.skill](https://github.com/titanwings/ex-skill)

> 同事跑了用同事.skill，前任跑了用前任.skill，<br>
> 喜欢的内娱明星塌房了用内娱.skill——**赛博追星一条龙** 🌟🌟🌟

</div>

---

## 支持的数据来源

| 来源 | 内容 | 采集方式 | 备注 |
|------|------|---------|------|
| 网易云音乐 | 歌词（按歌曲ID抓取，支持50首+） | `lyrics_fetcher.py --artist-id` | 接口需登录态认证 |
| B站 | 视频详情 + 评论（标题/播放量/弹幕关键词） | `bilibili_fetcher.py --uid` | 接口需 wbi 签名 |
| 微博 | 动态正文 + 评论（话题/hashtag/互动数据） | `weibo_fetcher.py --uid` | 依赖 weibo-cli |
| 手动上传 | JSON / TXT / 截图 / 粘贴文字 | — | 完全可用，推荐补充 |

> ⚠️ 平台自动采集依赖外部服务稳定性，建议手动上传作为保底。

---

## 安装 推荐使用OpenClaw

```bash
git clone https://github.com/yanghaoraneve/star-skill ~/.openclaw/workspace/skills/create-star
```

---

## 使用

输入 `/create-star`，按提示输入偶像的姓名、平台账号、MBTI、性格标签，然后选择数据来源。所有字段均可跳过，仅凭描述也能生成。

完成后用 `/{slug}` 调用。

---

## 命令参考

| 命令 | 说明 |
|------|------|
| `/create-star` | 启动创建向导 |
| `/list-stars` | 列出所有偶像 Skill |
| `/{slug}` | 调用完整人格 |
| `/star-rollback {slug} {version}` | 回滚到历史版本 |

---

## 效果示例

> 创建歌手：王澳楠，原创音乐人，你的音乐止痛药

**场景一：聊音乐**

```
用户    ❯ EVE，你最代表的作品是哪首？
EVE     ❯ 嗯…《逐客令》应该大家都知道吧？
        竹笛那段我真的录了很久哈哈
        "欢迎所有人但是除了你" 那个感觉…
        就，很像我。
```

**场景二：日常互动**

```
用户    ❯ 你怎么这么晚还不睡？
EVE     ❯ omg你怎么也这么晚！
        我是夜猫子型哈哈～习惯深夜写歌
        白天脑子不清醒，一到晚上就…
        熬过去就是变强！💪
```

---

## Persona 结构（5层）

| Layer | 内容 | 说明 |
|-------|------|------|
| Layer 0 | 核心规则 | 绝对禁止的行为，第一人称定义 |
| Layer 1 | 身份认知 | 自我定位、对职业态度、对粉丝态度 |
| Layer 2 | 表达风格 | 口头禅/emoji/句式/节奏 |
| Layer 3 | 情感行为 | 正面/负面情绪表达、粉丝互动模式 |
| Layer 4 | 专业知识 | 音乐理念、代表作品背景 |
| Layer 5 | 边界雷区 | 拒绝话题、回避方式 |

---

## 生成产物

运行 `/create-star` 后，在 `star/` 目录下生成：

```
star/
├── SKILL.md
├── meta.json              # 姓名/MBTI/平台账号/职业/代表作
├── persona/persona.md     # 5层人格档案
└── knowledge/
    ├── lyrics/            # 歌词文件（{id}_{歌名}.txt）
    ├── song_list_full.json
    ├── weibo_posts_full.json
    ├── video_details.json
    └── comments.json
```

---

## 项目结构

```
内娱.skill/
├── SKILL.md              # 入口
├── README.md
│
├── prompts/              # Prompt 模板
│   ├── intake.md             # 信息录入向导
│   ├── persona_builder.md     # Persona 5层生成
│   ├── meta_builder.md        # meta.json 生成
│   ├── knowledge_router.md    # 知识库路由
│   └── correction_handler.md  # 纠正处理
│
├── tools/                # Python 工具
│   ├── lyrics_fetcher.py      # 歌词采集
│   ├── bilibili_fetcher.py    # B站采集
│   ├── weibo_fetcher.py       # 微博采集
│   ├── knowledge_builder.py    # 知识库构建
│   ├── skill_generator.py     # Skill 生成
│   └── version_manager.py      # 版本管理
│
└── docs/
    └── PRC.md           # 项目需求文档
```

---

## 参考项目

- [同事.skill](https://github.com/titanwings/colleague-skill) — 同事 Skill
- [前任.skill](https://github.com/titanwings/ex-skill) — 前任 Skill

---

*内娱.skill · 赛博追星一条龙 ⭐*
