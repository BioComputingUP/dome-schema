#!/usr/bin/env python3
"""
DOME Registry Schema Validator
Validates a DOME Registry JSON file (entry or user) against a chosen schema version.

Usage:
    python validate.py --schema-type entry --schema-version v1.0.0 --file path/to/entry.json
    python validate.py --schema-type user  --schema-version v1.0.0 --file path/to/user.json
    python validate.py --list-versions
"""

import argparse
import json
import os
import sys
from pathlib import Path

try:
    import jsonschema
    from jsonschema import Draft7Validator
except ImportError:
    sys.exit("ERROR: 'jsonschema' is not installed. Run: pip install jsonschema")

try:
    from colorama import Fore, Style, init as colorama_init
    colorama_init(autoreset=True)
    HAS_COLOR = True
except ImportError:
    HAS_COLOR = False
    class Fore:
        GREEN = RED = YELLOW = CYAN = RESET = ""
    class Style:
        BRIGHT = RESET_ALL = ""


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parent.parent
RELEASES_DIR = REPO_ROOT / "releases"

# The 21 DOME content fields, grouped by section.
# These are the user-facing fields for which completeness is tracked (score 0–21).
DOME_CONTENT_FIELDS = {
    "dataset":      ["availability", "provenance", "redundancy", "splits"],
    "optimization": ["algorithm", "features", "encoding", "config",
                     "parameters", "fitting", "regularization", "meta"],
    "model":        ["availability", "interpretability", "output", "duration"],
    "evaluation":   ["availability", "measure", "method", "comparison", "confidence"],
}

# Publication fields shown in the report (not counted in the 21-field score).
PUBLICATION_FIELDS = ["title", "authors", "journal", "year", "doi", "pmid", "pmcid"]

USER_FIELDS = ["email", "name", "surname", "orcid", "roles", "organizations"]
# Fields that are legacy/deprecated — shown in output but not counted as completeness failures.
USER_LEGACY_FIELDS = {"organisation"}

# Keys in our schema files that are not part of JSON Schema proper — strip before validating.
NON_STANDARD_SCHEMA_KEYS = {"x-dome-schema-version", "_comment"}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def available_versions():
    if not RELEASES_DIR.exists():
        return []
    return sorted(
        d.name for d in RELEASES_DIR.iterdir()
        if d.is_dir() and not d.name.startswith(".")
    )


def schema_path(version: str, schema_type: str) -> Path:
    filename = f"dome-registry-{'user-' if schema_type == 'user' else ''}schema.json"
    return RELEASES_DIR / version / filename


def load_json(path: Path, label: str) -> dict:
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        sys.exit(f"ERROR: {label} not found: {path}")
    except json.JSONDecodeError as exc:
        sys.exit(f"ERROR: {label} is not valid JSON: {exc}")


def strip_non_standard(schema: dict) -> dict:
    return {k: v for k, v in schema.items() if k not in NON_STANDARD_SCHEMA_KEYS}


def ok(msg):
    return f"  {Fore.GREEN}[✓]{Style.RESET_ALL if HAS_COLOR else ''} {msg}"

def fail(msg):
    return f"  {Fore.RED}[✗]{Style.RESET_ALL if HAS_COLOR else ''} {msg}"

def warn(msg):
    return f"  {Fore.YELLOW}[!]{Style.RESET_ALL if HAS_COLOR else ''} {msg}"

def separator():
    return "─" * 52


# ---------------------------------------------------------------------------
# Structural validation (JSON Schema)
# ---------------------------------------------------------------------------

def run_structural_validation(schema: dict, instance: dict) -> list:
    clean = strip_non_standard(schema)
    validator = Draft7Validator(clean)
    errors = sorted(validator.iter_errors(instance), key=lambda e: list(e.path))
    return errors


# ---------------------------------------------------------------------------
# Completeness check (content-level, custom)
# Fields are "filled" if the value is a non-empty string (or non-empty for arrays/bools).
# ---------------------------------------------------------------------------

