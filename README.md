# skill-trendline-breakdown-reversal

A 股日线下跌突破划线压力位反转因子 Skill。它使用 PandData 获取全市场日线数据，识别下降压力线被有效下破、随后在确认窗口内反转的股票。

## 功能

- 自动获取指定交易日及历史窗口的 PandData 行情
- 计算 `pressure_line`、连续 `factor` 和离散 `signal`
- 输出目标日期 `signal=1` 的股票代码
- 使用 `scripts/validate.py` 生成基础质量报告

## 快速开始

安装依赖：

```bash
pip install panda_data pandas numpy
```

在 PandAI 完成注册并开通股票数据权限后，设置 `PANDADATA_USERNAME` 和 `PANDADATA_PASSWORD`。调用方式和输入字段详见 [SKILL.md](SKILL.md)；因子定义详见 [references/formula.md](references/formula.md)。

本项目仅允许 PandData 作为在线行情源。数据源不可用时不会自动切换到其他服务，用户可以改为提供包含 `ts_code,trade_date,open,close,high,low,vol` 的 CSV/Parquet 数据。

## 许可证

本项目仅以 GPL-3.0-only 发布，详见 [LICENSE](LICENSE)。结果仅供研究，不构成投资建议。
