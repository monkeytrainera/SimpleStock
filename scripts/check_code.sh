#!/bin/bash
# 代码质量检查脚本
# 使用方式: ./scripts/check_code.sh [--fix]

set -e

echo "========================================"
echo "         代码质量检查脚本"
echo "========================================"

# 检查是否有 --fix 参数
FIX_MODE=false
if [ "$1" = "--fix" ]; then
    FIX_MODE=true
    echo "模式: 自动修复模式"
else
    echo "模式: 检查模式"
fi

echo ""
echo "1/5: 运行 isort (import排序)..."
if $FIX_MODE; then
    isort src/ --profile black
    echo "     ✓ isort 自动修复完成"
else
    if isort --check --profile black src/; then
        echo "     ✓ isort 检查通过"
    else
        echo "     ✗ isort 检查失败"
        echo "     建议运行: isort src/ --profile black"
        exit 1
    fi
fi

echo ""
echo "2/5: 运行 black (代码格式化)..."
if $FIX_MODE; then
    black src/
    echo "     ✓ black 自动修复完成"
else
    if black --check src/; then
        echo "     ✓ black 检查通过"
    else
        echo "     ✗ black 检查失败"
        echo "     建议运行: black src/"
        exit 1
    fi
fi

echo ""
echo "3/5: 运行 flake8 (代码风格检查)..."
if flake8 src/; then
    echo "     ✓ flake8 检查通过"
else
    echo "     ✗ flake8 检查失败"
    exit 1
fi

echo ""
echo "4/5: 运行 mypy (类型检查)..."
if mypy src/; then
    echo "     ✓ mypy 检查通过"
else
    echo "     ✗ mypy 检查失败"
    exit 1
fi

echo ""
echo "5/5: 运行 pylint (静态代码分析)..."
if pylint src/; then
    echo "     ✓ pylint 检查通过"
else
    echo "     ✗ pylint 检查失败"
    exit 1
fi

echo ""
echo "========================================"
echo "         所有检查通过!"
echo "========================================"
