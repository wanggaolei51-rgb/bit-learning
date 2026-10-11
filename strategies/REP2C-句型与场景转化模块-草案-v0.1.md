# REP2C 汇报转化课程协议 · 句型与场景转化模块（模块四 / 五 / 六）

> 版本: v0.1 草案 | 日期: 2026-10-11 | 状态: 待评审
> 上游依据: `strategies/C5-课程生成策略.md`（规则C/D/E）、`strategies/BIT-词条规范.md`
> 适用对象: REP2C 转换流水线中的"句型提取 → 场景对话 → 问答对"三个工位

---

## 0. 模块总览与数据契约

### 0.1 三个模块的接力关系

```
模块四产出【句型模板库】──┐
                          ├─→ 模块五产出【场景对话稿】──→ 模块六产出【问答对库】──→ 进入 C 课程 Day 页面
话题 topic.vocab(20-40词)─┘
```

- 模块四是"骨架工厂"：把汇报原文变成可复用的印尼语模板。
- 模块五是"组装车间"：把模板组装成符合 C5 规则D 的 3 场景对话。
- 模块六是"弹药库"：把对话里预埋的追问，扩写成可独立练习的问答对。

### 0.2 输入输出物（每个都要有落盘文件，禁止心理笔记）

| 工位 | 输入 | 输出 |
|---|---|---|
| 模块四 | 周报/月报原文 + topic.vocab | `rep2c_<topic>_patterns.md`（句型模板表） |
| 模块五 | 句型模板表 + topic.vocab | `rep2c_<topic>_scenes.md`（S1/S2/S3 对话稿） |
| 模块六 | 场景对话稿 + 提问类型表 | `rep2c_<topic>_qa.md`（问答对库） |

---

## 模块四：核心句型提取规则

### 4.1 汇报结构五段切片

任何周汇报/月汇报，先按以下五段强制切片（切片是后续一切工作的索引）：

| 段编号 | 段名 | 典型中文标志词 | 必须提取句型数 |
|---|---|---|---|
| P1 | 已完成 | 本周完成、已交付、已投产、已验收 | ≥2 |
| P2 | 进行中 | 正在推进、截至目前、形象进度 | ≥1 |
| P3 | 下步计划 | 下周计划、下月安排、拟启动 | ≥1 |
| P4 | 问题与风险 | 存在问题、风险、滞后、制约因素 | ≥1 |
| P5 | 协调与请求 | 需协调、恳请、申请、建议 | ≥1 |

**规则 4.1.1**：切片后与原文逐段核对，五段各自非空。某段为空时，标记 `P4=空` 并在句型表中登记"本话题无风险段"，禁止跳过（空段也是课程设计信息：说明该话题要教"报喜"句式而非"报忧"句式）。

**规则 4.1.2**：五段映射为汇报课程的教学主线 `完成→进度→计划→风险→请求`，此顺序就是模块五场景对话主体的默认叙事顺序。

### 4.2 句型的印尼语模板化方法（骨架 + 槽位）

**四步流水线：**

**第 1 步 · 主干抽取**——从每段中文里挑高频句式，每段 1-2 个，先写成中文骨架：

```
本周完成 {X} 项工作 → 下周计划 {Y} → 需要协调 {Z}
```

**第 2 步 · 印尼语直译**：

```
Minggu ini kami telah menyelesaikan {X} pekerjaan → rencana minggu depan: {Y} → kami memerlukan dukungan {Z}.
```

**第 3 步 · 语序调优**（印尼语商务表达规范）：

- 时间状语前置：`Pada minggu ini, kami telah menyelesaikan...`
- 数字后置用 `sebesar`：`mencapai angka sebesar {X} persen`
- 正式动词优先：`menyampaikan`（汇报）> `bilang`；`mengalami kendala`（遇阻）> `ada masalah`

**第 4 步 · 槽位类型化**——把每个可变部分标为带类型的槽位：

