import utils.llm.doubao_usage

# 测试运行
if __name__ == "__main__":
    doubao_llm = utils.llm.doubao_usage.DoubaoChatModel()
    try:
        res = doubao_llm.invoke([{"role": "user", "content": "你好"}])
        print("✅ 代码运行成功！豆包回复：", res.content)
    except Exception as e:
        print("❌ 运行报错：", e)