from fastapi import FastAPI,HTTPException
from datetime import datetime

from jobs.script.scheduler import ScriptScheduler

# Cấu hình logging
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI(title="FastAPI Cronjob Example")

script_scheduler = ScriptScheduler()

@app.on_event("startup")
async def startup_event():
    """Khởi tạo scheduler khi ứng dụng khởi động"""

    # Thêm các scripts cần thực thi
    script_scheduler.add_script("C:/Users/hieunk/Documents/fastapi_cronjob/scripts_job/test.bat", "1 * * * *",run_immediately=True) 
    script_scheduler.add_script("scripts/weekly_backup.py", "0 0 * * 0")  # Chạy lúc 0:00 mỗi Chủ nhật
    script_scheduler.add_script("scripts/monthly_cleanup.py", "0 0 1 * *")  # Chạy lúc 0:00 ngày 1 mỗi tháng

    # Khởi động các scheduler

    script_scheduler.start()
    logger.info("Tất cả scheduler đã được khởi động")

@app.on_event("shutdown")
async def shutdown_event():
    """Dừng scheduler khi ứng dụng tắt"""

    script_scheduler.shutdown()
    logger.info("Tất cả scheduler đã được dừng")

@app.get("/")
async def root():
    """Endpoint chính của ứng dụng"""
    return {"message": "FastAPI Cronjob Example"}


# Script Scheduler Endpoints
@app.get("/scripts")
async def list_scripts():
    """Liệt kê tất cả các scripts đang chạy"""
    return {"scripts": script_scheduler.get_all_scripts()}
@app.get("/scripts/{script_path:path}")
async def get_script_info(script_path: str):
    try:
        job_info = script_scheduler.get_script_info(script_path)
        return job_info
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
@app.post("/scripts/{script_path:path}")
async def add_script(script_path: str, schedule: str):
    """Thêm một script cần thực thi
    Args:
        script_path: Đường dẫn đến file Python
        schedule: Lịch chạy theo định dạng cron (ví dụ: "0 8 * * *" cho 8:00 mỗi ngày)
    """
    script_scheduler.add_script(script_path, schedule)
    return {"message": f"Đã thêm script {script_path} vào scheduler"}

@app.delete("/scripts/{script_path:path}")
async def remove_script(script_path: str):
    """Xóa một script khỏi scheduler"""
    script_scheduler.remove_script(script_path)
    return {"message": f"Đã xóa script {script_path} khỏi scheduler"}

@app.put("/scripts/{script_path:path}")
async def update_script_schedule(script_path: str, schedule: str):
    """Cập nhật lịch chạy của một script"""
    script_scheduler.update_script_schedule(script_path, schedule)
    return {"message": f"Đã cập nhật lịch chạy cho script {script_path}"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001) 