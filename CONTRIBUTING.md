# Contributing to dome-schema

Thank you for your interest in contributing! This document outlines how to contribute to the **DOME Registry schema** — the community-maintained, versioned JSON schema that underpins the [DOME Registry](https://github.com/BioComputingUP/dome-registry) for supervised machine learning methods in biology.

Contributions are made via a GitHub-based workflow using Pull Requests (PRs), reviewed and merged by the project maintainers. All contributions are licensed under [CC BY 4.0](./LICENSE).

---

## On this page

- [How to Contribute](#how-to-contribute)
  - [Reporting Issues or Suggesting Schema Changes](#reporting-issues-or-suggesting-schema-changes)
  - [Submitting Changes via Pull Requests](#submitting-changes-via-pull-requests)
- [What to Contribute](#what-to-contribute)
- [What Not to Contribute](#what-not-to-contribute)
- [Versioning and Schema Evolution](#versioning-and-schema-evolution)
- [Contribution Licensing](#contribution-licensing)
- [Review Process](#review-process)

---

## How to Contribute

### Reporting Issues or Suggesting Schema Changes

If you find an error, want to propose a new field or category, or have an idea for improving the schema structure without submitting a PR yourself:

1. **Check existing issues:** See if someone has already raised the same point or a similar suggestion at [https://github.com/BioComputingUP/dome-schema/issues](https://github.com/BioComputingUP/dome-schema/issues).
2. **Create a new issue:** If not, open a new issue and include:
   - A clear title and description of the proposed change or problem.
   - For new fields, explain what DOME category it belongs to (Data, Optimisation, Model, or Evaluation), what information it captures, and why it is broadly useful.
   - For breaking changes, explain why the benefit outweighs the migration cost.
   - Links or references to supporting publications or community standards where applicable.

### Submitting Changes via Pull Requests

This is the preferred way to contribute schema changes.

1. **Fork the repository:** Create your own copy of [dome-schema](https://github.com/BioComputingUP/dome-schema) on GitHub.
2. **Create a branch:** Use a descriptive branch name:
   ```bash
   git checkout -b feat/add-field-xyz
   ```
   Common prefixes: `feat/` (new field/feature), `fix/` (correction), `docs/` (documentation only), `schema/` (structural schema change).
3. **Make your changes:**
   - Edit the relevant JSON schema file(s) under `releases/`.
   - For new versions, create a new version folder (e.g., `releases/v1.1.0/`) — do **not** edit existing released versions in place.
   - Ensure JSON is valid and the schema is self-consistent.
   - Update any user-facing documentation or the version `README.md` inside the release folder.
4. **Commit your changes:**
   ```bash
   git add .
   git commit -m "feat: Add field 'xyz' to Data section (closes #42)"
   ```
   Use clear, descriptive commit messages. Reference any related issues.
5. **Push to your fork:**
   ```bash
   git push origin feat/add-field-xyz
   ```
6. **Open a Pull Request:**
   - Go to the original [dome-schema](https://github.com/BioComputingUP/dome-schema) repository on GitHub.
   - Open a PR from your branch.
   - Provide a clear title and description explaining the change and its motivation.
   - If the change affects schema version numbering, state the proposed new version and the version type (patch / minor / major) — see [Versioning and Schema Evolution](#versioning-and-schema-evolution).

---

## What to Contribute

We welcome contributions that add or improve:

- **New schema fields:** Additional properties in the Data, Optimisation, Model, or Evaluation sections that capture information aligned with the [DOME Recommendations](https://doi.org/10.1038/s41592-021-01205-4) and community needs.
- **Field corrections:** Fixes to field types, descriptions, required/optional status, or enumerations.
- **Structural improvements:** Better organisation of nested objects, improved `$ref` references, or vocabulary standardisation — discuss major structural changes via an issue first.
- **Tooling and validation:** Scripts or CI workflows for validating entries against the schema, checking backward compatibility, or generating changelogs.
- **Documentation:** Improvements to field descriptions, version READMEs, or usage examples.

When proposing a new field, consider its alignment with the DOME Recommendations pillars:

| Pillar | Focus |
|---|---|
| **D — Data** | Training/test data, splits, provenance, accessibility |
| **O — Optimisation** | Cross-validation strategy, hyperparameter tuning, training conditions |
| **M — Model** | Architecture, algorithm type, parameters, availability |
| **E — Evaluation** | Metrics, benchmarks, comparison to baselines, fairness |

---

## What Not to Contribute

- Changes that **edit a previously released schema version** in place — released versions are immutable. Propose changes as a new version instead.
- Fields or changes that are **not broadly applicable** to supervised machine learning in biology; highly domain-specific extensions should be discussed in an issue first.
- Changes to **core infrastructure files** (GitHub Actions workflows, `.gitattributes`, etc.) without prior maintainer discussion.
- **Promotional content** or entries advertising specific tools without scientific grounding.

---

## Versioning and Schema Evolution

This repository follows [Semantic Versioning (SemVer)](https://semver.org/) for schema releases, using `vMAJOR.MINOR.PATCH`:

| Version type | When to use | Example |
|---|---|---|
| **PATCH** | Corrections to descriptions, fixing typos, clarifying enumerations — no structural change | `v1.0.0` → `v1.0.1` |
| **MINOR** | New optional fields or properties added in a backward-compatible way | `v1.0.0` → `v1.1.0` |
| **MAJOR** | Breaking changes: renaming or removing existing fields, changing field types, restructuring sections | `v1.0.0` → `v2.0.0` |

Each released version lives in its own folder under `releases/` (e.g., `releases/v1.0.0/`) and is **never modified after release**. This ensures that applications and tools depending on a specific version remain stable, and that DOME Registry entries remain valid and interpretable against the schema version they were created under — including those generated at scale by automated pipelines such as [DOME Copilot](https://doi.org/10.64898/2026.04.16.718888).

If you are unsure which version type applies to your proposed change, raise it as an issue to discuss with maintainers first.

---

## Contribution Licensing

By contributing to this repository, you agree that your contributions will be licensed under the [CC BY 4.0](./LICENSE) license. All contributed content must respect the intellectual property rights of others.

---

## Review Process

Project maintainers will review Pull Requests.

- We aim to review contributions promptly; complex changes or new major versions may take longer.
- Feedback or requests for revisions will be made via comments on the PR.
- Once approved, a maintainer will merge the PR into the `main` branch and, where appropriate, tag a new release.

We appreciate every contribution that helps make AI/ML methods in biology more transparent, reproducible, and FAIR.