| 槽位类型 | 标记 | 可替换内容来源 |
|---|---|---|
| 事物槽 | `{item}` | topic.vocab 名词 + BIT 同义词 |
| 动作槽 | `{aktivitas}` | topic.vocab 动词 |
| 数字槽 | `{angka}` | 占位符，不填真实数据（见红线 R1） |
| 时间槽 | `{tanggal/periode}` | 固定套语库（见 4.4） |
| 人员/单位槽 | `{unit}` | 部门名、承包商名套语 |

**产出格式**（句型模板表每行一条）：

```markdown
| 模板ID | 段 | 印尼语骨架 | 槽位类型 | 中文对照 |
|---|---|---|---|---|
| REP-CMP-01 | P1 | Minggu ini kami telah menyelesaikan {item}. | item:名词 | 本周我们已完成{item}。 |
```

### 4.3 一模板 → 多句扩展机制（纵横两轴）

每个模板必须做两轴扩展，单模板最小产出 6 个句子变体，达不到不准入库。

**横轴 · 槽位替换**：每个槽位从 topic.vocab 及 BIT synonyms 中取 ≥5 个同域替换词：

```
REP-CMP-01 × item ∈ {pemasangan pipa, uji coba tungku, perizinan AMDAL, pelatihan K3, pengiriman peralatan}
→ 5 个句子
```

**纵轴 · 时态/语态变体**：同一骨架至少做 2 种时态变体（教学上要求学生三种都会）：

```
已完成: Minggu ini kami telah menyelesaikan {item}.
进行中: Saat ini kami sedang mengerjakan {item}.
将计划: Minggu depan kami akan menyelesaikan {item}.
```

**扩展公式**：`变体句数 = 槽位替换数 ≥3 × 时态变体数 ≥2 = 每模板 ≥6 句`。

**校验 4.3.1**：扩展产出的句子逐句人工/Agent 复读，凡读起来不像总经理会说的，删。检验标准：能否想象在 Morowali 园区会议室里对董事长/政府官员说出口。

### 4.4 句型套语库（首批 12 个模板，直接入库）

| 模板ID | 类别 | 印尼语骨架 | 中文 |
|---|---|---|---|
| REP-CMP-01 | 完成 | Minggu ini kami telah menyelesaikan {item}. | 本周已完成{item}。 |
| REP-PROG-01 | 进度 | Progres {proyek} telah mencapai angka sebesar {angka} persen. | {proyek}进度已达{angka}%。 |
| REP-PLN-01 | 计划 | Rencana minggu depan: kami akan {aktivitas}. | 下周计划：我们将{aktivitas}。 |
| REP-ISS-01 | 问题 | Di {area} kami mengalami kendala {kendala}. | {area}遇到{kendala}困难。 |
| REP-RISK-01 | 风险 | Ada risiko {risiko} yang perlu diwaspadai; mitigasinya {mitigasi}. | 存在{risiko}风险， mitigation 措施是{mitigasi}。 |
| REP-ASK-01 | 请求 | Kami memerlukan dukungan {unit} untuk {tujuan}. | 需要{unit}支持以{tujuan}。 |
| REP-DATA-01 | 数据 | {Indikator} bulan ini mencapai {angka} {satuan}. | 本月{指标}达{angka}{单位}。 |
| REP-CMPC-01 | 对比 | {Indikator} {naik/turun} sebesar {angka} persen dibandingkan {periode} lalu. | 指标环比{升/降}{angka}%。 |
| REP-SFT-01 | 安全 | Insiden K3 minggu ini: {jumlah} kasus, tidak ada korban jiwa. | 本周K3事故{jumlah}起，无人员伤亡。 |
| REP-COMP-01 | 合规 | {Dokumen} telah {status} sesuai ketentuan {instansi}. | {文件}已按{机构}规定{状态}。 |
| REP-FUP-01 | 跟进 | Tindak lanjut rapat: {poin}; penanggung jawabnya {unit}. | 会议跟进项：{poin}，责任单位{unit}。 |
| REP-APR-01 | 审批 | Kami mengajukan {permohonan} untuk {tujuan}. | 我们申请{事项}以{tujuan}。 |

