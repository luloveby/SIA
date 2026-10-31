# Hernandez, Russel

Activity 9 — Queuing system sample

## 1. What is one design choice that makes your Selenium suite easier to maintain?

I would read credentials from configuration and reuse LoginPage instead of repeating sign-in code. This makes security-related changes easier to review and avoids real secrets in the tests.

## 2. Why is an explicit or condition-based wait better than guessing a fixed sleep?

I would wait for the specific attempt number or lock message after each invalid login. A fixed sleep cannot confirm whether the server has actually processed the attempt.

## 3. Which automated test belongs in a pull-request smoke suite, and why?

I would include AUTO-Q02 short-password rejection because invalid input must not expose protected queue content. AUTO-Q03 lockout is also critical, but its five repeated attempts fit the broader regression run.

