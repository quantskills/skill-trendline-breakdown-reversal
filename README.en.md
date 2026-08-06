# skill-trendline-breakdown-reversal

An A-share daily trendline-breakdown reversal factor Skill. It uses PandData daily bars to identify stocks that break below a declining pressure line and then recover within the confirmation window.

## Features

- Fetch PandData full-market daily bars for a target date and historical window
- Calculate `pressure_line`, continuous `factor`, and discrete `signal`
- Return symbols with `signal=1` on the target date
- Produce a basic quality report with `scripts/validate.py`

## Quick start

Install dependencies:

```bash
pip install panda_data pandas numpy
```

Register with PandAI, enable the required stock-data permission, and set `PANDADATA_USERNAME` and `PANDADATA_PASSWORD`. See [SKILL.md](SKILL.md) for invocation and input fields, and [references/formula.md](references/formula.md) for the factor definition.

PandData is the only permitted online market-data source. The Skill does not silently fall back to another provider. For offline use, provide CSV/Parquet data containing `ts_code,trade_date,open,close,high,low,vol`.

## License

This project is released under GPL-3.0-only. See [LICENSE](LICENSE). Outputs are for research only and are not investment advice.
