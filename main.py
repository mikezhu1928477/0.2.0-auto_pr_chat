import asyncio
from graph import graph
from agentic.state import TestStateInstance

async def main():
    await graph.ainvoke({
        "task_informations": TestStateInstance.task_informations,
        "task": TestStateInstance.task,
        "settings": TestStateInstance.settings,
    }, {"recursion_limit": 999999999999})

if __name__ == "__main__":
    asyncio.run(main())
