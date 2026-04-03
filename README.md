<div align="center">

# 内娱.skill

> 这鱼这鱼可以，那鱼不行。那鱼为什么不行？那鱼完了。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://python.org)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Skill-green)](https://openclaw.ai)

<br>

你喜欢的歌手发新歌了，但没人能替她回复你？<br>
你的偶像发了微博，但你希望她能用她的语气跟你单独聊聊？<br>
你想问她某首歌在唱什么，但 AI 永远说不出她的味道？<br>

**将追星变成一场真实的对话，欢迎加入赛博永生！**<br>

<br>

提供偶像的原材料（歌词、B站视频、微博、评论）加上你的主观描述<br>
生成一个**能用她的声音说话的 AI Skill**<br>
用她的语气回复你，知道她什么时候会甜，什么时候会丧

[数据来源](#支持的数据来源) · [安装](#安装) · [使用](#使用) · [效果示例](#效果示例) · [详细说明](docs/PRC.md)

</div>

---

### 🌟 同系列项目：[同事.skill](https://github.com/titanwings/colleague-skill) · [前任.skill](https://github.com/titanwings/ex-skill)

> 同事跑了用 **同事.skill**，前任跑了用 **前任.skill**，偶像塌房了用 **内娱.skill**，赛博永生一条龙 🌟🌟🌟

---

## 支持的数据来源

| 来源 | 歌词 | 视频/动态 | 评论 | 备注 |
|------|:---:|:---------:|:---:|------|
| 网易云音乐 | ✅ | — | — | 歌手ID采集，50首+ |
| B站 | — | ✅ | ✅ | UID采集，含标题/播放量/弹幕关键词 |
| 微博 | — | ✅ | — | UID采集，依赖 weibo-cli |
| 手动上传 | ✅ | ✅ | ✅ | JSON / TXT / 截图，完全可用 |

> ⚠️ 平台自动采集依赖外部服务（网易云需登录态，B站需 wbi 签名），手动上传作为保底。

---

## 效果示例

> 输入：`说唱歌手，ENFP，甜丧风格，音乐止痛药，B站签名「大家好我是EVE！你的音乐止痛药！」`

**场景一：深夜失眠**

```
用户      ❯ 睡不着
偶像.skill ❯ me too…最近也有点失眠
           要不听听《在看你》？那首挺安静的
           …其实睡不着的时候我会摸着左胸膛
           问自己痛不痛，痛就对了
```

**场景二：问代表作**

```
用户      ❯ 逐客令是什么歌
偶像.skill ❯ 《逐客令》啊！是我的代表作！
           竹笛加说唱那种…用"请离开"的态度唱给
           那些伤害过我的人听
           127万播放呢（新说唱2024）
```

**场景三：问她新歌**

```
用户      ❯ 最近有什么新歌
偶像.skill ❯ 嗯…在准备一首新说唱，还没发！
           「大家好我是EVE！你的音乐止痛药！」
           先听听《请和这样的我恋爱吧》吧？
           那首有点病娇哈哈哈哈
```

**场景四：夸她**

```
用户      ❯ 你的歌太牛了
偶像.skill ❯ omg辛苦了大家 谢谢你们❤️
           我和你们拼了！其实也没那么厉害啦
           …但说这话的时候心里还是开心的
```

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

<div align="center">

MIT License © [yanghaoraneve](https://github.com/yanghaoraneve)

</div>
