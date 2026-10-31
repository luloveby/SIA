# Queuing manual cases and traceability

Activity 5 is a CampusConnect fallback. QTC-01 to QTC-05 and QR1 to QR5 are newly assigned queue adaptations for Activity 9, not identifiers claimed to appear in Activity 5. The original source references are preserved below. Activity 8 supplies the small UI suite, Page Object, explicit-wait, synthetic-data and CI strategy. Its enrollment examples are not asserted to be queue requirements.

Common preconditions: synthetic staff account; fresh browser; reset attempts/sessions/tickets; local demo running; no parallel execution. QR4 is an assumed rule: at most one active Waiting ticket for the same customer and service. The prototype owner should confirm this rule before reusing the suite on the real system.

## QTC-01 Valid staff login

Automation: AUTO-Q01 — tests/test_queue.py::test_login[AUTO-Q01]

Original Activity 5: TC-01 / R1. Login success adapted from CampusConnect student login; MFA is not included in this sample.

Requirement: QR1 Staff authentication

Data: staff.demo / DEMO_PASSWORD

Steps: Open /login; enter valid synthetic staff credentials; select Sign in.

Expected: Queue dashboard opens, authenticated staff identity is visible and URL ends in #queue.

## QTC-03 Reject seven-character password

Automation: AUTO-Q02 — tests/test_queue.py::test_login[AUTO-Q02]

Original Activity 5: TC-03 / R3. The 8-character threshold is retained as a theoretical queue-login requirement.

Requirement: QR3 Password minimum length

Data: staff.demo / Abc123! (7 characters)

Steps: Open /login; submit the 7-character password; request /queue#queue without a valid session.

Expected: At least 8 characters validation appears; unauthenticated access does not expose the queue dashboard.

## QTC-02 Lock account after five wrong passwords

Automation: AUTO-Q03 — tests/test_queue.py::test_lockout_after_five_invalid_attempts

Original Activity 5: TC-02 / R2. Threshold adapted from Activity 5; the sample implements the corrected behavior, not its historical failure.

Requirement: QR2 Account lockout

Data: staff.demo / valid password plus -wrong; five consecutive attempts

Steps: Reset account; submit a wrong password five times; then submit correct credentials.

Expected: Attempts 1 to 4 show invalid credentials; attempt 5 locks the account; correct password still cannot open the queue.

## QTC-04 Prevent duplicate queue ticket

Automation: AUTO-Q04 — tests/test_queue.py::test_duplicate_ticket_is_prevented

Original Activity 5: TC-06 / R6. Adapted from duplicate enrollment prevention, not an original queue case in Activity 5. New defect ID QDEF-001.

Requirement: QR4 One active ticket per customer and service

Data: CUST-001 / Registrar; repeat the same submission

Steps: Reset tickets; log in; issue a Registrar ticket; issue the same customer/service again; compare records and refresh.

Expected: Second request is rejected; the original Q-001 is retained; exactly one matching Waiting ticket persists after refresh.

## QTC-05 Create a valid queue ticket

Automation: AUTO-Q05 — tests/test_queue.py::test_valid_ticket_is_saved

Original Activity 5: TC-08 / R7. Successful transaction principle adapted from valid enrollment.

Requirement: QR5 Valid ticket persistence

Data: CUST-002 / Cashier

Steps: Reset tickets; log in; issue one Cashier ticket; refresh the dashboard.

Expected: Q-001 is created once with the right customer, service and Waiting status; the record survives browser refresh.

## Deferred coverage

Capacity of 30 (TC-05/R5), prerequisite rules (TC-04/R4), student MFA (TC-01), and enrollment service interruption (TC-07/R7) are source-domain rules, not silently converted to queue requirements. Queue capacity, priority customers, call-next/FIFO, skipped numbers, concurrency, outage recovery and logout need confirmed queue specifications and additional tests. Five small UI cases do not prove those features.
