#!/usr/bin/env python3
"""
C4→C5 升级后自检脚本
"""

def check_braces(content, start_line=0):
    """检查括号平衡"""
    stack = []
    line_num = start_line
    char_num = 0
    
    for i, ch in enumerate(content):
        if ch == '\n':
            line_num += 1
            char_num = 0
        else:
            char_num += 1
        
        if ch in '({[':
            stack.append((ch, line_num, char_num))
        elif ch in ')}]':
            if not stack:
                return False, f"Unmatched closing brace '{ch}' at line {line_num}"
            last = stack.pop()
            pairs = {'(': ')', '{': '}', '[': ']'}
            if pairs[last[0]] != ch:
                return False, f"Mismatched braces: '{last[0]}' at line {last[1]} and '{ch}' at line {line_num}"
    
    if stack:
        return False, f"Unclosed braces: {[(s[0], s[1]) for s in stack[-5:]]}"
    return True, "OK"

def main():
    with open('/root/.openclaw/workspace/bit-deploy/index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("=" * 60)
    print("BIR V4.17.0 C4→C5 升级自检报告")
    print("=" * 60)
    
    # 1. 检查版本号
    print("\n📋 1. 版本号检查")
    if 'LEO-BIR V4.17.0-08162026 (C5课程结构升级)' in content:
        print("  ✅ Title: LEO-BIR V4.17.0-08162026 (C5课程结构升级)")
    else:
        print("  ❌ Title 版本号不正确")
    
    if 'LEO-BIR V4.17.0 · C5课程结构升级 · UKBI真题模拟' in content:
        print("  ✅ Sidebar: LEO-BIR V4.17.0 · C5课程结构升级 · UKBI真题模拟")
    else:
        print("  ❌ Sidebar 版本号不正确")
    
    # 2. 检查 topicCalendar
    print("\n📋 2. topicCalendar 检查")
    checks = [
        ('2026-08-16', 'ukbi_exam', '📜 UKBI 5级 · 真题模拟日'),
        ('2026-08-17', 'emotions_life', '💝 情感及生活 · Day 1'),
        ('2026-08-18', 'emotions_life', '💝 情感及生活 · Day 2'),
        ('2026-08-19', 'emotions_life', '💝 情感及生活 · Day 3'),
    ]
    for date, topic, label in checks:
        pattern = f'"{date}": {{topic: "{topic}"'
        if pattern in content:
            print(f"  ✅ {date}: {label}")
        else:
            print(f"  ❌ {date}: 未找到")
    
    # 3. 检查 topicData
    print("\n📋 3. topicData 新话题检查")
    topics = ['ukbi_exam', 'emotions_life']
    for topic in topics:
        if f'{topic}: {{' in content:
            print(f"  ✅ {topic}: 已定义")
        else:
            print(f"  ❌ {topic}: 未定义")
    
    # 4. 检查 C5 逻辑
    print("\n📋 4. C5 前置复习逻辑检查")
    c5_checks = [
        ('规则B: 话题间复习', '规则B: 话题间复习 (新话题第一天)'),
        ('规则A: 日内复习', '规则A: 日内复习 (每天的前置复习)'),
        ('buildC4Map 函数', 'function buildC4Map'),
        ('getPrevDate 函数', 'function getPrevDate'),
        ('reviewHtml 插入', 'html += reviewHtml;'),
    ]
    for name, pattern in c5_checks:
        if pattern in content:
            print(f"  ✅ {name}")
        else:
            print(f"  ❌ {name}: 未找到")
    
    # 5. 检查关键数据结构完整性
    print("\n📋 5. 新话题数据完整性检查")
    for topic in ['ukbi_exam', 'emotions_life']:
        print(f"  {topic}:")
        for field in ['title:', 'icon:', 'days:', 'grammar:', 'vocab:', 'scenes:', 'speeches:', 'quiz:']:
            pattern = f'{topic}: {{' if field == 'title:' else field
            # 在 topic 的定义范围内搜索
            start = content.find(f'{topic}: {{')
            if start == -1:
                print(f"    ❌ {field} - topic not found")
                continue
            end = content.find('}},', start)
            if end == -1:
                end = content.find('},\n};', start)
            segment = content[start:end]
            if field in segment:
                print(f"    ✅ {field}")
            else:
                print(f"    ❌ {field}")
    
    # 6. 括号平衡检查
    print("\n📋 6. 括号平衡检查")
    
    # 检查 topicData 区域
    td_start = content.find('const topicData = {')
    td_end = content.find('};\n\nfunction getTopicForDate')
    if td_start > -1 and td_end > -1:
        td_content = content[td_start:td_end+2]
        ok, msg = check_braces(td_content)
        print(f"  topicData: {'✅' if ok else '❌'} {msg}")
    
    # 检查 topicCalendar 区域
    tc_start = content.find('const topicCalendar = {')
    tc_end = content.find('};\n\nfunction getTopicForDate')
    if tc_start > -1 and tc_end > -1:
        tc_content = content[tc_start:tc_end+2]
        ok, msg = check_braces(tc_content)
        print(f"  topicCalendar: {'✅' if ok else '❌'} {msg}")
    
    # 检查整个文件的大括号（粗略）
    ok, msg = check_braces(content)
    print(f"  全局: {'✅' if ok else '❌'} {msg}")
    
    # 7. 统计信息
    print("\n📋 7. 文件统计")
    line_count = content.count('\n')
    print(f"  总行数: {line_count}")
    print(f"  文件大小: {len(content)} bytes")
    
    print("\n" + "=" * 60)
    print("自检完成。如有 ❌ 项，请检查对应代码。")
    print("=" * 60)

if __name__ == '__main__':
    main()
