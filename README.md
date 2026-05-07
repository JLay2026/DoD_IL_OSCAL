# DoD IL OSCAL Catalogs and Profiles (NIST SP 800-53 Rev 5)

**Version 1.0.0**

OSCAL 1.1.3 catalogs and profiles for the **DoD Cloud Computing SRG Impact Levels IL4 (Moderate), IL4 (High), IL5 (NSS), and IL6 (NSS)**, plus parallel RegScale-format catalogs and profiles. All content is reconciled directly to the official [DoD Rev 5 SSP Addendum spreadsheet](https://dl.dod.cyber.mil/wp-content/uploads/cloud/xls/rev5_ssp_addendum_controls.xlsx) and the [DoD Cloud Computing SRG](https://dl.dod.cyber.mil/wp-content/uploads/cloud/SRG/index.html).

> **Status: community release.** Not an official DISA or DoD publication. The control selection and DoD parameter values are taken verbatim from the addendum spreadsheet, but should still be cross-checked against the current SRG release before any authorization use.

## Reconciliation summary

The official `' IL5 (NSS)'` sheet contains **588 rows**:

| Row class | Count | Treatment |
|---|---:|---|
| NIST 800-53 Rev 5 controls | **578** | Included in the OSCAL profile |
| GRR-* General Readiness Requirements | 10 | Excluded (non-NIST policy items, not OSCAL-modelable) |

All **578** NIST controls cross-validated against the NIST SP 800-53 Rev 5 catalog — every ID resolves.

## Profile composition

| Group | Count | Source | Profile tag |
|---|---:|---|---|
| Baseline (FedRAMP High ⇒ NIST HIGH) | **362** | NIST HIGH baseline profile, flagged `Yes` in addendum | (untagged - inherited from base) |
| FedRAMP+ overlay (FedRAMP-High-only) | **38** | Catalog: PT family, IR-9.x, SC-12.2/3, SC-45.x, IA-2.6/10, IA-5.7, AC-2.7/9, SI-4.11/16, etc. | `il5-fedramp-plus-additions` |
| NSS overlay (the canonical 178) | **178** | Catalog: CNSSI 1253-derived NSS adds (AC-3(4), AC-7, AC-12(1)/(2), AC-16, AC-17(6)/(9)/(10), AC-23, AT-2(4)/(5)/(6), full SA-8 family, etc.) | `il5-nss-overlay` |
| **Total** | **578** | | |

The 178 NSS additions exactly match the figure cited in CC SRG v1r4 / v1r3 release notes ("178 net-new controls for IL5 NSS").

## DoD-Specified Parameter Values (DSPAV)

**21 set-parameter** entries override FedRAMP-default values per the addendum:

| Control | Parameter | DoD value (from addendum) |
|---|---|---|
| AC-7(a) | number / time period | three (3) consecutive failures (privileged); fifteen (15) minutes |
| AU-5(1) | percentage / time period | seventy-five percent (75%); one month before negative impact |
| CM-7(5)(c) | review frequency | at least quarterly or when there is a change |
| IA-5(1)(a) | password update freq | at least quarterly |
| IA-5(1)(h) | composition rules | minimum 15 characters across 4 character classes; modify ≥50% on change |
| MA-6 | maintenance time period | timeframe to support advertised uptime/availability |
| PS-3(4) | citizenship | U.S. citizens / nationals / persons; admins must be U.S. citizens/nationals/persons |
| PS-4 | termination disable | one (1) hour |
| SA-4(5)(a) | security configurations | DoDI 8510.01 + STIGs/SRGs |
| SA-9(1)(b) | approval authority | DoD Component CIO or delegate(s) |
| SA-9(5) | location restriction | U.S./U.S. Territories or U.S.-jurisdiction locations; all data, systems, or services |
| SC-17 | certificate policy | DoDI 8520.02 (PKI/PKE) |
| SC-18(4) | mobile code apps | email, scriptable office documents with embedded code |
| SC-24 | fail-secure state | known secure state; all failure types; all components |

Every parameter ID has been validated against the NIST Rev 5 catalog.

## Repository layout

```
DoD_IL_OSCAL/
├── profiles/
│   └── dod-il5-rev5-profile.json                       # OSCAL 1.1.3 profile (IL5 NSS)
├── catalogs/                                           # OSCAL + RegScale catalogs derived from the addendum
│   ├── dod-ccsrg-il4-moderate-catalog.json             # 335 controls, 18 families (OSCAL 1.1.3)
│   ├── dod-ccsrg-il4-high-catalog.json                 # 419 controls, 18 families (OSCAL 1.1.3)
│   ├── dod-ccsrg-il5-nss-catalog.json                  # 578 controls, 18 families (OSCAL 1.1.3)
│   ├── dod-ccsrg-il6-nss-catalog.json                  # 612 controls, 19 families (OSCAL 1.1.3)
│   ├── dod-il5-nss-manifest-catalog.json               # 578 slim metadata-only (OSCAL 1.1.3)
│   ├── dod-ccsrg-il4-moderate-catalog-regscale.json    # 335 controls (RegScale)
│   ├── dod-ccsrg-il4-high-catalog-regscale.json        # 419 controls (RegScale)
│   ├── dod-ccsrg-il5-nss-catalog-regscale.json         # 578 controls (RegScale)
│   ├── dod-ccsrg-il6-nss-catalog-regscale.json         # 612 controls (RegScale)
│   └── dod-il5-nss-manifest-catalog-regscale.json      # 578 slim metadata-only (RegScale)
├── references/
│   ├── NIST_SP-800-53_rev5_HIGH-baseline_profile.json  # Upstream NIST profile
│   ├── rev5_ssp_addendum_controls.xlsx                 # DoD authoritative XLSX
│   └── il5-nss-control-manifest.csv                    # Per-control traceability table
├── scripts/
│   └── resolve.sh                                      # Profile → flattened catalog
└── README.md
```

## OSCAL catalogs (derived from the addendum)

The `catalogs/` directory contains five OSCAL 1.1.3 catalogs converted directly from the DoD Rev 5 SSP Addendum spreadsheet plus the IL5 NSS manifest CSV. Each catalog stands on its own (no profile resolution required) and is suitable for direct import into OSCAL-aware tooling.

| Catalog | Source sheet/file | Controls | Families |
|---|---|---:|---:|
| `dod-ccsrg-il4-moderate-catalog.json` | XLSX sheet `IL4 Moderate` | 335 | 18 |
| `dod-ccsrg-il4-high-catalog.json` | XLSX sheet `IL4 High` | 419 | 18 |
| `dod-ccsrg-il5-nss-catalog.json` | XLSX sheet `' IL5 (NSS)'` | 578 | 18 |
| `dod-ccsrg-il6-nss-catalog.json` | XLSX sheet `IL6 (NSS)` | 612 | 19 |
| `dod-il5-nss-manifest-catalog.json` | `il5-nss-control-manifest.csv` | 578 | 18 |

### Catalog contents

The four full-text catalogs (IL4 Mod, IL4 High, IL5 NSS, IL6 NSS) preserve the addendum's full control text. Each control entry includes:

- `id` (OSCAL form, e.g. `ac-2.1`) and `class` (`SP800-53` or `SP800-53-enhancement`)
- `title` and `props` — `label`, `sort-id`, `responsible-role`, and `leveraged-from-fedramp-baseline` (where present)
- `params` parsed from `[Assignment: ...]` and `[Selection: ...]` markers in the addendum text
- `links` to related controls
- `parts`:
  - `statement` (with nested item enumeration)
  - `guidance`
  - `fedramp-parameter-values` and `fedramp-additional-guidance` where present in the addendum
  - `dod-fedramp-plus-parameters` for any DoD-specific overrides

DoD-specific properties and parts use namespace `https://dod.cyber.mil/ns/oscal` so they round-trip through standard OSCAL tooling without colliding with NIST/FedRAMP namespaces.

The slim manifest catalog (`dod-il5-nss-manifest-catalog.json`) is metadata-only — each entry has `id`, `title`, family/baseline props, and a `link` back to the upstream NIST control. Use it when you need a lightweight traceability artifact rather than full text.

### Notes on coverage

- All five catalogs structurally validate (well-formed OSCAL 1.1.3, every internal `param` reference resolves, every control ID is unique).
- `GRR-*` rows from each sheet (10 in IL4/IL5, 6 in IL6) are excluded — they are DoD General Readiness Requirements, not NIST controls, and are not OSCAL-modelable as catalog entries.
- `related-control` links may reference controls outside a given catalog's scope (e.g. an IL4 Moderate control referencing an enhancement that only appears at IL5). These are informational, not validation errors.
- IL6 (NSS) is the only level that includes a `pm` family entry (PM-12), hence its 19-family count vs. 18 in the others.

## OSCAL profiles (one per catalog)

Five OSCAL 1.1.3 profile files in `profiles/` import their corresponding catalog from `catalogs/` via relative href and include all of that catalog's controls.

| Profile | Imports catalog | Controls included |
|---|---|---:|
| `dod-ccsrg-il4-moderate-profile.json` | `dod-ccsrg-il4-moderate-catalog.json` | 335 |
| `dod-ccsrg-il4-high-profile.json` | `dod-ccsrg-il4-high-catalog.json` | 419 |
| `dod-ccsrg-il5-nss-profile.json` | `dod-ccsrg-il5-nss-catalog.json` | 578 |
| `dod-ccsrg-il6-nss-profile.json` | `dod-ccsrg-il6-nss-catalog.json` | 612 |
| `dod-il5-nss-manifest-profile.json` | `dod-il5-nss-manifest-catalog.json` | 578 |

Each profile contains:
- `metadata.title`, `version`, `oscal-version: 1.1.3`, `last-modified`, deterministic UUID
- `metadata.props` with DoD-namespaced impact-level/categorization/CIA values (`ns="https://dod.cyber.mil/ns/oscal"`) plus FedRAMP-style marking and keywords
- `metadata.links` to the CC SRG and the DoD Rev 5 SSP Addendum (authoritative source)
- `metadata.parties` and `responsible-parties` (DoD CIO as profile author)
- `imports[].href` — relative path to the sibling catalog file
- `imports[].include-controls[].with-ids` — explicit list of every control ID in the catalog (sorted in NIST family/number/enhancement order)
- `merge.as-is: true` — preserves the catalog's family group structure after profile resolution
- `back-matter.resources` — the catalog file, the addendum XLSX, and the CC SRG, each with proper `rlinks` and `media-type`

Validation: all 5 new profiles pass structural conformance (required fields, valid UUID format, ISO-8601 dates, OSCAL 1.1.3 version stamp) and reference integrity (every `with-ids` entry resolves to a real control in the linked catalog, every `back-matter` resource UUID is RFC 4122 compliant).

The original `dod-il5-rev5-profile.json` (v0.2 IL5 NSS) is kept as a legacy artifact — it uses fragment-style `href` (`#nist-800-53r5-high-profile`) into back-matter resources to point at the upstream NIST profile and catalog, plus the 21 verified DoD parameter overrides as `modify.set-parameters`. Use it when you need the parameter overrides; use the new IL5 NSS profile (`dod-ccsrg-il5-nss-profile.json`) for the simpler catalog-import workflow.

## RegScale-format catalogs

The `*-regscale.json` files in `catalogs/` are derived from the OSCAL catalogs and follow the **RegScale catalog schema** (the same shape used by RegScale's published FedRAMP R5 High catalog, `fedramp_r5_high_oscal_compliant.json`). They are intended for direct import into RegScale and other tools that consume that schema. RegScale's importer requires `title` on every control — these files satisfy that.

Key shape differences vs. standard OSCAL:

| OSCAL field | RegScale field |
|---|---|
| `catalog.metadata.title` | `catalog.title` (flat) |
| `catalog.groups[].controls[]` (nested) | `catalog.securityControls[]` (flat list) |
| `id` (e.g. `ac-2.1`) | `controlId` (`AC-2(1)`) + `otherId` (`ac-2.1`) + `sortId` (`ac-02.01`) |
| `title` | `title` (rendered as `XX-NN[(NN)] - Name`) |
| `params[]` | `parameters[]` (objects with `parameterId`, `text`, `default`, etc.) |
| `parts[type=statement]` (with nested items) | `objectives[]` array + HTML-rendered `description` |
| `parts[type=guidance]` and FedRAMP/DoD parameter parts | Concatenated into `description` HTML under bold section headings |
| `links[rel=related]` | `relatedControls` (comma-separated string) |
| Group titles | `family` field (string) on each control |

DoD-specific data is preserved:

- `leveragedFromFedRAMPBaseline` extra field on each control (RegScale ignores unknown fields)
- DoD FedRAMP+ parameter values are inlined into `description` under a `<strong>DoD FedRAMP+ Parameters</strong>` heading

UUIDs are deterministic (UUIDv5 over a stable key), so the same input produces the same UUIDs every run — enables idempotent re-imports.

## Per-control traceability

`references/il5-nss-control-manifest.csv` lists every IL5 (NSS) control with:

- `srg_id` — original DoD SRG identifier (e.g. `AC-2(1)`)
- `oscal_id` — OSCAL form (e.g. `ac-2.1`)
- `family`, `name`
- `leveraged_from_fedramp_high` — direct from XLSX column 15
- `in_nist_high_baseline` — whether the control is in NIST HIGH (vs. FedRAMP High-only)
- `profile_group` — which OSCAL group the control lands in
- `dod_param_present` — whether the addendum specifies a DoD FedRAMP+ parameter override

## Resolving the profile

OSCAL profiles must be *resolved* into a flattened catalog before use in an SSP. Use [oscal-cli](https://github.com/metaschema-framework/oscal-cli):

```bash
./scripts/resolve.sh
```

Produces `build/dod-il5-rev5-resolved-catalog.json` — a single OSCAL catalog containing all 578 controls with DoD parameter values applied.

## Using this in an SSP

```json
"import-profile": {
  "href": "https://your-org/path/to/dod-il5-rev5-profile.json"
}
```

Your SSP's `control-implementation` block then must have an `implemented-requirement` for every one of the 578 controls (or document inheritance from a leveraged authorization).

## NSS vs. non-NSS

This profile represents the **IL5 with NSS overlay** baseline. For a non-NSS IL5 system, remove the `il5-nss-overlay` `include-controls` group from import #2 before resolution — that drops the 178 NSS-specific controls and leaves the 362 baseline + 38 FedRAMP+ controls (400 total). Note: the addendum spreadsheet currently only ships the IL5 NSS sheet for Rev 5, so the non-NSS variant is not separately authoritative as of this writing.

## Authoritative sources used

| Source | URL |
|---|---|
| **DoD Rev 5 SSP Addendum XLSX (sheet ' IL5 (NSS)')** | https://dl.dod.cyber.mil/wp-content/uploads/cloud/xls/rev5_ssp_addendum_controls.xlsx |
| DoD CC SRG | https://dl.dod.cyber.mil/wp-content/uploads/cloud/SRG/index.html |
| NIST 800-53 Rev 5 catalog (OSCAL) | https://github.com/usnistgov/oscal-content |
| NIST 800-53 Rev 5 HIGH baseline (OSCAL) | https://raw.githubusercontent.com/usnistgov/oscal-content/main/nist.gov/SP800-53/rev5/json/NIST_SP-800-53_rev5_HIGH-baseline_profile.json |
| CNSSI No. 1253 | https://www.cnss.gov/CNSS/issuances/Instructions.cfm |

## Versioning

| Version | Notes |
|---|---|
| 0.1.0-draft | Initial scaffold (estimated NSS list) |
| 0.2.0-draft | Reconciled to official Rev 5 SSP Addendum XLSX. 578 controls, 178 NSS adds verified. |
| 0.3.0-draft | Added five derived OSCAL catalogs (IL4 Mod, IL4 High, IL5 NSS, IL6 NSS, IL5 NSS slim manifest). |
| 0.4.0-draft | Added parallel RegScale-format catalogs (`*-regscale.json`) matching the schema of FedRAMP R5 High RegScale catalogs. |
| 0.5.0-draft | Added RegScale-format security profiles as JSON. |
| 0.6.0-draft | Added RegScale profile XLSX files alongside JSON. |
| 0.7.0-draft | Removed RegScale profile files (JSON + XLSX). RegScale catalogs in `catalogs/` retained. |
| 0.8.0-draft | Added 5 OSCAL 1.1.3 profile files (one per catalog) with relative-href catalog imports, DoD-namespaced impact-level props, and back-matter resources. |
| 0.9.0-draft | Re-added RegScale-format profile files (6 JSON + 6 XLSX) alongside the OSCAL profiles. Both formats coexist in `profiles/`. |
| **1.0.0** | **First stable release. All catalogs and profiles bumped to version 1.0.0. Repository renamed to `DoD_IL_OSCAL` and published to GitHub.** |

## License

Profile content: [CC0 1.0 Universal](https://creativecommons.org/publicdomain/zero/1.0/) (same posture as upstream NIST OSCAL content).
