## Git推送命令示例

# Git推送命令大全

## 基础推送
```bash
# 推送当前分支到远程，并建立跟踪
git push -u origin 分支名

# 推送当前分支（已建立跟踪）
git push

# 强制推送（覆盖远程，谨慎使用）
git push -f
```

## 推送多个分支
```bash
# 推送所有分支
git push --all origin

# 推送标签
git push --tags

# 推送分支和标签
git push --follow-tags
```

## 删除远程分支
```bash
# 删除远程分支
git push origin --delete 分支名

# 删除远程标签
git push origin --delete tag v1.0.0
```

## 高级推送
```bash
# 只推送提交，不推送标签
git push --no-tags

# 使用原子推送（要么全部成功，要么全部失败）
git push --atomic

# 推送并设置上游分支
git push -u origin 分支名

# 推送特定提交
git push origin 提交ID:分支名
```

## 推送策略
```bash
# 默认策略（simple）
git config --global push.default simple

# 匹配所有同名分支
git config --global push.default matching

# 当前分支
git config --global push.default current

# 什么都不推送（需要显式指定）
git config --global push.default nothing
```

## 推送前检查
```bash
# 查看将要推送的内容
git push --dry-run

# 查看远程和本地的差异
git log --oneline origin/main..main

# 查看将要推送的提交
git log --oneline @{u}..
```

## 推送问题解决
```bash
# 推送被拒绝（需要先拉取）
git pull --rebase origin main
git push

# 推送被拒绝（有冲突）
git fetch origin
git merge origin/main
# 解决冲突后
git push

# 撤销错误的推送
git revert 提交ID
git push
```

## 自动化推送脚本
```bash
#!/bin/bash
# auto-push.sh

branch=$(git branch --show-current)
echo "当前分支: $branch"

# 检查是否有未提交的更改
if [[ -n $(git status --porcelain) ]]; then
    read -p "有未提交的更改，是否提交？(y/n): " answer
    if [[ $answer == "y" ]]; then
        git add .
        read -p "提交信息: " message
        git commit -m "$message"
    fi
fi

# 推送
echo "正在推送到远程..."
git push -u origin $branch

if [ $? -eq 0 ]; then
    echo "✅ 推送成功"
else
    echo "❌ 推送失败"
    exit 1
fi
```

## 最佳实践
1. **小步推送**：频繁推送小更改
2. **先拉后推**：避免冲突
3. **使用-u**：第一次推送时建立跟踪
4. **避免-f**：除非你知道在做什么
5. **检查差异**：推送前查看将要推送的内容

---

*推送代码是协作的关键，掌握这些命令让协作更顺畅！* 🦞
