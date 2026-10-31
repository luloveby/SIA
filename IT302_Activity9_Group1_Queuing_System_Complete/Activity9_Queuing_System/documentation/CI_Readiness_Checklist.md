# CI readiness checklist

Status means implemented in the sample project unless stated otherwise. A configured workflow is not evidence of a successful hosted run.

- [x] Dependency list: source/requirements.txt; Python 3.12 recommended; transitive versions recorded separately after setup.
- [x] Setup and commands: root README.md; auto-started local demo; five collected test variants.
- [x] Configurable BASE_URL, BROWSER, HEADLESS, DEMO_USER, DEMO_PASSWORD and TEST_RESET_TOKEN; .env.example contains public demo values only and is not auto-loaded.
- [x] Selenium Manager resolves the driver; first run needs driver-download network access and a supported installed browser.
- [x] Page Objects centralize stable data-test locators; WebDriverWait handles required states; no fixed sleeps.
- [x] Independent browser and reset fixture per test; reset before and after each case; driver.quit() on teardown. Run sequentially because the one-account demo state is shared.
- [x] Business assertions cover authenticated identity, rejection, lockout, duplicate prevention and persisted ticket fields.
- [x] Reports: run.log, JUnit XML, console log and screenshots; failure hook captures screenshots before driver teardown.
- [x] Smoke marker selects AUTO-Q01/AUTO-Q02; a full unfiltered run includes all five variants.
- [x] .github/workflows/selenium.yml runs PR smoke, main-branch full suite and nightly Chrome/Firefox; nightly 18:00 UTC is 02:00 Asia/Manila next day.
- [x] Workflow uploads artifacts with if: always() so failures retain evidence. Default permissions are contents: read.
- [x] Ownership: PR author first; Shanley coordinates; Russel handles access/security, Raiza records/data, Precious traceability/evidence, Aliah CI/recovery, Lovely quality review. These are the roles carried over from Activity 5.
- [x] Triage: classify product, test-code, test-data, environment/dependency or unknown; preserve first failure; reproduce; fix the cause; rerun affected case and regression; record residual risk.
- [ ] Hosted GitHub Actions run validated. Workflow is supplied but was not dispatched from this chat.
- [ ] Cross-browser and ten-run stability POC completed. Neither is claimed from the two local demonstration runs.

For release: the sample's duplicate defect is High severity and P1 priority. A failing critical queue rule blocks a GO recommendation until retested or explicitly accepted by the responsible lead. Passing the demo is not approval to release the real prototype.
