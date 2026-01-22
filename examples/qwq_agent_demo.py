"""
简单的langchain-qwq智能体demo
使用QwQ-32B模型
"""
from langchain_qwq import ChatQwQ
from langchain_core.prompts import ChatPromptTemplate

def main():
    print("初始化QwQ-32B模型...")
    print("Base URL: http://192.168.20.68:3000/v1/")
    print("Model: QwQ-32B")

    # 创建prompt模板
    prompt = ChatPromptTemplate.from_template("请回答以下问题：{question}")

    # 初始化QwQ模型
    model = ChatQwQ(
        base_url="http://192.168.20.68:3000/v1/",
        model="QwQ-32B",
        api_key="your-api-key",  # 可以使用任意值，因为这是本地部署的服务器
    )

    # 创建简单的链
    chain = prompt | model

    # 测试问题
    questions = [
        "什么是Python的列表推导式？",
        "用Python写一个快速排序算法",
        "解释一下REST API的概念"
    ]

    for q in questions:
        print(f"\n{'='*50}")
        print(f"问题: {q}")
        print(f"{'='*50}")
        response = chain.invoke({"question": q})
        print(f"回答: {response}")

    print("\n" + "="*50)
    print("演示完成！")

if __name__ == "__main__":
    main()
