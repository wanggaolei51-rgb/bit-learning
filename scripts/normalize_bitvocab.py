# -*- coding: utf-8 -*-
"""V4.51.0 前置修复: 摘除 bitVocabDB 内的回填批注行 + 收尾尾逗号, 恢复纯 JSON 合法, 使 md_to_dailynote 幂等解析恢复工作"""
import io, re

p = "/root/.openclaw/workspace/index.html"
s = io.open(p, encoding="utf-8").read()

# 1) 删除三处回填批注（226091/226108 为整行, 226139 与 }; 同行）
s = s.replace(" /* V4.50.0 回填结束 · CA 话题2-6 新词30 */\n", "\n", 1)
s = s.replace(" /* V4.50.0 回填A结束 · 话题7 Day1 */\n", "\n", 1)
s = s.replace(" /* V4.50.0 回填B结束 · 话题7 Day2+Day3 */};", "\n};", 1)

# 2) bitVocabDB 收尾尾逗号清理（定位对象末尾的 , 换行 }; ）
i = s.index("const bitVocabDB = {")
j = s.index("{", i)
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
tail = s[end-40:end+1]
fixed = re.sub(r",\s*\n\}$", "\n}", s[j:end+1])
s = s[:j] + fixed + s[end+1:]

io.open(p, "w", encoding="utf-8").write(s)
print("normalized; bitVocabDB end tail now:", repr(s[end-30:end+2]))
