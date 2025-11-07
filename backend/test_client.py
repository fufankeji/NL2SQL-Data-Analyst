#!/usr/bin/env python3
"""
测试后端API功能的客户端脚本
"""

import requests
import json
import pandas as pd
import io

# API基础URL
BASE_URL = "http://localhost:8000"

def test_api():
    """测试API功能"""
    print("🚀 开始测试 SQL Agent API...")

    # 1. 测试健康检查
    print("\n1. 测试健康检查...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ 服务器运行正常")
            print(f"   {response.json()}")
        else:
            print("❌ 服务器未运行，请先启动后端服务")
            return
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到服务器，请确保后端服务已启动")
        print("   运行命令: python run.py")
        return

    # 2. 创建测试数据
    print("\n2. 创建测试数据...")
    test_data = {
        "产品名称": ["产品A", "产品B", "产品C", "产品D", "产品E"],
        "销售额": [10000, 15000, 8000, 20000, 12000],
        "数量": [100, 150, 80, 200, 120],
        "类别": ["电子", "电子", "家居", "电子", "家居"],
        "日期": ["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04", "2024-01-05"]
    }
    df = pd.DataFrame(test_data)

    # 转换为CSV
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    csv_content = csv_buffer.getvalue().encode('utf-8')

    # 3. 测试文件上传
    print("\n3. 测试文件上传...")
    files = {"file": ("test_data.csv", csv_content, "text/csv")}
    response = requests.post(f"{BASE_URL}/upload", files=files)

    if response.status_code == 200:
        upload_result = response.json()
        file_id = upload_result["file_id"]
        print(f"✅ 文件上传成功")
        print(f"   文件ID: {file_id}")
        print(f"   列数: {upload_result['total_columns']}")
        print(f"   列名: {upload_result['headers']}")
    else:
        print(f"❌ 文件上传失败: {response.text}")
        return

    # 4. 测试自然语言查询
    print("\n4. 测试自然语言查询...")
    queries = [
        "显示销售额最高的3个产品",
        "计算每个类别的总销售额",
        "平均销售额是多少？"
    ]

    for query in queries:
        print(f"\n   查询: {query}")
        query_data = {
            "query": query,
            "file_id": file_id
        }

        response = requests.post(
            f"{BASE_URL}/query",
            json=query_data,
            headers={"Content-Type": "application/json"}
        )

        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ 查询成功")
            print(f"   回答: {result['answer'][:200]}...")
        else:
            print(f"   ❌ 查询失败: {response.text}")

    # 5. 测试可视化
    print("\n5. 测试数据可视化...")
    viz_data = {
        "file_id": file_id,
        "chart_type": "bar",
        "x_column": "产品名称",
        "y_column": "销售额",
        "title": "产品销售额对比"
    }

    response = requests.post(
        f"{BASE_URL}/visualize",
        json=viz_data,
        headers={"Content-Type": "application/json"}
    )

    if response.status_code == 200:
        print("✅ 可视化创建成功")
        print("   图表HTML已生成")
    else:
        print(f"❌ 可视化创建失败: {response.text}")

    # 6. 测试对话功能
    print("\n6. 测试对话功能...")
    chat_data = {
        "message": "请帮我分析这个销售数据，哪个产品表现最好？",
        "file_id": file_id
    }

    response = requests.post(
        f"{BASE_URL}/chat",
        json=chat_data,
        headers={"Content-Type": "application/json"}
    )

    if response.status_code == 200:
        result = response.json()
        print("✅ 对话成功")
        print(f"   会话ID: {result['session_id']}")
        print(f"   回答: {result['message'][:200]}...")

        # 继续对话
        follow_up = {
            "message": "那么各类别的销售额分别是多少？",
            "session_id": result["session_id"]
        }

        response = requests.post(
            f"{BASE_URL}/chat",
            json=follow_up,
            headers={"Content-Type": "application/json"}
        )

        if response.status_code == 200:
            result = response.json()
            print("✅ 对话继续成功")
            print(f"   回答: {result['message'][:200]}...")

    # 7. 查看文件列表
    print("\n7. 查看文件列表...")
    response = requests.get(f"{BASE_URL}/files")

    if response.status_code == 200:
        files = response.json()["files"]
        print(f"✅ 共有 {len(files)} 个文件")
        for f in files:
            print(f"   - {f['filename']} ({f['file_id']})")

    print("\n✅ API测试完成！")

if __name__ == "__main__":
    test_api()