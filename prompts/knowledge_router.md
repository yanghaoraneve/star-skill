# 知识库路由配置

> 当数字人格被问及特定类型的问题时，路由到对应的知识库文件。

---

## 路由表

```json
{
  "lyrics": {
    "query_patterns": ["歌词", "写的什么", "内容", "表达", "这首歌"],
    "file_pattern": "knowledge/lyrics/{song_id}_{song_name}.txt",
    "list_file": "knowledge/song_list_full.json",
    "search_command": "grep \"{keyword}\" knowledge/lyrics/*.txt"
  },
  "weibo": {
    "query_patterns": ["微博", "动态", "发的什么", "说了"],
    "file": "knowledge/weibo_posts_full.json",
    "format": "JSON数组，每条含 text/time/topic"
  },
  "bilibili_video": {
    "query_patterns": ["视频", "B站", "播放", "多少播放"],
    "file": "knowledge/video_details.json",
    "format": "JSON数组，每条含 title/desc/play_count/bvid"
  },
  "bilibili_comment": {
    "query_patterns": ["评论", "粉丝说", "留言"],
    "file": "knowledge/comments.json",
    "format": "JSON数组，每条含 text/author/like_count"
  },
  "basic_info": {
    "query_patterns": ["生日", "MBTI", "哪年的", "哪里人", "什么星座"],
    "file": "meta.json",
    "field_path": "basic_info.{field}"
  },
  "works": {
    "query_patterns": ["代表作", "专辑", "作品", "歌单", "热门歌曲"],
    "file": "knowledge/song_list_full.json"
  }
}
```

---

## 读取指令（供 AI 执行）

```bash
# 问歌词 → 先搜索歌名 → 再读取文件
grep "{歌名}" knowledge/song_list_full.json
cat knowledge/lyrics/{id}_{歌名}.txt

# 问歌曲列表
cat knowledge/song_list_full.json

# 问微博
cat knowledge/weibo_posts_full.json | jq '.[] | select(topic=="xxx")'

# 问B站视频
cat knowledge/video_details.json | jq '.[] | select(title|contains("xxx"))'

# 问基本信息 → 读 meta.json
cat meta.json

# 全局歌词搜索
grep -l "{关键词}" knowledge/lyrics/*.txt
```

---

## 回答模板

### 歌词类
```
「《{歌名}》啊！就是那种'{情绪关键词}'的感觉…
{引用1-2句标志性歌词}
就…那种{情绪描述}你懂吧！」
```

### 微博类
```
「哦那条啊！是{日期}发的…
{内容摘要}
#e记系列#」
```

### 作品类
```
「嗯…代表作的话…
《{歌1}》应该大家都知道吧？
{一句话特点}
还有《{歌2}》也很多人喜欢～」
```

---

## 知识库文件格式

### song_list_full.json
```json
[
  {
    "id": "2626025933",
    "name": "层层",
    "album": "专辑名",
    "year": "2023",
    "type": "original" // original/accompaniment/live
  }
]
```

### weibo_posts_full.json
```json
[
  {
    "id": "N",
    "text": "微博正文",
    "time": "YYYY-MM-DD HH:mm",
    "topic": "#e记系列#",
    "likes": N,
    "comments": N
  }
]
```

### video_details.json
```json
[
  {
    "bvid": "BVxxx",
    "title": "视频标题",
    "desc": "视频描述",
    "play_count": N,
    "pubdate": "YYYY-MM-DD"
  }
]
```

### comments.json
```json
[
  {
    "text": "评论内容",
    "author": "用户昵称",
    "like_count": N,
    "video_bvid": "BVxxx"
  }
]
```
