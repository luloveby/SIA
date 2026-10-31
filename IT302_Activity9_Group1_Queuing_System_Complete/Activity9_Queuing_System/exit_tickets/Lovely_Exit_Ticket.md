# Culilap, Lovely Joyce J.

Activity 9 — Queuing system sample

## 1. What is one design choice that makes your Selenium suite easier to maintain?

I would put login and ticket actions in Page Objects. If a locator changes, I can update it once while keeping the tests focused on the expected queue outcome.

## 2. Why is an explicit or condition-based wait better than guessing a fixed sleep?

I would wait for the refreshed ticket list and completed response before checking its contents. A guessed sleep might end before the record appears or delay a fast run unnecessarily.

## 3. Which automated test belongs in a pull-request smoke suite, and why?

I would include AUTO-Q01 valid staff login in the PR smoke suite. If staff cannot open the dashboard, the queue workflow cannot proceed, and this short test gives fast feedback.

