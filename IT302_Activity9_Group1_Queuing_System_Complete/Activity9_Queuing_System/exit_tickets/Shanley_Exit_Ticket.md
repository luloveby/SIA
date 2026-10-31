# Lopez, Shanley Nina DG.

Activity 9 — Queuing system sample

## 1. What is one design choice that makes your Selenium suite easier to maintain?

I would use a fresh browser and reusable reset fixture for every test. The five-attempt lockout test must not leave the account locked for the next test.

## 2. Why is an explicit or condition-based wait better than guessing a fixed sleep?

An explicit wait checks the state needed by the next step. This is more reliable when the local machine and CI runner respond at different speeds.

## 3. Which automated test belongs in a pull-request smoke suite, and why?

I would include AUTO-Q01 and AUTO-Q02 in PR smoke. They cover successful access and a short negative validation case while keeping the PR feedback quick.

