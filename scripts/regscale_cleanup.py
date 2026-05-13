#!/usr/bin/env python3
"""
regscale_cleanup.py — Delete a stale RegScale security profile (and its mappings)
in preparation for re-importing a clean export envelope from this repo.

Use this when a previous import bound the profile to the wrong catalog (e.g. the
FedRAMP High profile that imported as 257/410 because the importer fell back to
IL4 catalogs instead of the DoW CNSSI 1253 catalog).

What this script does:
  1. Connects to RegScale via base URL + API key.
  2. Looks up the target profile by name (exact match).
  3. Prints a summary: profile id, uuid, owner, mapping count, distinct catalogs.
  4. Optionally exports a backup JSON before delete (./backups/<name>-<ts>.json).
  5. Asks for explicit confirmation (or honors --yes).
  6. Deletes all profileMapping rows for that profile, then the profile itself.
  7. Verifies the profile is gone.

Usage:
  python regscale_cleanup.py \\
      --base-url https://regscale.example.com \\
      --api-key  <token> \\
      --profile-name "FedRAMP Rev 5 High Baseline" \\
      [--backup-dir ./backups]   # default: ./backups
      [--skip-backup]            # skip writing the backup JSON
      [--yes]                    # non-interactive
      [--dry-run]                # show what would happen, change nothing

Exit codes:
  0  success (or dry-run / nothing to delete)
  1  invalid input / connection failure
  2  user declined confirmation
  3  delete failed or verification mismatch
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import datetime as _dt
from pathlib import Path
from typing import Any
from urllib import request, error, parse


def _http(method: str, url: str, api_key: str, body: Any = None) -> tuple[int, dict | list | None]:
    """Minimal HTTP client (no external deps)."""
    headers = {
        "Authorization": api_key,
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    data = None
    if body is not None:
        data = json.dumps(body).encode("utf-8")
    req = request.Request(url, data=data, method=method, headers=headers)
    try:
        with request.urlopen(req, timeout=60) as resp:
            raw = resp.read().decode("utf-8") if resp.length != 0 else ""
            status = resp.status
            try:
                return status, json.loads(raw) if raw else None
            except json.JSONDecodeError:
                return status, None
    except error.HTTPError as exc:
        try:
            payload = json.loads(exc.read().decode("utf-8"))
        except Exception:
            payload = None
        return exc.code, payload
    except error.URLError as exc:
        print(f"ERROR: cannot reach RegScale: {exc.reason}", file=sys.stderr)
        sys.exit(1)


def find_profile(base_url: str, api_key: str, name: str) -> dict | None:
    status, body = _http("GET", f"{base_url.rstrip('/')}/api/profiles/getList", api_key)
    if status != 200 or not isinstance(body, list):
        print(f"ERROR: GET /api/profiles/getList returned status={status}", file=sys.stderr)
        sys.exit(1)
    for p in body:
        if p.get("name") == name:
            return p
    return None


def get_mappings(base_url: str, api_key: str, profile_id: int) -> list[dict]:
    status, body = _http(
        "GET",
        f"{base_url.rstrip('/')}/api/profileMapping/getByProfile/{profile_id}",
        api_key,
    )
    if status != 200 or not isinstance(body, list):
        return []
    return body


def summarize_mappings(maps: list[dict]) -> dict:
    catalogs: dict[Any, int] = {}
    for m in maps:
        key = (m.get("catalogId") or m.get("securityControl", {}).get("catalogueId") or "?")
        catalogs[key] = catalogs.get(key, 0) + 1
    return {"count": len(maps), "by_catalog_id": catalogs}


def backup_profile(base_url: str, api_key: str, profile: dict, maps: list[dict],
                   backup_dir: Path) -> Path:
    backup_dir.mkdir(parents=True, exist_ok=True)
    ts = _dt.datetime.now(_dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    safe = "".join(c if c.isalnum() or c in "-_." else "_" for c in profile["name"])
    out = backup_dir / f"{safe}_id{profile['id']}_{ts}.json"
    payload = {
        "exportedAt": _dt.datetime.now(_dt.timezone.utc).isoformat(),
        "baseUrl": base_url,
        "profile": profile,
        "mappings": maps,
        "summary": summarize_mappings(maps),
    }
    out.write_text(json.dumps(payload, indent=2))
    return out


def delete_mappings(base_url: str, api_key: str, maps: list[dict], dry_run: bool) -> int:
    """Delete profile mappings one-by-one (DELETE /api/profileMapping/<id>)."""
    deleted = 0
    for m in maps:
        mid = m.get("id") or m.get("profileMappingId")
        if not mid:
            continue
        if dry_run:
            deleted += 1
            continue
        status, _ = _http("DELETE", f"{base_url.rstrip('/')}/api/profileMapping/{mid}", api_key)
        if status not in (200, 204):
            print(f"  WARN: DELETE /api/profileMapping/{mid} returned {status}", file=sys.stderr)
            continue
        deleted += 1
    return deleted


def delete_profile(base_url: str, api_key: str, profile_id: int, dry_run: bool) -> bool:
    if dry_run:
        return True
    status, _ = _http("DELETE", f"{base_url.rstrip('/')}/api/profiles/{profile_id}", api_key)
    if status not in (200, 204):
        print(f"ERROR: DELETE /api/profiles/{profile_id} returned status={status}", file=sys.stderr)
        return False
    return True


def main() -> None:
    ap = argparse.ArgumentParser(description="Delete a stale RegScale security profile.")
    ap.add_argument("--base-url", required=True, help="https://your-tenant.regscale.com")
    ap.add_argument("--api-key", default=os.environ.get("REGSCALE_API_KEY"),
                    help="RegScale API token (or set REGSCALE_API_KEY env var)")
    ap.add_argument("--profile-name", required=True,
                    help='Exact RegScale profile name, e.g. "FedRAMP Rev 5 High Baseline"')
    ap.add_argument("--backup-dir", default="./backups", help="Where to write backup JSON")
    ap.add_argument("--skip-backup", action="store_true", help="Skip writing the backup")
    ap.add_argument("--yes", action="store_true", help="Skip interactive confirmation")
    ap.add_argument("--dry-run", action="store_true", help="Report only; don't change anything")
    args = ap.parse_args()

    if not args.api_key:
        print("ERROR: --api-key required (or set REGSCALE_API_KEY)", file=sys.stderr)
        sys.exit(1)

    print(f"==> Looking up profile {args.profile_name!r} on {args.base_url}")
    profile = find_profile(args.base_url, args.api_key, args.profile_name)
    if not profile:
        print(f"    No profile named {args.profile_name!r} found. Nothing to do.")
        sys.exit(0)
    pid = profile["id"]
    print(f"    Found: id={pid}  uuid={profile.get('uuid')}  owner={profile.get('profileOwner')}")

    print(f"==> Fetching mappings for profile {pid}")
    maps = get_mappings(args.base_url, args.api_key, pid)
    summary = summarize_mappings(maps)
    print(f"    Mappings: {summary['count']}")
    for cid, n in sorted(summary["by_catalog_id"].items(), key=lambda kv: str(kv[0])):
        print(f"      catalogId={cid}: {n} mappings")

    backup_path: Path | None = None
    if not args.skip_backup:
        backup_path = backup_profile(args.base_url, args.api_key, profile, maps,
                                     Path(args.backup_dir))
        print(f"==> Backup written: {backup_path}")
    else:
        print("==> Skipping backup (--skip-backup)")

    if args.dry_run:
        print("==> Dry run: would delete profile + mappings here. Stopping.")
        sys.exit(0)

    if not args.yes:
        print()
        print(f"  About to DELETE profile id={pid} ({profile['name']!r})")
        print(f"  and {summary['count']} mappings on {args.base_url}.")
        ans = input("  Type the profile name to confirm: ").strip()
        if ans != args.profile_name:
            print("  Aborted.")
            sys.exit(2)

    print(f"==> Deleting {summary['count']} mappings...")
    deleted = delete_mappings(args.base_url, args.api_key, maps, dry_run=False)
    print(f"    Deleted {deleted}/{summary['count']} mappings")

    print(f"==> Deleting profile id={pid}...")
    if not delete_profile(args.base_url, args.api_key, pid, dry_run=False):
        sys.exit(3)

    # Verify
    print("==> Verifying deletion")
    again = find_profile(args.base_url, args.api_key, args.profile_name)
    if again:
        print(f"    ERROR: profile id={again['id']} still present after delete", file=sys.stderr)
        sys.exit(3)
    print(f"    OK. Profile {args.profile_name!r} is gone.")

    if backup_path:
        print()
        print(f"Restore path (if needed): {backup_path}")


if __name__ == "__main__":
    main()