def is_filled(value) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return value.strip() not in ("", "undefined")
    if isinstance(value, (list, dict)):
        return len(value) > 0
    if isinstance(value, bool):
        return True  # explicit boolean is considered filled
    return True


# ---------------------------------------------------------------------------
# Report printers
# ---------------------------------------------------------------------------

def report_entry(instance: dict, structural_errors: list, file_label: str, version: str):
    error_paths = {".".join(str(p) for p in e.path): e.message for e in structural_errors}

    print()
    print(f"{Style.BRIGHT if HAS_COLOR else ''}DOME Registry Validator")
    print(separator())
    print(f"Schema type   : entry")
    print(f"Schema version: {version}")
    print(f"File          : {file_label}")
    print(separator())

    completeness_issues = []

    for section, fields in DOME_CONTENT_FIELDS.items():
        print(f"\nSection: {Fore.CYAN if HAS_COLOR else ''}{section}{Style.RESET_ALL if HAS_COLOR else ''}")
        section_data = instance.get(section, {})
        if not isinstance(section_data, dict):
            print(fail(f"section '{section}' is present but not an object"))
            continue
        for field in fields:
            path_key = f"{section}.{field}"
            value = section_data.get(field)
            if path_key in error_paths:
                print(fail(f"{field} — schema error: {error_paths[path_key]}"))
                completeness_issues.append(path_key)
            elif value is None:
                print(fail(f"{field} — field absent"))
                completeness_issues.append(path_key)
            elif not is_filled(value):
                print(warn(f"{field} — present but empty"))
                completeness_issues.append(path_key)
            else:
                print(ok(field))

    # Publication section
    print(f"\nSection: {Fore.CYAN if HAS_COLOR else ''}publication{Style.RESET_ALL if HAS_COLOR else ''}")
    pub = instance.get("publication", {})
    if not isinstance(pub, dict):
        print(fail("'publication' is present but not an object"))
    else:
        for field in PUBLICATION_FIELDS:
            value = pub.get(field)
            path_key = f"publication.{field}"
            if path_key in error_paths:
                print(fail(f"{field} — schema error: {error_paths[path_key]}"))
            elif value is None:
                print(warn(f"{field} — absent"))
            elif not is_filled(value):
                print(warn(f"{field} — present but empty"))
            else:
                print(ok(field))

    # Any remaining structural errors not already shown
    top_level_errors = [e for e in structural_errors
                        if not any(str(p) in DOME_CONTENT_FIELDS or str(p) == "publication"
                                   for p in e.path)]

    print()
    print(separator())
    incomplete = completeness_issues
    n_structural = len(structural_errors)

    if n_structural == 0 and not incomplete:
        print(f"{Fore.GREEN}{Style.BRIGHT if HAS_COLOR else ''}Result: COMPLIANT")
    else:
        print(f"{Fore.RED}{Style.BRIGHT if HAS_COLOR else ''}Result: NON-COMPLIANT")

    print(f"{Style.RESET_ALL if HAS_COLOR else ''}  Structural errors   : {n_structural}")
    print(f"  Completeness issues : {len(incomplete)} field(s) absent or empty")

    if incomplete:
        print(f"\n  Fields to complete:")
        for f in incomplete:
            print(f"    - {f}")

    print(separator())
    print()
    return 0 if (n_structural == 0 and not incomplete) else 1


