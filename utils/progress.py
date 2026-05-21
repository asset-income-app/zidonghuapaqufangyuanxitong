from tqdm import tqdm
from typing import Iterator, Any
import time


class ProgressBar:
    def __init__(self, total: int, desc: str = "Processing"):
        self.pbar = tqdm(total=total, desc=desc, unit="项", ncols=100)

    def update(self, n: int = 1):
        self.pbar.update(n)

    def set_description(self, desc: str):
        self.pbar.set_description(desc)

    def close(self):
        self.pbar.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


class TaskProgress:
    def __init__(self):
        self.tasks = {}
        self.current_task = None

    def start_task(self, task_name: str, total: int):
        self.tasks[task_name] = {
            'total': total,
            'completed': 0,
            'start_time': time.time(),
            'pbar': tqdm(total=total, desc=task_name, unit="项", ncols=100)
        }
        self.current_task = task_name

    def update(self, task_name: str, n: int = 1):
        if task_name in self.tasks:
            self.tasks[task_name]['completed'] += n
            self.tasks[task_name]['pbar'].update(n)

    def complete_task(self, task_name: str):
        if task_name in self.tasks:
            self.tasks[task_name]['pbar'].close()
            elapsed = time.time() - self.tasks[task_name]['start_time']
            print(f"\n✅ {task_name} 完成！耗时: {elapsed:.2f}秒")

    def get_progress(self, task_name: str) -> dict:
        if task_name in self.tasks:
            task = self.tasks[task_name]
            return {
                'total': task['total'],
                'completed': task['completed'],
                'percentage': (task['completed'] / task['total'] * 100) if task['total'] > 0 else 0,
                'elapsed': time.time() - task['start_time']
            }
        return {}
