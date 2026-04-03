# 纠正处理器

> 当用户说「她不会这样」「她应该是xxx」时，触发纠正流程。

---

## 纠正类型

### 类型 A：表达纠正
```
用户：她不说"omg"，她说"天哪"
→ 写入 Layer 2 表达风格 的对应位置
→ 标记：v1.0.1-correction-001
```

### 类型 B：事实纠正
```
用户：她不是ENFP，是INTP
→ 写入 meta.json + Layer 1 身份认知
→ 标记：v1.0.1-correction-002
```

### 类型 C：边界纠正
```
用户：她可以聊恋爱话题，只是不聊具体细节
→ 写入 Layer 5 边界与雷区
→ 调整回避规则
```

### 类型 D：知识纠正
```
用户：《逐客令》是2021年的，不是2024年的
→ 写入 meta.json events + 歌词文件注释
→ 标记：v1.0.1-correction-003
```

---

## 纠正执行流程

1. **识别纠正类型**（A/B/C/D）
2. **定位目标位置**（Layer X / meta.json）
3. **写入修正内容**
4. **生成版本快照**
5. **回复用户确认**

---

## 格式

```
✅ 已纠正 [{slug}] v{version}
类型：A / B / C / D
位置：Layer {N} / meta.json
内容：{修正内容}
版本：v{version}.{patch}
```

---

## 版本快照

每次纠正后自动生成快照：
```
versions/
├── v1.0/
│   └── snapshot.md
├── v1.0.1/
│   ├── snapshot.md
│   └── corrections.md
└── ...
```

corrections.md 格式：
```markdown
# 纠正记录 v1.0.1

## #001 [{date}]
- 类型：A
- 内容：口头禅从"omg"改为"天哪"
- 依据：用户反馈
```

---

## 批量纠正

当纠正积累 ≥5 条时，触发**合并重构**：
- 将所有 corrections 合并到对应 Layer
- 生成新版本 snapshot
- 清空 corrections.md
