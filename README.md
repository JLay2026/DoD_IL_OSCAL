# DoD IL OSCAL Catalogs and Profiles (NIST SP 800-53 Rev 5)

**Version 2.4.0**

OSCAL 1.1.3 catalogs and profiles for the **DoD Cloud Computing SRG Impact Levels IL4 Moderate, IL4 High, IL5 NSS, and IL6 NSS** and the **FedRAMP Rev 5 High Baseline**, packaged as ready-to-import **RegScale export envelopes** that target the DoW CNSSI 1253 catalog.

All DoD content is reconciled directly to the [DoD Rev 5 SSP Addendum spreadsheet](https://dl.dod.cyber.mil/wp-content/uploads/cloud/xls/rev5_ssp_addendum_controls.xlsx) and the [DoD Cloud Computing SRG](https://dl.dod.cyber.mil/wp-content/uploads/cloud/SRG/index.html). FedRAMP content is derived from the RegScale-published FedRAMP R5 High OSCAL-compliant catalog (2024-07-31).

> **Status: community release.** Not an official DISA or DoD publication. Cross-check against the current SRG release before any authorization use.

---

## What's in the box

```
DoD_IL_OSCAL/
├── catalogs/
│   ├── cnssi-1253-dow-rev5-catalog.json       ← unified RegScale source (1,014 controls)
│   ├── dod-ccsrg-il4-moderate-catalog.json    ← 335 (OSCAL 1.1.3)
│   ├── dod-ccsrg-il4-high-catalog.json        ← 419
│   ├── dod-ccsrg-il5-nss-catalog.json         ← 578
│   ├── dod-ccsrg-il6-nss-catalog.json         ← 612
│   ├── dod-il5-nss-manifest-catalog.json      ← 578 (slim metadata-only)
│   └── fedramp-rev5-high-catalog.json         ← 410
├── profiles/
│   ├── fedramp_rev5_high-regscale-export.json          ← 410 mappings
│   ├── dod_ccsrg_il4_moderate-regscale-export.json     ← 335
│   ├── dod_ccsrg_il4_high-regscale-export.json         ← 419
│   ├── dod_ccsrg_il5_nss-regscale-export.json          ← 578
│   ├── dod_ccsrg_il6_nss-regscale-export.json          ← 612
│   ├── dod_il5_nss_manifest-regscale-export.json       ← 578
│   ├── dod-ccsrg-regscale-export.json                  ← 5 DoD profiles combined (2,522 mappings)
│   └── archive/                                        ← OSCAL 1.1.3 XML+JSON profiles (12 files)
├── references/                                         ← NIST baselines, DoD XLSX, IL5 NSS manifest CSV
└── scripts/
    ├── regscale_cleanup.py    ← purge a stale RegScale profile + verify
    └── regscale_rebind.py     ← re-target export envelopes to a new tenant's catalog ids
```

## Per-profile control counts

| Profile | Mappings | Notes |
|---|---:|---|
| IL4 Moderate | 335 | Lowest impact baseline |
| IL4 High | 419 | |
| IL5 NSS | 578 | 362 FedRAMP-High base + 38 FedRAMP+ overlay + 178 NSS overlay |
| IL6 NSS | 612 | |
| IL5 NSS Manifest | 578 | Slim metadata-only variant |
| FedRAMP Rev 5 High | 410 | 191 base + 219 enhancements, 18 families |
| **Combined (5 DoD profiles)** | **2,522** | `dod-ccsrg-regscale-export.json` |

---

## RegScale export envelope shape

Each `*-regscale-export.json` is a round-trippable export of `{profile, mappings, exportDate, exportVersion}` that RegScale can re-ingest via the UI. Per-mapping fields:

```json
{
  "profileMappingId": 5001,
  "controlId": 10756,
  "controlIdentifier": "AC-01",
  "controlGuid": "4bed009e-58d4-4ea1-9ffd-e6f2afaf2c5f",
  "controlTitle": "AC-01 - Policy and Procedures",
  "catalogId": 24,
  "catalogGuid": "476dbabf-f394-4375-8ddd-0a13f34c2f82",
  "catalogTitle": "DoW - NIST 800-53 - Rev 5 (CNSSI 1253)",
  "catalogUrl": "https://cybersecurityks.osd.mil/dodcs/ControlsandAuthorization/securitycontrols/"
}
```

Three identifiers carry the lookup; all three must align with the tenant catalog:

| Field | Source | Stability across tenants |
|---|---|---|
| `controlGuid` | `securityControl.uuid` | **Stable** — same UUID in every tenant |
| `controlIdentifier` | `securityControl.controlId` | **Stable** — padded format (`AC-01`, `AC-02(01)`) |
| `controlId` (int) | `securityControl.id` | **Tenant-local** — must be remapped per tenant |
| `catalogId` (int) | `catalog.id` | **Tenant-local** — must be remapped per tenant |
| `catalogGuid` | `catalog.uuid` | **Stable** — `476dbabf-f394-4375-8ddd-0a13f34c2f82` |

---

## Importing into a new RegScale tenant

The repo ships with files pre-bound to a specific tenant (`catalog.id=24`, `controlId` range 10756..11769). If you're importing into a different tenant, you **must** rebind first — see below.

### Step 1: Load the DoW catalog (one-time per tenant)

The DoW CNSSI 1253 catalog must exist in the tenant before any profile import. Either:

- Import `catalogs/cnssi-1253-dow-rev5-catalog.json` directly through RegScale's catalog import flow, **or**
- Confirm the catalog already exists by UUID `476dbabf-f394-4375-8ddd-0a13f34c2f82`.

Note the tenant-assigned `catalog.id` — RegScale's UI shows this on the catalog detail page (e.g. id=24).

### Step 2: Rebind the export envelopes to the tenant's catalog

The shipped files reference a specific tenant's integer ids. Rebind with the bundled script:

```bash
export REGSCALE_API_KEY=<token>

# Dry-run first (recommended)
python scripts/regscale_rebind.py \
    --base-url https://your-tenant.regscale.com \
    --dry-run

# Rewrite all 7 export files in place
python scripts/regscale_rebind.py \
    --base-url https://your-tenant.regscale.com

# Or just one profile, written to a different directory
python scripts/regscale_rebind.py \
    --base-url https://your-tenant.regscale.com \
    --profile fedramp_rev5_high \
    --output-dir ./out
```

The script:
1. Looks up the DoW catalog by stable UUID `476dbabf-f394-4375-8ddd-0a13f34c2f82` (falls back to exact title).
2. Fetches every `securityControl` from that catalog and indexes by stable UUID and padded `controlId`.
3. For each export envelope, rewrites:
   - `catalogId` → tenant's `catalog.id`
   - `controlId` (int) → tenant's `securityControl.id`
   - Catalog refs (`catalogGuid`, `catalogTitle`, `catalogUrl`) refreshed from the live catalog
4. Validates **every** mapping resolves by all three keys before writing.
5. Refuses to write any file if any mapping cannot resolve in the target catalog.

### Step 3: Import the rebound profile in the RegScale UI

In RegScale: **Catalogs & Profiles → Profiles → Import** → upload the rebound `*-regscale-export.json`. After import, verify:

- The profile shows the expected mapping count (e.g. 410 for FedRAMP High)
- The mappings tab lists controls bound to the DoW catalog (not IL4/IL5/other)

### Step 4 (if needed): Clear a stale prior import

If the profile was previously imported against the wrong catalog (e.g. the FedRAMP 257-of-410 case), delete it first with the cleanup script:

```bash
# Dry-run with backup
python scripts/regscale_cleanup.py \
    --base-url https://your-tenant.regscale.com \
    --profile-name "FedRAMP Rev 5 High Baseline" \
    --dry-run

# Real delete (writes a backup JSON first, then asks for confirmation)
python scripts/regscale_cleanup.py \
    --base-url https://your-tenant.regscale.com \
    --profile-name "FedRAMP Rev 5 High Baseline"
```

The cleanup script writes a timestamped backup of the profile + all mappings to `./backups/` before deleting, asks for the profile name as confirmation, then removes all mappings and the profile itself.

---

## Re-validating IDs when generating in a new tenant

When the source-of-truth catalog moves to a new tenant (or the tenant rebuilds its catalog), do **all** of these checks before publishing rebound envelopes:

### 1. Catalog UUID match
The DoW catalog UUID **must** stay `476dbabf-f394-4375-8ddd-0a13f34c2f82`. If the tenant has multiple catalogs with similar titles, look up by UUID — not by name. The rebind script enforces this.

### 2. Catalog has all 1,014 controls
After loading the DoW catalog into the tenant, fetch its `securityControls` and confirm:
- Total count = 1,014
- All 20 NIST families present: `AC, AT, AU, CA, CM, CP, IA, IR, MA, MP, PE, PL, PM, PS, PT, RA, SA, SC, SI, SR`
- Every `controlId` is in **padded** form: `AC-01`, `AC-02(01)`, `CM-03(06)` (not `AC-1`, `AC-2(1)`)

### 3. Per-control UUID stability
Spot-check 5 known UUIDs against the new tenant:

| controlId | Expected UUID |
|---|---|
| AC-01 | `4bed009e-58d4-4ea1-9ffd-e6f2afaf2c5f` |
| AC-02 | `3bf56e40-566c-4668-8b84-78ccea8f70ae` |
| AC-02(01) | `5ce4dcb4-c2fc-4e5a-9d75-4e30db383c2c` |
| SR-12 | `d30371ad-c432-498f-801b-540880282ffd` |
| SI-04(11) | (look up in `catalogs/cnssi-1253-dow-rev5-catalog.json`) |

If UUIDs drift, the source catalog has been mutated — DO NOT proceed. Investigate before rebinding.

### 4. Integer ranges
The shipped files use range `10756..11769`. A different tenant will have a different integer range — the rebind script handles this automatically. **Do not** hand-edit integers; always use `regscale_rebind.py`.

### 5. Validation gate
After rebinding, run the validator inline (it's the same logic baked into `regscale_rebind.py`, but here as a one-shot check):

```bash
python - <<'PY'
import json, sys
from pathlib import Path

# Load the rebound catalog (use whatever path you saved the tenant export to)
catalog = json.load(open("catalogs/cnssi-1253-dow-rev5-catalog.json"))["catalog"]
by_uuid = {c["uuid"]: c for c in catalog["securityControls"]}
by_cid  = {c["controlId"]: c for c in catalog["securityControls"]}

ok = True
for f in sorted(Path("profiles").glob("*-regscale-export.json")):
    d = json.loads(f.read_text())
    maps = d["mappings"]
    fails = 0
    for m in maps:
        live = by_uuid.get(m["controlGuid"])
        if not live or live["controlId"] != m["controlIdentifier"] or live["id"] != m["controlId"]:
            fails += 1
    status = "PASS" if fails == 0 else f"FAIL ({fails})"
    print(f"{f.name:<55} n={len(maps):<5} {status}")
    ok = ok and fails == 0
sys.exit(0 if ok else 1)
PY
```

This must report **PASS** for every file with the expected counts (335 / 419 / 578 / 612 / 578 / 410 / 2,522) before importing.

### 6. Post-import smoke check
After importing one profile (e.g. FedRAMP High = 410), export it back out of RegScale and diff against the source:

- Mapping count matches
- `catalogId` and `catalogGuid` reference the DoW catalog (not IL4/IL6/other)
- A 5-control spot check (AC-01, AC-02(13), CP-09(05), SI-04(11), SR-12) shows the expected `controlId` ints

If the export shows `catalogId` pointing to a different catalog, the importer fell back to identifier-based resolution against the wrong catalog. Stop, run the cleanup script, fix the catalog binding, and re-import.

---

## Profile composition reference

### IL5 NSS — 578 controls

| Group | Count | Source | Tag |
|---|---:|---|---|
| Baseline (FedRAMP High ⇒ NIST HIGH) | 362 | NIST HIGH, flagged `Yes` in addendum | (inherited) |
| FedRAMP+ overlay (FedRAMP-High-only) | 38 | PT family, IR-9.x, SC-12.2/3, SC-45.x, IA-2.6/10, IA-5.7, AC-2.7/9, SI-4.11/16, etc. | `il5-fedramp-plus-additions` |
| NSS overlay (canonical 178) | 178 | CNSSI 1253-derived NSS adds | `il5-nss-overlay` |

The 178 NSS additions exactly match CC SRG v1r4 / v1r3 release notes ("178 net-new controls for IL5 NSS").

### DoD-Specified Parameter Values (DSPAV)

21 set-parameter entries override FedRAMP defaults per the addendum:

| Control | Parameter | DoD value |
|---|---|---|
| AC-7(a) | failures / lockout | 3 consecutive failures (privileged); 15 minutes |
| AU-5(1) | percentage / period | 75%; one month before negative impact |
| CM-7(5)(c) | review frequency | at least quarterly or when there is a change |
| IA-5(1)(a) | password update | at least quarterly |
| IA-5(1)(h) | composition | min 15 chars across 4 classes; modify ≥50% on change |
| MA-6 | maintenance | timeframe to support advertised uptime |
| PS-3(4) | citizenship | U.S. citizens / nationals / persons; admins U.S. only |
| PS-4 | termination disable | 1 hour |
| SA-4(5)(a) | configurations | DoDI 8510.01 + STIGs/SRGs |
| SA-9(1)(b) | approval | DoD Component CIO or delegate |
| SA-9(5) | location | U.S./territories / U.S.-jurisdiction |
| SC-17 | cert policy | DoDI 8520.02 (PKI/PKE) |
| SC-18(4) | mobile code | email, scriptable office documents |
| SC-24 | fail-secure | known secure state; all failure types |

Every parameter ID is validated against the NIST Rev 5 catalog.

### FedRAMP Rev 5 High — 410 controls

191 base controls + 219 enhancements across 18 families. Family breakdown:

```
AC:50  AT:6   AU:27  CA:16  CM:34  CP:35  IA:30  IR:24  MA:12
MP:10  PE:26  PL:7   PS:11  RA:13  SA:25  SC:35  SI:35  SR:14
```

---

## Authoritative sources

| Source | Use |
|---|---|
| [DoD Rev 5 SSP Addendum](https://dl.dod.cyber.mil/wp-content/uploads/cloud/xls/rev5_ssp_addendum_controls.xlsx) | DoD control selections + parameter values |
| [DoD Cloud Computing SRG](https://dl.dod.cyber.mil/wp-content/uploads/cloud/SRG/index.html) | DoD impact-level definitions |
| [NIST SP 800-53 Rev 5](https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final) | Underlying control catalog |
| [CNSSI 1253](https://www.cnss.gov/) | NSS overlay basis |
| [FedRAMP R5 High OSCAL catalog (RegScale)](https://github.com/RegScale/regscale-public-catalogs) | FedRAMP High baseline source |
| [RegScale OSCAL profile importer](https://github.com/RegScale/regscale-cli) | Reference for the API-import payload shape |

---

## Versioning

| Version | Notes |
|---|---|
| 1.0.0 | First stable release. OSCAL XML+JSON profiles + RegScale-native profile JSON. |
| 1.1.0 | Added FedRAMP Rev 5 High Baseline (410 controls) alongside the DoD profiles. |
| 1.1.1–1.1.2 | Added required `props` metadata array to OSCAL profiles (FedRAMP-namespaced for FedRAMP profile; DoD-namespaced for DoD profiles — `marking`, `keywords`, `resolution-tool`, `profile-type`, `impact-level`, `sensitivity-level`, `nss`). |
| 1.2.0–1.2.1 | RegScale profile artifacts switched to API-import payloads, then export envelopes alongside. |
| 2.0.0 | BREAKING. Unified RegScale catalog: all profile artifacts point at one shared `catalogs/cnssi-1253-dow-rev5-catalog.json`. Removed per-baseline RegScale catalogs. Zero control-selection drift. |
| 2.1.0 | Repository reorganization: `profiles/` holds only the 7 RegScale export envelopes. OSCAL XML/JSON profiles and API-import payloads moved to `profiles/archive/`. |
| 2.2.0 | Padded `controlIdentifier` to match catalog `controlId` (`AC-1` → `AC-01`). Did not fix the FedRAMP 257-of-410 import drop — see 2.3.0. |
| 2.3.0 | Live-tenant catalog retarget. Replaced static DoW catalog with live tenant export (`catalog.id=24`). Re-pointed all 7 export envelopes: `catalogId 219 → 24`, `controlId` ints remapped to tenant range (10756..11769). Root cause of the FedRAMP 257 bug: previous `catalogId=219` didn't exist in the tenant, so the importer fell back to IL4 catalogs which only carry 257 of FedRAMP's 410 controls. |
| **2.4.0** | **Cleanup + tenant-rebinding tooling. Removed stale `*-regscale-profile.json` API-import payloads from `profiles/archive/` (7 files, superseded by the export envelopes in `profiles/`). Removed unused `scripts/resolve.sh` (referenced a deleted profile path). Added `scripts/regscale_cleanup.py` (purge a stale profile + verify, with timestamped backup) and `scripts/regscale_rebind.py` (auto-discover the DoW catalog in any tenant by stable UUID, fetch live `securityControls`, rewrite every export envelope's `catalogId` and `controlId` integers, validate 100% resolution before writing). README rewritten to focus on current-state usage, with a new "Importing into a new RegScale tenant" walkthrough and a "Re-validating IDs when generating in a new tenant" checklist.** |

## License

Profile content: [CC0 1.0 Universal](https://creativecommons.org/publicdomain/zero/1.0/) (same posture as upstream NIST OSCAL content).
