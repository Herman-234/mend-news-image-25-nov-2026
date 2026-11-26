# The World in One Image — 25 November 2026

[![make.fun](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/Herman-234/mend-news-image-25-nov-2026/rank.svg)](https://make.fun/bounty/news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/Herman-234/mend-news-image-25-nov-2026/reward.svg)](https://make.fun/bounty/news-image-20261125)

Entry for the [news-image-20261125 bounty](https://make.fun/bounty/news-image-20261125): sum up 25 November 2026's world news in a single picture.

The front page carries five stories from the day. The lead is Ukraine confirming a drone strike on a Russian cargo ship in the Gulf of Finland. Below it, four more: the Houthi strike on Riyadh's tallest tower, Huawei's conviction in a sprawling US trial, NATO sending early-warning jets to Poland, and the International Day for the Elimination of Violence against Women. Each story gets its own hand-drawn pictogram — a ship, a tower, a chip, a radar screen, a ribbon — under a navy masthead with the date in gold.

## How it is made

- `build_image.py` draws `entry.png` (1024×1024) with Pillow. Everything is fixed numbers — no network, no clock, no randomness — so running it twice produces the same bytes.
- `main.py` is the part the grader runs: it copies the finished `entry.png` into the output folder and checks the copy with a sha256 hash and a PNG size read from the header. It uses nothing but the standard library — no Pillow, no network — so it runs the same everywhere.
- `entry.png` is the finished front page.

## Run it

```sh
python3 build_image.py   # redraw entry.png
python3 main.py          # copy entry.png to the output folder and verify it
```

No installs beyond Pillow for the drawing step, and no network at any point.
