#!/usr/bin/env python3
"""
BIR C4→C5 升级 - 第二部分
添加topicData和C5逻辑
"""

def main():
    with open('/root/.openclaw/workspace/bit-deploy/index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # ==================== 1. 在topicData末尾添加新话题 ====================
    new_topics = '''ukbi_exam: {
  title: "UKBI 5级 · 真题模拟日",
  icon: "📜",
  days: 1,
  grammar: {
    title: "UKBI 5级 · 词汇语法精讲",
    rules: [
      "🔹 UKBI 5级 (Madya) 考试结构：阅读·写作·听力·口语",
      "🔹 词汇量要求：3500-4500词，覆盖正式/非正式场合",
      "🔹 语法重点：复合句、被动语态、因果连接词、条件句",
      "🔹 阅读策略：先读题→扫读定位→精读分析→验证答案"
    ],
    examples: [
      "复合句：Meskipun cuaca buruk, pesawat tetap berangkat tepat waktu.",
      "被动语态：Laporan tersebut telah ditinjau oleh dewan direksi.",
      "因果连接：Karena harga naik, masyarakat mulai mencari alternatif.",
      "条件句：Apabila ada kendala, segera hubungi tim maintenance."
    ]
  },
  vocab: [
    ['memahami', '理解', '/məˈmahami/'], ['menyimak', '聆听', '/məˈɲimak/'],
    ['berbicara', '说话', '/bərbiˈtʃara/'], ['menulis', '写作', '/məˈnulis/'],
    ['membaca', '阅读', '/məmˈbatʃa/'], ['paragraf', '段落', '/paˈraɡraf/'],
    ['kesimpulan', '结论', '/kəˈsimpulan/'], ['gagasan utama', '主旨', '/ˈɡaɡasan ˈutama/'],
    ['pendapat', '观点', '/pɛnˈdapət/'], ['argumen', '论点', '/ˈarɡumɛn/'],
    ['alasan', '理由', '/aˈlasan/'], ['bukti', '证据', '/ˈbukti/'],
    ['perbandingan', '比较', '/pərbanˈdiŋan/'], ['perbedaan', '差异', '/pərˈbɛdaan/'],
    ['persamaan', '相似', '/pərˈsamaan/'], ['sebab akibat', '因果', '/ˈsabat ˈakitˈbat/'],
    ['urutan', '顺序', '/ˈurutan/'], ['prosedur', '程序', '/proˈsedur/'],
    ['proses', '过程', '/ˈprosɛs/'], ['saran', '建议', '/ˈsaran/'],
    ['solusi', '解决方案', '/ˈsolusi/'], ['kemahiran', '熟练度', '/kəˈmahiran/'],
    ['berbahasa', '使用语言', '/bərˈbahasa/'], ['ujian', '考试', '/uˈdʒian/'],
    ['materi', '材料', '/maˈtɛri/'], ['struktur', '结构', '/ˈstruktur/'],
    ['kosakata', '词汇', '/kosaˈkata/'], ['tata bahasa', '语法', '/ˈtata ˈbahasa/'],
    ['topik', '话题', '/ˈtopik/'], ['contoh', '例子', '/ˈtonto/']
  ],
  scenes: [
    {title: "📖 阅读理解 A · 印尼数字经济发展", icon: "📚", dialogue: [
      {speaker: "Narrator", text: "Indonesia telah mengalami pertumbuhan ekonomi digital yang pesat dalam lima tahun terakhir. Berdasarkan data Kementerian Komunikasi dan Informatika, nilai transaksi e-commerce mencapai 400 triliun rupiah pada tahun 2023. Namun, tantangan utama yang dihadapi adalah kesenjangan infrastruktur digital antara wilayah Jawa dan luar Jawa. Pemerintah telah meluncurkan program Palapa Ring untuk memperluas jaringan internet ke seluruh pelosok negeri. Selain itu, literasi digital masyarakat masih perlu ditingkatkan agar manfaat ekonomi digital bisa dirasakan secara merata.", trans: "印尼在过去五年经历了快速的数字经济增长。根据通信与信息部的数据，2023年电子商务交易额达到400万亿印尼盾。然而，主要挑战是爪哇岛与岛外地区之间的数字基础设施差距。政府已启动Palapa Ring项目，将互联网网络扩展到全国各地。此外，民众的数字素养仍需提高，以便数字经济的效益能够均等惠及。"}
    ]},
    {title: "📖 阅读理解 B · 印尼制造业升级", icon: "📚", dialogue: [
      {speaker: "Narrator", text: "Presiden Joko Widodo telah menegaskan komitmennya untuk menjadikan Indonesia pusat manufaktur global melalui kebijakan hilirisasi. Kebijakan ini bertujuan mengurangi ketergantungan pada ekspor bahan mentah dan meningkatkan nilai tambah produk dalam negeri. Sektor prioritas meliputi nikel, timah, bauksit, dan tembaga. IWIP (Indonesia Weda Bay Industrial Park) di Morowali menjadi contoh sukses implementasi kebijakan ini. Dengan investasi dari perusahaan-perusahaan global, Indonesia kini memiliki fasilitas produksi baterai lithium terintegrasi dari hulu hingga hilir.", trans: "佐科·维多多总统已强调其通过下游化政策将印尼打造为全球制造中心的承诺。该政策旨在减少对原材料出口的依赖，并提高国内产品的附加值。优先行业包括镍、锡、铝土矿和铜。莫罗瓦利的IWIP（印尼维达湾工业园）是这一政策成功实施的典范。随着全球企业的投资，印尼现在拥有从上游到下游集成的锂电池生产设施。"}
    ]},
    {title: "✍️ 写作部分 · 框架指导", icon: "✍️", dialogue: [
      {speaker: "Prompt", text: "Tulis pendapatmu tentang pentingnya kerja sama dalam tim (120-150 kata). Gunakan minimal 2 kata sambung dan 1 ungkapan sopan.", trans: "就团队合作的重要性发表你的观点（120-150词）。至少使用2个连接词和1个礼貌用语。"},
      {speaker: "Framework", text: "【写作框架】\\n1. Pendahuluan: Pernyataan umum tentang kerja sama tim\\n2. Argumen 1: Keuntungan kerja sama (contoh konkret)\\n3. Argumen 2: Konsekuensi jika tidak bekerja sama\\n4. Kesimpulan: Saran atau harapan\\n\\n【常用连接词】Oleh karena itu, Selain itu, Namun, Meskipun, Sehingga\\n【礼貌用语】Mohon maaf, Terima kasih, Bila berkenan", trans: "【写作框架】\\n1. 引言：关于团队合作的普遍性陈述\\n2. 论点1：合作的好处（具体例子）\\n3. 论点2：如果不合作的后果\\n4. 结论：建议或期望\\n\\n【常用连接词】因此、此外、然而、尽管、以至于\\n【礼貌用语】抱歉、谢谢、如果您愿意"}
    ]}
  ],
  speeches: [
    {day: 1, title: "📖 阅读理解策略讲解", icon: "📖", content: "Dalam ujian UKBI 5级, bagian membaca menguji kemampuan memahami teks akademik dan berita. Strategi yang efektif adalah: pertama, baca pertanyaan terlebih dahulu untuk mengetahui informasi apa yang dicari. Kedua, scan teks untuk menemukan kata kunci. Ketiga, baca kalimat sekitar kata kunci secara cermat. Keempat, perhatikan kata sambung seperti 'namun', 'sehingga', 'karena' yang menunjukkan hubungan logis antar kalimat. Terakhir, pastikan jawaban didukung oleh teks, bukan opini pribadi.", trans: "在UKBI 5级考试中，阅读部分测试理解学术文本和新闻的能力。有效的策略是：第一，先读问题以了解需要寻找什么信息。第二，扫读文本找到关键词。第三，仔细阅读关键词周围的句子。第四，注意'然而'、'所以'、'因为'等连接词，它们显示了句子之间的逻辑关系。最后，确保答案由文本支持，而非个人观点。", time: 90, words: 85}
  ],
  quiz: {
    title: "UKBI 5级 · 词汇语法测试 (15题)",
    questions: [
      {q: "1. 'Meskipun hujan lebat, acara tetap dilanjutkan.' Kata 'meskipun' menunjukkan hubungan?", options: ["A) Sebab-akibat", "B) Pertentangan", "C) Urutan"], a: 1, explain: "'Meskipun' = 尽管，表示转折/对立关系"},
      {q: "2. 'Laporan ________ oleh tim audit kemarin.' 被动语态的正确形式是？", options: ["A) menulis", "B) ditulis", "C) tulis"], a: 1, explain: "被动语态前缀 di-，'ditulis' = 被写"},
      {q: "3. 'Apabila cuaca buruk, penerbangan akan ________.' 条件句的正确动词是？", options: ["A) berangkat", "B) ditunda", "C) sampai"], a: 1, explain: "条件句+被动：'ditunda' = 被推迟"},
      {q: "4. 'Pendapat' 的同义词是？", options: ["A) Argumen", "B) Opini", "C) Fakta"], a: 1, explain: "'Pendapat' = 观点，'opini' = 意见/观点"},
      {q: "5. 'Karena inflasi tinggi, harga barang ________.' 因果句的正确连接是？", options: ["A) turun", "B) naik", "C) tetap"], a: 1, explain: "通胀高→价格上涨，'naik' = 上涨"},
      {q: "6. 'Dewan direksi ________ proposal tersebut secara mendalam.' 正确的动词前缀是？", options: ["A) membaca", "B) meninjau", "C) membuat"], a: 1, explain: "'meninjau' = 审查/审视，适合用于董事会审查提案"},
      {q: "7. 'Kesenjangan' antar daerah perlu diperhatikan.' 'Kesenjangan' 的意思是？", options: ["A) 合作", "B) 差距", "C) 繁荣"], a: 1, explain: "'Kesenjangan' = 差距/鸿沟"},
      {q: "8. 'Program ini bertujuan ________ nilai tambah produk.' 正确的介词搭配是？", options: ["A) mengurangi", "B) meningkatkan", "C) mempertahankan"], a: 1, explain: "'meningkatkan nilai tambah' = 提高附加值"},
      {q: "9. 'PT Vale dan partners berinvestasi di sektor ________.' 冶炼行业的印尼语是？", options: ["A) pertanian", "B) smelter / pengolahan mineral", "C) perikanan"], a: 1, explain: "'smelter' / 'pengolahan mineral' = 冶炼/矿物加工"},
      {q: "10. 'Hilirisasi' 政策的核心目标是？", options: ["A) 增加原材料出口", "B) 提高国内产品附加值", "C) 减少外国投资"], a: 1, explain: "下游化(hilirisasi) = 提高国内产品附加值，减少原材料出口"},
      {q: "11. 'Laporan tersebut telah ________ oleh tim keamanan.' 完成时被动语态的正确形式？", options: ["A) diperiksa", "B) memeriksa", "C) periksa"], a: 0, explain: "'telah diperiksa' = 已被检查（完成时被动）"},
      {q: "12. '________ ada kendala, segera hubungi supervisor.' 正式的条件连接词是？", options: ["A) Kalau", "B) Apabila", "C) Jika"], a: 1, explain: "'Apabila' = 倘若/如果（最正式）"},
      {q: "13. 'Produktivitas meningkat ________ adanya pelatihan kerja.' 表示原因的连接词？", options: ["A) meskipun", "B) karena", "C) sehingga"], a: 1, explain: "'karena' = 因为，表原因"},
      {q: "14. 'Tim kami mengusulkan ________ baru untuk efisiensi energi.' 正确的名词是？", options: ["A) solusi", "B) masalah", "C) kesulitan"], a: 0, explain: "'solusi' = 解决方案，与'efisiensi energi'搭配"},
      {q: "15. 'Dia sangat ________ dalam bidang teknik elektro.' 描述专业能力的形容词？", options: ["A) ahli", "B) pemula", "C) penasihat"], a: 0, explain: "'ahli' = 专家/熟练的，'sangat ahli' = 非常专业"}
    ]
  },
  quiz_answers: "Kunci Jawaban UKBI 5级:\\n1.B | 2.B | 3.B | 4.B | 5.B | 6.B | 7.B | 8.B | 9.B | 10.B\\n11.A | 12.B | 13.B | 14.A | 15.A\\n\\n Strategi: Perhatikan kata sambung dan konteks kalimat untuk menentukan jawaban yang tepat."
},
emotions_life: {
  title: "情感及生活 · Emosi dan Kehidupan",
  icon: "💝",
  days: 3,
  grammar: {
    title: "情感表达语法 · Tata Bahasa Ungkapan Emosi",
    rules: [
      "🔹 情感形容词：senang (高兴), sedih (悲伤), marah (生气), takut (害怕), malu (害羞), bangga (自豪)",
      "🔹 表达感受句型：Saya merasa + [情感形容词] / Saya sangat + [情感形容词] + ketika...",
      "🔹 描述他人情感：Dia kelihatan + [情感形容词] / Wajahnya tampak + [情感形容词]",
      "🔹 情感变化：Awalnya saya..., kemudian..., akhirnya... (起初...然后...最终...)",
      "🔹 安慰/祝贺用语：Turut berduka cita (节哀), Selamat atas... (祝贺...), Semoga lekas sembuh (祝早日康复)"
    ],
    examples: [
      "Saya sangat senang ketika mendengar berita baik itu.",
      "Dia kelihatan sedih setelah mendengar keputusan tersebut.",
      "Awalnya saya marah, tetapi setelah berdiskusi, saya mengerti alasannya.",
      "Selamat atas promosi jabatan barumu! Saya bangga padamu."
    ]
  },
  vocab: [
    ['senang', '高兴', '/səˈnaŋ/'], ['sedih', '悲伤', '/ˈsɛdih/'], ['marah', '生气', '/ˈmarah/'],
    ['takut', '害怕', '/ˈtakut/'], ['malu', '害羞', '/ˈmalu/'], ['bangga', '自豪', '/ˈbaŋɡa/'],
    ['cemas', '焦虑', '/ˈtʃɛmas/'], ['kecewa', '失望', '/kəˈtʃɛwa/'], ['tenang', '平静', '/ˈtɛnaŋ/'],
    ['gembira', '快乐', '/ɡɛmˈbira/'], ['kesal', '恼怒', '/ˈkɛsal/'], ['khawatir', '担心', '/ˈkhawatir/'],
    ['terkejut', '惊讶', '/tərˈkədʒut/'], ['lega', '宽慰', '/ˈlɛɡa/'], ['bersyukur', '感恩', '/bərˈsyukur/'],
    ['merasa', '感觉', '/məˈrasa/'], ['kelihatan', '看起来', '/kəˈlihatan/'], ['wajah', '脸', '/ˈwadʒah/'],
    ['tampak', '显得', '/ˈtampak/'], ['perasaan', '感受', '/pəˈrasaaŋ/'], ['hati', '心', '/ˈhati/'],
    ['jiwa', '灵魂', '/ˈdʒiwa/'], ['pikiran', '想法', '/pikiˈran/'], ['suasana', '氛围', '/suaˈsana/'],
    ['semangat', '精神', '/səˈmaŋat/'], ['motivasi', '动力', '/motiˈvasi/'], ['harapan', '希望', '/haˈrapan/'],
    ['mimpi', '梦想', '/ˈmimpi/'], ['cita-cita', '理想', '/ˈtʃita ˈtʃita/'], ['bahagia', '幸福', '/baˈhaɡia/'],
    ['sakit hati', '伤心', '/ˈsakit ˈhati/'], ['rindu', '思念', '/ˈrindu/'], ['sayang', '爱/疼', '/ˈsajaŋ/'],
    ['cinta', '爱情', '/ˈtʃinta/'], ['peduli', '关心', '/ˈpɛduli/'], ['memahami', '理解', '/məˈmahami/'],
    ['mendengarkan', '倾听', '/mɛnˈdɛŋarakan/'], ['mendukung', '支持', '/mɛnˈdukuŋ/'], ['menghibur', '安慰', '/mɛŋˈhibur/'],
    ['berbagi', '分享', '/bərˈbaɡi/'], ['bersama', '一起', '/bərˈsama/'], ['keluarga', '家庭', '/kəˈluarga/'],
    ['teman', '朋友', '/ˈtɛman/'], ['rekan kerja', '同事', '/ˈrɛkan ˈkɛrdʒa/'], ['atasan', '上司', '/aˈtasan/'],
    ['bawahan', '下属', '/baˈwahan/'], ['pasangan', '伴侣', '/ˈpasanɡan/'], ['anak', '孩子', '/ˈanak/'],
    ['orang tua', '父母', '/ˈoraŋ ˈtua/'], ['saudara', '兄弟姐妹', '/sauˈdara/']
  ],
  scenes: [
    {title: "🏠 家庭情感交流", icon: "👨‍👩‍👧", dialogue: [
      {speaker: "Ibu", text: "Kamu kelihatan sedih hari ini, Nak. Ada apa?", trans: "你今天看起来很难过，孩子。怎么了？"},
      {speaker: "Anak", text: "Iya, Bu. Saya kecewa karena tidak lulus ujian kemarin.", trans: "是的，妈。我很失望因为昨天考试没通过。"},
      {speaker: "Ibu", text: "Jangan terlalu sedih. Yang penting kamu sudah berusaha. Kita bisa belajar bersama untuk ujian berikutnya.", trans: "别太难过。重要的是你已经努力了。我们可以一起准备下次考试。"},
      {speaker: "Anak", text: "Terima kasih, Bu. Saya merasa lebih lega setelah bicara dengan Ibu.", trans: "谢谢妈。跟您说完我感觉宽慰多了。"}
    ]},
    {title: "👥 朋友间分享喜悦", icon: "🎉", dialogue: [
      {speaker: "A", text: "Halo! Aku punya kabar baik! Aku akhirnya diterima kerja di perusahaan impianku!", trans: "你好！我有个好消息！我终于被梦想的公司录用了！"},
      {speaker: "B", text: "Wah, selamat! Aku sangat bangga padamu. Kamu sudah bekerja keras untuk ini.", trans: "哇，恭喜！我真为你骄傲。你为此付出了很多努力。"},
      {speaker: "A", text: "Terima kasih atas dukungannya selama ini. Aku sangat bersyukur punya teman sepertimu.", trans: "谢谢你一直以来的支持。我很感恩有你这样的朋友。"},
      {speaker: "B", text: "Sama-sama! Kita harus merayakan ini! Makan malam di restoran favoritku, aku yang traktir!", trans: "不客气！我们得庆祝一下！去我最喜欢的餐厅吃晚饭，我请客！"}
    ]},
    {title: "💼 职场情绪管理", icon: "🏢", dialogue: [
      {speaker: "Karyawan", text: "Pak, maaf mengganggu. Saya merasa cemas tentang deadline proyek yang sangat ketat.", trans: "先生，抱歉打扰。我对项目紧迫的截止日期感到焦虑。"},
      {speaker: "Manager", text: "Saya mengerti perasaanmu. Deadline memang menantang, tapi tim kami bisa mengatasinya bersama. Ada kendala spesifik?", trans: "我理解你的感受。截止日期确实有挑战，但我们团队可以一起解决。有具体的困难吗？"},
      {speaker: "Karyawan", text: "Saya kesulitan dengan data dari departemen lain yang belum lengkap.", trans: "我在等其他部门的数据，目前还不完整。"},
      {speaker: "Manager", text: "Baik, saya akan koordinasi dengan mereka. Fokus saja pada bagian yang bisa kamu kerjakan sekarang. Jangan terlalu khawatir.", trans: "好的，我会跟他们协调。你专注于现在能做的部分。别太担心。"}
    ]},
    {title: "💑 伴侣间表达关心", icon: "❤️", dialogue: [
      {speaker: "Pasangan A", text: "Sayang, kamu kelihatan lelah hari ini. Kerjaanmu banyak ya?", trans: "亲爱的，你今天看起来很累。工作很多吗？"},
      {speaker: "Pasangan B", text: "Iya, ada beberapa masalah di kantor yang harus diselesaikan. Saya merasa sedikit stres.", trans: "是的，办公室有些问题需要解决。我感觉有点压力。"},
      {speaker: "Pasangan A", text: "Aku di sini untukmu. Mau aku siapkan teh hangat? Atau kita bicara saja sambil bersantai?", trans: "我在这儿陪着你。要我准备热茶吗？还是我们边放松边聊聊？"},
      {speaker: "Pasangan B", text: "Terima kasih sayang. Hanya dengan mendengarkanmu, hatiku sudah merasa lebih tenang.", trans: "谢谢亲爱的。光是听你说，我的心就平静多了。"}
    ]},
    {title: "🎓 祝贺与鼓励", icon: "🌟", dialogue: [
      {speaker: "Senior", text: "Selamat atas kelulusanmu! Saya tahu perjalananmu tidak mudah, tapi kamu berhasil!", trans: "恭喜毕业！我知道你的路不容易，但你成功了！"},
      {speaker: "Junior", text: "Terima kasih, Pak. Saya sangat bangga bisa menjadi bagian dari perusahaan ini.", trans: "谢谢您，先生。我很骄傲能成为这家公司的一员。"},
      {speaker: "Senior", text: "Ingat, ini baru awal. Tetaplah semangat dan jangan pernah berhenti belajar. Saya yakin kamu akan sukses.", trans: "记住，这只是开始。保持热情，永远不要停止学习。我相信你会成功的。"},
      {speaker: "Junior", text: "Saya akan berusaha sebaik mungkin. Terima kasih atas motivasinya, Pak!", trans: "我会尽我所能。谢谢您的鼓励，先生！"}
    ]},
    {title: "🤝 道歉与和解", icon: "🕊️", dialogue: [
      {speaker: "A", text: "Maafkan saya atas kesalahan kemarin. Saya tidak bermaksud menyakiti perasaanmu.", trans: "请原谅我昨天的错误。我不是故意要伤害你的感情。"},
      {speaker: "B", text: "Saya memang kecewa, tapi saya menghargai kejujuranmu. Apa yang sebenarnya terjadi?", trans: "我确实失望，但我欣赏你的诚实。到底发生了什么？"},
      {speaker: "A", text: "Saya terlalu emosional saat itu. Seharusnya saya lebih tenang dan mendengarkan pendapatmu dulu.", trans: "我当时太情绪化了。我应该更冷静，先听取你的意见。"},
      {speaker: "B", text: "Baiklah, saya maafkanmu. Mari kita belajar dari ini dan menjadi lebih baik ke depannya.", trans: "好吧，我原谅你。让我们从中学习，以后变得更好。"}
    ]}
  ],
  speeches: [
    {day: 1, title: "💝 我的情感世界", icon: "💭", content: "Setiap manusia memiliki berbagai perasaan. Ada kalanya saya merasa sangat senang, seperti ketika berhasil menyelesaikan proyek besar. Ada kalanya saya merasa sedih, terutama ketika berjauhan dengan keluarga. Namun, yang terpenting adalah bagaimana kita mengelola emosi tersebut. Saya belajar untuk selalu bercerita dengan teman dekat ketika merasa cemas. Saya juga belajar untuk bersyukur dalam setiap situasi. Perasaan bangga muncul ketika melihat orang-orang yang saya sayangi berhasil. Hidup ini penuh dengan warna emosi, dan itu yang membuat kita manusia.", trans: "每个人都有各种情感。有时我感到非常高兴，比如成功完成大项目时。有时我感到难过，尤其是与家人分离时。然而，最重要的是我们如何管理这些情绪。我学会了在感到焦虑时总是与密友倾诉。我也学会了在任何情况下都心怀感恩。当看到所爱的人成功时，自豪感油然而生。生活充满了情感色彩，这正是我们作为人类的意义。", time: 75, words: 95},
    {day: 2, title: "❤️ 爱与关怀的力量", icon: "🌈", content: "Dalam hidup ini, tidak ada yang lebih berharga daripada kasih sayang dan perhatian dari orang-orang terdekat. Saya masih ingat ketika pertama kali datang ke Morowali, saya merasa sangat rindu keluarga. Namun, dukungan dari rekan kerja membuat saya merasa seperti di rumah sendiri. Sekecil apa pun perhatian, seperti secangkir kopi hangat atau pertanyaan sederhana 'Apa kabar?', bisa membuat hari seseorang menjadi lebih baik. Mari kita menjadi orang yang peduli, yang mau mendengarkan, dan yang selalu siap membantu. Karena pada akhirnya, hubungan antar manusia adalah kekayaan sejati.", trans: "在生活中，没有什么比身边人的爱与关怀更珍贵。我仍然记得第一次来到莫罗瓦利时，我非常想念家人。然而，同事们的支持让我感觉像在自己家一样。再小的关心，比如一杯热咖啡或一句简单的'你好吗?'，都能让一个人的一天变得更美好。让我们成为关心他人、愿意倾听、随时伸出援手的人。因为归根结底，人与人之间的关系才是真正的财富。", time: 80, words: 105},
    {day: 3, title: "🌟 面对挑战的勇气", icon: "🔥", content: "Hidup tidak selalu berjalan sesuai rencana. Ada tantangan, ada kegagalan, dan ada momen-momen yang membuat kita ingin menyerah. Namun, saya percaya bahwa setiap kesulitan membawa pelajaran berharga. Ketika proyik kami mengalami kendala teknis, tim saya sempat merasa frustrasi. Tetapi setelah berdiskusi dan bekerja sama, kami menemukan solusi yang bahkan lebih baik dari rencana semula. Yang terpenting adalah jangan pernah kehilangan harapan. Bangkit dari kegagalan, belajar dari kesalahan, dan terus melangkah maju. Itulah arti sejati dari keberanian.", trans: "生活并不总是按计划进行。有挑战，有失败，也有让我们想要放弃的时刻。然而，我相信每一次困难都带来宝贵的教训。当我们的项目遇到技术困难时，我的团队一度感到沮丧。但经过讨论和合作，我们找到了比原计划更好的解决方案。最重要的是永远不要失去希望。从失败中站起来，从错误中学习，继续向前迈进。这才是勇气的真正含义。", time: 85, words: 110}
  ],
  quiz: {
    title: "情感及生活 · 综合测试 (10题)",
    questions: [
      {q: "1. 'Saya merasa ________ ketika mendengar berita itu.' 表达'高兴'的正确词？", options: ["A) sedih", "B) senang", "C) marah"], a: 1, explain: "'senang' = 高兴"},
      {q: "2. 'Dia kelihatan ________ setelah kehilangan dompetnya.' 表达'焦虑'？", options: ["A) tenang", "B) cemas", "C) bangga"], a: 1, explain: "'cemas' = 焦虑/担心"},
      {q: "3. 'Selamat atas promosimu! Saya ________ padamu.' 表达'自豪'？", options: ["A) bangga", "B) malu", "C) takut"], a: 0, explain: "'bangga' = 骄傲/自豪"},
      {q: "4. 'Turut berduka cita' 用于什么场合？", options: ["A) 婚礼", "B) 葬礼/哀悼", "C) 升职庆祝"], a: 1, explain: "'Turut berduka cita' = 节哀顺变（哀悼用语）"},
      {q: "5. 'Saya sangat ________ punya teman sepertimu.' 表达'感恩'？", options: ["A) khawatir", "B) bersyukur", "C) kesal"], a: 1, explain: "'bersyukur' = 感恩/感谢"},
      {q: "6. 'Maafkan saya, saya tidak bermaksud menyakiti ________mu.' 正确的词是？", options: ["A) pikiran", "B) perasaan", "C) wajah"], a: 1, explain: "'perasaan' = 感情/感受，'menyakiti perasaan' = 伤害感情"},
      {q: "7. 'Hati' 在印尼语中的引申义是？", options: ["A) 器官", "B) 感情/内心", "C) 智力"], a: 1, explain: "'hati' = 心，引申为感情/内心，如'sakit hati' = 伤心"},
      {q: "8. 'Semoga lekas sembuh' 的意思是？", options: ["A) 祝你生日快乐", "B) 祝早日康复", "C) 恭喜发财"], a: 1, explain: "'Semoga lekas sembuh' = 祝早日康复"},
      {q: "9. 'Saya merasa lebih ________ setelah bicara denganmu.' 表达'宽慰'？", options: ["A) sedih", "B) lega", "C) marah"], a: 1, explain: "'lega' = 宽慰/释然"},
      {q: "10. 'Mari kita ________ pengalaman ini dan menjadi lebih baik.' 正确的动词？", options: ["A) lupakan", "B) pelajari", "C) hindari"], a: 1, explain: "'pelajari' = 学习/吸取教训，'belajar dari pengalaman' = 从经验中学习"}
    ]
  },
  quiz_answers: "Kunci Jawaban Emosi dan Kehidupan:\\n1.B | 2.B | 3.A | 4.B | 5.B\\n6.B | 7.B | 8.B | 9.B | 10.B\\n\\n Tips: Perhatikan konteks kalimat dan hubungan antar karakter untuk memahami emosi yang tepat."
}'''

    # 在 ukbi_map 的最后一个 } 和 }; 之间插入
    # 找到 "ukbi_map: { ... },\n\n};" 的模式
    marker = """  speeches: [
    {day: 1, title: "🧠 UKBI思维导图复习指南", content: "今天使用C4_MAP模式复习UK中级全部内容。请切换到左侧导航的 UKBI思维导图 查看完整的四级知识结构。复习重点：1) 语法规则与例句 2) 核心词汇表 3) 场景对话 4) 考试策略。建议结合思维导图和前几日的课程材料进行系统复习。", trans: "今天使用C4_MAP模式复习UKBI中级全部内容。请切换到左侧导航查看完整知识结构。"}
  ]
},

};"""
    
    if marker in content:
        content = content.replace(marker, marker.rstrip("};\n") + ",\n" + new_topics + "\n};")
        print("✅ topicData 已添加 ukbi_exam 和 emotions_life")
    else:
        print("ERROR: 无法找到 topicData 的插入标记")
        return
    
    # ==================== 2. 在 renderTopicDetail 中注入 C5 逻辑 ====================
    # 在 let html = ``; 之后插入 C5 逻辑
    
    c5_logic = '''
  // ========== C5: 前置复习模块 ==========
  // 规则A: 日内复习 - 如果前一天有数据，插入前一天的C4_MAP
  // 规则B: 话题间复习 - 如果是day=1且存在前一话题，插入前一话题的完整C4_MAP
  const prevDate = getPrevDate(ds);
  const prevTopicInfo = prevDate ? topicCalendar[prevDate] : null;
  
  function getPrevDate(dateStr) {
    const d = new Date(dateStr + 'T00:00:00');
    d.setDate(d.getDate() - 1);
    return d.toISOString().split('T')[0];
  }
  
  function buildC4Map(topicKey, topicDay, allDays = false) {
    const t = topicData[topicKey];
    if (!t) return '';
    let mapHtml = `<div class="mind-map-container" style="margin-bottom:16px;">`;
    mapHtml += `<div class="mind-l1" onclick="this.classList.toggle('open');this.nextElementSibling.classList.toggle('open');" style="cursor:pointer;">${t.icon} ${t.title}${allDays ? ' · 全内容' : ' · Day ' + topicDay}</div>`;
    mapHtml += `<div class="mind-l2-wrap" style="display:none;">`;
    
    // 语法要点
    if (t.grammar) {
      mapHtml += `<div class="mind-l2"><div class="mind-l2-header" onclick="this.classList.toggle('open');this.nextElementSibling.classList.toggle('open');">📖 语法: ${t.grammar.title}</div><div class="mind-l2-body">`;
      t.grammar.rules.forEach(r => {
        mapHtml += `<div style="font-size:12px;color:var(--text-dim);margin:3px 0;">• ${r}</div>`;
      });
      mapHtml += `</div></div>`;
    }
    
    // 核心词汇
    if (t.vocab && t.vocab.length > 0) {
      mapHtml += `<div class="mind-l2"><div class="mind-l2-header" onclick="this.classList.toggle('open');this.nextElementSibling.classList.toggle('open');">🎯 核心词汇 (${t.vocab.length}词)</div><div class="mind-l2-body">`;
      const vocabSlice = allDays ? t.vocab : t.vocab.slice(0, 15);
      vocabSlice.forEach(v => {
        mapHtml += `<div class="mind-l3"><span class="mind-l3-label">${v[0]}</span> ${v[1]}</div>`;
      });
      mapHtml += `</div></div>`;
    }
    
    // 场景对话
    if (t.scenes && t.scenes.length > 0) {
      mapHtml += `<div class="mind-l2"><div class="mind-l2-header" onclick="this.classList.toggle('open');this.nextElementSibling.classList.toggle('open');">💬 场景对话 (${t.scenes.length}个)</div><div class="mind-l2-body">`;
      t.scenes.forEach((sc, si) => {
        mapHtml += `<div style="font-size:12px;color:var(--text-dim);margin:3px 0;">• ${sc.icon} ${sc.title}</div>`;
      });
      mapHtml += `</div></div>`;
    }
    
    // 演讲
    if (t.speeches && t.speeches.length > 0) {
      mapHtml += `<div class="mind-l2"><div class="mind-l2-header" onclick="this.classList.toggle('open');this.nextElementSibling.classList.toggle('open');">🎤 演讲 (${t.speeches.length}篇)</div><div class="mind-l2-body">`;
      t.speeches.forEach((sp, spi) => {
        mapHtml += `<div style="font-size:12px;color:var(--text-dim);margin:3px 0;">• ${sp.title}</div>`;
      });
      mapHtml += `</div></div>`;
    }
    
    mapHtml += `</div></div>`;
    return mapHtml;
  }
  
  // 生成复习HTML
  let reviewHtml = '';
  
  // 规则B: 话题间复习 (新话题第一天)
  if (day === 1 && prevTopicInfo && prevTopicInfo.topic !== topicInfo.topic) {
    const prevTopic = topicData[prevTopicInfo.topic];
    if (prevTopic) {
      reviewHtml += `<div class="card" style="border:2px solid var(--accent);margin-bottom:16px;">`;
      reviewHtml += `<div class="card-header" style="cursor:pointer;" onclick="this.nextElementSibling.style.display=this.nextElementSibling.style.display==='none'?'block':'none';this.querySelector('.toggle-icon').textContent=this.nextElementSibling.style.display==='none'?'▶':'▼';">`;
      reviewHtml += `<h2>📚 前一话题复习 · ${prevTopic.icon} ${prevTopic.title}</h2>`;
      reviewHtml += `<span class="badge toggle-icon" style="font-size:16px;">▶</span>`;
      reviewHtml += `</div>`;
      reviewHtml += `<div style="display:none;padding:0 20px 20px;">`;
      reviewHtml += buildC4Map(prevTopicInfo.topic, prevTopicInfo.day, true);
      reviewHtml += `</div></div>`;
    }
  }
  
  // 规则A: 日内复习 (每天的前置复习)
  if (prevTopicInfo && prevTopicInfo.topic === topicInfo.topic && prevTopicInfo.day === day - 1) {
    const prevTopic = topicData[prevTopicInfo.topic];
    if (prevTopic) {
      const prevLabel = prevTopicInfo.label || `Day ${prevTopicInfo.day}`;
      reviewHtml += `<div class="card" style="border:2px solid var(--primary-dim);margin-bottom:16px;">`;
      reviewHtml += `<div class="card-header" style="cursor:pointer;" onclick="this.nextElementSibling.style.display=this.nextElementSibling.style.display==='none'?'block':'none';this.querySelector('.toggle-icon').textContent=this.nextElementSibling.style.display==='none'?'▶':'▼';">`;
      reviewHtml += `<h2>📚 昨日复习 · ${prevDate} · ${prevLabel}</h2>`;
      reviewHtml += `<span class="badge toggle-icon" style="font-size:16px;">▶</span>`;
      reviewHtml += `</div>`;
      reviewHtml += `<div style="display:none;padding:0 20px 20px;">`;
      reviewHtml += buildC4Map(prevTopicInfo.topic, prevTopicInfo.day, false);
      reviewHtml += `</div></div>`;
    }
  }
  
  // ========== C5 结束 ==========
'''
    
    # 在 renderTopicDetail 中找到 "let html = ``;" 并替换
    old_pattern = "  const topic = topicData[topicInfo.topic];\n  const day = topicInfo.day;\n  let html = ``;"
    new_pattern = "  const topic = topicData[topicInfo.topic];\n  const day = topicInfo.day;\n  let html = ``;\n" + c5_logic
    
    if old_pattern in content:
        content = content.replace(old_pattern, new_pattern)
        print("✅ C5 前置复习逻辑已注入 renderTopicDetail")
    else:
        print("ERROR: 无法找到 renderTopicDetail 的插入位置")
        return
    
    # 在第一个 html += `<div class="card"> 之前插入 reviewHtml
    old_card = '  html += `<div class="card"><div class="card-header"><h2>${topic.icon} ${topic.title}</h2><span class="badge">Day ${day}/3'
    new_card = '  html += reviewHtml;\n  html += `<div class="card"><div class="card-header"><h2>${topic.icon} ${topic.title}</h2><span class="badge">Day ${day}/3'
    
    if old_card in content:
        content = content.replace(old_card, new_card)
        print("✅ reviewHtml 已插入到课程卡片前")
    else:
        print("ERROR: 无法找到 card 的插入位置")
        return
    
    # ==================== 3. 写入文件 ====================
    with open('/root/.openclaw/workspace/bit-deploy/index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("\n🎉 C4→C5 升级完成！")
    print("  - ukbi_exam 话题已添加")
    print("  - emotions_life 话题已添加 (3天课程)")
    print("  - C5 前置复习逻辑已注入")

if __name__ == '__main__':
    main()
