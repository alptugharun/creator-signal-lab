# Contributing

Focused improvements are welcome: parser edge cases, scoring documentation, tests, synthetic examples and clearer error messages.

Before a PR:

```bash
python -m unittest discover -s tests -v
python tools/signal2content_score.py examples/signal2content-opportunities.csv --validate-only
python tools/outlier_score.py examples/social-outlier-posts.csv --validate-only
```

Do not present a heuristic score as a prediction, live trend metric, or guaranteed performance result.
