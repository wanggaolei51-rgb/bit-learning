# -*- coding: utf-8 -*-
"""V4.50.0: 合并 topic7Negotiation 入 caData（幂等）"""
import io, json

def extract_obj_text(s, marker):
    i = s.index(marker)
    j = s.index("{", i)
    depth = 0; in_str = False; esc = False; q = ""
    for k in range(j, len(s)):
        ch = s[k]
        if in_str:
            if esc: esc = False; continue
            if ch == "\\": esc = True; continue
            if ch == q: in_str = False
            continue
        if ch in ('"', "'", "`"): in_str = True; q = ch; continue
        if ch == "{": depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0: return j, k + 1
    raise SystemExit("object end not found for " + marker)

p = "/root/.openclaw/workspace/index.html"
s = io.open(p, encoding="utf-8").read()

# 幂等：已合并则先摘除
if '"negotiation":' in s:
    a = s.index('"negotiation":')
    # 找到该条目的结束（利用 topic7 对象的配平）
    j = s.index("{", a)
    depth = 0; in_str = False; esc = False; q = ""
    end = -1
    for k in range(j, len(s)):
        ch = s[k]
        if in_str:
            if esc: esc = False; continue
            if ch == "\\": esc = True; continue
            if ch == q: in_str = False
            continue
        if ch in ('"', "'", "`"): in_str = True; q = ch; continue
        if ch == "{": depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0: end = k; break
    tail = s[end+1:end+3]
    assert tail[0] == ",", "unexpected tail after negotiation entry"
    s = s[:a] + s[end+2:]
    io.open(p, "w", encoding="utf-8").write(s)
    print("previous merge removed")

t7 = io.open("/root/.openclaw/workspace/agents/CA/topic7_negotiation.js", encoding="utf-8").read()
j, e = extract_obj_text(t7, "const topic7Negotiation =")
obj = t7[j:e]

js, je = extract_obj_text(s, "const caData = {")
tail = s[je-1:je+1]
assert tail == "};", "caData tail unexpected: " + repr(tail)
insert_at = je - 1  # '}' 位置
block = ',\n "negotiation": ' + obj + ","
new = s[:insert_at] + block + s[insert_at:]
io.open(p, "w", encoding="utf-8").write(new)
print("merged negotiation into caData at", insert_at)
