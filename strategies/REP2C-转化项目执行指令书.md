# REP2C 转化项目 · 执行指令书
# 任务指令：将周/月汇报转化为 LEO-BIR 可直接消费的成品数据

> 版本: v1.0 | 日期: 2026-10-11 | 指令来源: Leo_kimi（指挥官）
> 执行方: 新项目（REP2C 转化项目）
> 接收方: Leo_kimi Agent（主执行位，负责合并部署）
> 依据协议: `strategies/REP2C-汇报转化课程协议.md` v1.0（规则细节以协议为准，本文是操作指令）

---

## 一、你的使命

接收用户的周汇报/月汇报原文，按 REP2C 协议加工成**三个成品数据文件**，交给主执行位（Leo_kimi Agent）直接合并入 LEO-BIR 平台。**你只做转化，不做部署**。

---

## 二、输入

| 项目 | 规格 |
|---|---|
| 输入材料 | 用户周汇报/月汇报全文（中文为主，可含印尼语片段） |
| 到达方式 | 用户直接粘贴，或文件投递 |
| 汇报场景 | 项目管理 / 商务 / 冶炼工业园区运营 |

---

## 三、输出（三件套，缺一不可）

### 产出物 1：BIT 定稿 md（文件名: `rep2c_<日期>_bit.md`）

这是核心产出。格式必须**逐字遵守**以下模板——主执行位用 `md_to_dailynote.py` 机器解析，格式偏差 = 解析失败 = 打回。

**词条模板（每个词一份）：**

```markdown
### 1. menyelesaikan
- **中文**: 完成（工作/任务）
- **English**: to complete / to finish
- **词根**: selesai
- **变形**:

| 形式 | 词性 | 含义 |
|------|------|------|
| menyelesaikan | 动词 | 完成（meN- 主动） |
| diselesaikan | 被动动词 | 被完成（di- 被动） |
| penyelesaian | 名词 | 完成/解决（peN--an 名词化） |

- **变形说明**: meN- 主动 / di- 被动 / peN--an 名词化
- **词汇注释**: 自中文'完成'转译；REP2C 原始词
- **同义词**: menuntaskan、merampungkan
- **反义词**: menunda、menghentikan
- 场景: *Minggu ini kami telah menyelesaikan pemasangan pipa utama.* 本周我们已完成主管道安装。
- 场景: *Pekerjaan ini akan diselesaikan paling lambat Jumat depan.* 这项工作最迟下周五完成。
- 场景: *Penyelesaian masalah pendingin membutuhkan teknisi dari pabrikan.* 冷却问题的解决需要厂方技术员。
```

**格式硬性规则（违反即打回）：**

1. 词条分隔符必须是 `### N. word`（N 从 1 开始连续编号，word 为印尼语词根原形）
2. 元信息字段必须是 `- **中文**: `、`- **English**: `、`- **词根**: `、`- **变形**: `、`- **变形说明**: `、`- **词汇注释**: `、`- **同义词**: `、`- **反义词**: `（注意冒号后有一个空格）
3. **变形必须用表格**（三列：形式/词性/含义），禁止顿号列表。表格下必须有空行与后续内容分隔
4. 例句格式：`- 场景: *印尼语句* 中文翻译`（场景标签可换，但 `*id* cn` 结构不可换）
5. 同义词/反义词用顿号分隔
6. 词数 20-40 词/期（目标 38-40）
7. note 字段标注规则：
   - 原始汇报词：`- **词汇注释**: REP2C 原始词`（如有补充信息接在后面）
   - 中文转译词：`- **词汇注释**: 自中文'达产'转译`
   - 扩展词：`- **词汇注释**: [REP2C-EXT 同义:anggaran]`

### 产出物 2：场景对话 JSON（文件名: `rep2c_<日期>_scenes.json`）

3 个场景，每场景 10-20 句对话（建议 14-16 句）。格式直接对接 LEO-BIR topic 数据结构：

```json
[
  {
    "type": "S-A",
    "title": "向董事长汇报周进度",
    "icon": "📊",
    "dialogue": [
      {"speaker": "A", "text": "Bapak Liu, terima kasih atas waktunya. Hari ini saya akan melaporkan progres pembangunan smelter untuk minggu ini.", "trans": "刘董，感谢您的时间。今天我汇报本周冶炼厂建设进度。"},
      {"speaker": "B", "text": "Silakan, Bapak Zhang.", "trans": "请讲，张总。"}
    ],
    "vocabCoverage": ["progres", "pemasangan", "kendala", "jadwal"],
    "hooks": [
      {"id": "H-01", "line": 5, "type": "Q-T1", "question": "Bagaimana dengan uji coba tungku?", "note": "进度质疑钩子"}
    ]
  }
]
```

**格式硬性规则：**

1. 必须 3 个场景：S-A（向上汇报，必选）+ S-B1 或 S-B2（轮换）+ S-C（条件触发，不满足则第二个 S-B）
2. 每个 `dialogue` 条目必须含 `speaker`/`text`/`trans` 三键，缺一不可
3. 核心词覆盖 ≥8/场景，3 场景合计 ≥20，且每个核心词至少出现在 2 个场景中
4. `hooks` 数组：每场景埋 1-2 个追问钩子，编号 H-01 起连续
5. 数字一律用 `{angka}` 占位——禁止真实数据
6. 语言难度：句长 ≤25 词/句；被动 di- ≤3 处/场景；`bahwa/ketika` 从句 ≤3 处/场景

