# MEMORY.md - 长期记忆(任何会话重开必读)

> 本文件是跨会话的核心记忆。每次启动优先读本文件。
> 最后更新：2026-10-23（V4.46.9 视频列表补全三天 + 1022视频 + BIT_BIV写入SOP）

---

## 一、我是谁 & 用户是谁

### 我(Agent)
- **角色**:Leo_kimi 的个人助理 + LEO-BIR 项目执行位
- **SOUL 核心**:真诚帮助而非表演性帮助;有观点敢说不;先自己查再问人;内外有别--内部大胆(读文件/整理/学习),外部谨慎(发邮件/公开发文先问);不替用户发声
- **Emoji 签名**:未选定(IDENTITY.md 待填)
- **原则**:重要事情必须写文件,不做"心理笔记"

### 用户
- **名字**:Leo_kimi
- **时区**:Asia/Shanghai (GMT+8)
- **身份**:BIT 项目所有者,常驻印尼 Morowali 冶炼工业园区相关商务场景
- **沟通渠道**:微信(openclaw-weixin)、Kimi 群聊
- **已知习惯**:深夜活跃(23:00-01:00 常见);用"?"催促回复表示在等

---

## 二、LEO-BIR 策略体系(核心认知,不得再说不认识)

### 产品本体
**LEO-BIR** 印尼语学习平台--单文件 HTML + GitHub Pages,当前 **V4.46.6**。
为印尼 Morowali 冶炼工业园区总经理定制的个人学习工具。词库 120+ 词条,主题课 topic22-29。

### 策略代号一览

| 代号 | 角色 | 职责 | 备注 |
|---|---|---|---|
| **BIR** | 产品本体 | LEO-BIR 平台本体 | V2.0 SPA 起步 → V4.39.5;艾宾浩斯复习/三关生词本/课时测试/会员系统 |
| **BIT** | 内容生产标准 | 九字段词条规范 V1.0 体例 | 内嵌任务模板:"按BIT V1.0策略更新 xx 的笔记单词并更新上传" |
| **BIO** | 内容审查 | BIT 初稿 → BIO 定稿 | 双审、R1-R17 修订、视频注册表 BIO 印章 3d63246c |
| **RCO** | 审计 | A1 抽样 / A3 词级三方对账 / W1-W2 处置 / WARN 拦截 / APPROVE | 同类问题 N 次直报 |
| **TSO** | 执行 | 改 index.html | 曾审出 EPISODE.parts=8 阻塞缺陷 |
| **C5** | 课程结构策略 | C4→C5 升级(V4.17.0) | 3.5 vocabDB 防漏 / 3.6 BIT 九字段 / 3.7 生词本同步;10/1-10/10 课程合规 |
| **M2** | 管理机制 | M2 V2.3 时间管理(30 秒确认+工期考核+部署复审) | M2.2 三审机制(TSO+RCO+BIO) |
| **BIV** | 视频策略 | 剪影引擎 v2、daily-1.0.0 / daily-2.0.0 | 对应工作区 id-dialogue-video 管线 |

### 运行机制
BIT 生成 → BIO 审查定稿(R1-Rn 修订)→ RCO 审计(WARN/FAIL→修复→APPROVE)→ TSO 执行改 index.html → 部署 → 上线验证。
三方审核(TSO+RCO+BIO)持续运行。

### 策略文档缺口 ✅ 已解决 2026-10-02
策略库已落盘到 `/strategies/` 目录(6 个文件):
- README.md(索引)
- C5-课程生成策略.md (v2.1)
- M2-管理机制.md (v2.3)
- BIT-词条规范.md (v1.0)
- RCO-审计策略.md (v1.0)
- BIV-视频策略.md (v2.2)

---

## 三、进化史(版本脉络)

