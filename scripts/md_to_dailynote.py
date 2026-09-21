#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
md_to_dailynote.py — BIT 每日单词笔记 → BIR dailyNotesDB 转换器（可复用）

用法:
  python3 md_to_dailynote.py <note_final.md> <date> <topicKey> <index.html>

流程:
  1. 解析 BIT 定稿 md（49 词条体例）
  2. 生成 JS 数据片段 dailynote_<mmdd>.js:
       const dailyNotesDB = { "<date>": { date, topicKey, source, entries:[...] } };
  3. 合并进 index.html:
       a. 在 topicCalendar 结束后插入 dailyNotesDB
       b. 在 function startTopicQuiz(topicKey) 前插入 buildDailyNoteCard/toggleDailyNote
       c. startTopicQuiz 主渲染行前置 ${buildDailyNoteCard(topicKey)}
  幂等：已存在 dailyNotesDB 时先移除旧块再插入（重跑安全）。
"""
import json, re, sys, io

def parse_entries(md_text):
    """按 `### N. word` 切分词条"""
    # 词条起点
    pat = re.compile(r'^###\s+(\d+)\.\s+(.+?)\s*$', re.M)
    matches = list(pat.finditer(md_text))
    entries = []
    for idx, m in enumerate(matches):
        num = int(m.group(1))
        word = m.group(2).strip()
        start = m.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(md_text)
        body = md_text[start:end]
        entries.append((num, word, body))
    return entries

def grab(rx, text, flags=0, group=1, default=""):
    m = re.search(rx, text, flags)
    return m.group(group).strip() if m else default

def parse_entry(num, word, body):
    e = {"word": word, "cn": "", "en": "", "root": "",
         "forms": [], "formsNote": "", "note": "",
         "synonyms": [], "antonyms": [], "examples": []}

    e["cn"] = grab(r'^\s*-\s*\*\*中文\*\*:[ \t]*(.+?)\s*$', body, re.M)
    e["en"] = grab(r'^\s*-\s*\*\*English\*\*:[ \t]*(.+?)\s*$', body, re.M)
    e["root"] = grab(r'^\s*-\s*\*\*词根\*\*:[ \t]*(.+?)\s*$', body, re.M)

    # 变形：表格式 or 文本式
    m_forms = re.search(r'^\s*-\s*\*\*变形\*\*[^:]*:[ \t]*(.*)$', body, re.M)
    if m_forms:
        rest = m_forms.group(1).strip()
        if rest:
            e["formsNote"] = rest
        # 收集后续表格行（跳过 |---| 分隔行），直到空行或非表行。
        # 行内注释与表格可并存（如「—（无派生形态；列常见搭配）」+ 搭配表），表格照常解析。
        tbl = []
        for line in body[m_forms.end():].splitlines()[1:]:
            ls = line.strip()
            if not ls:
                if tbl: break
                continue
            if ls.startswith('|') and ls.endswith('|'):
                if re.match(r'^\|[\s\-\u2013\u2014|]+\|$', ls):  # 分隔行
                    continue
                cells = [c.strip() for c in ls.strip('|').split('|')]
                if len(cells) >= 3:
                    if cells[:3] == ['形式', '词性', '含义']:  # 表头行
                        continue
                    tbl.append({"form": cells[0], "pos": cells[1], "mean": cells[2]})
            else:
                break
        e["forms"] = tbl

    # 附加注释：变形说明 / 词汇注释 / 易混提示
    notes = re.findall(r'^\s*-\s*\*\*(?:变形说明|词汇注释|易混提示)\*\*:[ \t]*(.+?)\s*$', body, re.M)
    if notes:
        e["note"] = " ".join(n.strip().strip('*').strip() for n in notes)

    # 同义 / 反义：顿号分隔（保留「；」在内的说明文本）
    syn = grab(r'^\s*-\s*\*\*同义词\*\*:[ \t]*(.+?)\s*$', body, re.M)
    if syn:
        e["synonyms"] = [s.strip() for s in syn.split('、') if s.strip()]
    ant = grab(r'^\s*-\s*\*\*反义词\*\*:[ \t]*(.+?)\s*$', body, re.M)
    if ant:
        e["antonyms"] = [s.strip() for s in ant.split('、') if s.strip()]

    # 场景应用 bullet: - 场景: *id句* 中文
    # 注意：元信息行形如 `- **xxx**: ...`（标签带 ** 包裹），场景 bullet 为纯文本标签。
    # 不得按场景标签黑名单过滤——「变形」既是元信息标签也是合法场景标签（操练变形例句），
    # 2026-09-17 RCO 审计事故：startswith('变形') 误杀 62 条例句。此处只按行首 ** 判定元信息。
    for line in body.splitlines():
        if re.match(r'^\s*-\s*\*\*.+?\*\*:', line):
            continue  # 元信息行（中文/English/词根/变形/同义词/反义词/变形说明/词汇注释/易混提示）
        m = re.match(r'^\s*-\s*(.+?):[ \t]*\*(.+)\*[ \t]*(.+?)\s*$', line)
        if m:
            scene = m.group(1).strip().replace('**', '')
            id_s = m.group(2).strip()
            cn_s = m.group(3).strip()
            e["examples"].append({"scene": scene, "id": id_s, "cn": cn_s})
    return e

def build_js(date, topic_key, source, entries):
    payload = {
        date: {
            "date": date,
            "topicKey": topic_key,
            "source": source,
            "entries": entries,
        }
    }
    js = "const dailyNotesDB = " + json.dumps(payload, ensure_ascii=False, indent=2) + ";\n"
    return js

RENDER_FUNCS = r'''
// ===== 每日笔记模块（BIT V1.0 生产 → BIO 审查定稿） V4.26.0 新增 =====
function toggleDailyNote(id) {
  var el = document.getElementById(id);
  if (!el) return;
  el.style.display = el.style.display === "none" ? "block" : "none";
}

function buildDailyNoteCard(topicKey) {
  if (typeof dailyNotesDB === "undefined" || !dailyNotesDB) return "";
  var dates = Object.keys(topicCalendar).filter(function (d) {
    return topicCalendar[d] && topicCalendar[d].topic === topicKey && dailyNotesDB[d];
  }).sort();
  if (!dates.length) return "";
  var esc = function (s) {
    return String(s == null ? "" : s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  };
  var rich = function (s) {
    return esc(s).replace(/\*\*(.+?)\*\*/g, '<strong style="color:var(--primary)">$1</strong>');
  };
  return dates.map(function (ds) {
    var note = dailyNotesDB[ds];
    var entriesHtml = note.entries.map(function (e, i) {
      var detailId = "dn-" + ds + "-" + i;
      var formsHtml = "";
      if (e.forms && e.forms.length) {
        formsHtml = '<table style="width:100%;border-collapse:collapse;font-size:12px;margin:8px 0;">'
          + '<tr style="background:var(--bg-elev);">'
          + '<th style="text-align:left;padding:5px 8px;border:1px solid var(--border);color:var(--text-dim);">形式</th>'
          + '<th style="text-align:left;padding:5px 8px;border:1px solid var(--border);color:var(--text-dim);">词性</th>'
          + '<th style="text-align:left;padding:5px 8px;border:1px solid var(--border);color:var(--text-dim);">含义</th></tr>'
          + e.forms.map(function (f) {
            return '<tr><td style="padding:5px 8px;border:1px solid var(--border);color:var(--primary);font-weight:600;">' + esc(f.form) + '</td>'
              + '<td style="padding:5px 8px;border:1px solid var(--border);color:var(--text);">' + esc(f.pos) + '</td>'
              + '<td style="padding:5px 8px;border:1px solid var(--border);color:var(--text);">' + esc(f.mean) + '</td></tr>';
          }).join("") + '</table>';
      }
      var formsNoteHtml = e.formsNote ? '<div style="font-size:12px;color:var(--text-dim);margin:6px 0;line-height:1.6;">📎 变形：' + rich(e.formsNote) + '</div>' : "";
      var noteHtml = e.note ? '<div style="font-size:12px;color:#d4a017;background:rgba(212,160,23,.08);border-left:2px solid #d4a017;padding:6px 8px;border-radius:6px;margin:6px 0;line-height:1.6;">💡 ' + rich(e.note) + '</div>' : "";
      var synHtml = (e.synonyms && e.synonyms.length) ? '<div style="margin:8px 0;"><span style="font-size:12px;color:var(--text-dim);">🔗 同义词：</span>' + e.synonyms.map(function (s) { return '<span style="display:inline-block;font-size:12px;background:var(--bg-elev);border:1px solid var(--border);border-radius:10px;padding:2px 8px;margin:2px 4px 2px 0;color:var(--text);">' + rich(s) + '</span>'; }).join("") + '</div>' : "";
      var antHtml = (e.antonyms && e.antonyms.length) ? '<div style="margin:8px 0;font-size:12px;color:var(--text);"><span style="color:var(--text-dim);">⚖️ 反义词：</span>' + e.antonyms.map(function (s) { return rich(s); }).join('<span style="color:var(--text-dim);">　</span>') + '</div>' : "";
      var exHtml = (e.examples && e.examples.length) ? '<div style="margin-top:8px;"><div style="font-size:12px;color:var(--text-dim);margin-bottom:4px;">🗣️ 场景应用：</div>'
        + e.examples.map(function (x) {
          return '<div style="font-size:12px;line-height:1.7;margin:6px 0;padding:6px 8px;background:var(--bg-elev);border-radius:6px;">'
            + '<span style="display:inline-block;font-size:11px;color:var(--primary);background:rgba(0,212,170,.1);border-radius:4px;padding:1px 6px;margin-right:6px;">' + esc(x.scene) + '</span>'
            + '<div style="color:var(--text);margin-top:3px;">' + rich(x.id) + '</div>'
            + '<div style="color:var(--text-dim);">' + esc(x.cn) + '</div></div>';
        }).join("") + '</div>' : "";
      return '<div style="border:1px solid var(--border);border-radius:8px;margin-bottom:6px;overflow:hidden;">'
        + '<div onclick="toggleDailyNote(\'' + detailId + '\')" style="padding:10px 12px;cursor:pointer;display:flex;align-items:center;gap:8px;transition:background .15s;" onmouseenter="this.style.background=\'var(--bg-elev)\'" onmouseleave="this.style.background=\'transparent\'">'
        + '<span style="font-size:11px;color:var(--text-dim);min-width:22px;">' + String(i + 1).padStart(2, "0") + '</span>'
        + '<span style="font-size:14px;font-weight:700;color:var(--primary);">' + esc(e.word) + '</span>'
        + '<span style="font-size:12px;color:var(--text);">' + esc(e.cn) + '</span>'
        + '<span style="font-size:11px;color:var(--text-dim);margin-left:auto;">▾</span>'
        + '</div>'
        + '<div id="' + detailId + '" style="display:none;padding:4px 12px 12px;border-top:1px dashed var(--border);">'
        + '<div style="font-size:12px;color:var(--text-dim);margin:6px 0;">🇬🇧 ' + esc(e.en) + '</div>'
        + '<div style="font-size:12px;color:var(--text);background:rgba(0,212,170,.06);border-left:2px solid var(--primary);padding:6px 8px;border-radius:6px;margin:6px 0;line-height:1.6;">🌱 词根：' + rich(e.root) + '</div>'
        + formsHtml + formsNoteHtml + noteHtml + synHtml + antHtml + exHtml
        + '</div></div>';
    }).join("");
    return '<div class="card" style="margin-bottom:16px;border-left:3px solid var(--primary);">'
      + '<div class="card-header" style="flex-wrap:wrap;gap:8px;"><h2>📓 当日笔记 / Catatan Harian</h2>'
      + '<span class="badge">' + ds + '</span>'
      + '<span class="badge">' + note.entries.length + '词条</span></div>'
      + '<div style="padding:16px;">'
      + '<div style="font-size:12px;color:var(--text-dim);margin-bottom:12px;padding:10px 12px;background:rgba(0,212,170,.06);border-radius:8px;border-left:3px solid var(--primary);">'
      + '📚 本日学习笔记（' + esc(note.source) + '）· 点击词条展开翻译、词根、变形、同反义词与场景例句</div>'
      + entriesHtml + '</div></div>';
  }).join("");
}
'''

def main():
    if len(sys.argv) >= 5:
        md_path, date, topic_key, html_path = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
    else:
        md_path = "/root/.openclaw/workspace/agents/BIT/notes/2026-09-16_note_final.md"
        date, topic_key = "2026-09-16", "interview"
        html_path = "/root/.openclaw/workspace/bit-deploy/index.html"
    with io.open(md_path, encoding="utf-8") as f:
        md = f.read()

    raw = parse_entries(md)
    # 按原词条编号保序
    entries = [parse_entry(n, w, b) for n, w, b in sorted(raw, key=lambda t: t[0])]

    js_data = build_js(date, topic_key, "BIT V1.0 + BIO 审查", entries)

    # 输出片段文件（可复用存档）
    mmdd = date[5:].replace("-", "")
    snippet_path = "/root/.openclaw/workspace/bit-deploy/dailynote_%s.js" % mmdd
    with io.open(snippet_path, "w", encoding="utf-8") as f:
        f.write(js_data)

    with io.open(html_path, encoding="utf-8") as f:
        html = f.read()

    # 多日期合并（V4.27.0）：保留既有 dailyNotesDB 中其他日期键（如 2026-09-16），仅覆盖同日期键
    m_db = re.search(r'const dailyNotesDB = (\{.*?\n\});\n', html, flags=re.S)
    existing = {}
    if m_db:
        try:
            existing = json.loads(m_db.group(1))
        except Exception as ex:
            print("WARN: parse existing dailyNotesDB failed:", ex)
            existing = {}
    new_payload = json.loads(js_data[len("const dailyNotesDB = "):-2])
    existing.update(new_payload)
    js_data = "const dailyNotesDB = " + json.dumps(existing, ensure_ascii=False, indent=2) + ";\n"

    # 幂等：移除旧 dailyNotesDB 块（如果重跑）
    html = re.sub(r'\n?const dailyNotesDB = \{.*?\n\};\n', '\n', html, flags=re.S)
    # 幂等：移除旧渲染函数块
    html = re.sub(r'\n?// ===== 每日笔记模块（BIT V1\.0 生产 → BIO 审查定稿） V4\.26\.0 新增 =====\n.*?\n\}\n(?=\nfunction startTopicQuiz)', '\n', html, flags=re.S)

    # 1) 插入 dailyNotesDB：topicCalendar 结束后（getTopicForDate 之前）
    # 用正则锚点，兼容旧块移除后残留的多余空行
    m_anchor = re.search(r'\n+function getTopicForDate\(ds\) \{', html)
    assert m_anchor, "getTopicForDate anchor not found"
    html = html[:m_anchor.start()] + '\n\n' + js_data + '\nfunction getTopicForDate(ds) {' + html[m_anchor.end():]
    assert html.count('const dailyNotesDB = {') == 1, "dailyNotesDB count=%d" % html.count('const dailyNotesDB = {')

    # 2) 插入渲染函数：startTopicQuiz 前
    anchor_fn = 'function startTopicQuiz(topicKey) {'
    assert html.count(anchor_fn) == 1, "anchor_fn count=%d" % html.count(anchor_fn)
    html = html.replace(anchor_fn, RENDER_FUNCS.strip() + '\n\n' + anchor_fn)

    # 3) startTopicQuiz 主渲染行前置笔记卡片（幂等：已打过补丁则跳过）
    old_line = 'c.innerHTML = `<div class="card"><div class="card-header" style="flex-wrap:wrap;gap:8px;"><h2>🎯 ${topic.title || topicKey} 课时测试 / Ujian Pelajaran</h2><span class="badge">${questions.length}题 / soal</span></div><div id="quizArea" style="padding:16px;"></div></div>`;'
    new_line = 'c.innerHTML = `${buildDailyNoteCard(topicKey)}<div class="card"><div class="card-header" style="flex-wrap:wrap;gap:8px;"><h2>🎯 ${topic.title || topicKey} 课时测试 / Ujian Pelajaran</h2><span class="badge">${questions.length}题 / soal</span></div><div id="quizArea" style="padding:16px;"></div></div>`;'
    if html.count(new_line) == 1:
        pass  # 已打过补丁，重跑安全
    else:
        assert html.count(old_line) == 1, "quiz render line count=%d" % html.count(old_line)
        html = html.replace(old_line, new_line)

    with io.open(html_path, "w", encoding="utf-8") as f:
        f.write(html)

    n_forms = sum(len(e["forms"]) for e in entries)
    n_ex = sum(len(e["examples"]) for e in entries)
    print("OK entries=%d forms=%d examples=%d snippet=%s" % (len(entries), n_forms, n_ex, snippet_path))

if __name__ == "__main__":
    main()
