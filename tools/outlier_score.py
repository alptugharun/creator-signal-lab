#!/usr/bin/env python3
"""Rank social posts against a creator's own baseline.

Dependency-free by design. Input CSV columns:
platform,post_id,views,likes,comments,shares,saves

The scorer uses median-normalized engagement and reach so one viral post does not
inflate the baseline. It is a research aid, not a claim about algorithmic ranking.
"""

from __future__ import annotations

import argparse
import csv
import math
import sys
import statistics
from pathlib import Path

METRICS = ("views", "likes", "comments", "shares", "saves")
WEIGHTS = {"views": 0.25, "likes": 0.20, "comments": 0.20, "shares": 0.20, "saves": 0.15}


INPUT_COLUMNS = ("platform", "post_id", *METRICS)
INPUT_EXAMPLE = "examples/social-outlier-posts.csv"
INPUT_CONTRACT = "docs/INPUTS.md#social-posts"


def number(value: str) -> float:
    try:
        result = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError("must be numeric (use a decimal point, not a comma)") from exc
    if not math.isfinite(result) or result < 0:
        raise ValueError("must be finite and non-negative")
    return result


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle, strict=True)
        if not reader.fieldnames:
            raise ValueError("CSV has no header")
        if any(not field.strip() for field in reader.fieldnames):
            raise ValueError("CSV header names must not be empty")
        if len(reader.fieldnames) != len(set(reader.fieldnames)):
            raise ValueError("CSV has duplicate column names")
        missing = set(INPUT_COLUMNS).difference(reader.fieldnames)
        if missing:
            raise ValueError("Missing columns: " + ", ".join(sorted(missing))
                             + ". Use a comma-delimited CSV and exact header names.")
        rows = []
        for record, row in enumerate(reader, start=1):
            try:
                if None in row or any(value is None for value in row.values()):
                    raise ValueError("row width differs from the header; check separators and quoting")
                for field in ("platform", "post_id"):
                    if not row[field].strip():
                        raise ValueError(f"{field} must not be blank")
                for metric in METRICS:
                    try:
                        number(row[metric])
                    except ValueError as exc:
                        raise ValueError(f"{metric} {exc}") from exc
            except (ValueError, KeyError) as exc:
                raise ValueError(f"data record {record}: {exc}") from exc
            rows.append(row)
        if not rows:
            raise ValueError("CSV has no data rows")
        return rows


def score_rows(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    if not rows:
        return []

    baselines = {}
    for metric in METRICS:
        values = [number(row[metric]) for row in rows]
        baseline = statistics.median(values) or 1.0
        if not math.isfinite(baseline):
            raise ValueError(f"{metric}: values are too large for a finite median")
        baselines[metric] = baseline

    scored = []
    for row in rows:
        ratios = {metric: number(row[metric]) / baselines[metric] for metric in METRICS}
        if any(not math.isfinite(value) for value in ratios.values()):
            raise ValueError("Metric ratios exceed numeric range; check data magnitudes")
        score = sum(min(ratios[m], 10.0) * WEIGHTS[m] for m in METRICS)
        scored.append({
            **row,
            "outlier_score": round(score, 2),
            "view_multiple": round(ratios["views"], 2),
            "engagement_multiple": round(
                sum(ratios[m] / 4 for m in ("likes", "comments", "shares", "saves")), 2
            ),
        })

    return sorted(scored, key=lambda item: float(item["outlier_score"]), reverse=True)


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", newline="")
    parser = argparse.ArgumentParser(description="Rank social posts against their own median baseline.")
    parser.add_argument("csv_file", type=Path)
    parser.add_argument("--top", type=int, default=10, help="Number of ranked posts to print")
    parser.add_argument("--validate-only", action="store_true", help="Check the input without ranking it")
    args = parser.parse_args()

    try:
        rows = load_rows(args.csv_file)
        if args.validate_only:
            print(f"VALID {args.csv_file}: {len(rows)} data rows")
            return 0
        ranked = score_rows(rows)[: max(1, args.top)]
    except (OSError, UnicodeError, csv.Error, ValueError, KeyError) as exc:
        print(f"error: {args.csv_file}: {exc}\nExample: {INPUT_EXAMPLE}\nInput contract: {INPUT_CONTRACT}", file=sys.stderr)
        return 2
    writer = csv.DictWriter(
        sys.stdout,
        fieldnames=["rank", "platform", "post_id", "outlier_score", "view_multiple", "engagement_multiple"],
    )
    writer.writeheader()
    for rank, row in enumerate(ranked, 1):
        writer.writerow({"rank": rank, **{k: row.get(k, "") for k in writer.fieldnames if k != "rank"}})

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
