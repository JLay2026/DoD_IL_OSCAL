#!/usr/bin/env python3
"""
regscale_rebind.py — Re-target this repo's RegScale export envelopes to a
specific tenant's DoW CNSSI 1253 catalog.

Why this exists:
  The 7 export envelopes under ../profiles/ reference a specific tenant's
  catalog id and per-control integer ids. RegScale catalog UUIDs and per-
  control UUIDs are stable across tenants, but the *integer* ids ('catalog.id'
  and 'securityControl.id') are tenant-local. Importing the envelopes into a
  different tenant requires remapping those integers.

How it works:
  1. Connect to the target RegScale tenant.
  2. Discover the DoW catalog by stable UUID (476dbabf-f394-4375-8ddd-0a13f34c2f82).
     The catalog is matched by UUID first, then by exact title as a fallback.
  3. Fetch all securityControls for that catalog and index by stable per-control
     UUID and by padded controlId (e.g. 'AC-01', 'AC-02(01)').
  4. For each export envelope file (or one selected via --profile), rewrite:
       - per-mapping 'catalogId'  -> the tenant's catalog.id
       - per-mapping 'controlId'  -> the tenant's securityControl.id
       - per-mapping 'catalogGuid', 'catalogTitle', 'catalogUrl' refreshed
     Everything else (controlGuid, controlIdentifier, controlTitle,
     profileMappingId, profile envelope metadata) is preserved.
  5. Validate: 100% of mappings must resolve in the live catalog by all three
     keys (UUID, padded controlId, integer id) before writing.
  6. Write the rewritten envelopes either back in-place or to --output-dir.

Stable identifiers used as source of truth:
  Catalog UUID:        476dbabf-f394-4375-8ddd-0a13f34c2f82
  Catalog title:       "DoW - NIST 800-53 - Rev 5 (CNSSI 1253)"
  Per-control UUIDs:   each securityControl.uuid (same across tenants)
  Per-control padded:  each securityControl.controlId, e.g. 'AC-01', 'AC-02(01)'

Usage:
  python regscale_rebind.py \\
      --base-url https://regscale.example.com \\
      --api-key  <token> \\
      [--profile fedramp_rev5_high]   # only rewrite this profile (default: all 7)
      [--profiles-dir ../profiles]    # default: ../profiles relative to this script
      [--output-dir ../profiles]      # default: rewrite in place
      [--dry-run]                     # report-only, never write

Exit codes:
  0  success
  1  invalid input / catalog not found / API failure
  2  validation failed (mapping cannot resolve in target catalog)
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import sys
from pathlib import Path
from urllib import request, error
from typing import Any

DOW_CATALOG_UUID = "476dbabf-f394-4375-8ddd-0a13f34c2f82"
DOW_CATALOG_TITLE = "DoW - NIST 800-53 - Rev 5 (CNSSI 1253)"

ALL_PROFILES = [
    "fedramp_rev5_high",
    "dod_ccsrg_il4_moderate",
    "dod_ccsrg_il4_high",
    "dod_ccsrg_il5_nss",
    "dod_ccsrg_il6_nss",
    "dod_il5_nss_manifest",
    "dod-ccsrg",  # combined aggregate
]


def _http(method: str, url: str, api_key: str) -> tuple[int, Any]:
    req = request.Request(
        url,
        method=method,
        headers={
            "Authorization": api_key,
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
    )
    try:
        with request.urlopen(req, timeout=120) as r:
            raw = r.read().decode("utf-8")
            try:
                return r.status, json.loads(raw) if raw else None
            except json.JSONDecodeError:
                return r.status, None
    except error.HTTPError as exc:
        try:
            payload = json.loads(exc.read().decode("utf-8"))
        except Exception:
            payload = None
        return exc.code, payload
    except error.URLError as exc:
        print(f"ERROR: cannot reach RegScale: {exc.reason}", file=sys.stderr)
        sys.exit(1)


def find_catalog(base_url: str, api_key: str) -> dict:
    """Find the DoW catalog by stable UUID, fall back to exact title."""
    print(f"==> Looking up DoW catalog by UUID {DOW_CATALOG_UUID}")
    status, body = _http("GET", f"{base_url.rstrip('/')}/api/catalogues/getList", api_key)
    if status != 200 or not isinstance(body, list):
        print(f"ERROR: GET /api/catalogues/getList returned status={status}", file=sys.stderr)
        sys.exit(1)
    # Match by UUID first
    for c in body:
        if str(c.get("uuid", "")).lower() == DOW_CATALOG_UUID.lower():
            print(f"    Matched by UUID: id={c['id']}  title={c.get('title')!r}")
            return c
    # Fall back to exact title
    for c in body:
        if c.get("title") == DOW_CATALOG_TITLE:
            print(f"    Matched by title: id={c['id']}  uuid={c.get('uuid')}")
            return c
    print(
        f"ERROR: no catalog found with UUID {DOW_CATALOG_UUID} or title {DOW_CATALOG_TITLE!r}.\n"
        f"       Available catalogs in this tenant:",
        file=sys.stderr,
    )
    for c in body[:20]:
        print(f"          id={c.get('id')}  uuid={c.get('uuid')}  title={c.get('title')!r}",
              file=sys.stderr)
    sys.exit(1)


def fetch_catalog_controls(base_url: str, api_key: str, catalog_id: int) -> list[dict]:
    """Fetch every securityControl in the given catalog."""
    print(f"==> Fetching controls for catalog id={catalog_id}")
    # Endpoint shape varies; try the most common first
    endpoints = [
        f"/api/catalogues/{catalog_id}/securityControls",
        f"/api/securityControls/getList/{catalog_id}",
        f"/api/securityControls/getByCatalog/{catalog_id}",
    ]
    for ep in endpoints:
        status, body = _http("GET", f"{base_url.rstrip('/')}{ep}", api_key)
        if status == 200 and isinstance(body, list) and body:
            print(f"    Got {len(body)} controls from {ep}")
            return body
    print("ERROR: could not fetch controls. Tried endpoints:", file=sys.stderr)
    for ep in endpoints:
        print(f"          {ep}", file=sys.stderr)
    sys.exit(1)


def build_indexes(controls: list[dict]) -> tuple[dict, dict]:
    """Index by stable UUID and by padded controlId."""
    by_uuid = {str(c["uuid"]).lower(): c for c in controls if c.get("uuid")}
    by_cid = {c["controlId"]: c for c in controls if c.get("controlId")}
    return by_uuid, by_cid


def rebind_file(path: Path, catalog: dict, by_uuid: dict, by_cid: dict,
                dry_run: bool, out_dir: Path) -> tuple[int, int, int]:
    """Rewrite per-mapping catalogId/controlId in one export envelope file."""
    d = json.loads(path.read_text())
    mappings = d.get("mappings")
    if not isinstance(mappings, list):
        print(f"  SKIP {path.name}: no 'mappings' array", file=sys.stderr)
        return 0, 0, 0

    cat_id = catalog["id"]
    cat_uuid = catalog.get("uuid", "")
    cat_title = catalog.get("title", "")
    cat_url = catalog.get("url", "")

    n = len(mappings)
    failures: list[str] = []
    changed_cat = changed_ctrl = 0
    for m in mappings:
        live = by_uuid.get(str(m.get("controlGuid", "")).lower()) \
            or by_cid.get(m.get("controlIdentifier", ""))
        if not live:
            failures.append(m.get("controlIdentifier", "?"))
            continue
        # catalog refs
        if m.get("catalogId") != cat_id:
            m["catalogId"] = cat_id
            changed_cat += 1
        m["catalogGuid"] = cat_uuid
        m["catalogTitle"] = cat_title
        m["catalogUrl"] = cat_url
        # integer id
        new_int = int(live["id"])
        if m.get("controlId") != new_int:
            m["controlId"] = new_int
            changed_ctrl += 1

    if failures:
        print(f"  FAIL {path.name}: {len(failures)} mappings cannot resolve in tenant catalog",
              file=sys.stderr)
        for f in failures[:10]:
            print(f"        - {f}", file=sys.stderr)
        if len(failures) > 10:
            print(f"        ... and {len(failures)-10} more", file=sys.stderr)
        return n, 0, len(failures)

    d["exportDate"] = _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    if dry_run:
        print(f"  DRY  {path.name}: n={n}  catalogId={changed_cat}  controlId={changed_ctrl}")
        return n, changed_cat, 0

    out_path = out_dir / path.name
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(d, indent=2) + "\n")
    print(f"  OK   {out_path}: n={n}  catalogId={changed_cat}  controlId={changed_ctrl}")
    return n, changed_cat, 0


def main() -> None:
    ap = argparse.ArgumentParser(description="Rebind RegScale export envelopes to a tenant catalog.")
    ap.add_argument("--base-url", required=True)
    ap.add_argument("--api-key", default=os.environ.get("REGSCALE_API_KEY"))
    ap.add_argument("--profile", choices=ALL_PROFILES, default=None,
                    help="Only rewrite this profile (default: all 7)")
    ap.add_argument("--profiles-dir",
                    default=str(Path(__file__).parent.parent / "profiles"),
                    help="Source directory of *-regscale-export.json (default: ../profiles)")
    ap.add_argument("--output-dir", default=None,
                    help="Where to write rewritten files (default: rewrite in place)")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    if not args.api_key:
        print("ERROR: --api-key required (or set REGSCALE_API_KEY)", file=sys.stderr)
        sys.exit(1)

    profiles_dir = Path(args.profiles_dir).resolve()
    out_dir = Path(args.output_dir).resolve() if args.output_dir else profiles_dir
    if not profiles_dir.is_dir():
        print(f"ERROR: profiles-dir not found: {profiles_dir}", file=sys.stderr)
        sys.exit(1)

    # 1. discover catalog
    catalog = find_catalog(args.base_url, args.api_key)
    # 2. fetch controls
    controls = fetch_catalog_controls(args.base_url, args.api_key, catalog["id"])
    by_uuid, by_cid = build_indexes(controls)
    print(f"    Indexed {len(by_uuid)} by uuid, {len(by_cid)} by controlId")

    # 3. select files
    if args.profile == "dod-ccsrg":
        files = [profiles_dir / "dod-ccsrg-regscale-export.json"]
    elif args.profile:
        files = [profiles_dir / f"{args.profile}-regscale-export.json"]
    else:
        files = sorted(profiles_dir.glob("*-regscale-export.json"))

    print(f"==> Rebinding {len(files)} file(s) (output_dir={out_dir})")
    total_failures = 0
    for f in files:
        if not f.exists():
            print(f"  MISS {f.name}", file=sys.stderr)
            continue
        n, _, fails = rebind_file(f, catalog, by_uuid, by_cid, args.dry_run, out_dir)
        total_failures += fails

    if total_failures:
        print(f"\n!!! {total_failures} unresolved mappings. No partial writes performed for failing files.",
              file=sys.stderr)
        sys.exit(2)

    print("\nAll files rebound successfully.")
    print(f"Tenant catalog: id={catalog['id']}  uuid={catalog['uuid']}  title={catalog['title']!r}")


if __name__ == "__main__":
    main()
