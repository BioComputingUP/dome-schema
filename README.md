# dome-schema

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](./LICENSE)

The official repository for the **DOME Registry** schema — providing a shared, versioned, and community-maintained data model to improve visibility and interoperability of AI/ML resources across the [ELIXIR](https://elixir-europe.org/) infrastructure and the broader global data resource landscape. The schema is particularly relevant to assets concerned with AI/ML methods such as datasets, trained models, and associated code.

---

## The DOME Registry

The [DOME Registry](https://github.com/BioComputingUP/dome-registry) is a public resource for hosting supervised machine learning methods in biology in a **reusable, structured, and standardised format**, implementing the DOME Recommendations (Data, Optimisation, Model, Evaluation). By requiring authors to document their methods against a controlled schema, the Registry promotes transparency, reproducibility, and FAIRness across computational biology tools.

As the Registry has grown and evolved — with entries being added, updated, and increasingly generated at scale through automated pipelines such as the **DOME Copilot** — there is a clear need to manage the underlying schema as a versioned, independently governed artefact. This repository serves that purpose: it enables the community to track schema changes, contribute improvements, and build tooling that can depend on a stable, citable schema version. Versioning is essential as entries in the Registry must remain valid and interpretable as the schema evolves over time, particularly at scale.

---

## Repository Structure

```
dome-schema/
├── releases/
│   └── v1.0.0/
│       └── dome-registry-schema.json   # JSON Schema for DOME Registry entries
├── CITATION.cff                        # Citation metadata
├── CODE_OF_CONDUCT.md                  # Community code of conduct
├── CONTRIBUTING.md                     # How to contribute
├── LICENSE                             # CC BY 4.0
└── README.md
```

Each version folder under `releases/` contains the full JSON Schema for that version. Released versions are **immutable** — they are never edited after publication.

---

## Schema Versioning

This repository follows [Semantic Versioning (SemVer)](https://semver.org/) using `vMAJOR.MINOR.PATCH`:

| Version type | When to use |
|---|---|
| **PATCH** `v1.0.x` | Corrections to descriptions, typo fixes, clarified enumerations — no structural change |
| **MINOR** `v1.x.0` | New optional fields added in a backward-compatible way |
| **MAJOR** `vX.0.0` | Breaking changes: renaming/removing fields, changing types, restructuring sections |

The current stable release is **[v1.0.0](https://github.com/BioComputingUP/dome-schema/blob/main/releases/v1.0.0/dome-registry-schema.json)**.

DOME Registry entries record which schema version they conform to. This ensures that even as the schema evolves, older entries remain valid and tools targeting a specific version remain stable — including those produced at scale by automated pipelines such as [DOME Copilot](https://doi.org/10.64898/2026.04.16.718888).

---

## Community Contributions

We actively welcome community input on the schema. Whether you want to propose a new field, report an inconsistency, or suggest how the schema better supports emerging AI/ML reporting needs (e.g., generative models, foundation models, or multi-modal datasets), we want to hear from you.

- **Propose or discuss a schema change:** [Open an issue](https://github.com/BioComputingUP/dome-schema/issues)
- **Submit a schema change or fix:** [Read the contributing guide](./CONTRIBUTING.md)
- **Community standards:** [Code of Conduct](./CODE_OF_CONDUCT.md)

All contributions are licensed under [CC BY 4.0](./LICENSE).

---

## Publications

- **DOME Recommendations** — Walsh I, et al. (2021). *DOME: recommendations for supervised machine learning validation in biology.* Nature Methods, 18, 1122–1127. [https://doi.org/10.1038/s41592-021-01205-4](https://doi.org/10.1038/s41592-021-01205-4)

- **DOME Registry** — Attafi OA, Clementel D, Kyritsis K, Capriotti E, Farrell G, et al. (2024). *DOME Registry: implementing community-wide recommendations for reporting supervised machine learning in biology.* GigaScience, 13, giae094. [https://doi.org/10.1093/gigascience/giae094](https://doi.org/10.1093/gigascience/giae094)

- **DOME Copilot** — Farrell G, Attafi OA, Fragkouli SC, Heredia I, et al. (2026). *DOME Copilot: Making transparency and reproducibility for artificial intelligence methods simple.* bioRxiv. [https://doi.org/10.64898/2026.04.16.718888](https://doi.org/10.64898/2026.04.16.718888)

---

## Citation

If you use or reference this schema, please cite the DOME Registry paper. Citation metadata is available in [CITATION.cff](./CITATION.cff).

> Attafi OA, Clementel D, Kyritsis K, Capriotti E, Farrell G, et al. (2024). *DOME Registry: implementing community-wide recommendations for reporting supervised machine learning in biology.* GigaScience, 13, giae094. https://doi.org/10.1093/gigascience/giae094

---

## Contact

For questions, feedback, or general enquiries about the DOME schema, please contact us at [contact@dome-ml.org](mailto:contact@dome-ml.org) or [open an issue](https://github.com/BioComputingUP/dome-schema/issues).

---

## Related Resources

- DOME Registry application and codebase: [https://github.com/BioComputingUP/dome-registry](https://github.com/BioComputingUP/dome-registry)

---

## License

This repository and its contents are licensed under [Creative Commons Attribution 4.0 International (CC BY 4.0)](./LICENSE).

