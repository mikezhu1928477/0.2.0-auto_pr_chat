from typing import Annotated, TypedDict
from typing import Dict, Any


class State(TypedDict):
    #博主基础信息
    task_informations: Dict[str, Any]

    #ai媒介任务
    task: Dict[str, Any]

    #逻辑控制
    settings: Dict[str, Any]


class TestStateInstance(TypedDict):#上一个api需传输
    #命名规范
    #task_ 跟任务有关的所有
    #creator_ 跟博主/达人有关的所有
    #node_ 跟节点切换有关的所有

    task_informations= {
        "creator_name": "测试博主",
    }
    task = [
    {   # [0] ai媒介 预期
        "maximum_price": "1000",
        "collab_type": "单推",
        "delivery_type": "送拍",
        "video_type": "",
        "schedule": "", 
        "product": "",
    },
    {   # [1] 真人 真实offer
        "maximum_price": "",
        "collab_type": "",
        "delivery_type": "",
        "video_type": "",
        "schedule": "",
        "product": "",
    }]

    settings = {
        "openai_previous_id": None,#openai的历史id
        "node_change": False, #改stage的时候这里变
        "node_current": "greet_run", #进哪个stage
        "creator_latest_response": "(你已经加上了博主)" ,#放进input的达人的一串话
    }
