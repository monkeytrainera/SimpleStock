# 极简库存管理系统

一款专为小微企业和小型仓库设计的单机轻量化库存管理工具。

## 功能特性

- 商品基础管理（新增、编辑、删除、查询）
- 入库管理（手动录入、库存自动更新）
- 出库管理（库存校验、负库存拦截）
- 库存查询（实时数据、精准搜索）
- 台账报表（流水记录、Excel导出）
- 账号管理（用户增删、密码修改）
- 数据备份与恢复

## 技术栈

- Python 3.10+
- PyQt6
- SQLite
- openpyxl

## 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 运行项目

```bash
python main.py
```

## 项目结构

```
SimpleStock/
├── src/              # 源代码目录
│   ├── ui/           # UI组件
│   ├── business/     # 业务逻辑
│   ├── data/         # 数据访问
│   ├── utils/        # 工具函数
│   └── config/       # 配置文件
├── tests/            # 测试目录
├── resources/        # 静态资源
├── main.py           # 应用入口
└── requirements.txt  # 依赖清单
```

## 登录信息

- 用户名：admin
- 密码：admin123

**首次登录后请强制修改密码！**

## 文档

- `docs/requirements.md` - 需求规格说明书
- `docs/technical_design.md` - 技术设计文档
- `docs/ui_design.md` - UI/交互设计文档
- `docs/test_plan.md` - 测试计划
- `docs/deployment_guide.md` - 部署指南
- `docs/user_manual.md` - 用户手册
- `docs/changelog.md` - 变更日志