新话题的模板 60% 从此库直接取用，40% 按 4.2 流程从当周汇报原文新提取；新模板必须补齐纵横两轴扩展后才算入库。

### 4.5 模块四验收清单

- [ ] 五段切片齐全，空段已登记
- [ ] 模板总数 ≥10（含套语库取用）
- [ ] 每个模板槽位已类型化、每个槽位 ≥5 替换词
- [ ] 每个模板变体 ≥6 句
- [ ] 全部句子通过"总经理口吻"复读检验
- [ ] 数字槽一律 `{angka}` 占位，无真实数据残留

---

## 模块五：场景对话生成规则

### 5.1 汇报场景 → C5 场景对话映射

C5 规则D 要求每话题 3 个场景。四类候选场景按以下决策矩阵选 3：

| 场景类型 | 标志 | 触发条件（看话题语义） | 优先级 |
|---|---|---|---|
| **S-A 向上汇报** | 对董事会/董事长/总部视频会 | 每个话题**必选**（汇报课程主线） | 固定 |
| **S-B1 平级协调** | 跨部门：工程↔生产↔采购↔物流 | 话题含 接口/配套/移交/到货 类语义 | 二选一 |
| **S-B2 下属指导** | 给部门经理布置任务、查进度 | 话题含 执行/班组/节点/验收 类语义 | 二选一 |
| **S-C 外部对接** | 对政府部门/供应商/承包商/社区 | 话题含 许可/合规/采购/物流/劳工 类语义 | 条件选 |

**规则 5.1.1**：每话题 3 场景 = S-A + (S-B1 或 S-B2) + (S-C 若触发，否则 S-B 两选二)。

**规则 5.1.2**：三个场景类型不得重复；话题连续两周出现时，第二次 S-B 必须轮换（B1↔B2）。

**规则 5.1.3**：全部场景人物、职务沿用平台统一设定（总经理 + 董事会 + 部门经理 + 外部单位），保持跨话题连续性。

### 5.2 单场景对话结构设计（开场 → 主体 → 收尾）

每场景 10-20 句（建议落 14-16 句），三段式固定分配：

| 段落 | 句数 | 功能 | 写作要点 |
|---|---|---|---|
| 开场 | 2-4 | 寒暄 + 定调 | 称呼（Bapak/Ibu/Pak/Bu）+ 一句 agenda："Hari ini saya akan melaporkan progres..." |
| 主体 | 6-10 | 五段叙事 | 按 4.1.2 主线顺序排话轮；每个话轮 = 汇报人 1-2 句（嵌模板）+ 对方 1 句（追问/确认） |
| 收尾 | 2-3 | 行动项 + 跟进 | 确认 action items、下次汇报时间、礼貌收尾 "Terima kasih atas perhatian Bapak." |

**话轮配比规则**：主体至少 3 个话轮；对方追问中至少 1 个必须是"非善意话轮"（质疑/追问），不能只演顺毛对话——真实汇报一定有质询（此句同时是模块六的钩子来源）。

### 5.3 核心词汇嵌入规则

- **覆盖硬指标**：单场景 ≥8 个 topic.vocab 核心词，3 场景合计 ≥20 个（对齐 C5 规则C 的 20-40 词区间下限）。
- **复现硬指标**：每个核心词至少出现在 2 个不同场景中（间隔复现，利于记忆）。
- **密度红线**：生词（用户未掌握的词）密度 ≤30% 的句子；一句不塞 2 个以上生词。
- **BIT 接入**：核心词首次出现处标注 `[BIT: word]`，渲染层走 `showBITInfo` 四级回退链弹窗（对齐 C5 规则C.4 与 BIT 规范四）。
- **自然度要求**：模板句必须揉进对话流，禁止连续 2 句都是模板原句；模板句之间用口语短句过渡（"Baik, saya lanjutkan..." / "Seperti tercantum di laporan...")。

