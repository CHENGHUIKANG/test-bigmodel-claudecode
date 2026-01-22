"""
最简单的langchain-qwq智能体demo
使用QwQ-32B模型
"""
from langchain_qwq import ChatQwQ

def main():
    print("=== QwQ-32B 智能体 Demo ===")
    print(f"Base URL: http://192.168.20.68:3000/v1/")
    print(f"Model: QwQ-32B")
    print()

    # 初始化QwQ模型
    model = ChatQwQ(
        base_url="http://192.168.20.68:3000/v1/",
        model="QwQ-32B",
        api_key="your-api-key",
        temperature=0.7,
    )

    # 测试问题
    question = "你好，请用一句话介绍一下Python"

    print(f"问题: {question}")
    print("-" * 50)

    try:
        # 获取回答
        response = model.invoke(question)

        # 直接输出响应内容
        if hasattr(response, 'content'):
            print(f"回答: {response.content}")
        else:
            print(f"回答: {response}")

        print("\n=== Demo 成功完成 ===")

    except Exception as e:
        print(f"发生错误: {e}")

if __name__ == "__main__":
    main()