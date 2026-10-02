# BIV 视频策略 / BIV Video Strategy

> 版本: 2.2 | 最后更新: 2026-10-02 | 状态: 生效中
> Skill: `~/.openclaw/skills/id-dialogue-video/SKILL.md` (v2.2)

---

## 一、引擎规格

| 项目 | 规格 |
|---|---|
| 剪影引擎 | renderer/engine.html v1.6（勿改，除非全量回归） |
| 每日视频引擎 | templates/daily_engine.html v2.0.0（daily-2.0.0 卡片式） |
| 每日视频管线 | scripts/biv_daily.py（BIO 门 + lint 全检 + 时长模型） |
| 构建 | `python3 scripts/biv_daily.py --date YYYY-MM-DD` |
| 时长目标 | 60-90 秒/集 |
| 每集词数 | 8-15 词 |

## 二、Guru 人设

- 剪影人物（💁 Guru）
- **幽默、有逻辑** — 像真人老师讲课，不是念稿机器
- 不硬讲词——词活在搭配里，搭配活在句型里

## 三、教学技巧（v2.2 强化）

### 3.1 讲解要求（每日视频管线强制）
- **每个词必须有 coach beat**：head beat 之后自动插入 Guru 讲解
- **解释+引申**：从词条数据提取——近义词对比、反义词提示、变形规律、例句语境
- **不像"念完就过"**：讲解文本以自然语言呈现（印尼语对比 + 中文注解）
- **素材来源**：synonyms gloss、antonyms、transforms mean、examples id——全部自动提取，零手工

### 3.2 节奏控制
- **句间气口 520ms**（v2.2 从 420ms 上调）：每个 utterance 结束后停顿 520ms 再切下一句
- beat 之间也有自然过渡停顿
- TTS 中通过在 onend 回调中插入 setTimeout(520ms) 实现
- **红线：绝不允许 220ms 或更短的句间停顿**——太紧凑像连珠炮

### 3.3 字号防溢出（v2.2 新增 · 强制）

| 元素 | 字号 clamp | 必须 |
|---|---|---|
| `.ttl` 开场/结尾主标题 | `clamp(17px,3.2vw,34px)` | `word-break:break-word; overflow-wrap:break-word` |
| `.sub` 开场/结尾副标题 | `clamp(12px,1.7vw,18px)` | 同上 |
| `.h-word` 词头大词 | `clamp(24px,4.8vw,52px)` | 同上 |
| `.h-cn` 词头中文 | `clamp(14px,2.1vw,22px)` | 同上 |
| `.coach-txt` 讲解文本 | `clamp(13px,1.9vw,20px)` | 同上 |
| `.coach-zh` 讲解中文 | `clamp(11px,1.6vw,16px)` | 同上 |

**红线：任何文本元素必须有 word-break + overflow-wrap，防止长文本溢出屏幕。**

## 四、数据规格

### Episode Schema 关键字段
- `word` / `cn` / `ipa` / `root` / `forms[]` / `note` / `synonyms[]` / `antonyms[]` / `examples[]`

### 词卡规范
- 全部 8 张词卡齐（拖走再回来自动归位）→ 集末词卡缩略图
- 词卡从场地边缘外部入场
- 词卡含：变形行 / 同义行 / 反义行 / 例句行（含 fallback）
- 依赖字段写入 WordCard 类（非内联 onclick）

### TTS 规则
- 无 `coaching` → 在第三张词卡后插入 `__PAUSE_1200__`
- 有 `coaching` → 此时长不计入总时长
- `lessonTokenLimit=1400`
- `preferLocalTTS=true`

### Token 纪律
- 新词加入优先用同话题已有 episode 的既有 sinode
- 优先用**默认可复用 sinode**（schema 已列）
- 新增 sinode 要确认仍在 budget 内
- 非 guru_token 的 `parts` 里**禁止**写 guru_guide

### Coach Beat 规范（v2.2 新增）
```json
{
  "kind": "coach",
  "title": "CATATAN · 讲解",
  "text": "≈ synonym1、synonym2 ≠ antonym1",
  "zh": "变形:form(mean)；语境:example...",
  "tts": [{"l": "id", "t": "Kata ini mirip dengan x. Lawan katanya: y."}]
}
```

---

## 变更记录

| 日期 | 版本 | 变更 | 触发 |
|---|---|---|---|
| 2026-10-02 | 2.2 | ① 字号 clamp 全面下调 + word-break 防溢出；② 句间气口 420→520ms；③ 新增 coach beat 教学讲解规范 | 用户审核三个视频样片：字号溢出/讲解生硬/无气口 |
| 2026-10-02 | 2.1 | 新增教学技巧 3.1-3.3（讲解解释+引申、句间气口、字体溢出） | 用户审核三个视频样片 |
| 2026-10-01 | 2.0 | daily-2.0.0 剪影引擎 | V4.36.0 |
| 2026-09-30 | 1.0 | daily-1.0.0 初版 | V4.35.0 |
