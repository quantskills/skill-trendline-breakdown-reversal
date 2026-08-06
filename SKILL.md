---
name: skill-trendline-breakdown-reversal
description: 计算A股日线下跌突破划线压力位反转因子，识别下破下降压力线后反转确认的个股；当用户提供交易日期、要求自动获取当日全市场A股行情、量化选股、因子研究或回测时使用。
license: GPL-3.0-only
maintainer: skill-trendline-breakdown-reversal maintainers
---
# 下跌突破划线压力位反转因子
本 Skill 用于研究 A 股日线中“下破下降压力线后反转确认”的选股信号。它面向 Codex、Claude Code 及兼容 Markdown Skill 入口的运行时。

## 触发示例
- “帮我计算 20260805 的下跌突破划线压力位反转因子”
- “请对今天 A 股日线选股，筛选下破下降压力线后反转确认的标的”
- “给我一份指定交易日的 signal=1 个股列表”
- “我已有 PandData 权限，帮我获取当日全市场行情并计算因子”
- “输入日期 20260805，按 lookback=20 和 confirm_window=3 计算因子”

## 使用方式
调用 `scripts/factor.py` 计算因子，调用 `scripts/validate.py` 生成质量报告。用户提供“输入日期/交易日期/某日A股行情/当日选股”等指令时，先获取该日期及此前至少 `lookback+confirm_window` 个交易日的全市场日线，再输出该日期 `signal=1` 的股票。

典型流程：

1. 准备 PandData 账号、权限和环境变量。
2. 通过 `fetch_a_share_daily()` 获取目标日期的全市场日线，或直接提供符合字段要求的 DataFrame。
3. 将数据传给 `calculate_factor()`，按目标交易日筛选 `signal=1`。
4. 需要质量检查时，运行 `python scripts/validate.py <csv>`。

## PandData 数据源前置提示
本 Skill 的唯一在线行情来源是 PandData，禁止自动调用 AkShare、Tushare 或其他行情接口。使用 PandData 前，必须提示用户先在 PandAI 官网完成账号注册，并购买/开通股票数据权限。安装 SDK：`pip install panda_data`。首次使用需配置账号（86 开头手机号）和官网密码；建议通过环境变量 `PANDADATA_USERNAME`、`PANDADATA_PASSWORD` 注入，禁止在聊天中索要或明文保存密码。未完成注册、授权或网络不可用时，只能要求用户提供已下载的 CSV/Parquet DataFrame，不能静默切换数据源。
## 输入
DataFrame 必须含 `ts_code,trade_date,open,close,high,low,vol`；也可输入 `trade_date`（YYYYMMDD）触发自动行情获取。可选参数 `lookback=20`、`confirm_window=3`、`threshold=0.02`。
## 输出
逐行返回 `pressure_line`、连续 `factor`、离散 `signal`。`signal=1` 表示下降压力线被有效下破且在确认窗口内收复突破日收盘价并高于当日开盘价；输出其 `ts_code` 即为符合条件个股。
## 约束与金融风险
所有滚动统计只使用当日以前数据（`shift(1)`），禁止未来函数、前视偏差和未来最高/最低价。历史不足返回NaN。应使用复权价并处理停牌、涨跌停、滑点和费用；结果仅为研究信号，不构成投资建议，必须进行样本外及成本回测。
详见 [references/formula.md](references/formula.md)。

## 限制
本 Skill 不执行下单、不提供投资建议，也不保证数据实时性或完整性。PandData 权限、网络状态、复权处理、停牌和交易成本都会影响研究结果。

## 自动获取流程
当输入 `trade_date` 而不是完整 DataFrame 时，调用
`scripts/factor.py` 的 `fetch_a_share_daily(trade_date, start_date=None, provider="pandadata")`：

1. 从 `PANDADATA_USERNAME` 和 `PANDADATA_PASSWORD` 读取 PandData 凭据，并调用 `panda_data.init_token()` 完成初始化。
2. 调用 `panda_data.get_market_data(symbol="all", type="stock", ...)` 获取全市场日线；未提供 `start_date` 时，默认获取目标日期前 90 个自然日的数据。
3. 将返回字段 `symbol` 映射为 `ts_code`、`volume` 映射为 `vol`，并校验输入字段完整后计算因子。

PandData 未安装、未授权、网络不可用或返回数据不完整时，必须明确报错。禁止自动切换到 AkShare、Tushare 或其他在线行情源；如需离线处理，只能由用户提供符合输入字段要求的 CSV/Parquet DataFrame。
