# BIT_BIV 视频动画策略 / BIT Video Animation Strategy

> 版本: 1.0 | 创建: 2026-10-22 | 状态: 生效中
> 上级策略: [BIT-词条规范](BIT-词条规范.md) · 原策略: [BIV-视频策略](BIV-视频策略.md) v2.2
> Skill: `~/.openclaw/skills/id-dialogue-video/SKILL.md` (v2.2)
> 管线: `~/.openclaw/skills/id-dialogue-video/scripts/biv_daily.py`

---

## 一、职责

将 BIT 每日笔记词条转化为教学动画视频——剪影人物对话 + Guru 讲解 + 词卡，单文件 HTML、零依赖、浏览器直接播放。

## 一·补、每日笔记部署 SOP 集成（V4.46.9 起强制执行）

视频生成是每日笔记部署的**固有步骤**，不得遗漏。完整 SOP：

```
BIT md 定稿
  → python3 scripts/md_to_dailynote.py（笔记数据合并）
  → BIO 印章: printf 'sha8: <hash>' > agents/BIT/notes/.bio_pass/<date>
       (hash = sha256(note_final.md)[:8], 无尾部换行)
  → python3 ~/.openclaw/skills/id-dialogue-video/scripts/biv_daily.py --date <date> --force
       (lint 10项必须全PASS, 任何FAIL禁止部署)
  → 产物复制: cp -r bit-deploy/videos/daily/<date> videos/daily/
  → 注册表同步: cp bit-deploy/video_registry.js video_registry.js
  → check_syntax.py + deploy-check.sh
  → 版本号三处更新
  → git commit + push main
  → 线上验证（版本号 + VIDEO_DB 天数 + 视频 HTTP 200）
```

⚠️ **BIT md 写法约束**（防 lint#6 FAIL）：同义词/反义词无内容时写 `- **同义词**: —`（单独一个破折号），**不要**写 `—（无严格反义）` 或 `无严格同义`——中文括号/文字会进入 id 通道导致 lint#6 语言隔离 FAIL。

## 二、引擎规格

| 项目 | 规格 |
|---|---|
| 剪影引擎 | `renderer/engine.html` v1.6（勿改，除非全量回归） |
| 每日视频引擎 | `templates/daily_engine.html` v2.0.0（daily-2.0.0 卡片式） |
| 每日视频管线 | `scripts/biv_daily.py`（BIO 门 + lint 全检 + 时长模型） |
| 构建命令 | `python3 scripts/biv_daily.py --date YYYY-MM-DD` |
| 产物 | 单文件 HTML（零外链零注释），输出 `videos/daily/<date>/` |
| 注册表 | `video_registry.js`（唯一真相源，BIO 印章验证） |
| 部署分支 | **main**（GitHub Pages）——勿推 master |

### V4.46.7+ 泛化（支持任意词数日记）

| 项目 | 旧版（硬编码） | 新版（泛化） |
|---|---|---|
| 词条数 | 仅支持 39 词 | 任意 ≥1 词 |
| 分段 | 固定 3 集 × 13 词 | 动态 `make_part_map(n)`，每集 ≤13 词 |
| 例句格式 | 仅 `- **例句**: ` 字段 | 兼容场景行 `- 场景名: *印尼语* 中文` |
| NO_ANTONYM | 硬编码 39 词序号 | 非 39 词时自动清空 |
| 主题解析 | 仅 `**主题**: cn (id) Day N` | 兼容新版 `# DATE 每日笔记（话题 id · 主题 DayN）` |
| 注册表 words | `range(1, 40)` 硬编码 | `sorted(entries.keys())` 动态 |

## 三、生产流程

```
BIT 定稿 md（agents/BIT/notes/<date>_note_final.md）
  → 复制为 <date>_note_final.md（如命名不符）
  → BIO 印章: echo "sha8: $(sha256[:8])" > .bio_pass/<date>
  → python3 scripts/biv_daily.py --date <date> --dry-run（lint 全检）
  → lint 10/10 PASS → 去掉 --dry-run 正式生成
  → 产物自动写入 bit-deploy/videos/daily/<date>/
  → 复制产物 + video_registry.js 到主工作区
  → .gitignore 放行 videos/ → git add + commit + push main
  → 线上验证: curl -sI videos/daily/<date>/daily_<date>_p1.html → 200
```

### BIO 门

管线强制检查 `.bio_pass/<date>` 印章文件，sha8 必须等于 note_final.md 的 sha256 前 8 位。无印章 → 等 30s × 5 轮 → exit(3)。

### lint 全检（10 项，全 PASS 才能产出）

| # | 检查项 | 说明 |
|---|---|---|
| 0 | 非空断言 | 段数/产物大小/md5 差异核实 |
| 1 | 扩展句纯度 | 例句逐字来自 note，零编造 |
| 2 | 释义零改动 | 屏显字符串与 note 字节级一致 |
| 3 | 空槽静默 | 无反义词的词不出现反义槽 |
| 4 | 变形行上限 | 单块 ≤3 行 |
| 5 | 时长硬界 | 每集 ≤300s，单段 H≤45s / M≤38s |
| 6 | 语言通道隔离 | id 通道零 CJK，zh 通道零拉丁 |
| 7 | 顺序一致 | 同反义朗读顺序与 note 一致 |
| 8 | 预览/回顾齐套 | p2+ 预览条 / 每集回顾齐全 |
| 9 | 零外链零注释 | 单文件自包含 |

## 四、教学规范

### 五拍教学流
1. **场景入戏**：首句对话带目标词
2. **万能句型 ①**：老师点破句型骨架
3. **词组搭配**：2-3 个最高频搭配
4. **万能句型 ②**：第二个句型
5. **收口输出**：学生独立造句

### Guru 讲解（coach beat）
- 每个词 head beat 后必须有 coach beat
- 从词条数据自动提取：近义词对比、反义词提示、变形规律、例句语境
- TTS 印尼语列举用逗号（`, `），**禁用中文顿号（`、`）**——lint#6 CJK 隔离红线

### 节奏控制
- TTS onend 驱动推进，绝不抢话
- 最短展示 `minShow = 1600ms + 词数 × 520ms`
- 句间换气 520ms
- hardMax 兜底防挂死

## 五、变更记录

| 日期 | 版本 | 变更 | 触发 |
|---|---|---|---|
| 2026-10-22 | 1.0 | 从 BIV-视频策略 v2.2 归档为 BIT 子策略；biv_daily.py 泛化任意词数；部署分支修正为 main；10/21 首跑 2 集全 PASS | 用户指令"视频动画生成策略同步到 BIT 子策略并执行昨天视频生成" |
