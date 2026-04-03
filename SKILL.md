---
name: create-star-skill
description: 创建明星/偶像/公众人物数字人格 Skill 的工坊框架。
version: "1.0"
read:
  - README.md
  - prompts/intake.md
user-invocable: true
triggers:
  - /create-star
---

# ⭐ Star Skill 工坊

> 「用她的声音说话，用她的方式爱你。」

## 是什么

Star Skill 是一个**数字人格创建框架**，用于将真实明星/偶像/公众人物转化为可对话的 AI Skill。

基于 `colleague-skill`（by titanwings）理念演进，专注于**公众人物**场景。

## 快速开始

```bash
# 1. 安装依赖
pip install requests

# 2. 录入人物信息
python3 -c "
# 或直接编辑 prompts/intake.md 进行录入
"

# 3. 采集数据
python3 tools/lyrics_fetcher.py --artist-id <ID> --output star/
python3 tools/bilibili_fetcher.py --uid <UID> --output star/
python3 tools/weibo_fetcher.py --uid <UID> --output star/

# 4. 构建知识库
python3 tools/knowledge_builder.py --knowledge-dir star/

# 5. 生成 Skill 文件
python3 tools/skill_generator.py --output star/ --meta star/meta.json --persona star/persona.md
```

## 目录结构

```
star-skill/
├── SKILL.md
├── README.md
│
├── prompts/                   # Prompt 模板
│   ├── intake.md             # 信息录入向导
│   ├── persona_builder.md    # Persona 5层生成模板
│   ├── meta_builder.md       # meta.json 生成模板
│   ├── knowledge_router.md   # 知识库路由配置
│   └── correction_handler.md # 纠正处理逻辑
│
├── tools/                     # Python 采集工具
│   ├── lyrics_fetcher.py     # 歌词采集
│   ├── bilibili_fetcher.py  # B站数据采集
│   ├── weibo_fetcher.py      # 微博采集
│   ├── knowledge_builder.py   # 知识库构建
│   ├── skill_generator.py     # Skill 文件生成
│   └── version_manager.py     # 版本管理
│
└── docs/
    └── PRC.md                # 项目需求文档
```

## 参考项目

- [colleague-skill](https://github.com/titanwings/colleague-skill) by @titanwings
