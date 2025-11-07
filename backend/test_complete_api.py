#!/usr/bin/env python3
"""
完整的API测试脚本
"""

import requests
import json
import io
import pandas as pd

# API基础URL
BASE_URL = "http://localhost:8000"

def test_health():
    """测试健康检查"""
    print("1. 测试健康检查...")
    response = requests.get(f"{BASE_URL}/health")
    if response.status_code == 200:
        print("✅ 服务器运行正常")
        print(f"   {response.json()}")
        return True
    else:
        print(f"❌ 健康检查失败: {response.status_code}")
        return False

def test_upload():
    """测试文件上传"""
    print("\n2. 测试文件上传...")

    # 创建测试数据
    test_data = {
        "产品名称": ["iPhone 15", "MacBook Pro", "iPad Air", "AirPods", "Apple Watch"],
        "销售额": [1200000, 2400000, 800000, 400000, 600000],
        "数量": [1200, 600, 800, 2000, 1500],
        "类别": ["电子产品", "电子产品", "电子产品", "配件", "电子产品"]
    }
    df = pd.DataFrame(test_data)

    # 转换为CSV
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    csv_content = csv_buffer.getvalue().encode('utf-8')

    # 上传文件
    files = {"file": ("test_products.csv", csv_content, "text/csv")}
    response = requests.post(f"{BASE_URL}/upload", files=files)

    if response.status_code == 200:
        result = response.json()
        print("✅ 文件上传成功")
        print(f"   文件ID: {result['file_id']}")
        print(f"   列数: {result['total_columns']}")
        print(f"   列名: {result['headers']}")
        return result['file_id']
    else:
        print(f"❌ 文件上传失败: {response.text}")
        return None

def test_query(file_id):
    """测试数据查询"""
    print("\n3. 测试数据查询...")

    queries = [
        "显示前3条数据",
        "统计各类别的产品数量",
        "计算总销售额"
    ]

    for query in queries:
        print(f"\n   查询: {query}")
        response = requests.post(
            f"{BASE_URL}/query",
            json={"query": query, "file_id": file_id}
        )

        if response.status_code == 200:
            result = response.json()
            print("   ✅ 查询成功")
            print(f"   回答: {result['answer'][:100]}...")
            print(f"   返回行数: {result.get('returned_rows', 0)}")
        else:
            print(f"   ❌ 查询失败: {response.text}")

def test_chat(file_id):
    """测试对话功能"""
    print("\n4. 测试对话功能...")

    messages = [
        "你好",
        "这些数据有多少行？",
        "请分析一下销售额情况"
    ]

    session_id = None

    for msg in messages:
        print(f"\n   用户: {msg}")
        request_data = {
            "message": msg,
            "file_id": file_id
        }
        if session_id:
            request_data["session_id"] = session_id

        response = requests.post(
            f"{BASE_URL}/chat",
            json=request_data
        )

        if response.status_code == 200:
            result = response.json()
            print(f"   助手: {result['message'][:100]}...")
            session_id = result.get('session_id')
        else:
            print(f"   ❌ 对话失败: {response.text}")

def test_visualize(file_id):
    """测试可视化功能"""
    print("\n5. 测试可视化功能...")

    response = requests.post(
        f"{BASE_URL}/visualize",
        json={
            "file_id": file_id,
            "chart_type": "bar",
            "x_column": "产品名称",
            "y_column": "销售额",
            "title": "产品销售额对比"
        }
    )

    if response.status_code == 200:
        result = response.json()
        print("✅ 可视化创建成功")
        print(f"   HTML长度: {len(result.get('chart_html', ''))}")
    else:
        print(f"❌ 可视化创建失败: {response.text}")

def test_files():
    """测试文件列表"""
    print("\n6. 测试文件列表...")

    response = requests.get(f"{BASE_URL}/files")

    if response.status_code == 200:
        result = response.json()
        print(f"✅ 获取文件列表成功，共{len(result['files'])}个文件")
        for f in result['files']:
            print(f"   - {f['filename']} ({f['file_id'][:8]}...)")
    else:
        print(f"❌ 获取文件列表失败: {response.text}")

def main():
    """运行所有测试"""
    print("====================================")
    print("SQL Agent API 完整测试")
    print("====================================")

    # 测试健康检查
    if not test_health():
        print("\n❌ 测试失败：服务器未运行")
        return

    # 测试文件上传
    file_id = test_upload()
    if not file_id:
        print("\n❌ 测试失败：文件上传失败")
        return

    # 测试查询
    test_query(file_id)

    # 测试对话
    test_chat(file_id)

    # 测试可视化
    test_visualize(file_id)

    # 测试文件列表
    test_files()

    print("\n====================================")
    print("✅ 所有测试完成！")
    print("====================================")
    print("\n前端测试页面: http://localhost:5173/test_frontend.html")
    print("API文档: http://localhost:8000/docs")

if __name__ == "__main__":
    main()