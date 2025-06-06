from abc import ABC, abstractmethod
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class BaseJob(ABC):
    def __init__(self, job_id: str):
        self.job_id = job_id
        self.last_run = None

    @abstractmethod
    def execute(self):
        """Phương thức thực thi job, cần được implement bởi các class con"""
        pass

    def run(self):
        """Phương thức chạy job và ghi log"""
        try:
            self.execute()
            self.last_run = datetime.now()
            logger.info(f"Job {self.job_id} đã chạy thành công tại {self.last_run}")
        except Exception as e:
            logger.error(f"Job {self.job_id} gặp lỗi: {str(e)}")
            raise 