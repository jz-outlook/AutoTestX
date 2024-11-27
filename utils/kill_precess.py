import os
import signal
import psutil  # 需要安装 psutil: pip install psutil


def kill_process_by_name(name):
    """通过进程名杀死相关进程"""
    for proc in psutil.process_iter(['pid', 'name']):
        if name.lower() in proc.info['name'].lower():
            try:
                os.kill(proc.info['pid'], signal.SIGTERM)
                print(f"已终止进程: {proc.info['name']} (PID: {proc.info['pid']})")
            except Exception as e:
                print(f"无法终止进程 {proc.info['name']} (PID: {proc.info['pid']}): {e}")