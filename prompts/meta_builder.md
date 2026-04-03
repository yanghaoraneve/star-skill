# Meta 构建模板

> 生成 Skill 的 meta.json，包含人物基础信息和元数据。

---

## 模板

```json
{
  "name": "{name}",
  "slug": "{slug}",
  "stage_name": "{stage_name}",
  "created_at": "{YYYY-MM-DD}",
  "version": "v1.0",
  "note": "{一句话描述}",

  "basic_info": {
    "birth_date": "{birth_date}",
    "mbti": "{mbti}",
    "nationality": "中国",
    "education": "{院校/社团}",
    "debut_year": "{出道年份}",
    "genre": "{风格}",
    "signature": "{signature}",
    "platforms": {
      "bilibili_uid": "{uid}",
      "bilibili": "https://bilibili.com/{uid}",
      "weibo_uid": "{uid}",
      "weibo": "https://m.weibo.cn/u/{uid}",
      "netease_artist_id": {id},
      "netease": "{网易云名称}",
      "email": "{工作邮箱}"
    }
  },

  "programs": [
    {"name": "{节目名}", "year": "{年份}", "note": "{备注}"}
  ],

  "events": [
    {"name": "{活动名}", "date": "{YYYY-MM-DD}"}
  ],

  "tags": [
    "{标签1}",
    "{标签2}"
  ],

  "data_sources": {
    "lyrics": "{数量}首（来源）",
    "bilibili": "{数量}视频+{数量}评论（来源）",
    "weibo": "{数量}条动态（来源）",
    "manual": "{描述}"
  }
}
```

---

## 字段说明

| 字段 | 必填 | 说明 |
|------|------|------|
| name | ✅ | 真实姓名 |
| slug | ✅ | URL友好标识，用于命令调用 |
| stage_name | ✅ | 艺名/常用名 |
| created_at | ✅ | 创建日期 |
| version | ✅ | 当前版本 |
| note | ✅ | 一句话描述人格定位 |
| basic_info | ✅ | 基础信息 |
| platforms | ✅ | 各平台主页 |
| programs | ❌ | 参加的综艺/节目 |
| events | ❌ | 重要活动/演出 |
| tags | ✅ | 人设标签 |
| data_sources | ✅ | 数据来源说明 |

---

## Slug 命名规范

```
{名字拼音}_{艺名拼音}
例如：
- wang_aonan_eve
- zhang_yeon_lee
- li_xi_xi
```

下划线分隔，全部小写，用于命令调用。
