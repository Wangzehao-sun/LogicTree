# Security Policy

## Reporting a vulnerability

Please report vulnerabilities privately through GitHub Security Advisories for this repository. Do not open a public issue for an unpatched vulnerability and do not include live credentials in a report.

Include the affected version or commit, reproduction steps, impact, and any suggested mitigation. Maintainers should acknowledge a report before discussing a public disclosure timeline.

## Credential handling

LogicTree reads model credentials from environment variables. Real secrets must not be stored in source files, notebooks, sample data, logs, or issue reports. If a credential is committed at any point, revoke it immediately; deleting it from the current tree does not remove it from Git history.

## Model and data risks

Generated content is untrusted data. Validate model JSON before downstream use, avoid sending confidential inputs to external providers, and review provider retention policies. The framework does not sandbox content returned by a model.
