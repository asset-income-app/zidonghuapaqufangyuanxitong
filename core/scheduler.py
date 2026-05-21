from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime
import logging

logging.getLogger('apscheduler').setLevel(logging.WARNING)


class TaskScheduler:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()
        self.jobs = {}

    def add_crawl_job(self, job_id: str, cron_expression: str = None, 
                     interval_hours: int = None):
        from main import HouseCrawlerEngine

        def crawl_job():
            print(f"\n[定时任务] 开始执行爬取任务: {datetime.now()}")
            try:
                engine = HouseCrawlerEngine()
                result = engine.run()
                print(f"[定时任务] 爬取完成，共获取 {len(result['dataframe'])} 条房源")
            except Exception as e:
                print(f"[定时任务] 执行失败: {e}")

        if cron_expression:
            parts = cron_expression.split()
            if len(parts) == 5:
                trigger = CronTrigger(
                    minute=parts[0],
                    hour=parts[1],
                    day=parts[2],
                    month=parts[3],
                    day_of_week=parts[4]
                )
            else:
                raise ValueError("Cron表达式格式错误")
        elif interval_hours:
            trigger = IntervalTrigger(hours=interval_hours)
        else:
            raise ValueError("必须提供cron_expression或interval_hours")

        job = self.scheduler.add_job(crawl_job, trigger, id=job_id)
        self.jobs[job_id] = job

        print(f"[定时任务] 已添加任务: {job_id}")
        return job

    def remove_job(self, job_id: str):
        if job_id in self.jobs:
            self.scheduler.remove_job(job_id)
            del self.jobs[job_id]
            print(f"[定时任务] 已移除任务: {job_id}")

    def pause_job(self, job_id: str):
        if job_id in self.jobs:
            self.scheduler.pause_job(job_id)
            print(f"[定时任务] 已暂停任务: {job_id}")

    def resume_job(self, job_id: str):
        if job_id in self.jobs:
            self.scheduler.resume_job(job_id)
            print(f"[定时任务] 已恢复任务: {job_id}")

    def get_jobs(self):
        jobs = []
        for job in self.scheduler.get_jobs():
            jobs.append({
                'id': job.id,
                'next_run_time': str(job.next_run_time),
                'trigger': str(job.trigger)
            })
        return jobs

    def shutdown(self):
        self.scheduler.shutdown()
        print("[定时任务] 调度器已关闭")


scheduler = TaskScheduler()
