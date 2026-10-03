# Creator Signal Lab

[![English](https://img.shields.io/badge/English-0D1117?style=flat-square)](README.md) [![Türkçe](https://img.shields.io/badge/Türkçe-E30A17?style=flat-square)](README_TR.md)

<p align="center">
  <strong>Two small, transparent scoring tools for creator research — without pretending to predict virality.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-standard_library-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/network-none-16A34A?style=for-the-badge" alt="No network">
  <img src="https://img.shields.io/badge/input-CSV-F59E0B?style=for-the-badge" alt="CSV">
  <img src="https://img.shields.io/badge/license-MIT-2563EB?style=for-the-badge" alt="MIT">
</p>

Creator Signal Lab is a dependency-free pair of CLI tools for two jobs I keep needing in content work:

1. **Which content opportunity deserves attention first?**
2. **Which post actually behaved like an outlier against my own baseline?**

The tools do not scrape platforms, call an AI model, invent trend data, or promise reach. They turn **your explicit inputs** into inspectable rankings.

## Tool 1 — Opportunity scorer

Input columns:

```csv
name,evidence_strength,audience_fit,freshness,repeatability,production_ease,saturation
```

Run:

```bash
python tools/signal2content_score.py examples/signal2content-opportunities.csv --top 3
```

Bundled synthetic sample:

```text
rank,name,score
1,Pinterest seasonal visual series,83.05
2,AI before-after workflow,79.00
3,Creator teardown carousel,74.10
```

The formula is deliberately visible in the source. The score is a prioritization heuristic, **not a probability of success**.

## Tool 2 — Social-post outlier scorer

Input columns:

```csv
platform,post_id,views,likes,comments,shares,saves
```

Run:

```bash
python tools/outlier_score.py examples/social-outlier-posts.csv --top 3
```

Bundled synthetic sample ranks `reel-004` first with:

- outlier score: **6.73**
- view multiple: **3.94**
- engagement multiple: **8.91**

The baseline uses medians so one extreme post does not define the whole comparison set.

## Why transparent heuristics?

Creator analytics gets noisy fast. A neat-looking number is useless when nobody can explain where it came from.

This repository keeps:

- weights visible;
- input contracts explicit;
- malformed data as errors instead of silently turning it into zero;
- synthetic examples clearly labelled;
- zero network calls;
- zero hidden AI scoring.

You can disagree with the weights. That is fine. The point is that you can **see and change them**.

## Bring your own CSV

Start with [docs/INPUTS.md](docs/INPUTS.md).

Validate before ranking:

```bash
python tools/signal2content_score.py your-opportunities.csv --validate-only
python tools/outlier_score.py your-posts.csv --validate-only
```

The parsers handle UTF-8/BOM, quoted commas, multiline text, reordered columns and text IDs such as `001`. They reject missing columns, duplicate headers, malformed row widths, non-finite values and locale-formatted numbers that would be ambiguous.

## Test

```bash
python -m unittest discover -s tests -v
```

CI runs on Linux and Windows.

## What this is not

This is not:

- an Instagram/Pinterest/TikTok algorithm reverse-engineer;
- a virality predictor;
- a live analytics connector;
- a replacement for experiment design;
- evidence that one high-scoring idea will perform.

It is a small research aid that makes assumptions visible.

## Origin

These tools were extracted from [AI Social Media Toolkit](https://github.com/alptugharun/ai-social-media-toolkit) after the input validation and synthetic proof paths became useful enough to stand on their own.

Built by **Alptuğ Harun**.

## License

MIT.
