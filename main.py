from graph import graph
from agentic.state import TestStateInstance

if __name__ == "__main__":
    result = graph.invoke({
        "task_informations": TestStateInstance.task_informations,
        "task": TestStateInstance.task,
        "settings": TestStateInstance.settings,
    }, {"recursion_limit": 999999999999})

    print(result)