```
V0.1 (07-15)  基础框架:能力检测/词缀课程/场景对话/演讲背诵/每日录入/120+词
V0.2 (07-16)  实时翻译窗口/词缀自动拆解/语音朗读/翻译历史/移动端适配
V2.0          SPA + hash 路由 + 日历 + 生词本 + 课时测试 + 会员系统
V4.2-4.4      早期迭代
V4.16.2       稳定版
V4.17.0       C4→C5 升级(BROKEN 后有修复)
V4.28.x       批量修复期
V4.29-4.31    每日笔记系统上线
V4.33.0       0928 每日笔记 37 词(BIT 初稿+BIO 定稿 R1-R8,双库写入)
V4.34.0       0929 每日笔记 39 词(RCO 审计拦截热修,词表与用户输入逐词对齐)
V4.35.0       每日复习视频 Layer 1(视频库页+overlay 播放器,daily-1.0.0 引擎)
V4.36.0       每日视频引擎 daily-2.0.0(剪影人物+场景剧场化,时长-67%)
V4.37.0       0930 笔记 26 词(BIT 对账纠正 23→26,BIO R1-R17 定稿)
V4.38.0       C5 三优化(印尼语纯度+场景收敛+弹窗变形来源提示)
V4.38.3       话题 22-29 场景收敛 + 视频 8 集全量重生成
V4.38.4       视频合并重构(8集×5词→3集×13词)+ vocabDB 129 词 BIT 补全
V4.38.5       129 词 BIT 完整格式重写(BIO 双审,修正 10 处编造词/方言混入)
V4.38.6       紧急修复白屏(vocabDB 孤立逗号 → JS 语法错误)
V4.38.9       showTip 完整 BIT 弹窗 + 三级回退字段映射
V4.38.10      拼写勘误 memroyeksikan→memproyeksikan
V4.38.11      bitVocabDB 全量同步(121 条唯一词,修复生词本四级回退二级缺失)
V4.39.0-.2    showBITInfo 系列修复(引号/括号/闭合)
V4.39.3       删除重复 addWB + 版本号修复
V4.39.4       截断 </html> 后残留代码 + showTip/showWordPopup 接入 bitVocabDB
V4.39.5       1001 笔记 27 词(33 词元去重+对账表)+ .gitignore 治理
V4.39.6       C5核心词嵌套修复(三话题vocab双层括号→fallback兜底词表Bug) + BIV三视频修复(字号/气口/coach) + strategies策略库落盘
V4.39.7-.9    1002笔记三批(41→55→74词条, PMBOK复习+量化风险+环保合规专题) + agents/BIT笔记归档
V4.40.0       1003笔记 27词(26词元语义拆分+1, 13词覆盖更新含缩写小写键核验klhk/pplh/apd)
V4.40.1       1004笔记 11词(连字符归并x2, 4覆盖更新)
V4.40.2       1003笔记追加批次二 27词(28词元去重+同日重收x3, 54词条累计, ukl-upl小写键核验)
V4.41.0       REP2C首期课程上线: 0929周报转化话题30周汇报(38词+3场景16/14/12句+15题) · vocabDB插入查重WARN修复(18撞库撤重插20) · 话题30 allDays综合路由10-11 · 线上MD5验证PASS
V4.41.1-.3    1010笔记35词(K3应急) → 周汇报3天路由补全(10-11/12/13) → 话题30补speeches修Day3白屏
V4.42.0       任务三合一: 词根释义规范落地 + REP2C月报课monthly_report(10/14-16, 38词+3场景15/15/14句+3演讲+6语法{新对象格式}) + 1011日记补批17词
V4.42.1       月报课10-14/10-16白屏热修: grammar新格式{name,detail}无examples→渲染崩溃(同类第2次, check_syntax/deploy-check拦不住) · fmtGrammarRule双格式兼容+8渲染点适配 · renderTopicQuiz回退topic.vocab(修REP2C中文tag不匹配) · 线上数据端到端6/6 PASS
V4.42.2       1012笔记30词(综合事务: 32词元去重2+重收覆盖9, 谚语kepala-di-pijat-kelapa-di-parut+连字符due-date, 105变形+60例句, RCO对账逐词映射)
V4.42.3       1013笔记39词(园区运维专题: 40词元去重1+大小写归一3+重收覆盖13, 清淤排水pengerukan/saluran/pipa+合规治理transparan/dirahasiakan, 148变形+78例句, RCO对账逐词映射) · 线上MD5验证PASS
V4.42.4       镍冶炼地图补全: ASPIRE-Stargate工业园(东南苏拉威西省北科纳威Molore) - Astra集团United Tractors项目 · RKEF 2×33MVA在建1.31万镍吨+HPAL 3万吨级规划 · MottMac总体规划WBS5000(4×33MW RKEF+镍冰铜/硫酸镍常压浸出+450MW LNG电厂+Molore/Lameruru双码头) · 复盘: 中文研报信源盲区致本土项目漏检 → INDUSTRY-DATA v1.0监测策略落地
V4.43.0       UKBI考试认证课上线: ukbi_certification话题(10/17-19) · 38核心词+3场景+3演讲+6语法+15测试 · bitVocabDB+38 · 全站13页语料采集
V4.43.1       UKBI课优化: 核心词bitVocabDB双库渲染修复(38词全展,修Day1词卡空白) + 词缀玫瑰图集成(30词缀iframe隔离, C5复习模块入口10/17起) · 内嵌HTML转义规则: </script>→<\/script>, <!--→<\!--
V4.43.2-.4    1016二批14词 → 1017笔记20词(UKBI注册实操) → 1018笔记35词(UKBI实操深化·最大单批, iIstimewa归一+butir-soal复合归并) · 三天均 RCO A3 APPROVE
V4.44.0       1019笔记49词(UKBI七级评定全收录, 历史最大批) + 生词双库同步修复×3(showWordPopup/doTranslate/renderWBList) + 主页源码注释泄露修复 + BIT策略v1.3双库条款 · 线上MD5一致
V4.45.0       CA进阶课程首期上线(CA策略v1.1九项裁定): 话题1见面Bertemu×3天(10/20-22) · 独立caData+caCalendar+独立路由ca/topic/day · 每日四块(词汇15/词组10/万能句型12按3级别配比/常用表达15/词缀10·coef月度封顶5) · 22词入库 bitVocabDB 2784→2806
V4.45.1       CA路由热修: 站内hash约定无斜杠(#ca/), 我生成链接带斜杠(#/ca/)路由永不命中→“点了没反应” · parseRoute兼容双写法 · 教训: 改路由前先实测站内hash约定, 冒烟必须跑“点击→跳转→渲染”全链路 · E2E(模拟hash→路由→渲染→入口跳转目标)全PASS · commit 633dbc0
V4.46.0       双任务: 1C5新话题ukbi_real「UKBI实战」10/20-22 -- 真实考试五部分拆三天(Day1 听力4dialog+4monolog各5题/40题30min+语法反应找错25题20min+自适应teslet停止规则 / Day2 阅读8wacana×5题40题45min+写作2题100/150词35min提示句pemantik+infografik / Day3 口语2题录制7+3/8+7min+套餐Paket1-3+七级评定Istimewa725-800→Terbatas251-325+证书2年周末颁发+15天重考) · 38核心词28沿用+10新词BIT入库(2806→2816) · 3场景47句+3演讲452词+6语法规则+15题quiz · C5 v2.1双库合规38/38 2CA/C5同日共存 -- renderDateDetail不再CA独占早退, C5课程内容+CA紫卡同屏(纯CA日保持原样) 3当日笔记一键语音播报 -- 日记+BIT词条链式TTS(onend+150ms衔接自然, id/zh交替, 词根剥中文括号), 日期页+📓笔记卡双入口, render()导航自动停止 · 备份backup-V4.45.1-preUKBIreal-20261020.tar.gz · 坑: bitVocabDB追加必须keyed格式"word":{...}(无键数组元素=语法错误)+条目间逗号+正则双反斜杠三连坑 · commit 84db159 · 线上MD5一致
V4.46.1       1020每日笔记21词(BIT V1.0定稿, 挂ukbi_real): 13新词入库(riil/pemeringkatan/hak setara bagi连字符归并/berturut-turut/mampun古体=mampu/berjabat惯用berjabat tangan/panco扳手腕KBBI berpanco/cubit/sentil·toyor口语cakapan/menghancurkan/terhadap勘误terhatap→d/bertengkar) bitVocabDB 2816→2829 · sedang扩充"中等"义(rendah-sedang-tinggi等级语境) · RCO对账21/21逐词映射 · deploy-check须在commit后干净树才PASS(顺序调整为commit→check→push) · commit 52c6e62 · 线上MD5一致(4d918421)
V4.46.4       地图瓦片换源(用户实测失效): 行业数据+7月23全球镍地图共用 CARTO dark_all、电力地图 OSM -- 境内全不可达(实测OSM/CARTO/Wikimedia超时) → 5处tileLayer换 Esri全球CDN(镍4处→World_Dark_Gray_Base暗色maxZoom16, 电力→World_Street_Map) · 坑: Esri路径序{z}/{y}/{x}与OSM惯例相反 · 备选: OSM法国镜像 · commit 2b29be6 · 线上MD5一致(08f1143b)
V4.46.5       行业数据·光伏专版(用户指令): ☀️光伏专版独立tab(电力行业内, 绿色#22c55e) —— 2026-08-25普拉博沃揭幕14个PLTS全收录(5.3GWp/135万亿盾≈76.2亿美元): 已投运2/在建6/待招标6(Batam/Banyuwangi/Pasuruan/GajahMungkur/Karangkates/Saguling/Tembesi/Jatiluhur 1688/Cirata 1250扩建/Jatigede/Madura+BESS/Gilimanuk/BankTanah) · 100GW国家规划独立汇总块(已投0.001/在建0.667/待招标4.548/规划储备94.784 GWp·总投资643亿美元) · 地图+分组+搜索+flyTo全链路自动兼容 · 坑: edit锚点撞switchNickelTab同名段冒烟抓到落错函数→特征行消歧 · node冒烟13/13 · commit 67b9d57 · 线上MD5一致(b05d44d1) ★当前版本
V4.46.6       1021每日笔记19词(挂ukbi_real Day2阅读+写作, BIT V1.0定稿): 新增14(skimming/ejaan/tanda-baca/-dalam-bentuk/justru-itu分写注记/macam-macam/beralih/temanya/lengkap-dan-runtut写作评分用语/susun-kerangka/mengetik词根tik/kacau/tenda/foodcourt外来语) + 复习覆盖5(menyesuaikan/bahkan/disajikan/kencang/sederhana) · 61变形+38例句 · RCO对账19/19 · 坑: Pages构建卡in_progress 15分钟(前三次<40s), 轮询actions/runs等completed · commit eeff1b3+5eefa4d · 线上MD5一致(3b6ae087)
V4.46.7       播报热修复(回归事故): V4.46.6 md_to_dailynote.py 合并 dailynote js 时覆盖 script 块 → dnEsc/dnRich/buildNoteEntryHtml/buildDailyNoteCardForDate 四函数丢失 → typeof buildDailyNoteCardForDate!=="function" → 笔记卡不渲染+播报按钮静默消失(用户实测上报, 三处调用点守卫无报错) · 修复: 从 b00a316 恢复四函数+卡内🔊+dn-entry锚点 · 防复发: 部署后 grep 函数定义必须存在 · commit d123299 · 线上MD5一致(5fb28cf7)
V4.46.8       1022每日笔记15词(10新增+5复习覆盖, 挂ukbi_real Day3): 新增10(acara/ferware外来语[待核实拼写,疑为farewell]/minus/lasik缩写/pembedahan/komik/seni-bela-diri复合键/bersifat/menentukan-hal-berikutnya复合学习键/berulang-ulang) + 复习覆盖5(mata/jenjang/berturut-turut/ejaan/tanda) · 28变形+30例句 · RCO对账15/15 · **播报防复发治本**: md_to_dailynote.py RENDER_FUNCS 补齐V4.46.2/3四函数(dnEsc/dnRich/buildNoteEntryHtml/buildDailyNoteCardForDate+新版buildDailyNoteCard复用), 每次合并自动写入, 根除函数丢失(原RENDER_FUNCS只有旧版toggleDailyNote+内联buildDailyNoteCard) · 坑: 第263行删除正则会匹配整个区域含V4.46.2/3函数, RENDER_FUNCS不完整=每次跑管线都丢函数 · check_syntax PASS · deploy-check 8/8 · commit c504ab5 · 线上V4.46.8验证PASS
V4.46.9       视频列表补全+1022视频: VIDEO_DB注册表1天→3天(0929项目管理39词3集/1021 UKBI Day2 19词2集/1022 UKBI Day3 15词2集) · 1022视频 biv_daily.py --force 产出2集(p1:13词≈284s/p2:2词≈56s) lint 10/10 PASS · BIO印章1f2ea1b5 · **BIT md写法坑**: 同/反义词无内容必须写 `—`（单独破折号），写 `—（无严格反义）` 或 `无严格同义` 会致 lint#6 语言隔离FAIL(中文进id通道) · **BIO印章坑**: 文件必须 `sha8: xxx` 格式无尾部换行, printf默认加\n会致bio_gate regex `stamp=?` · **BIT_BIV v1.1**: 视频生成正式写入每日笔记部署SOP(固有步骤不得遗漏) · commit aa9ec4c+b3ef407 · 线上三天注册表+视频200全PASS ★当前版本
V4.46.3       播报二次归位(用户实测仍错位): 按钮下沉 buildDailyNoteCardForDate 卡内 -- 课时测试页(startTopicQuiz)/日记页/CA日三处共用一处源码, 每天日记一个🔊 · tc 课程分支移除无主按钮(该页无词条卡无可跟随=上版错位根因) · 纯文本日兜底按钮 · 22项冒烟全PASS · commit b00a316 · 线上MD5一致(ae372314)
V4.46.2       播报归位日记页+跟随高亮: 1入口修正 -- 日历日记页(showDateStudyRecord)新增🔊按钮+当日BIT词条卡, CA日底部补日记区, 课程日保留按钮, 三入口共用broadcastDay(ds) 2内容净化bcRootOk -- 词根仅干净单词(/^[A-Za-z][A-Za-z-]{2,}$/且≠词目)才播, 括号类词根(saj/saji)不再乱播 3跟随定位 -- 词条卡锚点dnw-<ds>-<i>+dn-entry, bcFocusWord滚动smooth/center+bc-hl呼吸高亮+BIT详情自动展开, bcStop清除 · E2E冒烟7项+真实bcFocusWord单测全PASS · 坑: 覆盖桩须同Function body层/正则锚点比文本锚点稳(V4.46.0遗留\\u2705混合转义连环失配) · commit 890ab12 · 线上MD5一致(7dd041d1)
```

