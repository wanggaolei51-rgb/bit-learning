# MEMORY.md — 长期记忆（任何会话重开必读）

> 本文件是跨会话的核心记忆。每次启动优先读本文件。
> 最后更新：2026-10-02（策略库落盘 + V4.39.6 核心词修复 + BIV 三修复）

---

## 一、我是谁 & 用户是谁

### 我（Agent）
- **角色**：Leo_kimi 的个人助理 + LEO-BIR 项目执行位
- **SOUL 核心**：真诚帮助而非表演性帮助；有观点敢说不；先自己查再问人；内外有别——内部大胆（读文件/整理/学习），外部谨慎（发邮件/公开发文先问）；不替用户发声
- **Emoji 签名**：未选定（IDENTITY.md 待填）
- **原则**：重要事情必须写文件，不做"心理笔记"

### 用户
- **名字**：Leo_kimi
- **时区**：Asia/Shanghai (GMT+8)
- **身份**：BIT 项目所有者，常驻印尼 Morowali 冶炼工业园区相关商务场景
- **沟通渠道**：微信（openclaw-weixin）、Kimi 群聊
- **已知习惯**：深夜活跃（23:00–01:00 常见）；用"？"催促回复表示在等

---

## 二、LEO-BIR 策略体系（核心认知，不得再说不认识）

### 产品本体
**LEO-BIR** 印尼语学习平台——单文件 HTML + GitHub Pages，当前 **V4.39.6**，240 个 commit。
为印尼 Morowali 冶炼工业园区总经理定制的个人学习工具。词库 120+ 词条，主题课 topic22–29。

### 策略代号一览

| 代号 | 角色 | 职责 | 备注 |
|---|---|---|---|
| **BIR** | 产品本体 | LEO-BIR 平台本体 | V2.0 SPA 起步 → V4.39.5；艾宾浩斯复习/三关生词本/课时测试/会员系统 |
| **BIT** | 内容生产标准 | 九字段词条规范 V1.0 体例 | 内嵌任务模板："按BIT V1.0策略更新 xx 的笔记单词并更新上传" |
| **BIO** | 内容审查 | BIT 初稿 → BIO 定稿 | 双审、R1–R17 修订、视频注册表 BIO 印章 3d63246c |
| **RCO** | 审计 | A1 抽样 / A3 词级三方对账 / W1–W2 处置 / WARN 拦截 / APPROVE | 同类问题 N 次直报 |
| **TSO** | 执行 | 改 index.html | 曾审出 EPISODE.parts=8 阻塞缺陷 |
| **C5** | 课程结构策略 | C4→C5 升级（V4.17.0） | 3.5 vocabDB 防漏 / 3.6 BIT 九字段 / 3.7 生词本同步；10/1–10/10 课程合规 |
| **M2** | 管理机制 | M2 V2.3 时间管理（30 秒确认+工期考核+部署复审） | M2.2 三审机制（TSO+RCO+BIO） |
| **BIV** | 视频策略 | 剪影引擎 v2、daily-1.0.0 / daily-2.0.0 | 对应工作区 id-dialogue-video 管线 |

### 运行机制
BIT 生成 → BIO 审查定稿（R1–Rn 修订）→ RCO 审计（WARN/FAIL→修复→APPROVE）→ TSO 执行改 index.html → 部署 → 上线验证。
三方审核（TSO+RCO+BIO）持续运行。

### 策略文档缺口 ✅ 已解决 2026-10-02
策略库已落盘到 `/strategies/` 目录（6 个文件）：
- README.md（索引）
- C5-课程生成策略.md (v2.1)
- M2-管理机制.md (v2.3)
- BIT-词条规范.md (v1.0)
- RCO-审计策略.md (v1.0)
- BIV-视频策略.md (v2.2)

---

## 三、进化史（版本脉络）

