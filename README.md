# 图书管理系统 (Library Management System)

ISYS3001 配置管理和采购管理演示项目 - 学生2

## 项目简介

这是一个基于Python FastAPI和前端三件套(HTML/CSS/JavaScript)开发的现代化图书管理系统，用于演示配置管理和采购管理的实际应用。

## 技术栈

- **后端**: Python 3.8+, FastAPI, Pydantic, Uvicorn
- **前端**: HTML5, CSS3, JavaScript (ES6+)
- **数据存储**: JSON文件 (模拟数据库)
- **异步处理**: aiofiles, async/await
- **API文档**: 自动生成的OpenAPI/Swagger文档
- **配置管理**: Git, 环境配置文件

## 功能特性

### 📚 图书管理
- 图书增删改查 (CRUD操作)
- 图书分类管理 (小说、科学、技术、历史等)
- 图书库存管理 (总库存、可借阅数量)
- 图书搜索功能 (按标题、作者、出版社)
- 可借阅图书查询

### 👤 用户管理
- 用户信息管理 (姓名、邮箱、电话)
- 用户类型分类 (学生、教职工、员工、访客)
- 用户状态管理 (活跃、暂停、非活跃)
- 借阅限制管理 (不同用户类型有不同借阅限制)
- 活跃用户统计

### 📖 借阅管理
- 借阅记录管理 (完整的借还记录)
- 图书借还功能 (实时更新库存)
- 逾期管理和罚金计算 (自动计算逾期罚金)
- 借阅状态跟踪 (借出、归还、逾期、丢失)

### 📊 统计分析
- 图书馆运营统计 (总图书数、借出数量等)
- 借阅趋势分析
- 用户活跃度统计
- 图书利用率分析
- 逾期记录统计

## 项目结构

```
library-system/
├── app/                    # FastAPI应用
│   ├── __init__.py
│   ├── main.py            # 主应用和路由
│   ├── models.py          # Pydantic数据模型
│   └── services.py        # 业务逻辑服务层
├── frontend/              # 前端静态文件
│   ├── index.html         # 主页面
│   ├── styles.css         # 样式文件
│   └── script.js          # JavaScript逻辑
├── data/                  # JSON数据文件
│   ├── books.json         # 图书数据
│   ├── users.json         # 用户数据
│   └── borrow_records.json # 借阅记录
├── config/                # 配置文件
├── deployment/            # 部署脚本
├── requirements.txt       # Python依赖
├── start.py              # 启动脚本
└── README.md
```

## 安装和运行

### 环境要求
- Python 3.8 或更高版本
- pip (Python包管理器)

### 安装步骤
1. 克隆仓库到本地
```bash
git clone <repository-url>
cd library-system
```

2. 安装Python依赖
```bash
pip install -r requirements.txt
```

3. 启动服务器
```bash
python start.py
```
或者
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

4. 访问应用
- 前端界面: http://localhost:8000
- API文档: http://localhost:8000/docs
- 健康检查: http://localhost:8000/api/health

## API端点

### 图书管理
- `GET /api/books` - 获取所有图书
- `POST /api/books` - 创建新图书
- `GET /api/books/{id}` - 获取指定图书
- `PUT /api/books/{id}` - 更新图书
- `DELETE /api/books/{id}` - 删除图书
- `GET /api/books/search?keyword=` - 搜索图书
- `GET /api/books/category/{category}` - 按分类获取图书

### 用户管理
- `GET /api/users` - 获取所有用户
- `POST /api/users` - 创建新用户
- `GET /api/users/{id}` - 获取指定用户
- `PUT /api/users/{id}` - 更新用户
- `DELETE /api/users/{id}` - 删除用户

### 借阅管理
- `GET /api/borrow-records` - 获取所有借阅记录
- `POST /api/borrow-records` - 创建借阅记录
- `PATCH /api/borrow-records/{id}/return` - 归还图书
- `DELETE /api/borrow-records/{id}` - 删除借阅记录

### 统计信息
- `GET /api/stats` - 获取图书馆统计信息
- `GET /api/health` - 健康检查

## 分支策略

- `main`: 主分支，稳定版本
- `develop`: 开发分支
- `feature/*`: 功能分支
- `hotfix/*`: 热修复分支

## 配置管理实践

本项目实施了以下配置管理实践：

### 版本控制
- Git版本控制和分支管理
- 提交信息规范化
- 功能分支开发模式

### 环境配置
- 开发/生产环境配置分离
- 环境变量管理
- 配置文件模板化

### 依赖管理
- requirements.txt管理Python依赖
- 版本锁定确保环境一致性
- 虚拟环境隔离

### 代码质量
- 代码结构模块化
- API文档自动生成
- 错误处理和日志记录

## 采购管理实践

### 技术选型决策
- **FastAPI vs Django**: 选择FastAPI因其现代化、高性能、自动API文档生成
- **JSON文件 vs 数据库**: 选择JSON文件简化部署，适合演示项目
- **Pydantic**: 数据验证和序列化，提高代码质量

### 工具和服务采购
- **开发工具**: Python, VS Code, Git
- **部署平台**: 本地部署，可扩展到云平台
- **监控工具**: 内置健康检查端点

## 开发进度

### 已完成功能
- [x] FastAPI后端架构搭建
- [x] Pydantic数据模型定义
- [x] 图书管理完整CRUD操作
- [x] 用户管理完整CRUD操作
- [x] 借阅记录管理
- [x] 统计信息API
- [x] 前端界面和交互
- [x] JSON文件数据持久化
- [x] API文档自动生成

### 待优化功能
- [ ] 用户认证和授权
- [ ] 数据备份机制
- [ ] 邮件通知功能
- [ ] 高级搜索功能
- [ ] 批量操作功能

## 许可证

本项目仅用于ISYS3001课程演示，不用于商业用途。

---

**ISYS3001 Managing Software Development Assignment**  
**Student 2 - Library Management System**  
**Technology Stack: Python FastAPI + HTML/CSS/JavaScript**