#!/usr/bin/env python3
"""check_syntax.py — 提取 index.html 内所有 <script> 块逐块 node --check 风格解析。

动态定位 script 边界（不再硬编码行号），防止内容膨胀后检查器静默失效。
"""
import re
import subprocess
import sys

PATH = sys.argv[1] if len(sys.argv) > 1 else 'index.html'

with open(PATH, 'r', encoding='utf-8') as f:
    html = f.read()

blocks = re.findall(r'<script>(.*?)</script>', html, re.S)
if not blocks:
    print("JS PARSE FAIL: no <script> blocks found")
    sys.exit(1)

ok = True
for i, block in enumerate(blocks):
    # 跳过纯外链/空块
    if not block.strip():
        continue
    tmp = f'/tmp/check_block_{i}.js'
    with open(tmp, 'w', encoding='utf-8') as f:
        f.write(block)
    result = subprocess.run(['node', '--check', tmp], capture_output=True, text=True)
    if result.returncode != 0:
        ok = False
        print(f"JS PARSE FAIL (block {i}):")
        print(result.stderr[:1000])
        print(f"block {i} 长度: {len(block)} 字符")

if ok:
    print(f"JS PARSE: PASS ({len(blocks)} blocks)")
else:
    sys.exit(1)

# --- TOOLS.md 检查清单第 8 项：dailynote 源档案禁引注释头 ---
import glob
import os

bad = []
for p in sorted(glob.glob(os.path.join(os.path.dirname(PATH), 'dailynote_*.js'))):
    with open(p, encoding='utf-8') as f:
        first = f.readline()
    if '源数据档案' not in first:
        bad.append(os.path.basename(p))
if bad:
    print(f"ARCHIVE HEADER FAIL: {', '.join(bad)} 缺禁引注释头（首行须含「源数据档案」）")
    sys.exit(1)
print(f"ARCHIVE HEADER: PASS ({len(glob.glob(os.path.join(os.path.dirname(PATH), 'dailynote_*.js')))} archives)")