```
V0.1 (07-15)  基础框架：能力检测/词缀课程/场景对话/演讲背诵/每日录入/120+词
V0.2 (07-16)  实时翻译窗口/词缀自动拆解/语音朗读/翻译历史/移动端适配
V2.0          SPA + hash 路由 + 日历 + 生词本 + 课时测试 + 会员系统
V4.2–4.4      早期迭代
V4.16.2       稳定版
V4.17.0       C4→C5 升级（BROKEN 后有修复）
V4.28.x       批量修复期
V4.29–4.31    每日笔记系统上线
V4.33.0       0928 每日笔记 37 词（BIT 初稿+BIO 定稿 R1-R8，双库写入）
V4.34.0       0929 每日笔记 39 词（RCO 审计拦截热修，词表与用户输入逐词对齐）
V4.35.0       每日复习视频 Layer 1（视频库页+overlay 播放器，daily-1.0.0 引擎）
V4.36.0       每日视频引擎 daily-2.0.0（剪影人物+场景剧场化，时长-67%）
V4.37.0       0930 笔记 26 词（BIT 对账纠正 23→26，BIO R1-R17 定稿）
V4.38.0       C5 三优化（印尼语纯度+场景收敛+弹窗变形来源提示）
V4.38.3       话题 22-29 场景收敛 + 视频 8 集全量重生成
V4.38.4       视频合并重构（8集×5词→3集×13词）+ vocabDB 129 词 BIT 补全
V4.38.5       129 词 BIT 完整格式重写（BIO 双审，修正 10 处编造词/方言混入）
V4.38.6       紧急修复白屏（vocabDB 孤立逗号 → JS 语法错误）
V4.38.9       showTip 完整 BIT 弹窗 + 三级回退字段映射
V4.38.10      拼写勘误 memroyeksikan→memproyeksikan
V4.38.11      bitVocabDB 全量同步（121 条唯一词，修复生词本四级回退二级缺失）
V4.39.0–.2    showBITInfo 系列修复（引号/括号/闭合）
V4.39.3       删除重复 addWB + 版本号修复
V4.39.4       截断 </html> 后残留代码 + showTip/showWordPopup 接入 bitVocabDB
V4.39.5       1001 笔记 27 词（33 词元去重+对账表）+ .gitignore 治理
V4.39.6       C5核心词嵌套修复(三话题vocab双层括号→fallback兜底词表Bug) + BIV三视频修复(字号/气口/coach) + strategies策略库落盘 ★当前版本
```

---

## 四、技能 / 工具链

### 每日笔记部署 SOP（BIT V1.0 体例，标准流程）
```
用户输入词元（空格分隔）
  → 去重统计唯一词
  → 按 BIT V1.0 体例生成定稿 md（附词数勘误对账表——附录一逐条映射）
  → python3 scripts/md_to_dailynote.py <md> <date> <topic> index.html
       （解析词条 → 生成 dailynote_<mmdd>.js → 合并 dailyNotesDB + bitVocabDB，幂等）
  → python3 check_syntax.py index.html（JS 解析 + 源档案注释头检查）
  → bash deploy-check.sh（8/8 硬性检查）
  → 版本号三处更新（title / ver badge / video_registry 版本记录）
  → git commit + push main
  → GitHub Pages ~70s 生效
  → 线上验证（curl md5 比对 + 日期存在性 + 版本号 badge）
```

### 工具链文件
| 文件 | 功能 |
|---|---|
| `scripts/md_to_dailynote.py` | BIT md → JS 数据片段 → 合并 index.html（幂等，同词覆盖） |
| `check_syntax.py` | 提取所有 `<script>` 块 node --check 解析 + dailynote 源档案注释头检查 |
| `deploy-check.sh` | 8 项硬性检查：分支/未提交/版本号/括号平衡×2/重复声明×3 |
| `deploy.sh` | 一键部署到 GitHub Pages（需 GITHUB_TOKEN + GITHUB_USER） |
| `video_registry.js` | BIR Video Registry — 唯一真相源（BIO 印章验证） |
| `bit-deploy-bak/upgrade_c5*.py` + `verify_c5.py` | C4→C5 升级脚本（TSO 执行） |

