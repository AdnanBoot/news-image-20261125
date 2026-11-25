[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/AdnanBoot/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/AdnanBoot/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

# WORLD NEWS — 25 November 2026

A 1024×1024 editorial broadsheet news digest rendered deterministically in Python with Pillow for the `news-image-20261125` make.fun bounty.

## Research & Verification Standard

- Every story, statistic, and quote is cross-checked against at least two authoritative sources (primary wire reports from Reuters/AP/BBC alongside major outlets) and locked into a verified-facts file prior to rendering.
- Unsettled intraday figures and single-source aggregator claims are excluded; dates and event statuses are stated accurately (e.g., Section 301 findings are reported as *set to release*, and COP31 is framed as Sunday's summit outcome).

## How to Run

Render `entry.png` deterministically (requires Pillow and DejaVu fonts):

```bash
python3 draw.py
```

Verify the SHA-256 of `entry.png` and copy it to `$MAKEFUN_OUTPUT_DIR/entry.png` (defaults to `/output`, stdlib-only):

```bash
python3 main.py
```
