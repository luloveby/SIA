# Bernardino, Aliah Jane D.

Activity 9 — Queuing system sample

## 1. What is one design choice that makes your Selenium suite easier to maintain?

I would make browser selection, headless mode and evidence folders configurable. The same test code can then support local investigation and scheduled cross-browser runs.

## 2. Why is an explicit or condition-based wait better than guessing a fixed sleep?

A condition-based wait adapts to slower processing without always using a long delay. It also times out when the expected state never arrives instead of assuming success after sleeping.

## 3. Which automated test belongs in a pull-request smoke suite, and why?

I would run AUTO-Q01 and AUTO-Q02 on PRs and all five cases after merge. Nightly Chrome/Firefox checks broaden browser coverage, but that CI matrix must be verified before we claim it passed.

