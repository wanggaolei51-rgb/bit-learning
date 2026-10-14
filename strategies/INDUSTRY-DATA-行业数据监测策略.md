# INDUSTRY-DATA 行业数据监测策略

> 版本: 1.0 | 创建: 2026-10-14 | 缘起: ASPIRE-Stargate 项目漏检事件 (V4.42.4)

---

## 一、背景与复盘

### 事件
用户发现 Astra 集团 United Tractors (UNTR) 旗下的 **ASPIRE-Stargate 工业园**（东南苏拉威西省北科纳威县 Molore， aspire.id）——含 MottMac 总体规划、RKEF 在建、HPAL 可研——未收录进 BIR 镍冶炼地图 (nickelData)。

### 根因（3 条）
1. **信源结构偏差**：nickelData 建库主要依赖 Mysteel/SMM/东方证券/紫金天风等**中文行业研报**，天然覆盖中资主导园区（IMIP/IWIP/OBI/德龙系）；ASPIRE 是印尼本土 Astra 集团项目，中文研报几乎不报道。
2. **项目"非事件化"**：2017 年收购 → 2021 年委任 MottMac/签约 PLN → 2022 年签 EPC → 投产从 2024 推迟到 2027，长期处建设前期，未触发任何"产能投产"类统计口径的收录。
3. **无持续监测机制**：镍地图为一次性建库，没有定期巡检信源的 SOP，本土开发商新项目（Astra/Adaro/ANTAM/MIND ID 系）漏检风险持续存在。

### 同类风险项目（非穷尽）
- ANTAM 系新项目（Pomalaa/UBN 扩建、Sorowako HPAL）
- MIND ID/IBC 系（Hydromet 等）
- Adaro Minerals (ADI) 巴鲁托项目
- ESG/GEM、SGI(Sunda Minerals)、NIC 二期等本土/合资
- 中资小体量：凡口、江苏汇鸿、Saroa 等

---

## 二、监测信源清单（分级）

### A 级 — 公司一手信源（项目级精度，优先）
| 信源 | 覆盖 |
|---|---|
| aspire.id / UNTR 投资者关系 (unitedtractors.com) | Astra 系镍 |
| antam.com / vale.com/indonesia | 国企系 |
| adaro.com / minerals.adaro.com | Adaro 系 |
| mindid.id / indonesiabattery.co.id | MIND ID/IBC |
| PLN RUPTL 年度电力供应规划 | 园区配套电源信号 |

### B 级 — 行业媒体（事件触发）
- **Petromindo**（印尼，英文，镍项目进度最细）
- **SMM/Mysteel 海外版 / Fastmarkets MB**
- **Kontan / Bisnis Indonesia / Investor.id**（本土财经，收购/EPC/点火事件）

### C 级 — 政府公示（合规信号）
- ESDM RKAB 开采计划批复公示
- 印尼投资部 BKPM 下游激励清单
- 环境部 KLHK AMDAL 批复（项目开工前哨）

### D 级 — 研报（产能口径校准，季度）
- 东方证券/紫金天风/国海证券镍专题
- Macquarie/Goldman 镍供需平衡表

---

## 三、巡检 SOP

| 频率 | 动作 | 产出 |
|---|---|---|
| **季度** | A 级信源扫一遍 + B 级关键词检索（"smelter 点火/EPC 签约/RKAB 批复"） | 镍地图差异清单（新增/状态变更/产能变更） |
| **半年** | 对照 D 级研报校准产能口径与状态标注 | nickelData 数据质量报告 |
| **即时** | 用户/群聊提供线索（如本次 MottMac 规划） | 48h 内完成收录部署（本次 V4.42.4 达标） |

### 收录触发条件（满足任一即收录）
1. 园区/项目有明确主体 PT 公司 + 地理坐标
2. 有官方产能/工艺披露（哪怕可研阶段）
3. EPC 合同签订或主体工程开工
4. RKAB/AMDAL/IUP 公示且计划建冶炼设施

### 数据字段规范
沿用 nickelData 现有 12 字段：`项目名/企业名_中文/企业名_英文_PT/工艺路线/产品/年产能_万镍金属吨/状态/主要股东及持股/数据来源/备注/投产时间/预计投产时间/建设进度/产能说明_品位口径/产线数`
- **数据来源必须标注具体信源+日期**（如 "Petromindo 2025-04"）
- 状态枚举限定：在产/在建/规划/停产/部分在产/已暂停
- 坐标口径：冶炼厂/矿区 IUP 实测坐标优先（学术论文/公司披露），禁止凭印象填

---

## 四、防呆机制（RCO 审计扩展）

- 镍地图数据变更纳入 RCO A1 抽样审计范围（同类错误 N 次直报）
- **每次收录必答三问**：①信源是什么 ②为什么此前没收录 ③同类项目还有谁可能漏
- 地图页版本记录中注明数据来源与复盘结论（changelog 可见）

---

## 五、本次执行记录（V4.42.4, 2026-10-14）

| 项 | 内容 |
|---|---|
| 收录对象 | 东南苏拉威西省::ASPIRE-Stargate工业园(北科纳威Molore) |
| 坐标 | (-3.328, 122.290) — JIPL 2022 论文 IUP 实测 122°16'59"–122°17'50"E / 3°19'35"–3°19'46"S |
| 条目 | RKEF一期 2×33MVA 在建 1.3万镍吨 + HPAL 3万吨级 规划 |
| 校验 | check_syntax PASS · deploy-check PASS · 线上 MD5 验证 PASS |
| 复盘结论 | 中文研报信源盲区 → 本策略落地 |
