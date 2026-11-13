# perkenalan 字段语义修正（V4.52.7 数据级修复）

> 生成器（V4.52.6）产出 caData.perkenalan 时字段语义与渲染器约定不符，本文档为修正映射表。
> 修正在 index.html 上以脚本化方式落盘，本文件留档备查（BIO 印章用途）。

## 修正项
1. 结构：days:{day1..3} → 平铺 day1/2/3 + days:3（与 meet/interview 对齐）
2. patterns.ex：字符串 → 数组（每条 2 例句，第二条按 slots 造句补写）
3. patterns.level：缺失 → 按内容难度标 basic/adv/pro（配比 1/2/2）
4. phrases：id="P1"编号 → 印尼语词组（原 cn 值）；cn=印尼语 → 中文翻译（本文档翻译）
5. expressions：id="E1"编号 → 印尼语（cn 括号前部分）；cn=印尼语+中文混排 → 纯中文（括号内）；补 scene 字段

## 翻译表（phrases cn）
### day1
- Perkenalkan, nama saya Budi. → 容我介绍一下，我叫布迪。
- Saya berasal dari Jakarta, tapi sekarang tinggal di Morowali. → 我来自雅加达，但现在住在莫罗瓦利。
- Saat ini saya bekerja di perusahaan tambang sebagai manajer proyek. → 目前我在一家矿业公司担任项目经理。
- Latar belakang pendidikan saya adalah teknik metalurgi. → 我的教育背景是冶金工程。
- Salam kenal, saya sangat senang bisa bergabung dengan tim ini. → 很高兴认识您，我非常开心能加入这个团队。
### day2
- Ini rekan saya, Rina. → 这是我的同事丽娜。
- Izinkan saya memperkenalkan Bapak Ahmad kepada Anda. → 请允许我向您介绍阿赫玛德先生。
- Beliau adalah kepala divisi pemasaran di perusahaan kami. → 他是我们公司市场部的负责人。
- Saya ingin memperkenalkan Anda dengan tim teknis kami. → 我想把您介绍给我们的技术团队。
- Mudah-mudahan kerja sama kita bisa berjalan lancar. → 希望我们的合作能够顺利进行。
### day3
- Boleh saya minta kartu nama Anda? → 可以给我一张您的名片吗？
- Berkenalan dengan Anda adalah kehormatan bagi saya. → 认识您是我的荣幸。
- Panggil saya Budi saja. → 叫我布迪就好。
- Mohon maaf, bagaimana sebenarnya pengucapan nama Anda? → 不好意思，您的名字确切怎么发音？
- Izinkan saya memperkenalkan anggota tim kami satu per satu. → 请允许我逐一介绍我们团队的成员。

## expressions 拆分（id=印尼语原句, cn=中文, scene 补写）
### day1
- Salam kenal! / 很高兴认识你！ / 万能寒暄
- Dari mana asalnya? / 您从哪里来？ / 询问籍贯
- Sudah berapa lama bekerja di sini? / 在这里工作多久了？ / 询问资历
- Boleh tahu, latar belakang pendidikannya di bidang apa? / 能问一下您的教育背景是什么专业吗？ / 正式提问
- Keahlian Anda sangat dibutuhkan di proyek ini. / 您的专长正是这个项目所需要的。 / 赞扬对方
### day2
- Silakan berkenalan. / 请互相认识吧。 / 促成认识
- Kalian saling kenal? / 你们互相认识吗？ / 询问相识
- Sudah pernah bertemu sebelumnya? / 以前见过面吗？ / 破冰提问
- Saya yakin Anda berdua akan sangat cocok bekerja sama. / 我相信你们俩合作会很愉快。 / 合作祝愿
- Perkenalkan, ini mitra bisnis kami dari Jakarta. / 介绍一下，这是我们来自雅加达的合作伙伴。 / 正式引荐
### day3
- Terima kasih atas waktunya. / 感谢您的时间。 / 会议致谢
- Mohon maaf, saya kurang mendengar namanya tadi. / 抱歉，我刚才没听清名字。 / 请求重复
- Silakan duduk, kita mulai rapatnya. / 请坐，我们开始开会吧。 / 会议开场
- Kami sangat mengapresiasi kesediaan Anda untuk bertemu hari ini. / 我们非常感激您今天愿意会面。 / 正式致谢
- Dengan hormat, izinkan saya memperkenalkan diri secara singkat. / 谨允许我简短地自我介绍一下。 / 正式开场

## patterns.ex 补写第二条例句 + level 标注
### day1
- 自我介绍 basic: [Perkenalkan, nama saya Sari.] + Halo, nama saya Sari.
- 籍贯说明 adv: [Saya berasal dari Makassar.] + Dia berasal dari Surabaya.
- 职务说明 adv: [Saat ini saya bekerja di PT BIR sebagai supervisor produksi.] + Dia bekerja sebagai insinyur di perusahaan itu.
- 寒暄收尾 pro: [Salam kenal, semoga kita bisa bekerja sama dengan baik.] + Senang bisa bertemu dengan Anda.
- 专长说明 pro: [Keahlian saya adalah manajemen konstruksi.] + Dia mahir di bidang pengelasan.
### day2
- 正式介绍 pro: [Izinkan saya memperkenalkan Ibu Sari.] + Perkenalkan, ini Bapak Ahmad, manajer kami.
- 身份说明 adv: [Beliau adalah direktur operasi di perusahaan kami.] + Ini Ibu Rina, kepala bagian keuangan.
- 询问认识 basic: [Kalian sudah saling kenal?] + Anda berdua sudah saling kenal?
- 非正式介绍 adv: [Ini rekan saya, Dimas.] + Ini teman saya, Budi.
- 促成认识 pro: [Silakan berkenalan, saya tinggal sebentar ya.] + Silakan berkenalan, ini rekan kerja saya.
### day3
- 荣幸表达 pro: [Berkenalan dengan Anda adalah kehormatan bagi kami semua.] + Bisa bertemu dengan Anda adalah kehormatan bagi saya.
- 确认发音 adv: [Mohon maaf, bagaimana pengucapan nama belakangnya?] + Boleh diulang cara bacanya?
- 索取名片 basic: [Boleh saya minta nomor telepon Anda?] + Boleh saya minta email Anda?
- 昵称请求 adv: [Panggil saya Dimas saja.] + Silakan panggil saya Budi.
- 团队介绍 pro: [Izinkan saya memperkenalkan tim kami dari divisi teknik.] + Izinkan saya memperkenalkan tim kami satu per satu.
