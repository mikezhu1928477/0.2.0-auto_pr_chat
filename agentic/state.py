from tkinter import YES
from typing import Annotated, TypedDict
from typing import Dict, Any


class State(TypedDict):
    #博主基础信息
    task_informations: Dict[str, Any]

    #ai媒介任务
    task: Dict[str, Any]

    #逻辑控制
    settings: Dict[str, Any]


class TestStateInstance(TypedDict):#可以在这里改值
    #命名规范
    #task_ 跟任务有关的所有
    #creator_ 跟博主/达人有关的所有
    #node_ 跟节点切换有关的所有

    task_informations= {
        "creator_name": "测试博主",
    }
    task = [
    {   # [0] ai媒介
        "maximum_price": "1000",
        "collab_type": "单推",
        "delivery_type": "送拍",
        "video_type": "",
        "schedule": "2月15日", 
        "product": "产品A - 护肤套装",
    },
    {   # [1] 真人
        "maximum_price": "",
        "collab_type": "",
        "delivery_type": "",
        "video_type": "",
        "schedule": "",
        "product": "",
    }]

    settings = {
        "openai_previous_id": None,#openai的历史id
        "node_change": YES, #改stage的时候这里变
        "node_current": "", #进哪个stage
        "creator_latest_response": "" ,#放进input的达人的一串话
        "ai_latest_response": "", #ai媒介的最新回复
        "creator_id": "", #博主唯一标识
        "classification": "", #分类结果: CONTINUE, RETRY, END, QUESTION
    }