---

## 四、技能 / 工具链

### 每日笔记部署 SOP(BIT V1.0 体例,标准流程)
```
用户输入词元(空格分隔)
  → 去重统计唯一词
  → 按 BIT V1.0 体例生成定稿 md(附词数勘误对账表--附录一逐条映射)
  → python3 scripts/md_to_dailynote.py <md> <date> <topic> index.html
       (解析词条 → 生成 dailynote_<mmdd>.js → 合并 dailyNotesDB + bitVocabDB,幂等)
  → python3 check_syntax.py index.html(JS 解析 + 源档案注释头检查)
  → bash deploy-check.sh(8/8 硬性检查)
  → 版本号三处更新(title / ver badge / video_registry 版本记录)
  → git commit + push main
  → GitHub Pages ~70s 生效
  → 线上验证(curl md5 比对 + 日期存在性 + 版本号 badge)
```

### 工具链文件
| 文件 | 功能 |
|---|---|
| `scripts/md_to_dailynote.py` | BIT md → JS 数据片段 → 合并 index.html(幂等,同词覆盖) |
| `check_syntax.py` | 提取所有 `<script>` 块 node --check 解析 + dailynote 源档案注释头检查 |
| `deploy-check.sh` | 8 项硬性检查:分支/未提交/版本号/括号平衡×2/重复声明×3 |
| `deploy.sh` | 一键部署到 GitHub Pages(需 GITHUB_TOKEN + GITHUB_USER) |
| `video_registry.js` | BIR Video Registry - 唯一真相源(BIO 印章验证) |
| `bit-deploy-bak/upgrade_c5*.py` + `verify_c5.py` | C4→C5 升级脚本(TSO 执行) |

