# Design Plan — TPF Rear Enclosure

**Written and committed before any CAD, printing, or drawing work on this phase.**
See git history: this file precedes all model, drawing, and results commits.

Author: Abhinav Maddisetty
Plan committed: 2026-08-20
Hard deadline: **Friday, 2026-10-02**
Target early finish: 2026-09-25
Budget: 10–15 hrs/week · $75 materials cap

Scope: design the missing rear enclosure for the existing TPF front frame, and produce a complete
drawing, tolerance, and manufacturability package for it.

---

## 1) Background and problem statement

TPF V1.0 exists as functional hardware: a 3D-printed ABS front frame housing a 5" display, dual
speakers, a Raspberry Pi, and audio I/O, with labeled port cutouts and threaded inserts for
assembly. It has **no rear enclosure** — the back is fully open, with the Pi, driver board,
speakers, and cabling exposed.

The original CAD model for the front frame was lost with the machine it lived on. The printed part
survives.

This creates a specific and useful engineering problem. The front frame can no longer be edited —
only measured. Any new part must mate with it **as built**, including whatever deviation the
original print process introduced. Designing to that interface requires reverse-modeling the frame
from physical measurement, establishing what the FDM process can actually hold, and tolerancing the
new part against measured capability rather than assumed values.

**Objective:** a rear enclosure that assembles to the as-built front frame without rework, with a
fully toleranced drawing package, a tolerance stack-up on the mating interface driven by measured
process capability, and a manufacturability analysis.

---

## 2) Deliverables

- **D1 — Front frame reverse model.** SOLIDWORKS part reconstructed from caliper measurement, with
  a measurement record containing raw readings rather than nominals alone.
- **D2 — Rear enclosure.** New part designed against the as-built interface, printed and assembled
  onto the existing hardware. Includes fan mount and airflow geometry, and clearance for the HDMI
  and USB-C cable bend at the connector exit.
- **D3 — Detail drawings.** Three parts maximum: front frame (as-built), rear enclosure, and at most
  one bracket or retention feature. ASME Y14.5-2018, with declared datum reference frames.
- **D4 — Assembly drawing.** Assembled view, fastener callouts, item balloons, parts list.
- **D5 — Tolerance stack-up.** The front-to-rear mating interface, computed worst-case and RSS, with
  stated assumptions and a numeric conclusion on fit and interference probability.
- **D6 — Process capability and conformance report.** Measured FDM capability from printed coupons,
  feeding D5; plus measured conformance of the as-printed enclosure against its own callouts.
- **D7 — DFM analysis.** How this part would move to injection molding: draft, wall thickness,
  parting line, gate location, ejection, and material selection rationale.
- **D8 — Image set with descriptions.** Photographs, drawing sheets, and analysis figures.
- **D9 — README update** reflecting accurate project status.

---

## 3) Out of scope

Declared in advance so that adding any of it is a visible decision rather than drift.

- **TPF V2 in any form** — no local or on-device model, no accelerator hardware, no latency work,
  no replacement of the existing cloud API calls. The V1 script is used unmodified as a functional
  fixture for verifying assembly and operation.
- Any electronics change beyond installing a fan and its power connection.
- Redesign of the front frame. It is a fixed measurement subject.
- A fourth detail drawing.
- Thermal characterization. One functional check only (AC-10), not a study.
- Vendor engagement or tooling quotes. D7 is analysis.

---

## 4) Acceptance criteria — LOCKED

Locked at the commit of this file. Not modified to accommodate results. A criterion that fails is
documented with root cause, corrective action, and re-verification — never resolved by loosening
the criterion.

**Reverse modeling**

- **AC-1** — Measurement record contains at least 3 independent caliper readings for each of at
  least 15 features of the front frame, with mean and range reported per feature.
- **AC-2** — Reverse model dimensions match the measured mean within 0.05 mm on all 15 features.

**Design and fit**

- **AC-3** — Rear enclosure assembles to the existing front frame using the existing threaded
  inserts, with no rework, no forcing, and no post-print material removal.
- **AC-4** — All original hardware remains installed and undisturbed: Raspberry Pi, display and
  driver board, both speakers, and all cabling. The assembled unit closes with cables routed and
  connectors seated.

**Drawings**

- **AC-5** — Every drawing declares a datum reference frame with datums applied in order of
  precedence, and the primary datum choice is justified in a note tied to the part's function.
- **AC-6** — Every functional feature carries either a size tolerance or a geometric callout. No
  functional feature is left to the general tolerance block.
- **AC-7** — Drawing package passes the self-audit checklist in §6 with zero open items.

