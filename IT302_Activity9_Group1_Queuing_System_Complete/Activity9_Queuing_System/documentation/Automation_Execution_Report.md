# Short Automation Execution Report

Group 1 — IT302 Activity 9 — Queuing System

Prepared 29 October 2026 (Asia/Manila)

## Basis and scope

This is a theoretical queuing-system submission supported by an executable classroom demo. The two reported runs were performed against that bundled demo, not against the group's deployed prototype. Activity 5 contains CampusConnect fallback cases; new QTC references explicitly adapt their test principles for queue workflows. Activity 8 supplies the small UI suite, Page Object, explicit-wait, synthetic-data and CI strategy. The duplicate rule is assumed: one active Waiting ticket per customer and service. No original Activity 5 observation is presented as an observation of the queue prototype.

Five collected Selenium cases cover valid staff login, seven-character password rejection, five-attempt account lockout, duplicate-ticket prevention and valid ticket persistence across browser refresh. Login is parameterized into two cases. Detailed steps and crosswalk are in Manual_Cases_and_Traceability.md and Traceability.csv.

## Environment and data

Windows; Python 3.12.14; Selenium 4.51.0; pytest 8.3.3; headless Google Chrome 156.0.8078.73; 1365 x 1000 browser window.

Builds: Q-DEMO-1.0-bug intentionally allows duplicate tickets; Q-DEMO-1.1-fixed enables duplicate rejection. Both are two selectable modes of the supplied source. URL: auto-assigned http://127.0.0.1:<port>; each test receives a fresh browser and a reset account/ticket store. Synthetic staff user: staff.demo. Customers: CUST-001/Registrar and CUST-002/Cashier. No production credentials or personal records are used.

## Results

| Run | Sample build | Planned | Passed | Failed | Errors | Duration | Pass rate |
|---|---|---:|---:|---:|---:|---:|---:|
| 1 | Q-DEMO-1.0-bug | 5 | 4 | 1 | 0 | 61.45 s | 80% |
| 2 | Q-DEMO-1.1-fixed | 5 | 5 | 0 | 0 | 75.36 s | 100% |

All five cases completed in each reported run; blocked/not-run = 0. Completion = (Pass + Fail)/5 = 100% in each run. Pass rate = Pass/(Pass + Fail), giving 80% then 100%. Run durations are the JUnit suite totals and include browser setup/teardown. Browser-driver acquisition before the successful setup is excluded from these two run records.

| Automated ID | Queue manual ID | Activity 5 source | Scenario | Run 1 | Run 2 |
|---|---|---|---|---|---|
| AUTO-Q01 | QTC-01 | TC-01 / R1 | Valid staff login | PASS | PASS |
| AUTO-Q02 | QTC-03 | TC-03 / R3 | Reject seven-character password | PASS | PASS |
| AUTO-Q03 | QTC-02 | TC-02 / R2 | Lock account after five wrong passwords | PASS | PASS |
| AUTO-Q04 | QTC-04 | TC-06 / R6 | Prevent duplicate queue ticket | FAIL | PASS |
| AUTO-Q05 | QTC-05 | TC-08 / R7 | Create a valid queue ticket | PASS | PASS |

## Failure triage and correction

AUTO-Q04 failed in Run 1 because the same customer/service produced Q-001 and Q-002, both Waiting. This is an intentionally seeded product defect in the sample, QDEF-001, related to the duplicate-prevention principle in Activity 5 TC-06/R6 and DEF-004. It is not a claim that the real queue prototype has that defect. Severity High: duplicate queue positions compromise record integrity and service order. Priority P1: correct the core rule before release.

The fixed mode checks for an existing active customer/service pair while holding the server lock, returns the existing ticket with HTTP 409, and does not increment the queue number or add a record. The UI displays rejection and refreshes the list. The Selenium assertion remains unchanged. After independent data reset, a full five-case rerun passed. This is a specific product correction followed by regression, not a blind retry.

Preparation note: an older Selenium dependency initially failed to resolve EdgeDriver through a retired download endpoint. That setup issue was classified environment/dependency and corrected by pinning Selenium 4.51.0. Edge then crashed in the restricted runner, so the recorded executions use Chrome instead. It was not counted as a product defect.

## Evidence and ownership

evidence/run-01 and run-02 each contain junit.xml, run.log, console.log and screenshots. evidence/index.html links each result to its case and screenshot. Original raw reports are retained, including the expected failure traceback. Sample screenshots show the bundled app's Classroom demo label. The logs identify sample demo execution.

Roles carried over from Activity 5: Shanley coordinates scope/triage; Precious maintains traceability/evidence; Raiza checks data integrity; Russel checks security/access; Aliah checks CI/concurrency/recovery; Lovely reviews system outcomes and acceptance. For QDEF-001, Raiza owns technical triage and Lovely reviews the visible ticket outcome; Shanley coordinates the retest. These assignments describe the sample work plan, not independent claims about who ran commands in this chat.

## CI readiness and exit decision

Dependencies, synthetic configuration, headless mode, reset/cleanup fixtures, smoke markers, JUnit output, screenshots and an always-upload artifact step are supplied. PRs select the two smoke cases; main merges run all five; nightly runs target Chrome/Firefox. Hosted CI and that browser matrix have not been executed here. Detailed status is in CI_Readiness_Checklist.md.

Run 1 recommendation: NO-GO for the sample while QDEF-001 is open. Run 2: the five-case demo exit criterion is met and QDEF-001 is closed in the fixed mode. This does not authorize release of the actual queuing system. Confirm real requirements, adapt selectors/setup and run the actual build before making a prototype release decision.

## Limitations

Only the sample and local Chrome were exercised. Five cases do not establish overall security, usability, performance or queue correctness. No call-next/FIFO, priority queue, concurrent-user load, queue capacity, logout, outage recovery, real database durability or ten-run stability claim is made. In-memory persistence is checked across browser refresh only, not server restart. Student MFA, course prerequisites and enrollment capacity from the references are not queue requirements without explicit adaptation. The test-only reset route is for the loopback demo only.

## Supplemental captures

The PDF report uses full-height captures recreated after the original runs via source/scripts/capture_demo.py so the full ticket list is visible. These are supplementary reproductions of AUTO-Q04 in each sample mode; original per-test screenshots and timestamps remain unchanged in run-01/run-02. See evidence/supplemental/README.txt.
