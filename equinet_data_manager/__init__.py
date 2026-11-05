"""
equinet-data-manager —— EquiNet 的独立数据仓库与数据维护工具

对外边界只有两件事：

1. **一份 SQLite 行情库**（位置由 `paths.DB_PATH` 决定，默认 `data/equinet.db`）。
   训练侧以只读方式查询，不持有任何写入逻辑。
2. **数据契约**（`contract`）。采样几何、样本列语义、股票池口径、特征基准的
   唯一定义处，训练侧 import 它就够，不需要知道本包其余实现。

其余模块（update / check / audit / pit_pool / fetch_status / adjust_factor /
selfcheck）都是「怎么把这份库维护好」的实现细节，只在维护本库时需要。

`DatabaseManager` 与 `paths` 用惰性导入：契约和路径只需要标准库，
不该因为 `import equinet_data_manager` 就把 pandas / numpy 拉进来。
"""

from .paths import BACKUP_DIR, DATA_DIR, DB_PATH

__all__ = ['DatabaseManager', 'DATA_DIR', 'DB_PATH', 'BACKUP_DIR']
__version__ = '1.0.0'


def __getattr__(name):
    if name == 'DatabaseManager':
        from .database import DatabaseManager
        return DatabaseManager
    raise AttributeError(f'module {__name__!r} has no attribute {name!r}')
