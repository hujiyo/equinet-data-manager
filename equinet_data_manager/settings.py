"""
抓数配置

数据源选择属于「怎么取数」，因此由本仓库持有；训练侧不再需要知道用的是哪家源。
命令行 `--source` 可临时覆盖。
"""

# 'baostock' 或 'akshare'。baostock 免费、限流宽松，全量拉取更稳；
# akshare 用于 baostock 缺数据时的补拉与交叉校验。
DATA_SOURCE = 'baostock'

VALID_SOURCES = ('baostock', 'akshare')


def resolve_data_source(source=None) -> str:
    """返回生效的数据源名，非法值直接报错（避免静默退回另一个源）。"""
    src = (source or DATA_SOURCE).strip().lower()
    if src not in VALID_SOURCES:
        raise ValueError(f'未知数据源 {src!r}，可选 {VALID_SOURCES}')
    return src


__all__ = ['DATA_SOURCE', 'VALID_SOURCES', 'resolve_data_source']
