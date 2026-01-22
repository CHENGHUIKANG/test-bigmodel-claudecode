"""
增强版的langchain-qwq智能体demo
使用QwQ-32B模型，处理编码问题
"""
import sys
from langchain_qwq import ChatQwQ
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

def safe_print(text):
    """安全打印中文字符"""
    try:
        print(text)
    except UnicodeEncodeError:
        # 如果编码失败，使用encode替换
        print(text.encode('utf-8', 'replace').decode('gbk', 'replace'))

def main():
    print("=== QwQ-32B 智能体 Demo ===")
    print(f"Base URL: http://192.168.20.68:3000/v1/")
    print(f"Model: QwQ-32B")
    print(f"LangChain-QwQ Version: 0.3.4")
    print()

    # 创建prompt模板
    prompt = ChatPromptTemplate.from_template("请用简体中文回答以下问题：{question}")

    # 初始化QwQ模型
    model = ChatQwQ(
        base_url="http://192.168.20.68:3000/v1/",
        model="QwQ-32B",
        api_key="your-api-key",  # 本地服务器，任意值
        temperature=0.7,
        max_tokens=2000,
    )

    # 创建处理链
    def process_response(response):
        """处理模型响应"""
        if hasattr(response, 'content'):
            return response.content
        elif isinstance(response, str):
            return response
        else:
            return str(response)

    chain = (
        {"question": RunnablePassthrough()}
        | prompt
        | model
        | process_response
    )

    # 测试问题列表
    questions = [
        "什么是Python的列表推导式？",
        "用Python写一个快速排序算法",
        "解释一下REST API的概念"
    ]

    try:
        for i, question in enumerate(questions, 1):
            print(f"{'='*50}")
            print(f"问题 {i}: {question}")
            print(f"{'='*50}")

            # 获取回答
            response = chain.invoke(question)
            safe_print(f"\n回答: {response}\n")

            print(f"---")
            print(f"回答完成，继续下一个问题...")
            print()

    except Exception as e:
        print(f"发生错误: {str(e)}")

    print("=== Demo 完成 ===")

if __name__ == "__main__":
    main()