def report_user(instance: dict, structural_errors: list, file_label: str, version: str):
    error_paths = {".".join(str(p) for p in e.path): e.message for e in structural_errors}

    print()
    print(f"{Style.BRIGHT if HAS_COLOR else ''}DOME Registry Validator")
    print(separator())
    print(f"Schema type   : user")
    print(f"Schema version: {version}")
    print(f"File          : {file_label}")
    print(separator())

    print(f"\nUser account fields:")
    completeness_issues = []

    all_report_fields = USER_FIELDS + sorted(USER_LEGACY_FIELDS)
    for field in all_report_fields:
        path_key = field
        value = instance.get(field)
        is_legacy = field in USER_LEGACY_FIELDS
        if path_key in error_paths:
            print(fail(f"{field} — schema error: {error_paths[path_key]}"))
            if not is_legacy:
                completeness_issues.append(field)
        elif value is None:
            if field in ("email", "roles"):
                print(fail(f"{field} — required field absent"))
                completeness_issues.append(field)
            elif is_legacy:
                print(f"  [legacy] {field} — absent (legacy field, not required)")
            else:
                print(warn(f"{field} — absent (optional)"))
        elif not is_filled(value):
            if is_legacy:
                print(f"  [legacy] {field} = '{value}' (legacy sentinel, not required)")
            else:
                print(warn(f"{field} — present but empty"))
                completeness_issues.append(field)
        else:
            print(ok(field))

    n_structural = len(structural_errors)
    print()
    print(separator())

    if n_structural == 0 and not completeness_issues:
        print(f"{Fore.GREEN}{Style.BRIGHT if HAS_COLOR else ''}Result: COMPLIANT")
    else:
        print(f"{Fore.RED}{Style.BRIGHT if HAS_COLOR else ''}Result: NON-COMPLIANT")

    print(f"{Style.RESET_ALL if HAS_COLOR else ''}  Structural errors   : {n_structural}")
    print(f"  Completeness issues : {len(completeness_issues)} field(s) absent or empty")

    if completeness_issues:
        print(f"\n  Fields to address:")
        for f in completeness_issues:
            print(f"    - {f}")

    print(separator())
    print()
    return 0 if (n_structural == 0 and not completeness_issues) else 1


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser():
    parser = argparse.ArgumentParser(
        description="Validate a DOME Registry JSON file against a schema version.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python validate.py --schema-type entry --schema-version v1.0.0 --file my-entry.json
  python validate.py --schema-type user  --schema-version v1.0.0 --file my-user.json
  python validate.py --list-versions
        """,
    )
    parser.add_argument(
        "--schema-type",
        choices=["entry", "user"],
        help="Type of document to validate: 'entry' (DOME Registry entry) or 'user' (user account).",
    )
    parser.add_argument(
        "--schema-version",
        help="Schema version to validate against, e.g. 'v1.0.0'.",
    )
    parser.add_argument(
        "--file",
        help="Path to the JSON file to validate.",
    )
    parser.add_argument(
        "--list-versions",
        action="store_true",
        help="List all available schema versions and exit.",
    )
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    versions = available_versions()

    if args.list_versions:
        if versions:
            print("Available schema versions:")
            for v in versions:
                print(f"  {v}")
        else:
            print(f"No schema versions found under: {RELEASES_DIR}")
        sys.exit(0)

    # Require all three args if not --list-versions
    missing = [a for a, v in [
        ("--schema-type", args.schema_type),
        ("--schema-version", args.schema_version),
        ("--file", args.file),
    ] if not v]
    if missing:
        parser.error(f"The following arguments are required: {', '.join(missing)}")

    if args.schema_version not in versions:
        sys.exit(
            f"ERROR: Schema version '{args.schema_version}' not found.\n"
            f"Available versions: {', '.join(versions) or 'none'}"
        )

    s_path = schema_path(args.schema_version, args.schema_type)
    if not s_path.exists():
        sys.exit(f"ERROR: Schema file not found: {s_path}")

    schema = load_json(s_path, "Schema file")
    instance = load_json(Path(args.file), "Input file")

    structural_errors = run_structural_validation(schema, instance)

    if args.schema_type == "entry":
        exit_code = report_entry(instance, structural_errors, args.file, args.schema_version)
    else:
        exit_code = report_user(instance, structural_errors, args.file, args.schema_version)

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
