def encouragement_generator(name, mood):
    # 基础鼓励消息
    messages = {
        "happy": "继续保持积极的心态，做得好！",
        "sad": "记住，即使在最黑暗的日子里，也会有阳光等待着你。",
        "tired": "你做得足够好了，现在是时候休息一下了。",
        "stressed": "深呼吸，一切都会好起来的。"
    }
    
    # 获取对应心情的鼓励消息
    message = messages.get(mood.lower(), "你今天感觉如何？我总是在这里支持你！")
    
    # 返回定制化的鼓励消息
    return f"亲爱的{name}，{message}"

# 使用示例
print(encouragement_generator("Alice", "tired"))
