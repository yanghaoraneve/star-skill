# ⭐ 内娱.skill

> 这鱼，这鱼可以，那鱼不行。那鱼为什么不行？那鱼完了。

数字人格创建工坊。将歌手/偶像/明星转化为可对话的 AI Skill。

---

## 理念

受 [colleague-skill](https://github.com/titanwings/colleague-skill) 启发，专注于**公众人物**场景：

- 同事跑了 → [colleague-skill](https://github.com/titanwings/colleague-skill)
- 前任跑了 → [前任.skill](https://github.com/titanwings/ex-skill)
- 喜欢的歌手/明星 → **内娱.skill** ⭐

---

## 数据来源

| 来源 | 内容 | 采集方式 | 备注 |
|------|------|---------|------|
| 网易云音乐 | 歌词（按歌曲ID抓取，支持50首+） | `lyrics_fetcher.py --artist-id` | 接口需登录态认证 |
| B站 | 视频详情 + 评论（标题/播放量/弹幕关键词） | `bilibili_fetcher.py --uid` | 接口需 wbi 签名 |
| 微博 | 动态正文 + 评论（话题/hashtag/互动数据） | `weibo_fetcher.py --uid` | 依赖 weibo-cli |
| 手动上传 | JSON / TXT / 截图 / 粘贴文字 | — | 完全可用，推荐补充 |

> ⚠️ 平台自动采集依赖外部服务稳定性，建议手动上传作为保底。

---

## 示例：采集王澳楠EVE

```bash
# 网易云歌手ID：12968787（王澳楠EVE）
python3 tools/lyrics_fetcher.py --artist-id 12968787 --output star/

# B站 UID：85841036
python3 tools/bilibili_fetcher.py --uid 85841036 --output star/

# 微博 UID：7514873083
python3 tools/weibo_fetcher.py --uid 7514873083 --output star/

# 构建知识库
python3 tools/knowledge_builder.py --knowledge-dir star/
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

## 效果示例

> 输入：`说唱歌手，ENFP，甜丧风格，音乐止痛药，B站签名「大家好我是EVE！你的音乐止痛药！」`

```
用户      ❯ 睡不着
偶像.skill ❯ me too…最近也有点失眠
           要不听听《在看你》？那首挺安静的
           …其实睡不着的时候我会摸着左胸膛
           问自己痛不痛，痛就对了
```

```
用户      ❯ 最近有什么新歌
偶像.skill ❯ 嗯…在准备一首新说唱，还没发！
           「大家好我是EVE！你的音乐止痛药！」
           先听听《请和这样的我恋爱吧》？
```

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

## 安装

```bash
git clone https://github.com/yanghaoraneve/star-skill ~/.openclaw/workspace/skills/create-star
```

---

## 命令参考

| 命令 | 说明 |
|------|------|
| `/create-star` | 启动创建向导 |
| `/list-stars` | 列出所有已创建 |
| `/{slug}` | 调用完整人格 |
| `/star-rollback {slug} {version}` | 回滚版本 |

---

## 参考项目

- [colleague-skill](https://github.com/titanwings/colleague-skill) — 同事 Skill
- [前任.skill](https://github.com/titanwings/ex-skill) — 前任 Skill

---

*内娱.skill · 赛博追星一条龙 ⭐*
