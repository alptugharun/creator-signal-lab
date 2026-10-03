# CSV input contract

Both tools are dependency-free and read local CSV files only.

## Shared rules

- comma-separated UTF-8 or UTF-8 BOM;
- header required;
- at least one data row;
- duplicate or blank column names are rejected;
- column order may change;
- extra **named** columns are accepted;
- truncated or wider unnamed rows are rejected;
- numeric inputs must be plain finite numbers;
- IDs remain text, so `001` stays `001`;
- input files are never modified.

## Content opportunities

Required header:

```csv
name,evidence_strength,audience_fit,freshness,repeatability,production_ease,saturation
```

All numeric ratings are 0–100.

| Field | Meaning |
| --- | --- |
| `name` | Non-blank opportunity label |
| `evidence_strength` | Strength of the evidence you supplied |
| `audience_fit` | Fit with the intended audience |
| `freshness` | Timeliness for the intended test |
| `repeatability` | How reusable the mechanic appears |
| `production_ease` | Ease of producing the test |
| `saturation` | Higher means a larger penalty |

Formula:

```text
0.30*evidence_strength
+ 0.25*audience_fit
+ 0.20*freshness
+ 0.15*repeatability
+ 0.10*production_ease
- 0.15*saturation
```

The result is clamped to 0–100.

These ratings are **your assessments**. The tool does not discover market demand.

## Social posts

Required header:

```csv
platform,post_id,views,likes,comments,shares,saves
```

Metrics must be finite and non-negative.

Use comparable posts from the same creator/format/observation window when possible. The tool pools all supplied rows; it does not automatically stratify platforms, accounts or dates.

Each metric is divided by its dataset median. The weighted outlier score uses:

- views 0.25
- likes 0.20
- comments 0.20
- shares 0.20
- saves 0.15

Individual ratios are capped at 10 only inside the weighted score.

## Validation

```bash
python tools/signal2content_score.py examples/signal2content-opportunities.csv --validate-only
python tools/outlier_score.py examples/social-outlier-posts.csv --validate-only
```

A validation failure returns exit code 2 and no ranked output.

When reporting an input bug, use a tiny synthetic reproducer rather than a private analytics export.
