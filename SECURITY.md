# Security Policy

Creator Signal Lab is designed to read local CSV input and write ranked output to stdout.

It should not need network access, API keys, social-media credentials, browser cookies or private account tokens.

## Potential vulnerabilities

Please report security-relevant behavior such as:

- unexpected network access;
- unexpected file modification/deletion;
- path traversal or reading files outside the intended input;
- parser behavior that can trigger code execution;
- unsafe handling of crafted CSV input;
- credential/private-data exposure;
- dependency/release compromise.

A scoring disagreement or ordinary malformed-input bug is usually not a security vulnerability unless it creates concrete security impact.

## Private vulnerability reporting

Do **not** publish exploit details, private analytics exports, credentials or confidential CSV rows in a normal issue.

Use GitHub Private Vulnerability Reporting:

https://github.com/alptugharun/creator-signal-lab/security/advisories/new

A useful private report includes:

- affected version/commit;
- OS and Python version;
- a small synthetic reproducer;
- expected vs actual behavior;
- security impact;
- sanitized output;
- suggested mitigation if known.

## Coordinated disclosure

The maintainer aims to acknowledge a private vulnerability report within **7 days**.

For confirmed vulnerabilities, coordinated disclosure after a fix/mitigation is preferred. A **90-day** remediation/disclosure target is a goal for ordinary cases, not a guarantee; severity and coordination may change the timeline.

Please avoid public disclosure of an unpatched vulnerability before coordination unless there is an overriding safety reason.

## Privacy rule

Use synthetic data for public bug reports whenever possible. Do not upload private client/account analytics just to reproduce a parser or scoring problem.

## Maintainer rule

Security fixes should add regression coverage when practical and must not weaken validation simply to make a test pass.
