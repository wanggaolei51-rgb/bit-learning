# BIT_RIDIAO 语音播报策略 / BIT Audio Broadcast Strategy

> 版本: 1.0 | 创建: 2026-10-22 | 状态: 生效中
> 上级策略: [BIT-词条规范](BIT-词条规范.md) · 协同: [BIV-视频策略](BIV-视频策略.md)
> 代码位置: index.html `broadcastDay()` / `bcFocusWord()` / `buildDailyNoteCardForDate()`

---

## 一、职责

每日笔记（BIT 词条卡）的语音播报系统——把当日所有词条以 TTS 链式朗读，支持跟随高亮、自动展开、导航联动。

## 二、架构

```
用户点击 🔊 播报按钮
  → broadcastDay(ds) 收集当日词条
  → 逐条 TTS: 印尼语 word → 中文 cn → 印尼语例句（id/zh 交替）
  → 每条播完 onend + 150ms 衔接下一条
  → bcFocusWord(ds, i) 跟随: 滚动居中 + 高亮描边 + 自动展开 BIT 详情
  → 全部播完自动停止 / 用户可随时点 ✕ 停止
```

### 核心函数

| 函数 | 职责 |
|---|---|
| `buildDailyNoteCardForDate(ds)` | 渲染当日笔记卡（含 🔊 按钮），日记页/CA日/课程页三处共用 |
| `buildNoteEntryHtml(e, i, ds)` | 单条词条渲染，外层锚点 `id="dnw-<ds>-<i>"` 供跟随定位 |
| `broadcastDay(ds)` | 播报主控：收集词条 → 链式 TTS → 状态管理 |
| `bcFocusWord(ds, i)` | 跟随定位：scrollIntoView + `.bc-hl` 高亮 + 自动展开 |
| `bcRootOk(r, w)` | 词根过滤：仅干净单词形（`/^[A-Za-z][A-Za-z-]{2,}$/` 且 ≠ 词目）才播 |
| `bcStop()` | 停止播报 + 清除高亮 |

### 播报内容规则

1. **词条链式播报**: 每词 = 印尼语 word → 中文 cn → 词根（仅 bcRootOk 通过时）→ 印尼语例句
2. **词根净化**: 括号类词根（如 `saj/saji`）不播——只播干净单词形
3. **id/zh 交替**: 印尼语用 `lang=id`，中文用 `lang=zh-CN`，onend 回调串联
4. **每条间隔 150ms**: 避免 TTS 引擎吞字
5. **纯日记文本日**: 无 BIT 词条时播日记文本本身（showDateStudyRecord 兜底按钮）

### 按钮位置规范（V4.46.3 定型）

| 页面 | 按钮位置 | 说明 |
|---|---|---|
| 日记页 `showDateStudyRecord` | 笔记卡内部（`buildDailyNoteCardForDate`） | 每篇日记一个 🔊 |
| CA 日 `renderDateDetail` | 同上 | 笔记卡渲染到哪按钮跟到哪 |
| 课程页 `startTopicQuiz` | 同上 | 当日笔记区内 |
| 纯日记文本日（无 BIT 词条） | 日记页/CA 日兜底按钮 | `_onlyNotes` 条件 |

## 三、样式规范

```css
.dn-entry          /* 词条卡容器 */
.dn-entry.bc-hl    /* 播报跟随高亮（呼吸描边动画）*/
.bc-btn            /* 🔊 播报按钮 */
```

- 跟随高亮：`.bc-hl` class 加呼吸描边（`border-color: var(--primary)` + 动画）
- 自动展开：播到某词时 `toggleDailyNote` 自动展开该词 BIT 详情
- 滚动定位：`scrollIntoView({behavior: 'smooth', block: 'center'})`

## 四、部署 SOP（随每日笔记同步）

```
md_to_dailynote.py 合并 dailynote js
  → ⚠️ 必须验证函数定义未被覆盖（grep 检查）
  → check_syntax.py（JS 解析 PASS）
  → deploy-check.sh 8/8
  → commit + push
  → 线上验证: curl 页面 → grep "function buildDailyNoteCardForDate" ✅
  → 浏览器实测: 日记页 → 点击 🔊 → 确认播报到跟随高亮全链路
```

### ⚠️ 防回归红线（V4.46.7 事故教训）

**V4.46.6 事故**：`md_to_dailynote.py` 合并 dailynote 数据时覆盖了整个 script 块，把 `dnEsc`/`dnRich`/`buildNoteEntryHtml`/`buildDailyNoteCardForDate` 四个函数定义一并删除 → `typeof buildDailyNoteCardForDate !== "function"` → 笔记卡不渲染 + 播报按钮静默消失（三处调用点都有守卫，无报错）。

**防复发措施**：
1. 每次部署后 `grep -c 'function buildDailyNoteCardForDate' index.html` 必须 = 1
2. `check_syntax.py` 后跑 `node -e "验证七函数存在"` 冒烟
3. 函数定义区不得与 dailyNotesDB 数据区混排在同一替换锚点内

## 五、变更记录

| 日期 | 版本 | 变更 | 触发 |
|---|---|---|---|
| 2026-10-22 | 1.0 | 初版：从 V4.46.2/3 实现提炼为 BIT 子策略 | 用户指令"把同步生成语音播报策略写到 BIT 下子项" |
