# Group 1 Activity 9 Queuing System Submission

This package provides the answered Activity 9 worksheet, a runnable Selenium/pytest project, a loopback sample queuing app, test traceability, sample execution evidence, execution/defect reports, CI checklist and six individual exit tickets. It is a theoretical adaptation for the group's queuing system, not a test result from the deployed prototype. The included evidence is produced against the bundled classroom demo; see the execution report for verification scope.

## Deliverables

| Required item | Location |
|---|---|
| Completed Activity 9 document | Activity9_Queuing_System_Answered.docx |
| Source-code folder/project | source/ |
| README/setup and dependencies | This file; source/requirements.txt; source/requirements-lock.txt |
| Five automated cases and manual references | source/tests/test_queue.py; documentation/Traceability.csv; documentation/Manual_Cases_and_Traceability.md |
| Logs, screenshots and reports | evidence/run-01/; evidence/run-02/; evidence/index.html |
| Short execution and defect reports | documentation/Automation_Execution_Report.md; documentation/Defect_QDEF-001.md; Automation_Execution_Report.pdf |
| CI readiness | documentation/CI_Readiness_Checklist.md; .github/workflows/selenium.yml |
| Individual exit tickets | exit_tickets/; documentation/Individual_Exit_Tickets.md; answered worksheet |

## Reference interpretation

Activity 5 contains CampusConnect login/MFA/enrollment fallback cases, not queue-specific manual cases. We preserve its TC references and assign new QTC IDs for queue adaptations. We do not claim that the queue cases originally appeared in that PDF. Activity 8 informs risk-based selection, the test pyramid, Page Objects, waits, evidence and CI. Queue-specific requirements and duplicate-ticket behavior are explicit sample assumptions.

## Windows setup and execution

Install Python 3.12 and Microsoft Edge, Chrome or Firefox. The first Selenium run needs internet for driver resolution through Selenium Manager. Open PowerShell in this package folder, then:

```powershell
Set-Location source
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-lock.txt
$env:BROWSER = 'chrome'
$env:HEADLESS = 'true'
$env:DEMO_USER = 'staff.demo'
$env:DEMO_PASSWORD = 'DemoQueue123!'
$env:TEST_RESET_TOKEN = 'local-demo-reset'
# Keep BASE_URL unset to let pytest start the bundled demo on a free loopback port.
.\.venv\Scripts\python.exe -m pytest -c pytest.ini tests --demo-bug --evidence-dir ../evidence/new-run-01 --junitxml=../evidence/new-run-01/junit.xml
# Expected intentional result: AUTO-Q04 fails, so pytest returns exit code 1.
.\.venv\Scripts\python.exe -m pytest -c pytest.ini tests --evidence-dir ../evidence/new-run-02 --junitxml=../evidence/new-run-02/junit.xml
# Expected fixed-demo result: all five pass, pytest returns exit code 0.
```

Use requirements.txt instead of requirements-lock.txt if you intentionally want to resolve newer compatible transitive dependencies. The lock file records the package versions used to prepare this sample on Python 3.12. No activation is required when calling the virtual-environment executable directly. `.env.example` is documentation only; pytest does not auto-load it.

The tests automatically start and stop the sample app. Each case resets attempts, sessions and tickets, starts a fresh browser, then resets data again and quits the browser. Do not run with pytest-xdist against this single shared demo account. To see the browser, set HEADLESS=false. Change BROWSER to edge or firefox after installing it.

For PR smoke:

```powershell
.\.venv\Scripts\python.exe -m pytest -c pytest.ini tests -m smoke --evidence-dir ../evidence/new-smoke --junitxml=../evidence/new-smoke/junit.xml
```

Linux/macOS: use `python3 -m venv .venv`, `.venv/bin/python -m pip install -r requirements-lock.txt` and `BROWSER=chrome HEADLESS=true .venv/bin/python -m pytest -c pytest.ini tests ...` from source/. All five pytest items come from four functions, because valid/short-password login is parameterized into two cases.

## Browse the sample manually

From source/, run `python -m demo.server --port 8765`, then open http://127.0.0.1:8765. Use the public synthetic demo account above. Add --duplicate-bug to reproduce the duplicate-ticket defect. This test-only server binds to loopback; its in-memory records disappear when it stops. Persistence assertions mean survival across browser refresh, not database durability across server restarts.

## Reuse on the real prototype

Confirm the queue requirements first, especially one active ticket per customer/service, minimum password length and lockout threshold. Replace Page Object selectors/routes and assertions to match the real UI. Supply synthetic accounts through environment/CI secrets. Replace the reset fixture with approved, non-production seed/cleanup methods. BASE_URL alone is not sufficient: the current reset fixture expects the sample-only `/__test__/reset` contract. Never expose that reset route on a production system. No real credentials or student/customer data are required by this sample.

## CI and triage

Push the complete package contents as a repository root so `.github/workflows/selenium.yml` can find source/. The workflow uses Chrome for PRs/main and Chrome/Firefox nightly; Selenium Manager resolves compatible drivers. The scheduled run is 02:00 Asia/Manila. GitHub-hosted execution and browser availability still need validation in your repository. The workflow runs the corrected app by default; the deliberate bug is only for the local demonstration.

PR author checks failures first; Shanley coordinates triage. Preserve logs/screenshots, classify the cause, fix it and rerun. A blind retry is not proof of reliability. See the readiness checklist for owners and pending verification.

## Technical references

- Selenium Manager: https://www.selenium.dev/documentation/selenium_manager/
- Microsoft Edge WebDriver: https://learn.microsoft.com/en-us/microsoft-edge/webdriver-chromium/
- GitHub workflow artifacts: https://docs.github.com/en/actions/concepts/workflows-and-actions/workflow-artifacts

## Preparation verification

The dependency-free HTTP verifier (`python -m scripts.verify_demo` from source/) exercises both bug/fixed service modes. Browser execution in the restricted preparation runner uses Chrome with `BROWSER_EXTRA_ARGS="--no-sandbox --disable-dev-shm-usage --disable-features=RendererCodeIntegrity"`; these optional runner flags are configurable and are not required by the application logic. The supplied workflow leaves extra flags unset. Native Edge was not successfully validated in that restricted runner.
