#!/bin/bash
# BIR 部署前检查脚本 — 每次部署前必须执行
# 用法: cd /root/.openclaw/workspace/bit-deploy && bash deploy-check.sh

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

ERRORS=0

echo "========================================"
echo "BIR 部署前硬性检查清单"
echo "========================================"
echo ""

# 1. 当前分支
echo -n "[1/8] 当前分支: "
BRANCH=$(git branch --show-current)
if [ "$BRANCH" = "main" ]; then
    echo -e "${GREEN}$BRANCH ✓${NC}"
else
    echo -e "${RED}$BRANCH ✗ (必须为 main)${NC}"
    ERRORS=$((ERRORS+1))
fi

# 2. git status
echo -n "[2/8] 未提交更改: "
if [ -z "$(git status --short)" ]; then
    echo -e "${GREEN}无 ✓${NC}"
else
    echo -e "${RED}有未提交更改 ✗${NC}"
    git status --short
    ERRORS=$((ERRORS+1))
fi

# 3. 版本号
echo -n "[3/8] 版本号: "
VERSION=$(grep -oP 'V\d+\.\d+\.\d+' index.html | head -1)
if [ -n "$VERSION" ]; then
    echo -e "${GREEN}$VERSION ✓${NC}"
else
    echo -e "${RED}未找到版本号 ✗${NC}"
    ERRORS=$((ERRORS+1))
fi

# 4. 括号平衡
echo -n "[4/8] vocabDB 括号平衡: "
python3 << 'PYEOF'
import sys
with open('index.html', 'r') as f:
    content = f.read()
start = content.find('const vocabDB = {')
end = content.find('const topicData = {')
if start > 0 and end > start:
    sec = content[start:end]
    if sec.count('{') == sec.count('}'):
        print(f"✓ {sec.count('{')}/{sec.count('}')}")
    else:
        print(f"✗ {sec.count('{')}/{sec.count('}')} UNBALANCED")
        sys.exit(1)
else:
    print("✗ 未找到 vocabDB")
    sys.exit(1)
PYEOF
if [ $? -ne 0 ]; then ERRORS=$((ERRORS+1)); fi

echo -n "[5/8] topicData 括号平衡: "
python3 << 'PYEOF'
import sys
with open('index.html', 'r') as f:
    content = f.read()
start = content.find('const topicData = {')
end = content.find('const topicCalendar = {')
if start > 0 and end > start:
    sec = content[start:end]
    if sec.count('{') == sec.count('}'):
        print(f"✓ {sec.count('{')}/{sec.count('}')}")
    else:
        print(f"✗ {sec.count('{')}/{sec.count('}')} UNBALANCED")
        sys.exit(1)
else:
    print("✗ 未找到 topicData")
    sys.exit(1)
PYEOF
if [ $? -ne 0 ]; then ERRORS=$((ERRORS+1)); fi

# 6. 无重复声明
echo -n "[6/8] topicCalendar 重复检查: "
COUNT=$(grep -c "const topicCalendar = {" index.html)
if [ "$COUNT" -eq 1 ]; then
    echo -e "${GREEN}1 次 ✓${NC}"
else
    echo -e "${RED}$COUNT 次 ✗ (必须为 1)${NC}"
    ERRORS=$((ERRORS+1))
fi

echo -n "[7/8] topicData 重复检查: "
COUNT=$(grep -c "const topicData = {" index.html)
if [ "$COUNT" -eq 1 ]; then
    echo -e "${GREEN}1 次 ✓${NC}"
else
    echo -e "${RED}$COUNT 次 ✗ (必须为 1)${NC}"
    ERRORS=$((ERRORS+1))
fi

echo -n "[8/8] vocabDB 重复检查: "
COUNT=$(grep -c "const vocabDB = {" index.html)
if [ "$COUNT" -eq 1 ]; then
    echo -e "${GREEN}1 次 ✓${NC}"
else
    echo -e "${RED}$COUNT 次 ✗ (必须为 1)${NC}"
    ERRORS=$((ERRORS+1))
fi

echo ""
echo "========================================"
if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}✅ 所有检查通过，可以部署${NC}"
    echo "========================================"
    exit 0
else
    echo -e "${RED}❌ 发现 $ERRORS 个错误，修复后才能部署${NC}"
    echo "========================================"
    exit 1
fi
