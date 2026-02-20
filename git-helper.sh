#!/bin/bash

# Git工作空间助手脚本

echo "=== Git工作空间助手 ==="
echo "工作目录: $(pwd)"
echo "当前分支: $(git branch --show-current)"
echo ""

case "$1" in
    "status")
        git status
        ;;
    "log")
        git log --oneline -10
        ;;
    "daily")
        echo "=== 每日工作开始 ==="
        git status
        echo ""
        read -p "提交信息: " message
        if [ -n "$message" ]; then
            git add .
            git commit -m "$message"
            echo "✅ 已提交: $message"
        else
            echo "❌ 提交信息不能为空"
        fi
        ;;
    "feature")
        if [ -z "$2" ]; then
            echo "用法: ./git-helper.sh feature <功能名称>"
            exit 1
        fi
        branch_name="feature/$2"
        git checkout -b "$branch_name"
        echo "✅ 创建并切换到分支: $branch_name"
        ;;
    "finish")
        current_branch=$(git branch --show-current)
        if [[ "$current_branch" == "main" ]]; then
            echo "❌ 不能在main分支上完成功能"
            exit 1
        fi
        echo "=== 完成功能: $current_branch ==="
        git status
        echo ""
        read -p "提交信息: " message
        if [ -n "$message" ]; then
            git add .
            git commit -m "$message"
            git checkout main
            git merge "$current_branch"
            echo "✅ 功能已合并到main分支"
        else
            echo "❌ 提交信息不能为空"
        fi
        ;;
    *)
        echo "可用命令:"
        echo "  status    - 查看状态"
        echo "  log       - 查看提交历史"
        echo "  daily     - 每日提交工作"
        echo "  feature   - 创建功能分支"
        echo "  finish    - 完成功能并合并"
        echo ""
        echo "示例:"
        echo "  ./git-helper.sh daily"
        echo "  ./git-helper.sh feature xiaohongshu-analysis"
        echo "  ./git-helper.sh finish"
        ;;
esac
