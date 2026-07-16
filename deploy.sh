#!/bin/bash
# BIT 一键部署脚本 — 部署到 GitHub Pages
# 使用方法：
# 1. 在 GitHub 创建 Personal Access Token（Settings → Developer settings → Personal access tokens → Tokens classic）
# 2. 给 token 勾选 "repo" 权限
# 3. 运行: GITHUB_TOKEN=your_token GITHUB_USER=your_username ./deploy.sh

set -e

TOKEN="${GITHUB_TOKEN:-}"
USER="${GITHUB_USER:-}"
REPO="${GITHUB_REPO:-bit-learning}"

if [ -z "$TOKEN" ] || [ -z "$USER" ]; then
    echo "❌ 错误: 请设置环境变量 GITHUB_TOKEN 和 GITHUB_USER"
    echo ""
    echo "示例:"
    echo "  export GITHUB_TOKEN=ghp_xxxxxxxxxxxx"
    echo "  export GITHUB_USER=your_username"
    echo "  ./deploy.sh"
    echo ""
    echo "获取 Token 步骤:"
    echo "  1. 打开 https://github.com/settings/tokens"
    echo "  2. 点击 'Generate new token (classic)'"
    echo "  3. 勾选 'repo' 权限"
    echo "  4. 复制 token"
    exit 1
fi

echo "🚀 开始部署 BIT 到 GitHub Pages..."
echo "   用户: $USER"
echo "   仓库: $REPO"

# 检查仓库是否存在
REPO_EXISTS=$(curl -s -o /dev/null -w "%{http_code}" \
    -H "Authorization: token $TOKEN" \
    "https://api.github.com/repos/$USER/$REPO")

if [ "$REPO_EXISTS" = "404" ]; then
    echo "📦 创建新仓库..."
    curl -s -X POST \
        -H "Authorization: token $TOKEN" \
        -H "Accept: application/vnd.github.v3+json" \
        -d "{\"name\":\"$REPO\",\"description\":\"🇮🇩 BIT - Bahasa Indonesia Learning Terminal\",\"homepage\":\"https://$USER.github.io/$REPO\",\"private\":false}" \
        "https://api.github.com/user/repos" > /dev/null
    echo "✅ 仓库创建成功"
else
    echo "✅ 仓库已存在"
fi

# 准备推送
cd "$(dirname "$0")"

# 设置远程仓库
if git remote | grep -q origin; then
    git remote remove origin
fi
git remote add origin "https://$TOKEN@github.com/$USER/$REPO.git"

# 推送
echo "📤 推送代码..."
git branch -M main 2>/dev/null || true
git push -u origin main --force

echo ""
echo "✅ 推送完成！"
echo ""
echo "🌐 启用 GitHub Pages:"
echo "   1. 打开 https://github.com/$USER/$REPO/settings/pages"
echo "   2. Source 选择 'Deploy from a branch'"
echo "   3. Branch 选择 'main'，文件夹选择 '/ (root)'"
echo "   4. 点击 Save"
echo ""
echo "⏳ 等待 1-2 分钟后访问:"
echo "   https://$USER.github.io/$REPO/"
echo ""
