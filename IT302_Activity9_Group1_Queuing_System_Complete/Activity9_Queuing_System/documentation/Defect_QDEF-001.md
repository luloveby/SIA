# QDEF-001 Duplicate queue ticket created on repeated submission

Type: intentional sample product defect. This report concerns the bundled classroom demo only.

- Linked automation: AUTO-Q04; queue manual case: QTC-04; requirement: QR4.
- Source principle: Activity 5 TC-06/R6 and DEF-004 concern duplicate enrollment; this new queue defect is QDEF-001.
- Environment: Windows; Python 3.12.14; Selenium 4.51.0; pytest 8.3.3; headless Google Chrome 156.0.8078.73; 1365 x 1000 browser window.
- Affected build: Q-DEMO-1.0-bug; corrected build: Q-DEMO-1.1-fixed.
- Preconditions: reset synthetic data; log in as staff.demo; CUST-001 has no active Registrar ticket.
- Steps: 1. Issue a Registrar ticket for CUST-001. 2. Confirm Q-001 is Waiting. 3. Submit the same customer/service again. 4. Inspect message and records.
- Expected: repeat request rejected; exactly one active Q-001 persists.
- Observed in Run 1: success message for Q-002; Q-001 and Q-002 both exist as Waiting tickets.
- Severity: High — duplicate positions corrupt queue data and can cause unfair/repeated service.
- Priority: P1 — a core queue integrity rule must be corrected before release.
- Triage category: product defect deliberately seeded in the demo; not a locator, timing or data issue.
- Owner plan: Raiza investigates record integrity; Lovely verifies the visible outcome; Shanley coordinates retest.
- Correction: check active customer/service uniqueness within the locked request handler; return 409 and the existing ticket without creating a second record.
- Retest: unchanged AUTO-Q04 and all other cases pass in Run 2; refresh confirms one matching record.
- Status: Closed for the fixed sample mode; deliberately reproducible with --demo-bug.
- Evidence: evidence/run-01/screenshots/*AUTO-Q04* and *_FAIL.png; evidence/run-01/junit.xml; corresponding Run 2 capture; see evidence/index.html for direct links.
- Release implication: NO-GO for the affected sample; passing this retest does not approve the actual prototype.