**嵌入密度自检表**（每场景对话稿末尾附）：

```markdown
场景 S-A 词汇覆盖: progres, tungku, pemasangan, uji coba, kendala, mitigasi, jadwal, target = 8/8 ✓
复现检查: mitigasi(S-A, S-C) ✓ | kendala(S-A, S-B1) ✓ | ...
BIT 弹窗点: [BIT: mitigasi] 第4句; [BIT: jadwal] 第7句
```

### 5.4 语言难度控制

对用户的水平假设：能用印尼语日常沟通 + 阅读简单公文，但**正式商务汇报句式不熟**。对话是给这个水平的人"开口用"的，不是文学作品。

| 控制项 | 硬约束 |
|---|---|
| 句长 | ≤25 词/句；超过则拆两句 |
| 信息密度 | 一句只承载一个信息点 |
| 时态优先级 | sedang → telah/sudah → akan 梯度出现；虚拟语气禁用 |
| 语态 | 主动 meN- 为主；被动 di- 每场景 ≤3 处 |
| 从句 | `yang` 定语从句可用；`bahwa/ketika` 从句每场景 ≤3 处 |
| 行业黑话 | 每场景新增 ≤2 个，必须给中文注释 |
| 术语规范 | 冶炼园区标准术语（tungku RKEF, ferronikel, AMDAL, K3, smelter），禁自造词 |

**降级通道**：写超难度时，优先删从句、拆长句，**不许删核心词**（核心词覆盖是硬指标，句法复杂度是可调项）。

### 5.5 场景对话片段示例（S-A 向上汇报 · 话题 smelter_construction，前 6 句）

> 1. 总经理：Bapak Liu, terima kasih atas waktunya. Hari ini saya akan melaporkan progres pembangunan smelter untuk minggu ini.
> （刘董，感谢您的时间。今天我汇报本周冶炼厂建设进度。）
> 2. 董事长：Silakan, Bapak Zhang. （请讲，张总。）
> 3. 总经理：Pada minggu ini, kami telah menyelesaikan pemasangan pipa utama. [BIT: pemasangan]
> （本周我们已完成主管道安装。）
> 4. 总经理：Progres keseluruhan telah mencapai angka sebesar {angka} persen, sesuai jadwal. [BIT: jadwal]
> （整体进度已达 X%，符合计划。）
> 5. 董事长：Bagaimana dengan uji coba tungku? Apakah sudah sesuai rencana?
> （炉体试运行怎么样？按计划了吗？）← 非善意话轮，模块六钩子 H-01
> 6. 总经理：Uji coba tungku pertama sedang berjalan. Namun kami mengalami kendala teknis di bagian pendingin. [BIT: kendala]
> （一号炉试运行正在进行，但冷却部分遇到技术困难。）

### 5.6 模块五验收清单

- [ ] 3 场景类型不重复，S-A 必选，S-B 轮换已核对
- [ ] 每场景句数 10-20，开场/主体/收尾三段齐全
- [ ] 主体含 ≥1 个非善意话轮
- [ ] 核心词覆盖 ≥8/场景，合计 ≥20；复现率 ≥2 达标
- [ ] [BIT:] 标注与 topic.vocab 逐词核对无遗漏
- [ ] 难度 7 项硬约束逐场景自检通过
- [ ] 数字槽未填真实数据

---

## 模块六：问答对设计规则

### 6.1 提问类型预判（4 类，覆盖汇报中被追问的 90% 场景）

