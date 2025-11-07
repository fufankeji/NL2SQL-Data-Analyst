<div align="center">
  <h1>🚀 基于 LangChain 的 NL2SQL 数据分析系统</h1>
  <p><em>让数据分析像聊天一样简单</em></p>
  <span>中文 | <a href="./README.md">English</a></span>
</div>

## ⚡ 项目简介

本项目是一个基于 **LangChain 1.0** 的 NL2SQL 数据分析系统，采用 FastAPI + React 构建。

你可以用自然语言对 数据库 或 上传的 CSV/Excel 数据进行查询、统计与可视化，无需编写 SQL，即可获得图表与结果。


## 🎯 主要功能

### 🔍 数据处理与建库
- 支持批量上传 .csv / .excel 文件，自动解析入库，并能够基于文件内容进行数据检索、可视化绘图及输出详细的数据分析报告
- 自动提取列头、预估行数等基础元信息，辅助快速探索
<div align="center"><img src="./assets//202511051102538.png" width="80%"></div>

### 🤖 自然语言查询（NL2SQL）
- 集成 LangChain SQL Agent，将自然语言自动转换为 SQL 查询
- 支持连接本地/云端的数据库，并选择数据库中的表，进行自然语言提问
<div align="center"><img src="./assets/202511051056094.png" width="80%"></div>

### 📈 数据可视化
- 可以选择单表、多表的自动数据分析，实时生成查询 SQL，并自动进行查询，同时还能基于查询结果进行可视化图表的生成
<div align="center"><img src="./assets/202511051059056.png" width="80%"></div>

## 🎥 项目演示


https://github.com/user-attachments/assets/09b43c6a-d10f-4d62-8f04-edb69d25c6bb


## 📁 项目结构

```
├── backend/                 # 后端（FastAPI + LangChain）
│   ├── app/                 # 应用核心（路由、Agent、可视化等）
│   ├── data/                # 数据目录（上传与可视化输出）
│   ├── requirements.txt     # Python 依赖
│   ├── api_with_db.py       # 启动脚本（带临时库）
│   └── .env                 # 环境变量文件（建议放此处）
|   └── ...
├── frontend/                # 前端（React + Vite）
│   ├── src/                 # 页面与组件
│   └── package.json         # Node 项目配置
|   └── ...
└── README.md  
```



## 🚀 快速开始


### 1. 配置环境变量（`.env` 文件）

在 `backend/.env` 中完善以下配置：

```
OPENAI_API_KEY=sk-your-api-key
OPENAI_BASE_URL=https://api.openai.com/v1
DEFAULT_MODEL=gpt-4o-mini
```

### 2. 启动后端服务

```bash
# 1. 进入后端目录
cd backend

# 2. 创建并激活虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows

# 3. 安装依赖
pip install -r requirements.txt

# 4. 启动服务
python api_with_db.py
```



### 3. 启动前端服务

```bash
# 1. 进入前端目录
cd frontend

# 2. 安装依赖
npm install

# 3. 启动开发服务器
npm run dev
```





## 🙈 贡献
欢迎通过GitHub提交 PR 或者issues来对项目进行贡献。我们非常欢迎任何形式的贡献，包括功能改进、bug修复或是文档优化。

## 😎 技术交流
探索我们的技术社区 👉 [大模型技术社区丨赋范空间](https://kq4b3vgg5b.feishu.cn/wiki/JuJSwfbwmiwvbqkiQ7LcN1N1nhd)

扫描添加小可爱，回复“NL2SQL”加入技术交流群，与其他小伙伴一起交流学习。
<div align="center">
<img src="assets\交流群.jpg" width="200" alt="技术交流群二维码">
<div>



