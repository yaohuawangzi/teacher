from model.task import Task
from typing import List, Dict, Set
import asyncio
import time
class TaskManager:
    def __init__(self):
        pass

    # 模拟 Agent 执行函数（实际场景中替换为真实的 Agent 调用逻辑）
    async def execute_agent_task(self, task: Task) -> Dict:
        """
        模拟执行单个 Agent 任务
        :param task: 任务字典，包含 task_id/agent_id/original_query 等
        :return: 执行结果
        """
        print(f"开始执行任务 {task.task_id} (Agent: {task.agent_id}) - {task.original_query}")
        # 模拟 Agent 执行耗时（实际场景替换为调用 Agent 的 API）
        await asyncio.sleep(2)  # 假设每个任务执行 2 秒
        result = {
            "task_id": task.task_id,
            "agent_id": task.agent_id,
            "status": "success",
            "result": f"任务 {task.task_id} 执行完成",
            "execution_time": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        print(f"完成执行任务 {task.task_id} (Agent: {task.agent_id})")
        return result

    async def schedule_tasks(self, tasks: List[Task]) -> List[Dict]:
        """
        任务调度核心逻辑：
        1. 先执行所有无依赖的任务（并行）
        2. 依赖任务等待其依赖的任务执行完成后再执行
        3. 全程异步并行，最大化执行效率
        """
        # 1. 预处理任务：建立 task_id 到任务的映射，方便快速查找
        task_map = {task.task_id: task for task in tasks}
        # 2. 记录已完成的任务 ID
        completed_tasks: Set[str] = set()
        # 3. 存储所有任务的执行结果
        task_results: List[Dict] = []
        # 4. 待执行的任务队列（异步任务对象）
        pending_tasks = []

        # 第一步：执行所有无依赖的任务（并行）
        for task in tasks:
            if not task.dependencies:
                # 创建异步任务并加入队列
                pending_task = asyncio.create_task(self.execute_agent_task(task))
                # 绑定 task_id，方便后续关联结果
                pending_task.task_id = task.task_id
                pending_tasks.append(pending_task)

        # 等待第一批无依赖任务完成
        while pending_tasks:
            # 等待任意一个任务完成
            done, pending_tasks = await asyncio.wait(pending_tasks, return_when=asyncio.FIRST_COMPLETED)
            for done_task in done:
                # 获取任务结果并保存
                result = await done_task
                task_results.append(result)
                completed_tasks.add(done_task.task_id)
                print(f"✅ 任务 {done_task.task_id} 已完成，已完成列表：{completed_tasks}")

        # 第二步：处理有依赖的任务（检查依赖是否完成，完成后执行）
        # 筛选出有依赖但未执行的任务
        dependent_tasks = [t for t in tasks if t.dependencies and t.task_id not in completed_tasks]
        while dependent_tasks:
            for task in dependent_tasks.copy():  # 遍历副本，避免修改原列表
                # 检查当前任务的所有依赖是否都已完成
                if all(dep in completed_tasks for dep in task.dependencies):
                    print(f"🔗 任务 {task.task_id} 的依赖 {task.dependencies} 已完成，开始执行")
                    # 执行当前依赖任务
                    result = await self.execute_agent_task(task)
                    task_results.append(result)
                    completed_tasks.add(task.task_id)
                    # 从待处理列表中移除
                    dependent_tasks.remove(task)
                    print(f"✅ 任务 {task.task_id} 已完成，已完成列表：{completed_tasks}")
            # 避免空循环（如果还有未满足依赖的任务，短暂等待后重试）
            if dependent_tasks:
                await asyncio.sleep(0.1)

        return task_results