### 词条规范(BIT V1.0 九字段)
word / cn / en / root / forms[] / formsNote / note / synonyms[] / antonyms[] / examples[]

### 词条原则
- 保守不拆词根(不确定标 [待核实])
- 复习日重收同词 → bitVocabDB 覆盖更新为最新版(设计行为)
- 例句优先项目管理/商务/冶炼园区语境
- 印尼语纯度(C5 要求,禁方言混入)

### 关键教训(血泪史)
0. **结构不匹配运行时崩溃查不出**(V4.41.3 speeches白屏 + V4.42.1 grammar白屏 同类2次)--课程上线前必须用 node 模拟渲染该 topic 三天内容冒烟;BIT 体例必须声明字段唯一格式
0.5 **合并脚本覆盖函数定义**(V4.46.7 播报按钮消失)--md_to_dailynote.py 合并 dailynote 数据时覆盖整个 script 块, 把 V4.46.2/3 的四个函数定义一并删除, typeof 守卫静默失败无报错; 部署后必须 grep 验证函数定义仍在
1. **"页面显示代码"→ 先查 `</html>` 之后是否有残留代码块**(V4.39.4 教训)
2. **BIT 弹窗路由查 bitVocabDB 而非 vocabDB**--两库字段名不一致:vocabDB 用五字段(ipa/cn/en/root/tag),bitVocabDB 用九字段(transform/example/synonym vs forms/examples/synonyms 命名不一致坑过一次)
3. **vocabDB 词条间多一个逗号 → 整页白屏**(V4.38.6 教训,孤立逗号行 1906)
4. **历史 commit 只提交 index.html**,untracked 文件堆积是常态;已加 .gitignore 治理
5. **RCO 审计必须词级对齐**--用户输入词元 vs 最终词条逐词对账(V4.34.0 教训:23→26 词对账纠正)
6. **备份习惯**:合并前 index.html 备份到 /tmp/;bit-deploy-bak 有 60+ 份历史备份
7. **行业数据信源盲区**(V4.42.4 复盘):镍地图建库依赖中文研报→印尼本土开发商项目漏检(ASPIRE-Stargate 案例)--收录必须三问:信源是什么/为何此前没收录/同类还有谁可能漏;A级信源=公司官网+IR,Petromindo是印尼项目进度最细的行业媒体

