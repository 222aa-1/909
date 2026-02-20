# Git远程仓库管理指南

## 🔗 远程仓库基础

### 查看远程仓库
```bash
git remote -v                    # 查看所有远程
git remote show origin           # 查看远程详情
```

### 添加远程仓库
```bash
# 添加HTTPS远程
git remote add origin https://github.com/用户名/仓库名.git

# 添加SSH远程  
git remote add origin git@github.com:用户名/仓库名.git
```

### 修改远程仓库
```bash
# 修改远程URL
git remote set-url origin 新URL

# 修改远程名称
git remote rename origin upstream

# 删除远程
git remote remove origin
```

## 🔐 认证方式

### SSH认证
```bash
# 生成SSH密钥
ssh-keygen -t ed25519 -C "邮箱"

# 查看公钥
cat ~/.ssh/id_ed25519.pub

# 测试SSH连接
ssh -T git@github.com
```

### HTTPS认证
```bash
# 使用凭证存储
git config --global credential.helper store
git config --global credential.helper osxkeychain  # macOS
git config --global credential.helper wincred      # Windows

# 使用个人访问令牌
git remote set-url origin https://用户名:令牌@github.com/用户名/仓库.git
```

### GitHub CLI认证
```bash
# 安装
brew install gh  # macOS

# 登录
gh auth login
# 选择HTTPS或SSH，按提示操作

# 查看状态
gh auth status
```

## 📤 推送和拉取

### 首次推送
```bash
# 创建新仓库后
git remote add origin URL
git branch -M main
git push -u origin main
```

### 推送所有内容
```bash
git push --all origin      # 所有分支
git push --tags origin     # 所有标签
git push --follow-tags     # 推送提交和关联的标签
```

### 拉取更新
```bash
git pull origin main              # 拉取并合并
git fetch origin                  # 只获取不合并
git fetch origin --prune          # 获取并清理已删除的远程分支
```

## 🌿 分支同步

### 跟踪远程分支
```bash
# 查看跟踪关系
git branch -vv

# 设置上游分支
git branch -u origin/分支名
git push -u origin 分支名

# 取消跟踪
git branch --unset-upstream
```

### 同步远程分支
```bash
# 获取所有远程分支
git fetch --all

# 创建本地分支跟踪远程
git checkout -b 新分支 origin/远程分支

# 删除本地已不存在的远程分支引用
git fetch --prune
```

## 🔄 多远程管理

### 添加多个远程
```bash
# 添加主要远程
git remote add origin https://github.com/用户名/主仓库.git

# 添加上游仓库（用于同步更新）
git remote add upstream https://github.com/原作者/原仓库.git

# 添加个人备份
git remote add backup https://github.com/用户名/备份仓库.git
```

### 多远程操作
```bash
# 推送到多个远程
git push origin main
git push backup main

# 从上游拉取更新
git fetch upstream
git merge upstream/main

# 查看所有远程
git remote -v
```

## 🛠️ 问题解决

### 认证失败
```bash
# SSH失败
ssh -T git@github.com              # 测试连接
cat ~/.ssh/config                  # 检查配置
ssh-add -l                         # 查看加载的密钥

# HTTPS失败
git config --list                  # 检查配置
git credential reject              # 清除缓存凭证
```

### 推送被拒绝
```bash
# 需要先拉取
git pull --rebase origin main
git push

# 强制推送（谨慎）
git push -f

# 仓库为空
git push -u origin main
```

### 远程分支已删除
```bash
# 清理本地远程分支引用
git fetch --prune

# 删除本地已不存在的远程分支
git branch -r | grep -v "origin/main" | xargs git branch -r -d
```

## 🚀 最佳实践

### 1. 使用SSH（推荐）
- 更安全，无需每次输入密码
- 配置一次，长期使用
- 支持多账号

### 2. 设置正确的远程URL
```bash
# 检查当前URL
git remote get-url origin

# 根据需要切换
git remote set-url origin git@github.com:用户名/仓库.git  # SSH
git remote set-url origin https://github.com/用户名/仓库.git  # HTTPS
```

### 3. 定期同步
```bash
# 每日工作前
git fetch --all --prune
git status

# 工作完成后
git push --all
git push --tags
```

### 4. 备份重要仓库
```bash
# 添加备份远程
git remote add backup 备份URL

# 定期推送备份
git push backup --all
```

## 📊 远程状态监控

### 查看差异
```bash
# 查看本地和远程的差异
git log --oneline origin/main..main    # 本地有，远程没有
git log --oneline main..origin/main    # 远程有，本地没有

# 查看所有分支状态
git remote show origin
```

### 统计信息
```bash
# 查看提交统计
git shortlog -s -n --all

# 查看贡献者
git log --format='%aN' | sort -u

# 查看仓库大小
git count-objects -vH
```

---

*掌握远程仓库管理，让协作更高效！* 🦞
