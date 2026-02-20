#!/bin/bash

# 股票系统部署脚本
# 作者: Clawd
# 日期: 2026-02-19

set -e

echo "🚀 开始部署股票分析系统..."
echo "========================================"

# 检查项目目录
if [ ! -d "stock" ]; then
    echo "❌ 项目目录不存在"
    exit 1
fi

cd stock

echo "📁 项目目录: $(pwd)"
echo "========================================"

# 1. 检查Python版本
echo "1. 检查Python环境..."
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "   Python版本: $PYTHON_VERSION"

if [[ "$PYTHON_VERSION" < "3.7" ]]; then
    echo "   ⚠️  Python版本较低，建议升级到3.7+"
fi

# 2. 查看项目结构
echo ""
echo "2. 查看项目结构..."
ls -la

# 3. 查看requirements.txt
echo ""
echo "3. 查看依赖文件..."
if [ -f "requirements.txt" ]; then
    echo "   ✅ 找到requirements.txt"
    head -20 requirements.txt
else
    echo "   ❌ 未找到requirements.txt"
    exit 1
fi

# 4. 安装Python依赖（简化版，跳过TA-Lib）
echo ""
echo "4. 安装Python依赖..."
echo "   注意：跳过TA-Lib安装，如需完整功能请手动安装"

# 创建虚拟环境（可选）
if [ ! -d "venv" ]; then
    echo "   创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
source venv/bin/activate

# 安装基本依赖（排除TA-Lib）
echo "   安装基本依赖包..."
pip install --upgrade pip

# 临时修改requirements.txt，注释掉TA-Lib
if grep -q "TA-Lib" requirements.txt; then
    echo "   跳过TA-Lib安装..."
    cp requirements.txt requirements.txt.backup
    grep -v "TA-Lib" requirements.txt > requirements_temp.txt
    mv requirements_temp.txt requirements.txt
fi

pip install -r requirements.txt

# 恢复原文件
if [ -f "requirements.txt.backup" ]; then
    mv requirements.txt.backup requirements.txt
fi

# 5. 检查配置文件
echo ""
echo "5. 检查配置文件..."
if [ -f "database.py" ]; then
    echo "   ✅ 找到database.py"
    echo "   当前数据库配置:"
    grep -E "db_host|db_user|db_password|db_port" database.py || echo "   使用默认配置"
else
    echo "   ⚠️ 未找到database.py，可能需要手动创建"
fi

# 6. 测试基本功能
echo ""
echo "6. 测试基本功能..."
echo "   a) 测试Python导入..."
python3 -c "import pandas as pd; import numpy as np; print('✅ pandas/numpy 导入成功')" || echo "   ⚠️ 导入失败"

echo "   b) 查看主要脚本..."
ls *.py | head -10

# 7. 启动Web服务测试
echo ""
echo "7. Web服务测试..."
echo "   要启动Web服务，请运行:"
echo "   cd $(pwd)"
echo "   source venv/bin/activate"
echo "   python run_web.py 或 python main.py (根据实际脚本名)"
echo ""
echo "   Web界面地址: http://localhost:9988/"

# 8. 数据抓取测试
echo ""
echo "8. 数据抓取测试..."
echo "   要测试数据抓取，请运行:"
echo "   python basic_data_daily_job.py"

echo ""
echo "========================================"
echo "✅ 简化部署完成！"
echo ""
echo "📋 后续步骤:"
echo "1. 安装MySQL数据库（如需完整功能）"
echo "2. 安装TA-Lib库（如需技术指标计算）"
echo "3. 配置东方财富Cookie（提高数据获取稳定性）"
echo "4. 配置代理（如需大量数据抓取）"
echo ""
echo "💡 提示: 完整部署指南请参考项目README.md"