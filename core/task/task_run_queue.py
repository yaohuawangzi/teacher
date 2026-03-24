# 消息队列拉取执行
# from model.task import Task, TaskStatus
# import time
#
#
# class TaskManager:
#     def __init__(self):
#         self.task_map = {}  # 存储所有任务：{task_id: Task}
#         self.pending_queue = []  # 待执行任务队列
#         self.running_tasks = set()  # 执行中任务ID
#
#     # 入队：添加任务并校验依赖
#     def enqueue_task(self, task: Task):
#         self.task_map[task.task_id] = task
#         # 无依赖的任务直接加入待执行队列
#         if not task.dependencies:
#             self.pending_queue.append(task)
#         print(f"任务 {task.task_id} 入队，状态：{task.status}")
#
#     # 调度：检查依赖并触发执行
#     async def schedule(self):
#         # 筛选出依赖已完成的任务
#         ready_tasks = []
#         for task in self.pending_queue:
#             if task.status != TaskStatus.PENDING:
#                 continue
#             # 校验所有依赖任务是否成功
#             all_deps_succeeded = all(
#                 self.task_map.get(dep, None) and self.task_map[dep].status == TaskStatus.SUCCEEDED
#                 for dep in task.dependencies or []
#             )
#             if all_deps_succeeded:
#                 ready_tasks.append(task)
#
#         # 执行就绪任务（并行）
#         for task in ready_tasks:
#             self.pending_queue.remove(task)
#             self.running_tasks.add(task.task_id)
#             task.status = TaskStatus.RUNNING
#             task.start_time = time.time()
#             # 调用Agent执行任务
#             await self.execute_task(task)