### 产出物 3：问答对 + 对账表（文件名: `rep2c_<日期>_qa.md`）

**Part A · 问答对（12-15 组，配比 4-4-3-2）：**

```markdown
## 问答对库

### Q-T1 进度质疑（4组）

**H-01 → Q-T1 → REP-ANS-01**
- 问: Mengapa uji coba tungku belum selesai sesuai jadwal?
- 问(变体): Kapan uji coba bisa selesai?
- 标准答: Benar, uji coba tungku pertama memang tertunda tiga hari. Penyebabnya adalah kendala teknis di sistem pendingin. Kami sudah memanggil teknisi dari pabrikan dan akan mengganti komponen pendingin. Uji coba akan selesai paling lambat pada Jumat pekan depan.
- 变体A: Tertunda tiga hari karena kendala pendingin, teknisi pabrikan sudah dipanggil.
- 变体B: Selesai paling lambat Jumat depan.
- 涉及核心词: tertunda、kendala、pendingin
```

四类：Q-T1 进度质疑 ×4 / Q-T2 数据追问 ×4 / Q-T3 风险询问 ×3 / Q-T4 资源请求 ×2。
每组必须有：标准答（态度→事实→措施→承诺四段）+ 2 个精简变体。

**Part B · RCO A3 对账表（附录一）：**

```markdown
## 附录一 · 词级三方对账表

| # | 汇报原文词元 | 出处 | 归位词根 | 分类 | 优先级 | 最终词条 | 备注 |
|---|---|---|---|---|---|---|---|
| 1 | 完成 | 第2段第3行 | menyelesaikan | B | P0 | ✅ 词条1 | 中文转译 |
| 2 | progress | 第1段第1行 | progres | A | P1 | ✅ 词条2 | bitVocabDB已有,复习重收 |
| 3 | 高度重视 | 第4段第2行 | — | — | — | ❌ X2排除 | 行政套话,转为"menyampaikan pentingnya" |
```

**规则：每一个从汇报原文提取的词元，必须在对账表中有去向说明（✅ 词条编号 / ❌ 排除原因 / ⏭ 下期待学）。任何词元无去向 = FAIL。**

---

## 四、执行流程

```
D0  收到汇报 → 词元登记（照抄原文,含出处行号,零改动）
D1  词汇提取（模块一：5标准+4排除 → 六分类A-F → P0-P2定级 → 20-40词配额）
    ↓ 产出：词元表（冻结,作为对账基线）
D2  词条化（模块二：清洗→查重→词形归位→九字段填充）
    ↓ 产出：BIT 定稿 md 初稿
D2  句型提取（模块四：五段切片→模板化→纵横两轴扩展≥6句/模板）
D3  场景对话（模块五：3场景组装,核心词嵌入+钩子预埋）
    ↓ 产出：场景对话 JSON
D3  问答对（模块六：4类13组,三级索引闭合）
    ↓ 产出：问答对 md
D4  扩展词（模块三：E1/E2/E3三标准,≤30%上限,回D2补词条）
D4  自检三件套齐全 + 对账表闭合
    ↓ 交付主执行位
```

**自检清单（交付前逐项勾选）：**

- [ ] BIT md：`### N. word` 编号连续无断号
- [ ] BIT md：每个词条 9 字段完整，变形全部是表格
- [ ] BIT md：每个例句含目标词
- [ ] BIT md：词数 20-40
- [ ] Scenes JSON：3 场景，dialogue 每条三键齐全
- [ ] Scenes JSON：核心词覆盖 ≥8/场景，复现 ≥2
- [ ] Scenes JSON：零真实数字（全部 {angka} 占位）
- [ ] QA：12-15 组，配比 4-4-3-2，每组有标准答+2变体
- [ ] 对账表：每个词元有去向，无遗漏
- [ ] 红线 R1-R8 全过（见协议第三章）

---

## 五、与主执行位的交接

| 事项 | 规格 |
|---|---|
| 交付物 | 三个文件：`rep2c_<日期>_bit.md` + `rep2c_<日期>_scenes.json` + `rep2c_<日期>_qa.md` |
| 交付方式 | 文件放到共享工作区，或直接发给用户转交 |
| 主执行位后续 | md_to_dailynote.py 解析 BIT md → 合并场景 JSON → 三审（BIO/RCO/TSO）→ 部署上线 |
| 你的边界 | **不碰 index.html，不做 git 操作，不做部署** |

---

## 六、质量红线（违反即打回，不二次警告）

| # | 红线 |
|---|---|
| R1 | 禁止真实数字进入课程，一律 `{angka}` 占位 |
| R2 | 印尼语纯度，禁方言混入 |
| R3 | 例句语境必须是项目管理/商务/冶炼园区 |
| R4 | BIT md 变形禁顿号列表，必须表格 |
| R5 | 核心词必须来自汇报原文提取，禁止凭空编词 |
| R6 | 不编造词根，不确定标 `[待核实]` |
| R7 | 例句必含目标词或其变形 |
| R8 | 场景对话禁连续 2 句模板原句 |

---

*本指令书由主执行位（Leo_kimi Agent）根据 REP2C 协议 v1.0 编制，指挥官审定后生效。*
