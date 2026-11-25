# news-image-20261125 — The World in One Image

[![make.fun bounty](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125)
[![make.fun rank](https://make.fun/badge/news-image-20261125/Herman-234/mend-news-image-25-nov-2026/rank.svg)](https://make.fun/bounty/news-image-20261125)
[![make.fun reward](https://make.fun/badge/news-image-20261125/Herman-234/mend-news-image-25-nov-2026/reward.svg)](https://make.fun/bounty/news-image-20261125)

Entry for the [make.fun bounty "Sum up 25 November's world news in one image"](https://make.fun/bounty/news-image-20261125) — $100 prize pool, 50 paid places, 1st $20, closes 27 Nov 2026 07:00 WIB.

## The image

A front-page-style infographic summing up Wednesday 25 November 2026 in five stories:

1. **Ukraine confirms drone strike on Russian ship** — Zelenskiy says Kyiv hit a Russian cargo ship in the Gulf of Finland; Norway urges caution.
2. **Houthi strike hits Riyadh's tallest tower** — 11 wounded, Saudi civil defence says, as Yemen's war spills into the Gulf.
3. **Huawei convicted in sprawling US trial** — guilty over its Iran business and trade secrets.
4. **NATO to send early-warning jets to Poland** — after missiles landed in Poland during an attack on Ukraine.
5. **Day against violence towards women** — 25 November is the International Day for the Elimination of Violence against Women.

Sources: Reuters (via Devdiscourse), Jagran Josh, Newsmriti, HuddleWorld — public news search, 25 Nov 2026.

## How it works

- `build_image.py` renders `entry.png` (1024×1024, PIL, no network, deterministic).
- `main.py` copies the pre-rendered `entry.png` to `/output/entry.png` and verifies the copy by sha256 — no network, byte-identical on every run.

```sh
python3 build_image.py   # regenerate entry.png
python3 main.py          # write /output/entry.png
```

## License

MIT — see [LICENSE](LICENSE).