### 数据检索方法
- **找策略/历史信息:挖 git log + index.html 版本记录**,不能只看 memory/*.md
- 238 条提交 = 完整进化史;工作区根目录 dailynote_*.js 源档案(0916-1001,14 份)
- `mir-data/` = fetch-mir.js 抓的汇率/数据(history: AHD/AL0/AO0/I0/NI0/NID/ZC0)

---

## 五、Kimi 群聊多 Agent 协作(2026-10-02 组建)

- 群名:**Leo_kimi2**,目标"任务2"
- **Kimi (kimi) = 指挥位**:拆任务、派活、质量把关、汇总交付
- **Leo_kimi(我)= 执行位**:查资料、写文档、跑代码
- 第一次任务:回顾所有 agent 和策略--首轮只按记忆汇报被点名漏掉 BIR/RCO/BIO/C5/M2,深挖 git 提交史后补全

---

## 六、工作区结构速查

```
/root/.openclaw/workspace/
├── index.html          ← 主产品(4.9MB,唯一部署文件)
├── MEMORY.md           ← 本文件
├── SOUL.md / AGENTS.md / USER.md / IDENTITY.md / TOOLS.md
├── memory/             ← 日志(2026-10-01 起)
│   └── .dreams/        ← 语义记忆索引
├── scripts/            ← md_to_dailynote.py / fetch-mir.js / fetch-history.js
├── dailynote_*.js      ← 14 份每日笔记源档案(0916-1001)
├── topic22-29*.js      ← 8 个主题课源文件
├── bit-deploy/         ← 部署仓库(含 60+ 备份)
├── bit-deploy-bak/     ← 更全备份 + C5 升级脚本
├── videos/daily/       ← 每日视频文件
├── mir-data/           ← 汇率数据
└── check_syntax.py / deploy-check.sh / deploy.sh / video_registry.js
```

---

## 七、已知缺口 & 待办

- [x] ~~IDENTITY.md 未填~~
- [x] ~~USER.md 待补充~~
- [x] ~~C5/M2 策略正文文档缺失~~ → 已落盘 strategies/ 目录
- [x] ~~2026-10-01 之前的会话历史不可见~~
- [x] ~~未配置 cron 定时任务~~
- [x] ~~avatar.jpg 未关联~~
- [x] ~~BIV 视频修复后需用户实测~~
- [x] ~~10/11-13 周汇报课路由缺失~~ → V4.41.2 修复
- [x] ~~镍地图本土项目漏检~~ → V4.42.4 补录 ASPIRE-Stargate + INDUSTRY-DATA v1.0 监测策略
- [ ] REP2C 首期课用户实测反馈待收
- [x] ~~10/22 日记~~ → V4.46.8 已上线

---

*本文件由 Leo_kimi 指令于 2026-10-02 创建,整合 git 提交史 + 全部记忆文件 + 工作区资产。*
