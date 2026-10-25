#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fix_skeleton_merge.py — 骨架词条修复合并器
只更新 bitVocabDB（不触碰 dailyNotesDB），键名保持原样（含空格）。
用法: python3 fix_skeleton_merge.py <md...> --html index.html
"""
import json, re, sys

def parse_entries(md_text):
    pat = re.compile(r'^###\s+(\d+)\.\s+(.+?)\s*$', re.M)
    matches = list(pat.finditer(md_text))
    entries = []
    for idx, m in enumerate(matches):
        word = m.group(2).strip()
        start = m.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(md_text)
        entries.append((word, md_text[start:end]))
    return entries

def grab(rx, text, flags=0, group=1, default=""):
    m = re.search(rx, text, flags)
    return m.group(group).strip() if m else default

def parse_entry(word, body):
    e = {"word": word, "cn": "", "en": "", "root": "",
         "forms": [], "formsNote": "", "note": "",
         "synonyms": [], "antonyms": [], "examples": []}
    e["cn"] = grab(r'^\s*-\s*\*\*中文\*\*:[ \t]*(.+?)\s*$', body, re.M)
    e["en"] = grab(r'^\s*-\*\*English\*\*:[ \t]*(.+?)\s*$'.replace('-\*\*','- \\*\\*'), body, re.M)
    e["en"] = grab(r'^\s*-\s*\*\*English\*\*:[ \t]*(.+?)\s*$', body, re.M)
    e["root"] = grab(r'^\s*-\s*\*\*词根\*\*:[ \t]*(.+?)\s*$', body, re.M)

    m_forms = re.search(r'^\s*-\s*\*\*变形\*\*[^:]*:[ \t]*(.*)$', body, re.M)
    if m_forms:
        rest = m_forms.group(1).strip()
        if rest and rest != '—':
            e["formsNote"] = rest
        tbl = []
        for line in body[m_forms.end():].splitlines()[1:]:
            s = line.strip()
            if not s:
                if tbl: break
                continue
            if s.startswith('|') and not re.match(r'^\|[\s:\-|]+\|$', s):
                cells = [c.strip() for c in s.strip('|').split('|')]
                if len(cells) >= 2 and cells[0] not in ('变形','形式'):
                    if len(cells) >= 3:
                        tbl.append({"form": cells[0], "pos": cells[1], "mean": cells[2]})
                    else:
                        # 两列表格（变形|说明）：说明进 mean，pos 留空
                        tbl.append({"form": cells[0], "pos": "", "mean": cells[1]})
            elif tbl:
                break
        e["forms"] = tbl

    e["formsNote"] = grab(r'^\s*-\s*\*\*变形说明\*\*:[ \t]*(.+?)\s*$', body, re.M) or e["formsNote"]
    e["note"] = grab(r'^\s*-\s*\*\*词汇注释\*\*:[ \t]*(.+?)\s*$', body, re.M)

    def list_field(name):
        # 与既有管线一致：整行作为一个数组元素（如 ["tersangkut, terperangkap"]）
        v = grab(r'^\s*-\s*\*\*' + name + r'\*\*:[ \t]*(.+?)\s*$', body, re.M)
        if not v or v == '—':
            return []
        return [v]
    e["synonyms"] = list_field('同义词')
    e["antonyms"] = list_field('反义词')

    for m in re.finditer(r'^\s*-\s*([^:：*][^:：]{0,20})[:：]\s*\*(.+?)\*\s*(.+?)\s*$', body, re.M):
        scene, id_, cn_ = m.group(1).strip(), m.group(2).strip(), m.group(3).strip()
        if scene in ('中文','English','词根','变形','变形说明','词汇注释','同义词','反义词'):
            continue
        e["examples"].append({"scene": scene, "id": id_, "cn": cn_})
    return e

def main():
    args = sys.argv[1:]
    html_path = args[args.index('--html')+1]
    md_paths = [a for a in args if a.endswith('.md')]
    new_entries = {}
    for p in md_paths:
        with open(p, encoding='utf-8') as f:
            for word, body in parse_entries(f.read()):
                new_entries[word] = parse_entry(word, body)
    print(f"解析词条: {len(new_entries)} 来自 {len(md_paths)} 个文件")

    with open(html_path, encoding='utf-8') as f:
        html = f.read()

    m = re.search(r'const bitVocabDB = (\{.*?\n\});', html, flags=re.S)
    if not m:
        m = re.search(r'const bitVocabDB = (\{\});', html)
    db = json.loads(m.group(1))
    print(f"现有 bitVocabDB: {len(db)} 词")

    # mengada-ada 只补 en
    if 'mengada-ada' in db and not db['mengada-ada'].get('en'):
        db['mengada-ada']['en'] = 'to make up; to fabricate; to feign'
        print("mengada-ada: 补 en ✓")

    applied, missed = [], []
    for w, e in new_entries.items():
        if w in db:
            db[w] = e
            applied.append(w)
        else:
            missed.append(w)
    print(f"更新: {len(applied)} | 库中无此键(未应用): {len(missed)}")
    if missed:
        print("  未命中:", missed)

    new_block = "const bitVocabDB = " + json.dumps(db, ensure_ascii=False, indent=2) + ";\n"
    html = html[:m.start()] + new_block + html[m.end():]
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print("合并完成 →", html_path)

if __name__ == '__main__':
    main()
