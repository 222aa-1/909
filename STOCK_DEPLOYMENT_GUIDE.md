# 股票分析系统部署指南

## 项目概述
项目名称：InStock股票系统
GitHub仓库：https://github.com/myhhub/stock
功能：股票数据抓取、技术指标计算、K线形态识别、策略选股、回测验证、自动交易

## 部署方案选择

### 方案A：简化测试部署（推荐初次使用）
- 仅安装Python依赖
- 跳过MySQL和TA-Lib
- 测试基本数据抓取和Web界面
- 适合功能验证和学习

### 方案B：完整功能部署
- 安装所有依赖（Python、MySQL、TA-Lib）
- 配置数据库和代理
- 支持所有功能模块
- 适合生产环境使用

## 简化部署步骤

### 1. 下载项目
```bash
cd /Users/imac/.openclaw/workspace
# 如果下载未完成，等待下载完成
```

### 2. 运行部署脚本
```bash
chmod +x deploy_stock.sh
./deploy_stock.sh
```

### 3. 安装Python依赖（跳过TA-Lib）
```bash
cd stock
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip

# 临时修改requirements.txt跳过TA-Lib
cp requirements.txt requirements.txt.backup
grep -v "TA-Lib" requirements.txt > requirements_temp.txt
mv requirements_temp.txt requirements.txt

pip install -r requirements.txt

# 恢复原文件
mv requirements.txt.backup requirements.txt
```

### 4. 测试基本功能
```bash
# 测试Python导入
python3 -c "import pandas as pd; import numpy as np; print('导入成功')"

# 查看项目结构
ls -la
```

### 5. 启动Web服务测试
```bash
# 根据实际脚本名启动
python run_web.py  # 或 python main.py，或查看项目中的启动脚本
```

### 6. 测试数据抓取
```bash
python basic_data_daily_job.py
```

## 完整部署步骤（如需完整功能）

### 1. 安装MySQL
```bash
# 使用Homebrew安装（如已安装）
brew install mysql

# 或从官网下载安装包
# https://dev.mysql.com/downloads/mysql/
```

### 2. 安装TA-Lib
```bash
# macOS使用Homebrew
brew install ta-lib

# 或从官网下载
# https://ta-lib.org/install/
```

### 3. 配置数据库
1. 启动MySQL服务
2. 创建数据库和用户
3. 修改`database.py`中的配置

### 4. 配置东方财富Cookie（提高稳定性）
1. 访问东方财富网并登录
2. 获取Cookie值
3. 设置环境变量或编辑`eastmoney_cookie.txt`

### 5. 配置代理（可选）
编辑`proxy.txt`文件添加代理服务器

## 常见问题解决

### 1. TA-Lib安装失败
- 跳过TA-Lib安装，系统仍可运行基本功能
- 技术指标计算功能将受限

### 2. MySQL连接问题
- 检查MySQL服务是否启动
- 确认数据库配置正确
- 测试数据库连接

### 3. 数据抓取失败
- 检查网络连接
- 配置东方财富Cookie
- 使用代理服务器

### 4. Web服务无法启动
- 检查端口9988是否被占用
- 查看日志文件`stock_web.log`
- 确认所有依赖已安装

## 系统功能模块

### 已部署可测试功能
1. **基础数据抓取** - 股票基本信息、行情数据
2. **Web可视化界面** - 数据查看和分析
3. **数据存储** - 使用文件系统或简化数据库

### 需要完整部署的功能
1. **技术指标计算** - 需要TA-Lib
2. **数据库存储** - 需要MySQL
3. **自动交易** - 需要交易软件和配置
4. **完整回测系统** - 需要历史数据存储

## 下一步建议

1. **先进行简化部署测试**，验证基本功能
2. **根据需求逐步完善**，安装缺失组件
3. **参考项目文档**，了解详细配置
4. **加入用户社区**，获取技术支持

## 联系方式
- 项目GitHub: https://github.com/myhhub/stock
- 问题反馈: GitHub Issues
- 文档参考: 项目README.md