#!/usr/bin/env python3
"""
简化的API测试服务器
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import io
import json
import uuid
from typing import Dict, Any

app = FastAPI(title="SQL Agent Test API")

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 存储文件数据
file_store: Dict[str, Dict] = {}

@app.get("/")
async def root():
    return {"message": "SQL Agent Test API is running"}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "files_loaded": len(file_store),
        "active_agents": 0,
        "active_sessions": 0
    }

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """上传文件"""
    try:
        # 读取文件内容
        content = await file.read()

        # 解析CSV或Excel
        if file.filename.endswith('.csv'):
            df = pd.read_csv(io.BytesIO(content))
        else:
            df = pd.read_excel(io.BytesIO(content))

        # 生成文件ID
        file_id = str(uuid.uuid4())

        # 存储文件信息
        file_store[file_id] = {
            "filename": file.filename,
            "data": df.to_dict('records'),
            "columns": df.columns.tolist(),
            "shape": df.shape
        }

        return {
            "success": True,
            "file_id": file_id,
            "message": f"File '{file.filename}' uploaded successfully",
            "headers": df.columns.tolist(),
            "total_columns": len(df.columns),
            "estimated_rows": len(df)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query")
async def query_data(request: Dict[str, Any]):
    """查询数据"""
    try:
        query = request.get("query", "")
        file_id = request.get("file_id")

        if not file_id or file_id not in file_store:
            raise HTTPException(status_code=404, detail="File not found")

        file_info = file_store[file_id]
        data = file_info["data"]

        # 简单的模拟查询响应
        if "前10" in query or "top10" in query.lower():
            result_data = data[:10]
            answer = f"已返回前10条数据，共{len(result_data)}条记录"
        elif "统计" in query or "总数" in query:
            result_data = [{
                "统计项": "总记录数",
                "数值": len(data)
            }]
            answer = f"数据总共有{len(data)}条记录"
        else:
            result_data = data[:5]
            answer = f"根据查询'{query}'，返回相关数据{len(result_data)}条"

        return {
            "success": True,
            "answer": answer,
            "data": result_data,
            "total_rows": len(data),
            "returned_rows": len(result_data),
            "columns": file_info["columns"]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat")
async def chat_with_data(request: Dict[str, Any]):
    """对话功能"""
    try:
        message = request.get("message", "")
        file_id = request.get("file_id")
        session_id = request.get("session_id", str(uuid.uuid4()))

        if not file_id or file_id not in file_store:
            raise HTTPException(status_code=404, detail="File not found")

        file_info = file_store[file_id]
        data = file_info["data"]

        # 模拟对话响应
        if "你好" in message:
            response = "您好！我是您的数据分析助手。请问您想了解这些数据的什么信息？"
        elif "多少" in message or "几" in message:
            response = f"根据您的数据，总共有{len(data)}条记录，包含{len(file_info['columns'])}个字段。"
        elif "分析" in message:
            response = f"数据分析完成。您的数据集包含{len(data)}条记录，主要字段有：{', '.join(file_info['columns'][:5])}等。"
        else:
            response = f"收到您的问题：{message}。基于数据，我为您提供相关分析。"

        return {
            "success": True,
            "message": response,
            "session_id": session_id,
            "data": data[:5]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/visualize")
async def create_visualization(request: Dict[str, Any]):
    """创建可视化"""
    try:
        file_id = request.get("file_id")
        chart_type = request.get("chart_type", "bar")

        if not file_id or file_id not in file_store:
            raise HTTPException(status_code=404, detail="File not found")

        # 返回模拟的HTML图表
        chart_html = f"""
        <div style="padding: 20px; text-align: center;">
            <h3>模拟图表 ({chart_type})</h3>
            <p>这是一个模拟的{chart_type}图表</p>
            <div style="width: 100%; height: 300px; background: #f0f0f0; display: flex; align-items: center; justify-content: center; border-radius: 8px;">
                图表区域 (真实环境会显示实际图表)
            </div>
        </div>
        """

        return {
            "success": True,
            "chart_html": chart_html
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/files")
async def list_files():
    """列出所有文件"""
    files = []
    for file_id, info in file_store.items():
        files.append({
            "file_id": file_id,
            "filename": info["filename"],
            "total_columns": len(info["columns"]),
            "estimated_rows": info["shape"][0]
        })
    return {"files": files}

if __name__ == "__main__":
    import uvicorn
    print("Starting Test API Server on http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)