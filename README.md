# news-image-20261125 — The World in One Image

[![make.fun bounty](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125)
[![make.fun rank](https://make.fun/badge/news-image-20261125/Herman-234/mend-news-image-25-nov-2026/rank.svg)](https://make.fun/bounty/news-image-20261125)
[![make.fun reward](https://make.fun/badge/news-image-20261125/Herman-234/mend-news-image-25-nov-2026/reward.svg)](https://make.fun/bounty/news-image-20261125)

This is my entry for the [make.fun bounty "Sum up 25 November's world news in one image"](https://make.fun/bounty/news-image-20261125). The pool is $100 across 50 paid places, $20 for first place, and entries close 27 Nov 2026 at 07:00 WIB.

## What the picture shows

Wednesday 25 November 2026, told as a newspaper front page with five stories:

1. **Ukraine confirms drone strike on Russian ship** — Kyiv says it hit a Russian cargo ship in the Gulf of Finland; Norway is calling for caution.
2. **Houthi strike hits Riyadh's tallest tower** — Saudi civil defence reports 11 people wounded as the war in Yemen reaches further into the Gulf.
3. **Huawei convicted in sprawling US trial** — a US jury found the company guilty over its Iran dealings and trade secrets.
4. **NATO to send early-warning jets to Poland** — surveillance aircraft are being deployed after missiles came down in Poland during an attack on Ukraine.
5. **Day against violence towards women** — 25 November is the International Day for the Elimination of Violence against Women.

The stories come from public news searches on 25 Nov 2026: Reuters (via Devdiscourse), Jagran Josh, Newsmriti and HuddleWorld.


## How the entry is put together

- `build_image.py` draws `entry.png` (1024×1024) with PIL. It works offline and always produces the same bytes.
- `main.py` is the part the grader runs: it copies the finished `entry.png` into the output folder and checks the copy with a sha256 hash and a PNG size read. It uses nothing but the standard library — no PIL, no network — so it runs the same everywhere.

```sh
python3 build_image.py   # redraw entry.png
python3 main.py          # place a verified copy in the output folder
```

## License

MIT — see [LICENSE](LICENSE).
