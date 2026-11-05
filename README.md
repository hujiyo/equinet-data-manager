# equinet-data-manager

EquiNet 的数据仓库与数据维护工具。行情数据库、数据契约、抓数/质检/审计/自检流水线都在这里，
训练侧（EquiNet 仓库）只读库、只 import 契约，不含任何数据维护代码。

本仓库是 EquiNet 的专职数据层：它按 EquiNet 需要的数据格式与数据类型提供结构，
需要新东西就在这里加模块，不改 EquiNet 的数据访问代码。别的项目要用同一份副本数据，
也指向这个仓库即可。

## 对外边界

训练侧只需要一个路径就能定位数据：

```python
DATA_MANAGER_ROOT = os.path.join(os.path.dirname(PROJECT_ROOT), 'equinet-data-manager')
DB_PATH = os.path.join(DATA_MANAGER_ROOT, 'data', 'equinet.db')
```

除此之外它只用 `equinet_data_manager.contract` —— 采样几何、样本列语义、股票池口径、
特征基准的唯一定义处。

## 目录结构

```
equinet-data-manager/
├── data/                      # 全部可变状态（不入库）
│   ├── equinet.db             # SQLite 行情库
│   ├── backup/                # 数据库备份
│   └── update_progress.json   # 增量更新断点
├── equinet_data_manager/
│   ├── paths.py               # 数据位置唯一定义处
│   ├── contract.py            # 数据契约（只依赖标准库）
│   ├── settings.py            # 数据源选择
│   ├── database.py            # 库操作与写入门禁
│   ├── update.py              # 增量/全量/训练池更新
│   ├── check.py               # 联网质检与修复
│   ├── quality.py             # 门禁规则与离线扫描
│   ├── audit.py               # 离线质量审计 → data_issues
│   ├── adjust_factor.py       # 后复权因子采集与物化
│   ├── features.py            # MA / MACD / 布林带
│   ├── pit_pool.py            # 逐日股票池
│   ├── fetch_status.py        # 逐日 tradestatus / isST
│   ├── provenance.py          # 派生状态血缘
│   ├── selfcheck.py           # 不变量自检
│   └── __main__.py            # 交互式菜单
├── pyproject.toml
└── requirements.txt
```

## 使用

```bash
pip install -r requirements.txt      # 或 pip install -e . （把 [fetch] 一起装上）

python -m equinet_data_manager            # 交互式菜单（更新 / 筛选 / 质检 / 审计 / PIT / 自检）
python -m equinet_data_manager.audit --write --pool pit
python -m equinet_data_manager.selfcheck --fast
```

数据目录固定是本仓库下的 `data/`；要从别的目录启动也没关系，路径按文件位置推，不看工作目录。

## 数据模型

- `stock_daily`：日行情（OHLCV、成交额、换手率、vwap、9 个衍生特征、后复权列、复权因子）
- `stock_pool`：今日口径的股票池（`all` / `selected`）
- `pool_membership`：PIT 池的逐日区间（当前生效池）
- `stock_status`：逐日交易状态与 ST 标记
- `data_issues`：逐条问题日（离线审计产出）
- `data_meta`：每份派生状态的血缘与新鲜度
- `adjust_factor`：除权事件级复权因子
- `stock_metadata` / `schema_info`

写入路径只有一条：`DatabaseManager.upsert_daily_data`，所有落库都过写入门禁
（`quality.gate_dataframe`），结构性非法的行直接拒绝入库。

## 与 EquiNet 的契约

- 训练侧 `src/config.py` 从本包 import 契约并做启动断言（列数、下标、污染半径）。
- 训练启动前调用 `equinet_data_manager.selfcheck.prerequisites()`，校验审计范围=训练池、
  派生状态未过期、契约列在库里真实存在；`STRICT_SELFCHECK=True` 时有 error 直接中止训练。
- 训练侧对库**只读**，写入只发生在本仓库。
