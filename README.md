# 智慧农业病害检测与防治系统

基于 YOLOv11 与 LLM 的农作物病虫害检测与防治系统。

## 功能特性

- 🔍 智能病害检测（YOLO + CNN）
- 📊 数据看板与统计分析
- 💊 智能治疗方案推荐
- 📈 效果评估与追踪
- 📚 知识库管理
- 👥 用户权限管理

## 技术栈

### 后端
- FastAPI
- SQLAlchemy
- PyTorch
- Ultralytics YOLO
- Transformers

### 前端
- Vue 3
- TypeScript
- Vite
- Pinia
- ECharts
- TailwindCSS

## 快速开始

### 前置要求

- Python 3.10+
- Node.js 18+
- CUDA (可选，用于 GPU 加速)

### 1. 克隆项目

```bash
git clone https://github.com/amy7445/amy.git
cd amy
```

### 2. 后端设置

```bash
# 创建虚拟环境
cd backend
python -m venv .venv

# 激活虚拟环境
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 3. 下载模型文件

由于模型文件较大，需要单独下载：

**必需的模型文件：**
- `yolov8n.pt` - 下载到 `backend/` 目录
- `best_cnn_v2.pth` - 下载到 `backend/models/` 目录
- `best_treatment_model.pth` - 下载到 `backend/models/` 目录
- `best_evaluation_model.pth` - 下载到 `backend/models/` 目录

模型文件下载链接：
- YOLOv8n: https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt
- 其他模型请联系项目维护者

### 4. 前端设置

```bash
# 返回项目根目录
cd ..

# 安装依赖
cd frontend
npm install
```

### 5. 启动项目

**启动后端：**
```bash
cd backend
.venv\Scripts\activate  # Windows
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**启动前端：**
```bash
# 新开一个终端
cd frontend
npm run dev
```

### 6. 访问应用

- 前端地址：http://localhost:5173
- 后端 API：http://localhost:8000
- API 文档：http://localhost:8000/docs

### 7. 默认账号

- 用户名：`admin`
- 密码：`admin`

## 项目结构

```
amy/
├── backend/              # 后端代码
│   ├── app/
│   │   ├── api/         # API 路由
│   │   ├── core/        # 核心配置
│   │   ├── ml/          # 机器学习模型
│   │   └── models/      # 数据模型
│   ├── models/          # 模型文件目录
│   └── requirements.txt # Python 依赖
├── frontend/            # 前端代码
│   ├── src/
│   │   ├── components/  # Vue 组件
│   │   ├── pages/       # 页面
│   │   ├── stores/      # Pinia 状态管理
│   │   └── api/         # API 配置
│   └── package.json     # Node 依赖
└── .gitignore          # Git 忽略配置
```

## 开发说明

### 后端开发

```bash
cd backend
.venv\Scripts\activate
uvicorn app.main:app --reload
```

### 前端开发

```bash
cd frontend
npm run dev
```

### 构建生产版本

```bash
# 前端构建
cd frontend
npm run build

# 后端部署
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## 常见问题

### 1. 模型文件缺失

如果启动时提示模型文件缺失，请确保已下载所有必需的模型文件到正确位置。

### 2. 数据库初始化

数据库会在首次运行时自动创建，默认管理员账号为 `admin/admin`。

### 3. 依赖安装失败

如果 pip 安装失败，尝试使用国内镜像：

```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

## 许可证

MIT License

## 联系方式

如有问题，请提交 Issue 或联系项目维护者。