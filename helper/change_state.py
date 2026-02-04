#之后会出现state["chat_messages"][1] 里面记录《人》和《ai媒介》对话，
# 有可能人类连续发了5条，然后人工智能发了1条这样的，需要的格式类似
#人： ['h:hi','ai:你好，可以麻烦发一下你的主页链接和最新的报价吗？谢谢！','h:ko', 'ai:你好，方便发一下你的主页链接和报价吗？谢谢！','h:ko']

#需要把h: 这样的加上
def state_add_message(state, message, sender="h"):
    """
    添加消息到state的chat_messages列表
    
    Args:
        state: 状态字典
        message: 消息内容
        sender: 发送者标识，"h" 代表人类，"ai" 代表AI媒介
    
    Returns:
        更新后的state
    """
    if "chat_messages" not in state:
        state["chat_messages"] = []
    
    formatted_message = f"{sender}:{message}"
    state["chat_messages"].append(formatted_message)
    
    return state
