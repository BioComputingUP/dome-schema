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

# Top-level schema properties that are infrastructure/metadata, NOT DOME content sections.
NON_DOME_TOP_LEVEL = {
    "publication", "_id", "uuid", "shortid", "__v", "update",
    "score", "reviewState", "public", "isAiGenerated", "tags",
    "created", "updated", "user",
}

# Sub-fields present in every DOME section for system tracking — not content fields.
SECTION_SYSTEM_FIELDS = {"done", "skip"}

# Publication sub-fields that are system/tracking, not user-facing content.
PUBLICATION_SYSTEM_FIELDS = {"done", "skip", "updated", "created"}

# Keys in our schema files that are not part of JSON Schema proper — strip before validating.
NON_STANDARD_SCHEMA_KEYS = {"x-dome-schema-version", "_comment"}


# ---------------------------------------------------------------------------
# Schema-driven field discovery
# These functions derive section/field structure directly from the schema JSON
# at runtime, so no code changes are needed when a new schema version is added.
# ---------------------------------------------------------------------------

def extract_dome_sections(schema: dict) -> dict:
    """
    Return an ordered {section_name: [field_name, ...]} map derived from the
    schema JSON itself.  Works for any schema version that follows the DOME
    convention:
      - Top-level `required` lists the DOME content sections (plus 'publication').
      - Each section has `properties` whose keys are the DOME content fields
        plus the system tracking fields `done` and `skip`.
    """
    top_props = schema.get("properties", {})
    # Prefer canonical order from `required`; fall back to properties key order.
    ordered_keys = schema.get("required", list(top_props.keys()))
    sections = [k for k in ordered_keys if k not in NON_DOME_TOP_LEVEL]
    result = {}
    for section in sections:
        sec_props = top_props.get(section, {}).get("properties", {})
        fields = [
            f for f in sec_props
            if f not in SECTION_SYSTEM_FIELDS and not f.startswith("_")
        ]
        result[section] = fields
    return result


def extract_publication_fields(schema: dict) -> list:
    """Derive the user-facing publication fields from the schema, in schema order."""
    pub_props = (
        schema.get("properties", {})
              .get("publication", {})
              .get("properties", {})
    )
    return [
        f for f in pub_props
        if f not in PUBLICATION_SYSTEM_FIELDS and not f.startswith("_")
    ]


def extract_user_fields(schema: dict) -> tuple:
    """
    Derive (active_fields, legacy_field_set) from the user schema properties.
    A field is legacy if its description contains '[Legacy]' or '[legacy]'.
    System fields (_id, __v) are excluded entirely.
    Returns a tuple: (list_of_active_fields, set_of_legacy_fields).
    """
    system = {"_id", "__v"}
    props = schema.get("properties", {})
    active, legacy = [], set()
    for field, fschema in props.items():
        if field in system or field.startswith("_"):
            continue
        desc = fschema.get("description", "")
        if "[Legacy]" in desc or "[legacy]" in desc:
            legacy.add(field)
        else:
            active.append(field)
    return active, legacy


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
    if isinstance(value, bool):
        return True  # explicit boolean is always considered filled
    if isinstance(value, str):
        return value.strip() not in ("", "undefined")
    if isinstance(value, list):
        return len(value) > 0
    if isinstance(value, dict):
        # For v2.0.0 structured sub-field objects: filled if at least one
        # non-underscore-prefixed sub-field has a non-null, non-empty value.
        for k, v in value.items():
            if k.startswith("_"):
                continue
            if is_filled(v):
                return True
        return False
    return True


# ---------------------------------------------------------------------------
# Report printers
# ---------------------------------------------------------------------------

def report_entry(instance: dict, structural_errors: list, file_label: str,
                 version: str, schema: dict):
    error_paths = {".".join(str(p) for p in e.path): e.message for e in structural_errors}

    print()
    print(f"{Style.BRIGHT if HAS_COLOR else ''}DOME Registry Validator")
    print(separator())
    print(f"Schema type   : entry")
    print(f"Schema version: {version}")
    print(f"File          : {file_label}")
    print(separator())

    completeness_issues = []

    # Derive sections and fields directly from the schema — no hardcoded maps.
    dome_sections = extract_dome_sections(schema)
    pub_fields = extract_publication_fields(schema)

    for section, fields in dome_sections.items():
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

    # Publication section — derived from schema, not hardcoded.
    print(f"\nSection: {Fore.CYAN if HAS_COLOR else ''}publication{Style.RESET_ALL if HAS_COLOR else ''}")
    pub = instance.get("publication", {})
    if not isinstance(pub, dict):
        print(fail("'publication' is present but not an object"))
    else:
        for field in pub_fields:
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


def report_user(instance: dict, structural_errors: list, file_label: str,
                version: str, schema: dict):
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

    # Derive user fields and legacy set from the schema — no hardcoded lists.
    user_fields, user_legacy = extract_user_fields(schema)
    schema_required = set(schema.get("required", []))
    all_report_fields = user_fields + sorted(user_legacy)

    for field in all_report_fields:
        path_key = field
        value = instance.get(field)
        is_legacy = field in user_legacy
        if path_key in error_paths:
            print(fail(f"{field} — schema error: {error_paths[path_key]}"))
            if not is_legacy:
                completeness_issues.append(field)
        elif value is None:
            if field in schema_required:
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
        exit_code = report_entry(instance, structural_errors, args.file, args.schema_version, schema)
    else:
        exit_code = report_user(instance, structural_errors, args.file, args.schema_version, schema)

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
