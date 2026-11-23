# The World in One Day — Monday, 23 November 2026

[![Make.fun Bounty](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![Make.fun Rank](https://make.fun/badge/news-image-20261123/chongphoshun/makefun-news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![Make.fun Reward](https://make.fun/badge/news-image-20261123/chongphoshun/makefun-news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

A single newspaper front page that sums up world news on Monday, 23 November 2026: 3 lead stories, 12 main stories, 6 numbers, and 23 briefs — 38 stories in one 1024×1024 image.

Leads: the COP31 climate talks collapse in Antalya, two supertankers ablaze in the Strait of Hormuz, and the AI sell-off spreading in Asia. The Riemann Hypothesis item is labelled as a claim, not a confirmed proof.

The image is drawn by `draw_news.py` (Pillow + DejaVu fonts, no network, no downloaded assets) and `main.py` copies the finished `entry.png` to the output directory. `main.py` uses only the Python standard library.

## Contents

- `draw_news.py` — draws `entry.png` (1024×1024)
- `entry.png` — the finished front page
- `main.py` — copies `entry.png` to the output directory
- `LICENSE` — MIT

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

To redraw the image first:

```sh
python3 draw_news.py
```

Running `main.py` twice, from any working directory, writes byte-identical output.
