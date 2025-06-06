from ..base_job import BaseJob
import subprocess
import logging
import os
from datetime import datetime
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)
logger = logging.getLogger(__name__)

class ScriptJob(BaseJob):
    """Job thực thi file Python hoặc Shell script"""
    def __init__(self, script_path: str):
        super().__init__(f"script_{os.path.basename(script_path)}")
        self.script_path = script_path
        self.script_type = self._get_script_type()
        self.last_run = None
        self.last_status = None
        self.last_output = None
        self.last_error = None
    def _get_script_type(self):
        """Xác định loại script dựa vào phần mở rộng"""
        ext = os.path.splitext(self.script_path)[1].lower()
        if ext == '.py':
            return 'python'
        elif ext == '.sh':
            return 'sh'
        elif ext == '.bat':
            return 'bat'
        else:
            raise ValueError(f"Không hỗ trợ loại file {ext}")

    def execute(self):
        """Thực thi file script"""
        try:
            # Kiểm tra file có tồn tại không
            if not os.path.exists(self.script_path):
                raise FileNotFoundError(f"Không tìm thấy file {self.script_path}")

            # Thực thi script dựa vào loại
            if self.script_type == 'python':
                result = subprocess.run(
                    ["python", self.script_path],
                    capture_output=True,
                    text=True,
                    check=True
                )
            elif self.script_type == 'bat':  # shell script
                result = subprocess.run(
                    [self.script_path],
                    capture_output=True,
                    text=True,
                    check=True,
                    shell=True
                )
            
            elif self.script_type == 'bat':  # shell script
                # Đảm bảo file có quyền thực thi
                os.chmod(self.script_path, 0o755)
                result = subprocess.run(
                    [self.script_path],
                    capture_output=True,
                    text=True,
                    check=True,
                    shell=True
                )
            self.last_status = "success"
            self.last_output = result.stdout
            self.last_error = result.stderr
            # Log kết quả
            if result.stdout:
                logger.info(f"Output của script {self.script_path}:\n{result.stdout}")
            if result.stderr:
                logger.warning(f"Warning của script {self.script_path}:\n{result.stderr}")
            self.last_run = datetime.now()
        except subprocess.CalledProcessError as e:
            self.last_run = datetime.now()
            self.last_status = "failed"
            self.last_output = e.stdout
            self.last_error = e.stderr
            logger.error(f"Script {self.script_path} thực thi thất bại: {e.stderr}")
            
        except Exception as e:
            self.last_run = datetime.now()
            self.last_status = "failed"
            self.last_output = str(e)
            
            logger.error(f"Lỗi khi thực thi script {self.script_path}: {str(e)}")
             