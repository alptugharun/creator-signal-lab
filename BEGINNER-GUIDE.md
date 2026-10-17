# Creator Signal Lab — Beginner Guide

Creator Signal Lab is for one specific situation:

> “I have explicit content ideas or post metrics, but I want a transparent way to prioritize them without pretending an AI can predict virality.”

The project contains **two local CSV tools**.

No scraping. No social login. No model call. No hidden scoring service.

---

## 1. What is a CSV?

CSV means “comma-separated values.”

It is a simple table stored as text.

Example:

```csv
name,evidence_strength,audience_fit,freshness,repeatability,production_ease,saturation
AI before-after workflow,8,9,8,7,8,5
```

The first row contains column names.

Each following row is one item you want to analyze.

You can create/edit CSV files with spreadsheet software, a text editor, or another export tool.

---

# 2. Tool A — Opportunity Scorer

## Question it answers

> “Which content opportunity deserves attention first, based on the factors I explicitly supplied?”

Required columns:

```csv
name,evidence_strength,audience_fit,freshness,repeatability,production_ease,saturation
```

### What the columns mean

- **name** — readable opportunity name;
- **evidence_strength** — how strong the supporting evidence is;
- **audience_fit** — how well it matches your audience;
- **freshness** — how current/timely it is;
- **repeatability** — whether the idea can become a repeatable format/system;
- **production_ease** — how practical it is to make;
- **saturation** — how crowded/overused the idea appears in your own evidence.

These are your explicit inputs.

The tool does not secretly fetch trend volume.

## Run the bundled synthetic example first

From the repository root:

```bash
python tools/signal2content_score.py examples/signal2content-opportunities.csv --top 3
```

Expected sample ranking begins with:

```text
rank,name,score
1,Pinterest seasonal visual series,83.05
2,AI before-after workflow,79.00
3,Creator teardown carousel,74.10
```

If your checkout does not produce the documented synthetic result, stop before using real data.

## Validate your own file before ranking

```bash
python tools/signal2content_score.py your-opportunities.csv --validate-only
```

Then:

```bash
python tools/signal2content_score.py your-opportunities.csv --top 5
```

---

# 3. Tool B — Social Post Outlier Scorer

## Question it answers

> “Which post behaved unusually well relative to my own sample?”

Required columns:

```csv
platform,post_id,views,likes,comments,shares,saves
```

## Why compare against a baseline?

10,000 views may be huge for one account and normal for another.

Raw numbers alone do not tell you whether a post is an outlier.

The tool compares post metrics with medians from the supplied dataset.

Median is used because one extreme viral post should not redefine the entire baseline.

## Run the synthetic example

```bash
python tools/outlier_score.py examples/social-outlier-posts.csv --top 3
```

The bundled sample ranks `reel-004` first with the documented outlier/view/engagement multiples.

## Validate your own export

```bash
python tools/outlier_score.py your-posts.csv --validate-only
```

Then:

```bash
python tools/outlier_score.py your-posts.csv --top 5
```

---

# 4. What does a score mean?

A score is a **ranking heuristic**.

It means:

> “Given this formula and these explicit inputs, this row ranks higher/lower.”

It does not mean:

- 83% chance of success;
- 6.73x chance of virality;
- the platform algorithm will boost the post;
- guaranteed reach, saves, sales or followers.

Always keep formula and real outcome separate.

---

# 5. Why is the formula visible?

Because a black-box “AI score” is hard to challenge.

Here you can:

- inspect the weights;
- disagree with them;
- change them;
- rerun the same input;
- compare output deterministically.

The point is **decision support**, not algorithm mysticism.

---

# 6. What data should I use?

Start with synthetic examples.

Then use:

- your own analytics exports;
- authorized client data;
- manually prepared evidence tables;
- public-safe research data you are allowed to use.

Do not upload private analytics to a public issue.

---

# 7. Common CSV problems

Use `docs/INPUTS.md` for the full contract.

Common errors include:

- missing required columns;
- duplicate header names;
- row width mismatch;
- ambiguous locale-formatted numbers;
- non-finite values;
- broken quoting;
- wrong encoding.

The parsers intentionally fail instead of silently converting bad data into zero.

---

# 8. Spreadsheet-safe output

The ranked output is CSV, so labels and identifiers are prepared defensively before you open them in a spreadsheet.

If a user-controlled `name`, `platform` or `post_id` starts with `=`, `+`, `-` or `@` after leading whitespace, the output adds a leading single quote. For example, `=1+1` becomes `'=1+1` in the ranked CSV.

This happens **only in output**. Your input file is never rewritten and the score is unchanged.

Why: spreadsheet programs may interpret formula-like text as a formula instead of a literal label. The guard reduces that risk for these three exported fields.

What PASS means: the repository test confirms the covered prefixes are neutralized and ordinary values such as `instagram` and `001` remain unchanged.

What PASS does not mean: every spreadsheet app, import option or downstream CSV transformation is guaranteed safe. If another system modifies cells after export, review that system separately.

See `docs/INPUTS.md` for the exact contract.

---

# 9. What this project does NOT do

It is not:

- an Instagram/TikTok/Pinterest algorithm reverse-engineer;
- a scraper;
- a live analytics connector;
- a trend-discovery API;
- an LLM classifier;
- a virality predictor;
- a revenue predictor.

If you need current external trend evidence, collect that evidence separately and label the source/date.

---

# 10. Recommended workflow

### Opportunity analysis

1. define the decision;
2. collect evidence;
3. convert it to the documented CSV;
4. validate;
5. rank;
6. inspect why the top item won;
7. run a real content experiment;
8. compare real outcome with the heuristic.

### Outlier analysis

1. choose a comparable post cohort;
2. export metrics;
3. validate;
4. calculate outliers;
5. inspect the actual posts;
6. look for repeatable mechanics;
7. create a new original test;
8. measure again.

Do not copy a winning post merely because it scored highly.

---

# 11. Test the code

```bash
python -m unittest discover -s tests -v
```

CI runs on Linux and Windows.

---

# 12. Security/privacy

The project reads local CSV input and writes results to stdout.

It should not need:

- API keys;
- browser cookies;
- social account credentials;
- network access.

For a vulnerability, use the private reporting path in `SECURITY.md`.

For a normal input/parser bug, use a small synthetic reproducer.

---

## Final rule

**Use scores to decide what to investigate next, not to pretend uncertainty disappeared.**