### 词条规范（BIT V1.0 九字段）
word / cn / en / root / forms[] / formsNote / note / synonyms[] / antonyms[] / examples[]

### 词条原则
- 保守不拆词根（不确定标 [待核实]）
- 复习日重收同词 → bitVocabDB 覆盖更新为最新版（设计行为）
- 例句优先项目管理/商务/冶炼园区语境
- 印尼语纯度（C5 要求，禁方言混入）

### 关键教训（血泪史）
1. **"页面显示代码"→ 先查 `</html>` 之后是否有残留代码块**（V4.39.4 教训）
2. **BIT 弹窗路由查 bitVocabDB 而非 vocabDB**——两库字段名不一致：vocabDB 用五字段（ipa/cn/en/root/tag），bitVocabDB 用九字段（transform/example/synonym vs forms/examples/synonyms 命名不一致坑过一次）
3. **vocabDB 词条间多一个逗号 → 整页白屏**（V4.38.6 教训，孤立逗号行 1906）
4. **历史 commit 只提交 index.html**，untracked 文件堆积是常态；已加 .gitignore 治理
5. **RCO 审计必须词级对齐**——用户输入词元 vs 最终词条逐词对账（V4.34.0 教训：23→26 词对账纠正）
6. **备份习惯**：合并前 index.html 备份到 /tmp/；bit-deploy-bak 有 60+ 份历史备份

### 数据检索方法
- **找策略/历史信息：挖 git log + index.html 版本记录**，不能只看 memory/*.md
- 238 条提交 = 完整进化史；工作区根目录 dailynote_*.js 源档案（0916–1001，14 份）
- `mir-data/` = fetch-mir.js 抓的汇率/数据（history: AHD/AL0/AO0/I0/NI0/NID/ZC0）

---

## 五、Kimi 群聊多 Agent 协作（2026-10-02 组建）

- 群名：**Leo_kimi2**，目标"任务2"
- **Kimi (kimi) = 指挥位**：拆任务、派活、质量把关、汇总交付
- **Leo_kimi（我）= 执行位**：查资料、写文档、跑代码
- 第一次任务：回顾所有 agent 和策略——首轮只按记忆汇报被点名漏掉 BIR/RCO/BIO/C5/M2，深挖 git 提交史后补全

---

## 六、工作区结构速查

```
/root/.openclaw/workspace/
├── index.html          ← 主产品（4.9MB，唯一部署文件）
├── MEMORY.md           ← 本文件
├── SOUL.md / AGENTS.md / USER.md / IDENTITY.md / TOOLS.md
├── memory/             ← 日志（2026-10-01 起）
│   └── .dreams/        ← 语义记忆索引
├── scripts/            ← md_to_dailynote.py / fetch-mir.js / fetch-history.js
├── dailynote_*.js      ← 14 份每日笔记源档案（0916–1001）
├── topic22-29*.js      ← 8 个主题课源文件
├── bit-deploy/         ← 部署仓库（含 60+ 备份）
├── bit-deploy-bak/     ← 更全备份 + C5 升级脚本
├── videos/daily/       ← 每日视频文件
├── mir-data/           ← 汇率数据
└── check_syntax.py / deploy-check.sh / deploy.sh / video_registry.js
```

---

## 七、已知缺口 & 待办

- [ ] IDENTITY.md 未填（名字/形象/Emoji 待选）
- [ ] USER.md 待补充细节
- [x] ~~C5/M2 策略正文文档缺失~~ → 已落盘 strategies/ 目录
- [ ] 2026-10-01 之前的会话历史不可见（记忆系统从 10-01 启动）
- [ ] 未配置 cron 定时任务
- [ ] avatar.jpg 已存在但未关联 IDENTITY.md
- [ ] BIV 视频修复后需用户实测验证（字号/气口/讲解三个问题）

---

*本文件由 Leo_kimi 指令于 2026-10-02 创建，整合 git 提交史 + 全部记忆文件 + 工作区资产。*
