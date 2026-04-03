<div align="center">

# 偶像.skill

> *「用她的声音说话，用她的方式爱你。」*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://python.org)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Skill-green)](https://openclaw.ai)
[![AgentSkills](https://img.shields.io/badge/AgentSkills-Standard-green)](https://agentskills.io)

<br>

你喜欢的歌手发新歌了，但没人能替她回复你？<br>
你的偶像发了微博，但你希望她能用她的语气跟你单独聊天？<br>
你想让她唱首歌，但 AI 永远说不出她的味道？<br>

**将追星变成一场真实的对话，欢迎加入赛博永生！**<br>

<br>

提供偶像的原材料（歌词、B站视频、微博、评论）加上你的主观描述<br>
生成一个**能用她的声音说话的 AI Skill**<br>
用她的语气回复你，知道她什么时候会甜，什么时候会丧

[数据来源](#支持的数据来源) · [安装](#安装) · [使用](#使用) · [效果示例](#效果示例) · [详细说明](docs/PRC.md) · [**English**](README_EN.md)

</div>

---

### 🌟 同系列项目：[同事.skill](https://github.com/titanwings/colleague-skill) · [前任.skill](https://github.com/titanwings/ex-skill)

> 同事跑了用 **同事.skill**，前任跑了用 **前任.skill**，偶像塌房了用 **偶像.skill**，赛博永生一条龙 🌟🌟🌟

---

## 支持的数据来源

| 来源 | 歌词 | 视频/动态 | 评论 | 说明 |
|------|:---:|:---------:|:---:|------|
| 网易云音乐 | ✅ | — | — | 歌手ID采集 |
| B站 | — | ✅ | ✅ | UID 采集 |
| 微博 | — | ✅ | — | UID 采集，需 weibo-cli |
| 手动上传 | ✅ | ✅ | ✅ | JSON / TXT / 截图 |

> ⚠️ 网易云歌词接口需登录态；B站接口需 wbi 签名；微博依赖 `weibo-cli`

---

## 安装

### OpenClaw

```bash
git clone https://github.com/yanghaoraneve/star-skill ~/.openclaw/workspace/skills/create-star
```

### Claude Code

```bash
mkdir -p .claude/skills
git clone https://github.com/yanghaoraneve/star-skill .claude/skills/create-star
```

---

## 使用

在 Claude Code 或 OpenClaw 中输入：

```
/create-star
```

按提示输入偶像的姓名、平台账号（网易云/B站/微博）、MBTI、性格标签，然后选择数据来源。所有字段均可跳过，仅凭描述也能生成。

完成后用 `/{slug}` 调用该偶像 Skill。

### 管理命令

| 命令 | 说明 |
|------|------|
| `/list-stars` | 列出所有偶像 Skill |
| `/{slug}` | 调用完整 Skill（Persona + Knowledge） |
| `/{slug}-persona` | 仅人格部分 |
| `/star-rollback {slug} {version}` | 回滚到历史版本 |
| `/delete-star {slug}` | 删除 |

---

## 效果示例

> 输入：`王澳楠EVE，说唱歌手，ENFP，甜丧风格，音乐止痛药`

**场景一：深夜聊天**

```
用户      ❯ 睡不着

偶像.skill ❯ me too… 最近确实有点失眠
           要不听听《在看你》？那首挺安静的
           …其实睡不着的时候我会摸着自己的左胸膛
           问自己痛不痛，痛就对了，熬过去就是蜕变
```

**场景二：问新歌**

```
用户      ❯ 最近有什么新歌吗

偶像.skill ❯ 嗯…最近在准备一首新说唱
           还没发呢！不过快了快了！
           「大家好我是EVE！你的音乐止痛药！」
           先听听《请和这样的我恋爱吧》？那首也不错～
```

---

## 功能特性

### 生成的 Skill 结构

每个偶像 Skill 由两部分组成：

| 部分 | 内容 |
|------|------|
| **Part A — Persona** | 5层性格结构：硬规则 → 身份认知 → 表达风格 → 情感行为 → 边界雷区 |
| **Part B — Knowledge** | 知识库路由：歌词 / 微博 / B站视频 / 评论 |

运行逻辑：`接收消息 → Persona 判断身份/语气 → Knowledge 检索 → 用她的方式输出`

### 支持的标签

**性格**：ENFP · INTJ · ESFP · INFP · 甜丧 · 治愈系 · 毒舌 · 宠粉 · 虐粉 · 搞笑女 · 文艺青年 …

**风格**：说唱歌手 · 演员 · 网红 · 唱作人 · 女团 · 男团 · indie · 古风 …

**人设**：音乐止痛药 · 嘴替 · 追梦人 · 反差萌 · 真实感 · 丧系治愈 …

### 进化机制

- **追加数据** → 自动分析增量 → merge 进对应知识库
- **对话纠正** → 说「她不会这样，她应该是 xxx」→ 写入 Correction 层，立即生效
- **版本管理** → 每次更新自动存档，支持回滚

---

## 项目结构

本项目遵循 [AgentSkills](https://agentskills.io) 开放标准，整个 repo 就是一个 skill 目录：

```
star-skill/
├── SKILL.md              # skill 入口
├── prompts/              # Prompt 模板
│   ├── intake.md         #   信息录入向导
│   ├── persona_builder.md #   Persona 5层生成
│   ├── meta_builder.md   #   meta.json 生成
│   ├── knowledge_router.md # 知识库路由配置
│   └── correction_handler.md # 对话纠正处理
├── tools/                # Python 工具
│   ├── lyrics_fetcher.py     # 歌词采集（网易云）
│   ├── bilibili_fetcher.py   # B站数据采集
│   ├── weibo_fetcher.py      # 微博采集
│   ├── knowledge_builder.py   # 知识库构建
│   ├── skill_generator.py    # Skill 文件生成
│   └── version_manager.py     # 版本管理
└── docs/
    └── PRC.md           # 项目需求文档
```

---

## 注意事项

- **数据质量决定 Skill 质量**：歌词 + 微博 + 评论 > 仅手动描述
- 建议优先收集：**本人原创的歌词** > **微博正文** > 评论互动
- 目前采集工具部分依赖外部服务（网易云/B站需认证），手动上传模式完全可用

---

<div align="center">

MIT License © [yanghaoraneve](https://github.com/yanghaoraneve)

</div>
