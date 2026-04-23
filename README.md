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
│       ├── dome-registry-schema.json          # DOME entry schema — all 21 DOME content fields + metadata
│       ├── dome-registry-entry-template.json  # Blank entry template — copy and fill for a new entry
│       ├── dome-registry-entry-annotated.json # Annotated entry guide — field-by-field descriptions
│       ├── dome-registry-entry-example.json   # Fictionalised fully-completed example entry
│       ├── dome-registry-user-schema.json     # DOME user account schema — links to entries via _id
│       ├── dome-registry-user-template.json   # Blank user account template
│       ├── dome-registry-user-annotated.json  # Annotated user guide — field-by-field descriptions
│       └── dome-registry-user-example.json    # Fictionalised user account example (no real PII)
├── validator/
│   ├── Dockerfile                             # Docker image for the DOME validator (only supported runtime)
│   ├── requirements.txt                       # Python dependencies (used by Dockerfile)
│   ├── validate.py                            # Validator script — run via Docker, not directly
│   └── examples/
│       ├── compliant-entry-v1.0.0.json        # Fully completed entry — validates as COMPLIANT (21/21)
│       └── non-compliant-entry-v1.0.0.json    # Incomplete entry — validates as NON-COMPLIANT (6/21)
├── CITATION.cff                               # Citation metadata
├── CODE_OF_CONDUCT.md                         # Community code of conduct
├── CONTRIBUTING.md                            # How to contribute
├── LICENSE                                    # CC BY 4.0
└── README.md
```

Each version folder under `releases/` is **immutable** after publication. There are two parallel schema families per version:

### Entry schema — `dome-registry-*`

Describes the structure of a DOME Registry entry: the 21 user-facing DOME content fields across Data, Optimisation, Model, and Evaluation, plus publication metadata and system fields. Entries are linked to user accounts via the `user` field (referencing the user `_id`).

| File | Purpose |
|---|---|
| `dome-registry-schema.json` | Schema document defining all entry field types, descriptions, and constraints |
| `dome-registry-entry-template.json` | Blank template with all 21 DOME content fields empty — copy and fill to create a new entry |
| `dome-registry-entry-annotated.json` | Each field value replaced with a descriptive prompt explaining what information to provide |
| `dome-registry-entry-example.json` | Fully completed fictionalised example entry showing expected level of detail |

### User schema — `dome-registry-user-*`

Describes the structure of a DOME Registry user account: authentication, identity, ORCID, role, and organisation affiliation. Personal data fields are clearly labelled `[PII]`. User records link to entries through the shared `_id` → `user.$oid` reference.

| File | Purpose |
|---|---|
| `dome-registry-user-schema.json` | Schema document defining all user account field types, descriptions, and constraints |
| `dome-registry-user-template.json` | Blank user account template |
| `dome-registry-user-annotated.json` | Each field value replaced with a descriptive prompt; PII fields clearly noted |
| `dome-registry-user-example.json` | Fictionalised example user account — no real personal data |

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

## Validator

This repository includes a command-line validator for checking DOME Registry JSON files (entries and user accounts) against a chosen schema version. The validator is packaged as a Docker image — this is the only supported runtime.

### Build the Docker image

Run from the repository root (both `releases/` and `validator/` must be available as build context):

```bash
docker build -t dome-validator -f validator/Dockerfile .
```

### Run the validator

Mount a directory containing your JSON file(s) at `/data` inside the container and pass the required arguments.

**Validate a DOME Registry entry:**

```bash
docker run --rm -v "$(pwd)/validator/examples:/data" dome-validator \
  --schema-type entry \
  --schema-version v1.0.0 \
  --file /data/compliant-entry-v1.0.0.json
```

**Validate a user account file:**

```bash
docker run --rm -v "/path/to/your/files:/data" dome-validator \
  --schema-type user \
  --schema-version v1.0.0 \
  --file /data/my-user.json
```

**List available schema versions:**

```bash
docker run --rm dome-validator --list-versions
```

### Output

The validator prints a per-field report and a summary result:

```
DOME Registry Validator
────────────────────────────────────────────────────
Schema type   : entry
Schema version: v1.0.0
File          : /data/compliant-entry-v1.0.0.json
────────────────────────────────────────────────────

Section: dataset
  [✓] availability
  [✓] provenance
  ...

────────────────────────────────────────────────────
Result: COMPLIANT
  Structural errors   : 0
  Completeness issues : 0 field(s) absent or empty
────────────────────────────────────────────────────
```

The process exits with code `0` (COMPLIANT) or `1` (NON-COMPLIANT), making it straightforward to use in CI pipelines.

### Example files

Two example entry files are provided in [`validator/examples/`](./validator/examples/) for testing and reference:

| File | Expected result | DOME score |
|---|---|---|
| `compliant-entry-v1.0.0.json` | COMPLIANT | 21/21 |
| `non-compliant-entry-v1.0.0.json` | NON-COMPLIANT | 6/21 |

---

## License

This repository and its contents are licensed under [Creative Commons Attribution 4.0 International (CC BY 4.0)](./LICENSE).

