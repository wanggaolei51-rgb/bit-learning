# BIT 日记 V2 进阶方案：从单词到词组与万能句型

> 状态：草案 v1.0（供 Leo_kimi 决策参考）
> 日期：2026-11-08
> 背景：学习内容已从单词扩展到词组（phrases）和万能句型（patterns），BIT 日记体系需同步升级

---

## 一、现状盘点

| 模块 | 现状 | 缺口 |
|---|---|---|
| BIT 词条库 | `bitVocabDB`（3142 词，九字段） | 只覆盖单词 |
| 日记 | `dailyNotesDB[date]` → 词条数组（每日一批） | 只收单词 |
| 一键 BIT | `oneClickBIT()`：分词（空白/标点切分）→ 生成任务文本 | 词组被切成单词；句型无法录入 |
| 翻译输入库 | 翻译弹窗走 `bitVocabDB` + `vocabDB` 单词库 | 词组/句型翻译无库可查 |
| 翻译版块 | `doTranslate` 单词级替换高亮 | 多词单位不能整体翻译 |
| 复习 | 生词本/艾宾浩斯按词条调度 | 词组句型无入口 |

## 二、核心决策：一个库还是三个库？

**推荐方案 B：三库并列**（决策建议，可讨论）

```
bitVocabDB     单词库（现有，不动）
phraseVocabDB  词组库（新增）：{id, cn, en, usage, note, examples[], source, synonyms[]}
patternVocabDB 句型库（新增）：{id, cn, level, formula, structure, grammar, scene, ex[], slots[]}
```

理由：
1. 字段结构差异大——词组要 usage（正式/通用/口语），句型要 formula/slots，硬塞一个库会造成大量空字段（vocabDB vs bitVocabDB 字段不一致的坑已经踩过）
2. 弹窗、复习、对账可以按 type 路由，逻辑清晰
3. 每库独立膨胀可控，RCO 对账单元明确

备选方案 A（统一库加 `type` 字段）：查询简单但字段稀疏、单库体积失控，**不推荐**。

## 三、翻译输入库设计

**新增 `phraseInputLib`（词组/句型翻译输入库）**，与三个内容库分离：

- 定位：纯翻译对缓存（轻量），不等于教学内容库
- 字段：`{key(小写原文), cn, en, kind(phrase|pattern), hit(命中次数), ts}`
- 作用：翻译版块和弹窗的**第一落点**——先查输入库（快），未命中回退内容库，再未命中走生成
- 治理：hit 排序、定期把高频命中沉淀为正式词条（BIO 双审）

## 四、各模块改造点

### 4.1 日记结构（dailyNotesDB V2）
```
dailyNotesDB[date] = {
  words:    [...现有词条...],
  phrases:  [{phrase库条目 + 当日笔记note}],
  patterns: [{pattern库条目 + 当日笔记note}]
}
```
- UI：日期详情页笔记卡分三个分组（📝 单词 / 🔗 词组 / 🧩 句型），可折叠
- 兼容：旧数据无 phrases/patterns 字段——渲染时 `||[]` 兜底，**不迁移历史数据**（零风险）

### 4.2 一键 BIT V2
- 输入解析升级：**最长匹配优先分词**——先用 phrase/pattern 库做整段匹配（"bertemu dengan klien" 作为词组命中就不拆），剩余部分按单词切
- 句型录入：输入含 `[方括号元]` 或命中 pattern 库 → 走句型通道
- 50 词上限改为"50 个学习单元"（词组/句型各算 1 单元）
- 任务文本模板更新：`按BIT V2.0策略更新 <date> 笔记: 单词x词 词组x组 句型x条`

### 4.3 翻译版块
- `doTranslate` 分词器改最长匹配：phrase/pattern 库 → bitVocabDB → vocabDB
- 高亮规则同步：多词单位整体包 span，点击弹对应库弹窗（showPhraseInfo / showPatternInfo）
- 弹窗家族新增两个：`showPhraseInfo(key)`、`showPatternInfo(key)`（复用 BIT 弹窗样式）

### 4.4 生词本/复习
- 三库统一调度表：`reviewQueue` 增加 `kind` 字段，艾宾浩斯曲线不变
- 生词本分组显示（词/词组/句型三个 tab）

## 五、RCO / M2 / BIT 策略条款调整

1. **BIT V1.0 → V2.0**：九字段体例扩展为三套体例（词条九字段 / 词组六字段 / 句型八字段），策略文档并列发布
2. **RCO 对账**：对账单元从"词"变为"学习单元"（word+phrase+pattern 三类分别计数，附录对账表分三段）
3. **lint 规则**：新增句型 formula 方括号闭合校验、词组 usage 字段枚举校验
4. **例句铁律延伸**：词组/句型例句同样执行"完整印尼句+全角中文括号"铁律
5. **撞库规则**：词组撞库按"小写全串"判重；句型撞库按 formula 去空格小写判重

## 六、分期落地建议

| 期 | 内容 | 预估 |
|---|---|---|
| P1 | phraseVocabDB + showPhraseInfo + 翻译最长匹配 + 一键 BIT 词组通道 | 1 个部署日 |
| P2 | patternVocabDB + showPatternInfo + 日记三块分组渲染 | 1 个部署日 |
| P3 | 复习调度 kind 化 + 生词本分组 + phraseInputLib 沉淀机制 | 1 个部署日 |

## 七、待你拍板的决策点

1. **库结构**：三库并列（推荐）还是统一库？
2. **词组标准**：词组最小单位——必须是≥2词的固定搭配？还是含短句（如 "Selamat pagi, Bapak Direktur."）？建议：固定搭配+套语句均可，usage 字段区分
3. **句型来源**：万能句型是否必须来自 CA 课程（patterns 字段），还是允许日记自由录入？
4. **复习优先级**：词组/句型是否进艾宾浩斯，还是只进生词本手动复习？
5. **P1 启动时间**：本周内还是等 CA 话题7 稳定后？

---

*本方案由 Leo_kimi（执行位）起草，供指挥官决策。*