| 类型ID | 名称 | 上级典型问法（中文） | 预判信号（对话中出现即预埋钩子） |
|---|---|---|---|
| Q-T1 | 进度质疑 | 为什么滞后？什么时候能补上？ | 对话报滞后/风险/变更 |
| Q-T2 | 数据追问 | 这数字怎么来的？口径是什么？ | 对话中出现任何数字 |
| Q-T3 | 风险询问 | 最大风险是什么？对策？ | 对话提及风险/合规/安全 |
| Q-T4 | 资源请求 | 还需要什么支持？什么时候到位？ | 对话提及请求/协调 |

**规则 6.1.1**：每个话题按 4-4-3-2 配比产 13 组问答对（T1×4、T2×4、T3×3、T4×2），落在 12-15 区间。超 15 的部分进题库备选池（供 C5 规则E 测试题取材）。

**规则 6.1.2**：问答对问句必须口语化（是"听出来的追问"），不用书面长句。每类至少 2 种问法变体。

### 6.2 标准回答模板（公式化，4 段式）

每类回答统一为 **"态度 → 事实 → 措施 → 承诺"** 四段，印尼语模板如下：

**Q-T1 进度质疑 → REP-ANS-01**

```
态度: Benar, {item} memang tertunda {durasi}. （确实滞后）
事实: Penyebabnya adalah {alasan objektif}. （客观归因，禁推责）
措施: Kami sudah {tindakan 1} dan akan {tindakan 2}. （补救）
承诺: {Item} akan selesai paling lambat pada {tanggal}. （新死线）
```

**Q-T2 数据追问 → REP-ANS-02**

```
口径: Angka {X} dihitung dengan metode {metode}. （怎么算的）
来源: Sumber datanya dari {sumber}. （从哪来）
对比: Dibandingkan {periode} lalu, angkanya {naik/turun} {Y} persen. （对比）
确认: Jika Bapak perlu, kami sertakan detail perhitungannya. （留口供材料）
```

**Q-T3 风险询问 → REP-ANS-03**

```
排序: Risiko utamanya adalah {risiko}. （最大的风险）
影响: Dampaknya pada {area}: {dampak}. （影响面）
措施: Mitigasi kami: {langkah 1}; {langkah 2}. [BIT: mitigasi] （对策）
责任: Penanggung jawabnya {unit}, pemantauan setiap {frekuensi}. （责任人+频率）
```

**Q-T4 资源请求 → REP-ANS-04**

```
需求: Kami memerlukan {sumber daya}. （要什么）
数量: Jumlahnya sekitar {jumlah}. （多少）
用途: Ini untuk {tujuan}. （干什么用）
时限: Idealnya tersedia sebelum {tanggal}. （最晚何时）
```

**规则 6.2.1**：每组问答对给出 1 个标准答（完整四段）+ 2 个精简变体（各 1-2 句，供口语应急）。变体从四段里砍，砍的顺序固定为 对比→确认→责任（先砍次要信息）。

### 6.3 问答对与场景对话的配合机制

三步配合法：

1. **对话里埋钩子**：模块五主体话轮中，对方追问句即钩子（示例 5.5 第 5 句），每场景埋 1-2 个，全话题 3-4 个。钩子句末标注 `← H-01` 编号。
2. **问答对编号回指**：问答对库每条标 `H-01 → Q-T1 → REP-ANS-01`，形成"场景 ↔ 钩子 ↔ 问答对"三级索引。
3. **课程呈现方式**：
   - 场景对话页：钩子处默认折叠"遇到追问怎么答"面板，点开显示对应标准答；
   - 测试区（C5 规则E 15 题）：钩子对应的问答对是口语应答题的优先素材池；
   - 复习日：整组问答对进 C4_MAP 总结，与场景对话并列回顾。

**规则 6.3.1**：任何出现在场景对话里的质疑/追问，问答对库必须有对应条目，禁止"对话里有坑、库里没弹药"。反向也成立：库里的每组问答对，至少在一个场景中找到它的钩子或适用语境，否则移出本话题。

