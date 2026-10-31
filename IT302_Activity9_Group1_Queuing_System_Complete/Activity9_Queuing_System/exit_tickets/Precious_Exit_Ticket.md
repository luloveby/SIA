# De Leon, Precious Eunice B.

Activity 9 — Queuing system sample

## 1. What is one design choice that makes your Selenium suite easier to maintain?

I would link every test to its queue manual ID and retain the original Activity 5 reference in the crosswalk. This helps us update the right tests when a requirement changes.

## 2. Why is an explicit or condition-based wait better than guessing a fixed sleep?

An explicit wait documents what must become ready, such as the validation message. A fixed sleep documents only an elapsed time and gives less useful information when it fails.

## 3. Which automated test belongs in a pull-request smoke suite, and why?

I would include AUTO-Q02 in PR smoke. Its seven-character input is a representative invalid partition just below the assumed eight-character minimum, so it checks a clear rule with little run time.

