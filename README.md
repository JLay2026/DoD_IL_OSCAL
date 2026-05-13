# DoD IL OSCAL Catalogs and Profiles (NIST SP 800-53 Rev 5)

**Version 2.1.0**

OSCAL 1.1.3 catalogs and profiles for the **DoD Cloud Computing SRG Impact Levels IL4 (Moderate), IL4 (High), IL5 (NSS), and IL6 (NSS)** and the **FedRAMP Rev 5 High Baseline**, plus parallel RegScale-format catalogs and profiles. All DoD content is reconciled directly to the official [DoD Rev 5 SSP Addendum spreadsheet](https://dl.dod.cyber.mil/wp-content/uploads/cloud/xls/rev5_ssp_addendum_controls.xlsx) and the [DoD Cloud Computing SRG](https://dl.dod.cyber.mil/wp-content/uploads/cloud/SRG/index.html). FedRAMP content is derived from the RegScale-published FedRAMP R5 High OSCAL-compliant catalog (dated 2024-07-31).

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
│   ├── dod-ccsrg-il4-moderate-profile.xml              # OSCAL 1.1.3 XML profile, 335 controls
│   ├── dod-ccsrg-il4-moderate-profile.json             # OSCAL 1.1.3 JSON profile, 335 controls
│   ├── dod-ccsrg-il4-high-profile.xml                  # OSCAL 1.1.3 XML profile, 419 controls
│   ├── dod-ccsrg-il4-high-profile.json                 # OSCAL 1.1.3 JSON profile, 419 controls
│   ├── dod-ccsrg-il5-nss-profile.xml                   # OSCAL 1.1.3 XML profile, 578 controls
│   ├── dod-ccsrg-il5-nss-profile.json                  # OSCAL 1.1.3 JSON profile, 578 controls
│   ├── dod-ccsrg-il6-nss-profile.xml                   # OSCAL 1.1.3 XML profile, 612 controls
│   ├── dod-ccsrg-il6-nss-profile.json                  # OSCAL 1.1.3 JSON profile, 612 controls
│   ├── dod-il5-nss-manifest-profile.xml                # OSCAL 1.1.3 XML profile, 578 controls
│   ├── dod-il5-nss-manifest-profile.json               # OSCAL 1.1.3 JSON profile, 578 controls
│   ├── fedramp-rev5-high-profile.xml                   # OSCAL 1.1.3 XML profile, 410 controls
│   ├── fedramp-rev5-high-profile.json                  # OSCAL 1.1.3 JSON profile, 410 controls
│   ├── dod_ccsrg_il4_moderate-regscale-profile.json    # RegScale-native profile + mappings
│   ├── dod_ccsrg_il4_high-regscale-profile.json        # RegScale-native profile + mappings
│   ├── dod_ccsrg_il5_nss-regscale-profile.json         # RegScale-native profile + mappings
│   ├── dod_ccsrg_il6_nss-regscale-profile.json         # RegScale-native profile + mappings
│   ├── dod_il5_nss_manifest-regscale-profile.json      # RegScale-native profile + mappings
│   ├── fedramp_rev5_high-regscale-profile.json         # RegScale-native profile + mappings
│   └── dod-ccsrg-regscale-profiles.json                # Combined RegScale export (5 profiles, 2,522 mappings)
├── catalogs/                                           # OSCAL + RegScale catalogs derived from the addendum
│   ├── dod-ccsrg-il4-moderate-catalog.json             # 335 controls, 18 families (OSCAL 1.1.3)
│   ├── dod-ccsrg-il4-high-catalog.json                 # 419 controls, 18 families (OSCAL 1.1.3)
│   ├── dod-ccsrg-il5-nss-catalog.json                  # 578 controls, 18 families (OSCAL 1.1.3)
│   ├── dod-ccsrg-il6-nss-catalog.json                  # 612 controls, 19 families (OSCAL 1.1.3)
│   ├── dod-il5-nss-manifest-catalog.json               # 578 slim metadata-only (OSCAL 1.1.3)
│   ├── fedramp-rev5-high-catalog.json                  # 410 controls, 18 families (OSCAL 1.1.3)
│   ├── dod-ccsrg-il4-moderate-catalog-regscale.json    # 335 controls (RegScale)
│   ├── dod-ccsrg-il4-high-catalog-regscale.json        # 419 controls (RegScale)
│   ├── dod-ccsrg-il5-nss-catalog-regscale.json         # 578 controls (RegScale)
│   ├── dod-ccsrg-il6-nss-catalog-regscale.json         # 612 controls (RegScale)
│   ├── dod-il5-nss-manifest-catalog-regscale.json      # 578 slim metadata-only (RegScale)
│   └── fedramp-rev5-high-catalog-regscale.json         # 410 controls (RegScale)
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

Each profile is shipped in **both OSCAL XML and OSCAL JSON** formats. The XML form matches RegScale's profile export shape exactly (verified against a live RegScale 6.x export). Each profile contains:

- `metadata.title` — short baseline name (e.g. `DoD IL5 w/ NSS Overlay`)
- `metadata.version` (`1.0.1`), `metadata.oscal-version` (`1.1.3`), `metadata.last-modified`, deterministic profile UUID
- `metadata.roles` — `creator` and `contact`, both titled `Document Creator`
- `metadata.parties` — RegScale, Inc. as organization party with full address
- `metadata.responsible-parties` — `creator` and `contact` both resolve to the RegScale party
- `import.href` — fragment-style reference (`#<catalog-uuid>`) to the corresponding catalog
- `import.include-controls.with-id` — explicit list of every control ID in lowercase OSCAL form (e.g. `ac-2.1`), sorted in NIST family/number/enhancement order

Validation: all 5 profiles pass structural conformance — required fields, valid UUID format, ISO-8601 dates, OSCAL 1.1.3 version stamp — and reference integrity: every `with-id` entry resolves to a real control in the linked catalog.

### RegScale-native profile exports

Each baseline also ships a `*-regscale-profile.json` file matching RegScale's native profile-export envelope (verified against a live export):

```json
{
  "profile": { /* 16-field metadata block */ },
  "mappings": [ /* per-control mapping objects */ ],
  "exportDate": "<ISO timestamp>",
  "exportVersion": 1.0
}
```

Each mapping object includes `profileMappingId`, `controlId`, `controlIdentifier` (e.g. `AC-2(1)`), `controlGuid` (deterministic UUIDv5 over `catalogGuid + controlIdentifier`), `controlTitle` (zero-padded — `AC-02(01) - Account Management | Automated System Account Management`), `catalogId`, `catalogGuid`, `catalogTitle`, and `catalogUrl`.

The combined file `dod-ccsrg-regscale-profiles.json` aggregates all 5 profiles and 2,522 total mappings into a single export envelope.

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

Produces `build/dod-ccsrg-il5-nss-resolved-catalog.json` — a single OSCAL catalog containing all 578 controls.

## Using this in an SSP

```json
"import-profile": {
  "href": "https://your-org/path/to/dod-ccsrg-il5-nss-profile.json"
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
| FedRAMP Rev 5 Baselines (program page) | https://www.fedramp.gov/rev5/baselines/ |
| FedRAMP R5 High catalog (RegScale OSCAL-compliant copy, 2024-07-31) | https://regscaleblob.blob.core.windows.net/catalogs/fedramp_r5_high_oscal_compliant.json |
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
| 1.0.0 | First stable release. All catalogs and profiles bumped to version 1.0.0. Repository renamed to `DoD_IL_OSCAL` and published to GitHub. |
| 1.0.1 | Profile generators rewritten to match actual RegScale 6.x export format. OSCAL profiles now emit both XML and JSON (XML matches RegScale's exported shape verbatim — minimal metadata with `creator`/`contact` roles, RegScale party, fragment-style `import.href`, sorted `with-id` elements). RegScale-native profile JSON files use the wrapped `{profile, mappings, exportDate, exportVersion}` envelope verified against a live export. Combined RegScale file (`dod-ccsrg-regscale-profiles.json`) aggregates 5 profiles + 2,522 mappings. Legacy `dod-il5-rev5-profile.json` and per-baseline `*-regscale-profile.xlsx` files removed. |
| 1.1.0 | Added FedRAMP Rev 5 HIGH Baseline catalog and profile in both OSCAL 1.1.3 (XML + JSON) and RegScale-native formats. 410 controls (191 base + 219 enhancements) across 18 families, derived from the RegScale-published FedRAMP R5 High OSCAL-compliant catalog (2024-07-31). All artifacts share UUID `0ef6e235-dee5-4c19-b8f0-d360e5d8f611` for cross-linking. Full parameter values, control objectives, assessment tests, and related-control links preserved. |
| 1.1.1 | Profile import fix. Added required FedRAMP metadata `props` array to `fedramp-rev5-high-profile.json` and `.xml` (RegScale OSCAL importer rejected v1.1.0 with: `Missing or invalid "props" array in the metadata`). Props: `marking` = Controlled Unclassified Information; `keywords`; FedRAMP-namespaced `resolution-tool` = RegScale, `profile-type` = baseline, `sensitivity-level` = high. No control changes — all 410 `with-id` entries and catalog UUID linkage preserved. |
| 1.1.2 | Extended the v1.1.1 props fix to all five DoD OSCAL profiles (XML + JSON): IL4 Moderate, IL4 High, IL5 NSS, IL6 NSS, IL5 NSS Manifest. Each now carries 7 metadata props — `marking`, `keywords`, and DoD-namespaced (`https://public.cyber.mil/dccs/ns/oscal`) `resolution-tool`, `profile-type`, `impact-level` (il4/il5/il6), `sensitivity-level` (moderate/high), and `nss` (true/false). No control changes — all `with-id` counts (335/419/578/612/578) and catalog `href` UUIDs preserved. |
| 1.2.0 | Replaced RegScale-export envelopes with RegScale API-import payloads. The 6 per-profile RegScale JSON files plus the combined `dod-ccsrg-regscale-profiles.json` now match the POST bodies produced by `oscal_profile_to_regscale.py` (`/api/profiles` profile body + `/api/profileMapping/batchCreate` mapping batch + optional `/api/catalog-templates` payload). Mappings use `controlIdentifier` (zero-padded, e.g. `AC-01(01)`) for tenant-side resolution to integer `controlID`. `profileID` and integer `controlID` carry the sentinel `"<resolved-at-import>"`. `catalogTemplate` is `null` because none of the current OSCAL profiles carry `modify.set-parameters`. Control counts preserved: IL4 Mod=335, IL4 High=419, IL5 NSS=578, IL6 NSS=612, IL5 Manifest=578, FedRAMP High=410. Combined aggregate: 5 profiles, 2,522 mappings. |
| 1.2.1 | Added RegScale export-envelope JSON alongside the v1.2.0 API-import payloads. Each profile now ships in two RegScale-format shapes: `*-regscale-profile.json` (script-compatible API-import payload — unchanged from v1.2.0) and `*-regscale-export.json` (round-trippable export envelope — `{profile, mappings, exportDate, exportVersion}` with full per-mapping decoration: `profileMappingId`, `controlId`, `controlIdentifier`, `controlGuid`, `controlTitle`, `catalogId`, `catalogGuid`, `catalogTitle`, `catalogUrl`). `controlGuid` is deterministic UUIDv5 over `(catalogGuid, controlIdentifier)` — matches v1.1.2 export values exactly. Combined `dod-ccsrg-regscale-export.json` aggregates the 5 DoD export envelopes (5 profiles, 2,522 mappings). OSCAL artifacts and catalogs unchanged. |
| 2.0.0 | BREAKING. Unified RegScale catalog: all RegScale profile artifacts (12 files — 6 API-import + 6 export envelope, plus 2 combined DoD aggregates) now point at a single shared source catalog: `catalogs/cnssi-1253-dow-rev5-catalog.json` (“DoW — NIST 800-53 — Rev 5 (CNSSI 1253)”, RegScale id=219, UUID `476dbabf-f394-4375-8ddd-0a13f34c2f82`, 1,014 controls). Per-mapping `controlGuid` values now come from the DoW catalog’s real RegScale tenant UUIDs (no longer UUIDv5-derived). Per-mapping `controlId` integers come from DoW’s real RegScale integer ids (e.g. AC-01=1015). The 5 per-baseline RegScale catalog files (`*-catalog-regscale.json` for IL4 Mod, IL4 High, IL5 NSS, IL6 NSS, IL5 Manifest, FedRAMP High) have been removed — RegScale-format users should use the DoW catalog as the single source of truth. Validated: zero unmatched controls, zero drift in control selection vs v1.2.1 (335/419/578/612/578/410 — identical). OSCAL XML/JSON profiles and OSCAL catalogs unchanged. |
| **2.1.0** | **Repository reorganization: `profiles/` now contains only the 7 RegScale export envelopes (6 per-baseline + 1 combined DoD aggregate). All 19 non-export files — 5 DoD OSCAL JSON profiles, 5 DoD OSCAL XML profiles, 1 FedRAMP OSCAL JSON profile, 1 FedRAMP OSCAL XML profile, 6 RegScale API-import `*-regscale-profile.json` payloads, and the combined RegScale API-import aggregate — moved to `profiles/archive/`. RegScale export-envelope JSON is now the sole shipped profile format. Archived files preserved with `git mv` for full history. No content changes; no control selection changes. The OSCAL XML/JSON profiles and OSCAL catalogs remain valid — they're simply housed under `profiles/archive/` to spotlight the export envelopes as the primary deliverable.** |

## License

Profile content: [CC0 1.0 Universal](https://creativecommons.org/publicdomain/zero/1.0/) (same posture as upstream NIST OSCAL content).
