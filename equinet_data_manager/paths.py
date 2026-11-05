"""
数据文件位置

代码与数据分开：本仓库只放代码，`data/` 放全部可变状态（数据库、备份、
断点续传进度）。这样同一份副本数据可以被多个项目共用，而代码各自独立。

库路径按本文件位置推出来，不看当前工作目录 —— 无论从哪个目录启动
`python -m equinet_data_manager`，指向的都是同一个库。

数据文件名固定：`equinet.db` / `backup/` / `update_progress.json`。
命令行 `--db` 可以逐次覆盖库位置（对比实验或只读快照用）。
"""

import os

PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(PACKAGE_DIR)

# 数据根目录
DATA_DIR = os.path.join(PROJECT_ROOT, 'data')

# 行情数据库（SQLite 单文件）
DB_PATH = os.path.join(DATA_DIR, 'equinet.db')

# 备份目录
BACKUP_DIR = os.path.join(DATA_DIR, 'backup')

# 增量更新的断点续传进度文件
UPDATE_PROGRESS_FILE = os.path.join(DATA_DIR, 'update_progress.json')


def ensure_dirs() -> None:
    """创建数据目录（幂等）。写库/备份前调用。"""
    os.makedirs(BACKUP_DIR, exist_ok=True)


__all__ = [
    'PACKAGE_DIR', 'PROJECT_ROOT', 'DATA_DIR',
    'DB_PATH', 'BACKUP_DIR', 'UPDATE_PROGRESS_FILE', 'ensure_dirs',
]
