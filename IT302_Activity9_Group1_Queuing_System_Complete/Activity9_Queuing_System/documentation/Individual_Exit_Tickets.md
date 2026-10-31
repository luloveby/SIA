# Activity 9 individual exit tickets

# Culilap, Lovely Joyce J.

Activity 9 — Queuing system sample

## 1. What is one design choice that makes your Selenium suite easier to maintain?

I would put login and ticket actions in Page Objects. If a locator changes, I can update it once while keeping the tests focused on the expected queue outcome.

## 2. Why is an explicit or condition-based wait better than guessing a fixed sleep?

I would wait for the refreshed ticket list and completed response before checking its contents. A guessed sleep might end before the record appears or delay a fast run unnecessarily.

## 3. Which automated test belongs in a pull-request smoke suite, and why?

I would include AUTO-Q01 valid staff login in the PR smoke suite. If staff cannot open the dashboard, the queue workflow cannot proceed, and this short test gives fast feedback.


# Lopez, Shanley Nina DG.

Activity 9 — Queuing system sample

## 1. What is one design choice that makes your Selenium suite easier to maintain?

I would use a fresh browser and reusable reset fixture for every test. The five-attempt lockout test must not leave the account locked for the next test.

## 2. Why is an explicit or condition-based wait better than guessing a fixed sleep?

An explicit wait checks the state needed by the next step. This is more reliable when the local machine and CI runner respond at different speeds.

## 3. Which automated test belongs in a pull-request smoke suite, and why?

I would include AUTO-Q01 and AUTO-Q02 in PR smoke. They cover successful access and a short negative validation case while keeping the PR feedback quick.


# Hernandez, Russel

Activity 9 — Queuing system sample

## 1. What is one design choice that makes your Selenium suite easier to maintain?

I would read credentials from configuration and reuse LoginPage instead of repeating sign-in code. This makes security-related changes easier to review and avoids real secrets in the tests.

## 2. Why is an explicit or condition-based wait better than guessing a fixed sleep?

I would wait for the specific attempt number or lock message after each invalid login. A fixed sleep cannot confirm whether the server has actually processed the attempt.

## 3. Which automated test belongs in a pull-request smoke suite, and why?

I would include AUTO-Q02 short-password rejection because invalid input must not expose protected queue content. AUTO-Q03 lockout is also critical, but its five repeated attempts fit the broader regression run.


# Evangelista, Raiza Joy P.

Activity 9 — Queuing system sample

## 1. What is one design choice that makes your Selenium suite easier to maintain?

I would keep record assertions in tests and locators/actions in QueuePage. That separation makes it easier to see whether a failure concerns interaction or saved queue data.

## 2. Why is an explicit or condition-based wait better than guessing a fixed sleep?

I would wait until the ticket response is complete and the table has refreshed. Otherwise, an assertion might read stale data and report a misleading failure.

## 3. Which automated test belongs in a pull-request smoke suite, and why?

I would keep AUTO-Q01 in PR smoke and AUTO-Q04 duplicate prevention in the full regression suite. Login is short; the repeated-submit and refresh checks provide deeper data-integrity coverage after merge.


# De Leon, Precious Eunice B.

Activity 9 — Queuing system sample

## 1. What is one design choice that makes your Selenium suite easier to maintain?

I would link every test to its queue manual ID and retain the original Activity 5 reference in the crosswalk. This helps us update the right tests when a requirement changes.

## 2. Why is an explicit or condition-based wait better than guessing a fixed sleep?

An explicit wait documents what must become ready, such as the validation message. A fixed sleep documents only an elapsed time and gives less useful information when it fails.

## 3. Which automated test belongs in a pull-request smoke suite, and why?

I would include AUTO-Q02 in PR smoke. Its seven-character input is a representative invalid partition just below the assumed eight-character minimum, so it checks a clear rule with little run time.


# Bernardino, Aliah Jane D.

Activity 9 — Queuing system sample

## 1. What is one design choice that makes your Selenium suite easier to maintain?

I would make browser selection, headless mode and evidence folders configurable. The same test code can then support local investigation and scheduled cross-browser runs.

## 2. Why is an explicit or condition-based wait better than guessing a fixed sleep?

A condition-based wait adapts to slower processing without always using a long delay. It also times out when the expected state never arrives instead of assuming success after sleeping.

## 3. Which automated test belongs in a pull-request smoke suite, and why?

I would run AUTO-Q01 and AUTO-Q02 on PRs and all five cases after merge. Nightly Chrome/Firefox checks broaden browser coverage, but that CI matrix must be verified before we claim it passed.

