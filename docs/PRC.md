# Star Skill Framework · 项目需求文档 (PRD)

> 数字人格 Skill 创建工坊 · v1.0

---

## 1. 背景与目标

### 1.1 问题陈述

- 喜欢的歌手/偶像/网红每天发内容，但 AI 无法用她的语气和你聊天
- 现有 AI 人格项目（如 colleague-skill）针对职场场景，不适用于公众人物
- 无法快速构建一个「用她的声音说话」的 AI 分身

### 1.2 目标

**构建一个通用框架**，让用户只需提供：
- 人物基本信息（姓名/平台/MBTI等）
- 数据来源（网易云/B站/微博等）
- 可选：补充描述

**框架自动完成**：
- 数据采集
- Persona 构建（Layer 0-5）
- 知识库路由
- Skill 文件生成
- 版本管理

### 1.3 成功标准

| 指标 | 目标 |
|------|------|
| 创建新 Skill 耗时 | ≤ 30 分钟（纯手动除外） |
| Persona 生成质量 | 5个用户测试，至少4人认为「像本人」|
| 支持平台 | 网易云 / B站 / 微博（≥3个）|
| 命令接口 | ≥5 个 |

---

## 2. 产品功能

### 2.1 核心功能

#### F1: 信息录入向导
- 对话式收集基本信息
- 支持跳过字段，仅描述也可生成
- 输出结构化 JSON

#### F2: 数据采集工具
- 网易云歌词采集（按歌手ID）
- B站视频+评论采集（按UID）
- 微博动态采集（按UID）
- 均支持命令行调用

#### F3: Persona 构建
- 基于歌词/微博/B站评论自动分析
- 5层人格结构（Layer 0-5）
- 识别：口头禅/情绪模式/句式特点/emoji偏好
- 结合人工描述填补空白

#### F4: 知识库路由
- 歌词/微博/视频/评论分类索引
- AI 查询时自动路由到对应文件
- 标准化 JSON 格式

#### F5: 版本管理与回滚
- 每次更新自动快照
- 支持回滚到任意历史版本
- 纠正记录追踪

#### F6: 对话调校
- 用户说「她不会这样」→「纠正处理器」生效
- 分类处理（A/B/C/D 四种类型）
- 立即生效 + 版本存档

### 2.2 边缘情况

| 场景 | 处理方式 |
|------|---------|
| 歌词采集失败 | 跳过该首，保留已有，记录失败列表 |
| 歌手改名/换号 | meta.json 中记录历史UID |
| 数据不足 | 降低 Persona 生成质量，但不阻止生成 |
| 平台反爬 | 添加延时 / 换 User-Agent / 提示手动 |

---

## 3. 技术架构

### 3.1 目录结构

```
star-skill-framework/
├── SKILL.md                   # 入口
├── README.md                  # 文档
│
├── prompts/                   # Prompt 模板
│   ├── intake.md             # 信息录入
│   ├── persona_builder.md    # Persona 生成
│   ├── meta_builder.md       # Meta 生成
│   ├── knowledge_router.md   # 知识库路由
│   └── correction_handler.md # 纠正处理
│
├── tools/                     # Python 工具
│   ├── lyrics_fetcher.py     # 歌词采集
│   ├── bilibili_fetcher.py  # B站采集
│   ├── weibo_fetcher.py      # 微博采集
│   ├── knowledge_builder.py   # 知识库构建
│   ├── skill_generator.py     # Skill 生成
│   └── version_manager.py     # 版本管理
│
├── examples/                  # 示例
│   └── wang_aonan_eve/        # EVE 示例
│       ├── SKILL.md
│       ├── meta.json
│       ├── persona/persona.md
│       ├── knowledge/
│       └── frontend/
│
└── docs/
    └── PRC.md                # 本文档
```

### 3.2 生成的 Skill 结构

每个生成的 Skill 独立运行，结构如下：

```
{slug}/
├── SKILL.md           # Skill 入口（OpenClaw 兼容）
├── meta.json          # 人物元信息
├── persona/
│   ├── persona.md     # 完整人格（Layer 0-5）
│   └── corrections.md # 纠正记录
├── knowledge/
│   ├── lyrics/         # 歌词文件（{id}_{name}.txt）
│   ├── song_list_full.json
│   ├── weibo_posts_full.json
│   ├── video_details.json
│   └── comments.json
└── frontend/
    └── server.py      # 对话前端（可选）
```

### 3.3 依赖

- Python 3.8+
- weibo-cli（微博采集，可选）
- requests / urllib（内置）

---

## 4. 用户旅程

### 4.1 主路径

```
用户输入 /create-star
  ↓
AI 启动 intake.md 向导
  ↓
收集：姓名/平台/描述
  ↓
采集数据（用户确认后）
  ↓
AI 分析 + 生成 persona + meta
  ↓
用户确认 / 纠正
  ↓
生成完整 Skill
  ↓
用户可用 /{slug} 调用
```

### 4.2 调校路径

```
用户：她不说"omg"，她说"天哪"
  ↓
AI 识别为「表达纠正」
  ↓
写入 Layer 2 + corrections.md
  ↓
版本快照
  ↓
用户确认生效
```

---

## 5. 竞品对比

| 功能 | colleague-skill | ex-skill | star-skill |
|------|----------------|-----------|-----------|
| 目标用户 | 离职同事 | 分手前任 | 喜欢的歌手 |
| 数据源 | 飞书/钉钉/Slack | 微信/iMessage | 网易云/B站/微博 |
| 人格层 | 5层 | 5层 | 5层 |
| 版本管理 | ✅ | ✅ | ✅ |
| 对话前端 | ❌ | ❌ | ✅（可选）|

---

## 6. Roadmap

### v1.0（当前）
- [x] 框架结构设计
- [x] Prompt 模板
- [x] 数据采集工具（歌词/B站/微博）
- [x] 知识库构建
- [x] Skill 生成器
- [x] 版本管理
- [ ] 前端对话界面（Web）
- [ ] 自动采集脚本完善

### v1.1
- [ ] 支持更多平台（网易云评论/抖音/小红书）
- [ ] 批量生成模式
- [ ] Persona 质量评分

### v2.0
- [ ] 多角色对话（多个明星同时在场）
- [ ] 实时学习（持续从社交媒体学习新表达）
- [ ] 语音合成（克隆音色）

---

## 7. 附录

### A. 术语表

| 术语 | 说明 |
|------|------|
| Skill | 可被 AI Agent 调用的能力模块 |
| Persona | 数字人格，包含说话风格/性格/边界 |
| Layer 0-5 | Persona 的5层结构定义 |
| Knowledge | 知识库，包含歌词/微博/B站数据 |
| Slug | Skill 的英文标识符（URL友好）|

### B. 参考资料

- [colleague-skill](https://github.com/titanwings/colleague-skill)
- [ex-skill](https://github.com/titanwings/ex-skill)
- [AgentSkills 开放标准](https://agentskills.io)