**Tolerance analysis**

- **AC-8** — Process capability derived from at least 5 printed coupons, at least 3 features each,
  with mean and standard deviation reported per feature. Every capability input to D5 traces to a
  measurement in D6; none are assumed.
- **AC-9** — Stack-up on the mating interface computed both worst-case and RSS, assumptions stated,
  with a numeric conclusion on fit and probability of interference.

**Function**

- **AC-10** — With the rear enclosure installed and the fan running, the unmodified V1 script runs
  for 30 continuous minutes with CPU temperature logged and no thermal throttling event.

**Integrity**

- **AC-11** — Measured conformance reported for every toleranced critical feature, pass or fail. Any
  nonconformance documented with root cause, corrective action, and re-verification.
- **AC-12** — No criterion in this section modified after commit. Git history shows this file
  preceding all CAD, drawing, and results commits.

**Documentation**

- **AC-13** — Image set contains at least 8 images with written descriptions, including at least one
  drawing sheet and one measurement or analysis figure.

---

## 5) Constraints

- **Time box:** six weeks from plan commit, at roughly 10–15 hours per week.
- **Materials budget:** $75 cap. Actual spend reported in the README with an on-hand versus
  purchased split.
- **Equipment:** Creality Ender 3 S1 Pro, digital calipers, SOLIDWORKS.
- **Slip rule:** a part that does not fit produces a documented iteration, not a relaxed criterion.
  If the time box is genuinely at risk, D7 is cut first.

---

## 6) Drawing self-audit checklist (AC-7)

1. Title block complete: part name, number, material, finish, scale, units, revision, date, author.
2. General tolerance block present and consistent with the callouts.
3. Datum reference frame declared; datums in order of precedence; primary datum justified in a note.
4. Every functional feature toleranced (AC-6).
5. Material condition modifiers (MMC/LMC/RFS) used deliberately, each justified in the notes.
6. Sufficient views and sections that no feature requires inference to manufacture.
7. Dimensions non-redundant and non-conflicting; no closed dimension loops.
8. Datum features physically accessible for inspection with available equipment.
9. Fastener and thread callouts complete, including insert specification.
10. Assembly sheet: item balloons, parts list, quantities, and fastener engagement note.
11. Every drawing sheet exported to PDF and committed to the repo.
12. Second reading performed at least 24 hours after drafting, with findings logged.

---

## 7) Known risks and pre-declared responses

| Risk | Response |
|---|---|
| FDM cannot hold a specified tolerance | Expected. Documented as a finding: callout, measured result, root cause, corrective action (revised callout with justification, print orientation change, or feature redesign), re-verification. |
| Reverse model diverges from the as-built part | Measure more features, not fewer. Where a feature cannot be measured to 0.05 mm with calipers, state the limitation rather than report false precision. |
| Cable bend radius makes the enclosure impractical | Treated as a design requirement: relocate the exit, add strain relief, or add clearance geometry. Constraint and decision documented. |
| Drawings deferred to the end | The front frame drawing is scheduled early, on a part that cannot change, specifically to prevent this. |

---

## 8) Definition of done

All thirteen acceptance criteria dispositioned PASS, or dispositioned FAIL with documented root
cause, corrective action, and re-verification. Repo published with drawings, measurement data,
stack-up, DFM analysis, and photographs. README updated to describe the project accurately,
including what this phase did and did not do.

## 9) Schedule

| Week | Dates | Work | Exit condition |
|---|---|---|---|
| **0** | Aug 22–23 | Commit this plan. Order fan, filament, fasteners. | Plan in git before any other commit |
| **1** | Aug 24–30 | GD&T refresher (~6–8 hrs). Full measurement inventory of the front frame. Reverse model. | AC-1, AC-2 |
| **2** | Aug 31–Sep 6 | **Front frame detail drawing** (first Y14.5 deliverable, on a fixed part). Design, print, and measure tolerance coupons. | Front frame sheet drafted; coupon data collected |
| **3** | Sep 7–13 | Rear enclosure design. Stack-up using week-2 capability data. **Design freeze.** | AC-8, AC-9; design frozen |
| **4** | Sep 14–20 | Print rear enclosure. Fit test, measure conformance, RCA and iterate if needed. Assemble. Functional run. | AC-3, AC-4, AC-10, AC-11 |
| **5** | Sep 21–27 | Rear enclosure detail drawing, assembly drawing, nonconformance report. Self-audit. | AC-5, AC-6, AC-7 |
| **6** | Sep 28–Oct 2 | DFM section. Portfolio page. README update. Retrospective. | AC-13; all deliverables published |
