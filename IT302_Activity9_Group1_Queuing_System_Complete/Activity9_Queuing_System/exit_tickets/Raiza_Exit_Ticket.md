# Evangelista, Raiza Joy P.

Activity 9 — Queuing system sample

## 1. What is one design choice that makes your Selenium suite easier to maintain?

I would keep record assertions in tests and locators/actions in QueuePage. That separation makes it easier to see whether a failure concerns interaction or saved queue data.

## 2. Why is an explicit or condition-based wait better than guessing a fixed sleep?

I would wait until the ticket response is complete and the table has refreshed. Otherwise, an assertion might read stale data and report a misleading failure.

## 3. Which automated test belongs in a pull-request smoke suite, and why?

I would keep AUTO-Q01 in PR smoke and AUTO-Q04 duplicate prevention in the full regression suite. Login is short; the repeated-submit and refresh checks provide deeper data-integrity coverage after merge.