### 6.4 问答对完整示例（每类 1 组）

**Q-T1 / H-01**
> 问: Mengapa uji coba tungku belum selesai sesuai jadwal?（为什么炉体试运没按计划完成？）
> 标准答: Benar, uji coba tungku pertama memang tertunda tiga hari. Penyebabnya adalah kendala teknis di sistem pendingin. Kami sudah memanggil teknisi dari pabrikan dan akan mengganti komponen pendingin. Uji coba akan selesai paling lambat pada Jumat pekan depan.
> 变体A: Tertunda tiga hari karena kendala pendingin, teknisi pabrikan sudah dipanggil.
> 变体B: Selesai paling lambat Jumat depan.

**Q-T2**
> 问: Angka progres itu dari mana?（进度数字哪来的？）
> 标准答: Angka progres dihitung dengan metode bobot pekerjaan, bukan perkiraan kasar. Sumber datanya dari laporan harian kontraktor dan tim survei kami. Dibandingkan minggu lalu, progres naik sebesar delapan persen. Jika Bapak perlu, kami sertakan detail perhitungannya.
> 变体A: Dari laporan harian kontraktor, pakai metode bobot pekerjaan.
> 变体B: Naik delapan persen dari minggu lalu.

**Q-T3**
> 问: Apa risiko terbesar proyek ini sekarang?（当前最大风险？）
> 标准答: Risiko utamanya adalah keterlambatan pengiriman peralatan impor. Dampaknya pada jadwal commissioning. Mitigasi kami: pesanan cadangan sudah diajukan; opsi sewa lokal sedang dievaluasi. Penanggung jawabnya tim pengadaan, pemantauan setiap tiga hari.
> 变体A: Risiko terbesar: pengiriman impor terlambat, mitigasi sudah jalan.
> 变体B: Tim pengadaan memantau setiap tiga hari.

**Q-T4**
> 问: Apa lagi yang dibutuhkan tim ini?（团队还需要什么？）
> 标准答: Kami memerlukan tambahan tenaga kerja lokal terampil. Jumlahnya sekitar lima puluh orang. Ini untuk mempercepat pemasangan pipa di area pembangunan. Idealnya tersedia sebelum bulan depan.
> 变体A: Butuh lima puluh pekerja lokal terampil untuk instalasi pipa.
> 变体B: Idealnya tersedia bulan depan.

### 6.5 模块六验收清单

- [ ] 问答对总数 12-15，配比 4-4-3-2
- [ ] 每类 ≥2 种问法变体，问句口语化
- [ ] 每组有标准答（四段）+ 2 变体，变体砍段顺序合规
- [ ] H 编号三级索引闭合（对话钩子 ↔ 问答对双向可查）
- [ ] 回答中核心词与 topic.vocab 对齐，[BIT:] 标注齐全
- [ ] 无任何真实数据残留（数字槽占位）

---

## 质量红线（三模块共用，违反即打回）

| # | 红线 | 依据 |
|---|---|---|
| R1 | 禁止虚构具体数字/吨数/日期进入课程内容，一律 `{angka}` 占位 | 汇报数据以真实周报为准，课程只教句式 |
| R2 | 印尼语纯度，禁方言混入 | BIT 规范原则 2 |
| R3 | 语境优先项目管理/商务/冶炼园区 | C5 规则D、BIT 规范原则 3 |
| R4 | 每话题 3 场景、每场景 10-20 句 | C5 规则D 硬约束 |
| R5 | 核心词必须从 topic.vocab 提取，禁兜底词表 | C5 规则C.3 教训 V4.39.6 |
| R6 | 不编造词根/变形，不确定标 `[待核实]` | BIT 规范原则 1 |

---

## 变更记录

| 日期 | 版本 | 变更 |
|---|---|---|
| 2026-10-11 | v0.1 | 模块四/五/六初始草案，待主 session 评审 |
