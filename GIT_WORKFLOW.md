# Git工作空间管理指南

## 📋 每日工作流程

### 早上开始工作
```bash
# 1. 查看状态
./git-helper.sh status

# 2. 如果有远程仓库，拉取最新
# git pull origin main
```

### 工作中
```bash
# 1. 创建功能分支（如果需要）
./git-helper.sh feature 功能名称

# 2. 定期保存
git add 修改的文件
git commit -m "类型(范围): 简要描述"
```

### 完成一个任务
```bash
# 1. 提交所有更改
./git-helper.sh daily

# 2. 或手动提交
git add .
git commit -m "feat(analysis): 完成小红书趋势分析"
```

### 结束一天工作
```bash
# 1. 查看今天的工作
git log --since="24 hours" --oneline

# 2. 确保所有更改已提交
git status

# 3. 如果有远程仓库，推送更改
# git push origin 当前分支
```

## 🎯 提交信息规范

### 格式
```
类型(范围): 简要描述

详细描述（可选）

- 做了什么改变
- 为什么做这个改变
- 如何测试

关联任务：#123
```

### 类型说明
- `feat`: 新功能
- `fix`: 修复bug  
- `docs`: 文档更新
- `style`: 代码格式
- `refactor`: 代码重构
- `test`: 测试相关
- `chore`: 构建/工具

### 示例
```
feat(xiaohongshu): 添加春季穿搭趋势分析

- 新增小红书热点分析脚本
- 添加春季衣橱整理模板
- 优化数据分析算法

关联任务：#45
```

## 🌿 分支策略

### 主要分支
- `main`: 稳定版本，生产就绪
- `develop`: 开发主分支

### 支持分支
- `feature/*`: 功能开发
- `docs/*`: 文档更新
- `hotfix/*`: 紧急修复

### 工作流程
1. 从 `develop` 创建 `feature/xxx`
2. 在功能分支开发
3. 完成测试后合并到 `develop`
4. 定期从 `develop` 合并到 `main`

## 🛠️ 常用命令

### 简化命令（别名）
```bash
git st    # status
git co    # checkout  
git br    # branch
git ci    # commit
git lg    # 彩色图形日志
```

### 实用命令
```bash
# 查看文件更改
git diff

# 撤销暂存
git unstage 文件

# 查看最后提交
git last

# 修改最后提交
git commit --amend

# 临时保存更改
git stash
git stash pop
```

## 📁 文件管理

### 已排除的文件（.gitignore）
- Python缓存文件 (`__pycache__/`, `*.pyc`)
- 系统文件 (`.DS_Store`, `Thumbs.db`)
- 临时文件 (`*.tmp`, `*.log`)
- 虚拟环境 (`.env`, `.venv/`)

### 需要手动处理的
- 子模块文件夹（作为独立仓库）
- 大型数据文件（考虑使用Git LFS）

## 🔧 故障排除

### 常见问题
1. **提交了不该提交的文件**
   ```bash
   git rm --cached 文件
   git commit -m "fix: 移除误提交的文件"
   ```

2. **想撤销上次提交**
   ```bash
   git reset --soft HEAD~1  # 保留更改
   git reset --hard HEAD~1  # 丢弃更改
   ```

3. **分支合并冲突**
   ```bash
   git status              # 查看冲突文件
   # 手动解决冲突后
   git add 冲突文件
   git commit -m "fix: 解决合并冲突"
   ```

## 📈 最佳实践

1. **小步提交** - 每次提交一个完整的小功能
2. **描述清晰** - 提交信息要能说明做了什么
3. **定期推送** - 避免本地丢失工作
4. **分支管理** - 不同功能使用不同分支
5. **代码审查** - 如果有团队，进行代码审查

## 🚀 快速开始

### 新功能开发
```bash
# 1. 创建功能分支
./git-helper.sh feature 新功能名称

# 2. 开发并提交
git add .
git commit -m "feat: 实现新功能"

# 3. 完成并合并
./git-helper.sh finish
```

### 日常维护
```bash
# 使用助手脚本
./git-helper.sh daily
```

---

*最后更新: 2026年2月21日*
*保持工作空间整洁，快乐编码！* 🦞
