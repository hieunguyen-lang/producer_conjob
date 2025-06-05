from ..scheduler import JobScheduler
from .jobs import ScriptJob
from apscheduler.triggers.cron import CronTrigger
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)
logger = logging.getLogger(__name__)

class ScriptScheduler:
    """Scheduler quản lý các job thực thi script"""
    def __init__(self):
        self.scheduler = JobScheduler()
        self.scripts = {}

    def add_script(self, script_path: str, schedule: str = "0 0 * * *",run_immediately: bool = False):
        """Thêm một script vào scheduler
        Args:
            script_path: Đường dẫn đến file script
            schedule: Lịch chạy theo định dạng cron (mặc định: chạy lúc 00:00 mỗi ngày)
        """
        if script_path in self.scripts:
            logger.warning(f"Script {script_path} đã tồn tại")
            return
        
        # Tạo job thực thi script
        script_job = ScriptJob(script_path)
        if run_immediately:
            script_job.execute()  # 🔥 Chạy ngay
        # Thêm job vào scheduler
        self.scheduler.add_job(
            script_job,
            trigger=CronTrigger.from_crontab(schedule)
        )

        self.scripts[script_path] = script_job
        logger.info(f"Current scripts: {self.scripts.keys()}")

    def remove_script(self, script_path: str):
        """Xóa một script khỏi scheduler"""
        if script_path not in self.scripts:
            logger.warning(f"Script {script_path} không tồn tại")
            return

        self.scheduler.remove_job(self.scripts[script_path].job_id)
        del self.scripts[script_path]
        logger.info(f"Đã xóa script {script_path} khỏi scheduler")

    def update_schedule(self, script_path: str, schedule: str):
        """Cập nhật lịch chạy của một script"""
        if script_path not in self.scripts:
            logger.warning(f"Script {script_path} không tồn tại")
            return

        self.scheduler.remove_job(self.scripts[script_path].job_id)
        self.scheduler.add_job(
            self.scripts[script_path],
            trigger=CronTrigger.from_crontab(schedule)
        )
        logger.info(f"Đã cập nhật lịch chạy cho script {script_path}")

    def start(self):
        """Khởi động scheduler"""
        self.scheduler.start()

    def shutdown(self):
        """Dừng scheduler"""
        self.scheduler.shutdown()

    def get_all_scripts(self):
        """Lấy danh sách tất cả các script đang được lên lịch"""
        return list(self.scripts.keys()) 
    def get_script_info(self, script_path: str):
        """Lấy thông tin chi tiết của một script"""
        # Kiểm tra xem script có tồn tại không
        if script_path not in self.scripts:
            raise ValueError(f"Script {script_path} không tồn tại trong scheduler.")

        script_job = self.scripts.get(script_path)

        # Lấy thông tin về job
        job_info = script_job
        
        return job_info