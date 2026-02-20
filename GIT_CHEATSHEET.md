# Git命令速查表

## 🔧 配置
```bash
git config --list                    # 查看所有配置
git config user.name                 # 查看用户名
git config user.email                # 查看邮箱
git config --global alias.st status  # 设置别名
```

## 📊 状态查看
```bash
git status                           # 完整状态
git status -s                        # 简洁状态
git log --oneline -20                # 简洁历史
git log --graph --all --oneline      # 图形化历史
git diff                             # 工作区差异
git diff --staged                    # 暂存区差异
```

## 📁 文件操作
```bash
git add 文件名                        # 添加文件
git add .                            # 添加所有
git rm 文件名                         # 删除文件
git mv 旧名 新名                      # 重命名
git restore 文件名                    # 撤销修改
git restore --staged 文件名           # 撤销暂存
```

## 💾 提交管理
```bash
git commit -m "消息"                  # 提交
git commit --amend                   # 修改上次提交
git reset HEAD~1                     # 撤销上次提交
git reset --soft HEAD~1              # 撤销提交，保留更改
git reset --hard HEAD~1              # 撤销提交，丢弃更改
```

## 🌿 分支管理
```bash
git branch                           # 查看分支
git branch 新分支                     # 创建分支
git checkout 分支名                   # 切换分支
git checkout -b 新分支                # 创建并切换
git merge 分支名                      # 合并分支
git branch -d 分支名                  # 删除分支
git branch -D 分支名                  # 强制删除
```

## 🔄 远程操作
```bash
git remote -v                        # 查看远程
git remote add origin URL            # 添加远程
git push -u origin 分支名             # 推送到远程
git pull origin 分支名                # 从远程拉取
git fetch origin                     # 获取远程更新
git clone URL                        # 克隆仓库
```

## 🗂️ 暂存和恢复
```bash
git stash                            # 暂存当前工作
git stash list                       # 查看暂存列表
git stash pop                        # 恢复暂存
git stash apply stash@{0}            # 恢复指定暂存
git stash drop stash@{0}             # 删除暂存
git stash clear                      # 清空所有暂存
```

## 🔍 搜索和查找
```bash
git log --grep="关键词"               # 搜索提交信息
git grep "关键词"                     # 搜索代码内容
git show 提交ID                       # 查看提交详情
git blame 文件名                      # 查看文件修改历史
git bisect start                     # 二分查找bug
```

## 🏷️ 标签管理
```bash
git tag                              # 查看标签
git tag v1.0.0                       # 创建标签
git tag -a v1.0.0 -m "版本说明"       # 创建带说明标签
git push origin v1.0.0               # 推送标签
git tag -d v1.0.0                    # 删除标签
```

## 🛠️ 实用技巧
```bash
# 清理已合并的分支
git branch --merged | grep -v "\*" | xargs -n 1 git branch -d

# 查看贡献统计
git shortlog -s -n

# 查看文件大小
git ls-files | xargs wc -l

# 导出某个提交的文件
git archive --format=zip HEAD -o backup.zip
```

## 🚀 工作流示例

### 日常开发
```bash
git checkout main
git pull origin main
git checkout -b feature/新功能
# ...开发...
git add .
git commit -m "feat: 新功能"
git push origin feature/新功能
```

### 代码审查后
```bash
git checkout main
git pull origin main
git merge --no-ff feature/新功能
git push origin main
git branch -d feature/新功能
```

### 紧急修复
```bash
git checkout main
git checkout -b hotfix/紧急问题
# ...修复...
git add .
git commit -m "fix: 紧急修复"
git checkout main
git merge --no-ff hotfix/紧急问题
git push origin main
git checkout develop
git merge --no-ff hotfix/紧急问题
git push origin develop
```

---

*保持命令熟练，高效开发！* 🦞
