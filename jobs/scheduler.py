from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)
logger = logging.getLogger(__name__)

class JobScheduler:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.jobs = {}

    def add_job(self, job, trigger, **kwargs):
        """Thêm một job vào scheduler"""
        job_id = job.job_id
        self.jobs[job_id] = job
        self.scheduler.add_job(
            job.execute,
            trigger=trigger,
            id=job_id,
            replace_existing=True,
            **kwargs
        )
        logger.info(f"Đã thêm job {job_id} vào scheduler")

    def remove_job(self, job_id):
        """Xóa một job khỏi scheduler"""
        if job_id in self.jobs:
            self.scheduler.remove_job(job_id)
            del self.jobs[job_id]
            logger.info(f"Đã xóa job {job_id} khỏi scheduler")

    def get_job(self, job_id):
        """Lấy thông tin một job"""
        return self.jobs.get(job_id)

    def get_all_jobs(self):
        """Lấy danh sách tất cả các jobs"""
        return list(self.jobs.values())

    def start(self):
        """Khởi động scheduler"""
        self.scheduler.start()
        logger.info("Scheduler đã được khởi động")

    def shutdown(self):
        """Dừng scheduler"""
        self.scheduler.shutdown()
        logger.info("Scheduler đã được dừng") 